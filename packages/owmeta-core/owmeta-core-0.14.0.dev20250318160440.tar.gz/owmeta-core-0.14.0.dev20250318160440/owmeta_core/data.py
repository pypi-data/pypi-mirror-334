from __future__ import print_function
import datetime
import os
import logging
import atexit
import hashlib

from rdflib import URIRef, Namespace, plugin
from rdflib.graph import Graph, ConjunctiveGraph, Dataset, DATASET_DEFAULT_GRAPH_ID
from rdflib.store import Store
from rdflib.events import Event
from rdflib.namespace import RDF, NamespaceManager
import transaction
from transaction.interfaces import NoTransaction
from zc.lockfile import LockError
import ZODB
from ZODB.FileStorage import FileStorage

from .utils import grouper, retrieve_provider
from .configure import Configurable, Configuration, ConfigValue

__all__ = [
    "Data",
    "DataUser",
    "RDFSource",
    "SPARQLSource",
    "SleepyCatSource",
    "DefaultSource",
    "ZODBSource",
    "SQLiteSource",
    "MySQLSource",
    "PostgreSQLSource"]

L = logging.getLogger(__name__)

ALLOW_UNCONNECTED_DATA_USERS = True

NAMESPACE_MANAGER_KEY = 'rdf.namespace_manager'
''' Constant for :confval:`rdf.namespace_manager` '''

NAMESPACE_MANAGER_STORE_KEY = 'rdf.namespace_manager.store'
''' Constant for :confval:`rdf.namespace_manager.store` '''

NAMESPACE_MANAGER_STORE_CONF_KEY = 'rdf.namespace_manager.store_conf'
''' Constant for :confval:`rdf.namespace_manager.store_conf` '''

TRANSACTION_MANAGER_PROVIDER_KEY = 'transaction_manager.provider'
''' Constant for :confval:`transaction_manager.provider` '''

TRANSACTION_MANAGER_KEY = 'transaction_manager'
''' Constant for :confval:`transaction_manager` '''

_B_UNSET = object()


ACTIVE_CONNECTIONS = []


def close_databases():
    for conn in ACTIVE_CONNECTIONS:
        conn.closeDatabase()


atexit.register(close_databases)


class OpenFailError(Exception):
    pass


class DatabaseConflict(Exception):
    pass


class _NamespaceManager(NamespaceManager):
    '''
    Overrides RDFLib's `NamespaceManager` to avoid binding things during init (e.g., for
    read-only stores).
    '''

    def __init__(self, *args, **kwargs):
        # Some B.S. we do to prevent RDFLib from binding namespaces during initialization
        self.__allow_binds = False
        super(_NamespaceManager, self).__init__(*args, **kwargs)
        self.__allow_binds = True

    def bind(self, *args, **kwargs):
        if self.__allow_binds:
            super().bind(*args, **kwargs)

    # Ignore the generate option so we only bind when `bind` is called. The prefix
    # generation logic is hard to account for, kinda worthless, and binds namespaces
    # during Turtle serialization which is more convenient as a read-only operation.
    def compute_qname(self, uri, generate=False):
        return super().compute_qname(uri, False)

    def compute_qname_strict(self, uri, generate=False):
        return super().compute_qname_strict(uri, False)


class _Dataset(Dataset):
    '''
    Overrides RDFlib's `~rdflib.graph.Dataset` to not call
    `~rdflib.graph.Dataset.add_graph` when just listing contexts
    '''
    def contexts(self, triple=None):
        default = False
        # We call Dataset's super (i.e., ConjunctiveGraph) because we *don't* want the
        # Dataset behavior
        for c in super(Dataset, self).contexts(triple):
            default |= c.identifier == DATASET_DEFAULT_GRAPH_ID
            yield c
        if not default:
            yield self._graph(DATASET_DEFAULT_GRAPH_ID)

    def quads(self, quad):
        for s, p, o, c in super(Dataset, self).quads(quad):
            if c == self.default_context:
                yield s, p, o, None
            else:
                yield s, p, o, c


class DataUserUnconnected(Exception):
    def __init__(self, msg):
        super(DataUserUnconnected, self).__init__(str(msg) + ': No connection has been made for this data'
        ' user (i.e., it is unconfigured)')


class _B(ConfigValue):

    def __init__(self, f):
        self.v = _B_UNSET
        self.f = f

    def get(self):
        if self.v is _B_UNSET:
            self.v = self.f()

        return self.v

    def invalidate(self):
        self.v = None

    def __repr__(self):
        if self.v is _B_UNSET:
            return 'Thunk of ' + repr(self.f)
        return repr(self.v)


ZERO = datetime.timedelta(0)


class _UTC(datetime.tzinfo):

    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = _UTC()


class DataUser(Configurable):

    """ A convenience wrapper for users of the database

    Classes which use the database should inherit from DataUser.
    """

    def __init__(self, *args, **kwargs):
        super(DataUser, self).__init__(*args, **kwargs)
        self.__base_namespace = None

    @property
    def base_namespace(self):
        if self.__base_namespace is not None:
            return self.__base_namespace
        return self.conf['rdf.namespace']

    @base_namespace.setter
    def base_namespace(self, value):
        self.__base_namespace = value

    @property
    def rdf(self):
        try:
            return self.conf['rdf.graph']
        except KeyError:
            if ALLOW_UNCONNECTED_DATA_USERS:
                return _Dataset(default_union=True)
            raise DataUserUnconnected('No rdf.graph')

    @property
    def namespace_manager(self):
        return self.conf.get(NAMESPACE_MANAGER_KEY, None)

    def _remove_from_store(self, g):
        # Note the assymetry with _add_to_store. You must add actual elements, but deletes
        # can be performed as a query
        for group in grouper(g, 1000):
            temp_graph = Graph()
            for x in group:
                if x is not None:
                    temp_graph.add(x)
                else:
                    break
            s = " DELETE DATA {" + temp_graph.serialize(format="nt") + " } "
            L.debug("deleting. s = " + s)
            self.conf['rdf.graph'].update(s)

    def _add_to_store(self, g, graph_name=False):
        if self.conf['rdf.store'] == 'SPARQLUpdateStore':
            # XXX With Sesame, for instance, it is probably faster to do a PUT over
            # the endpoint's rest interface. Just need to do it for some common
            # endpoints

            try:
                gs = g.serialize(format="nt")
            except Exception:
                gs = _triples_to_bgp(g)

            if graph_name:
                s = " INSERT DATA { GRAPH " + graph_name.n3() + " {" + gs + " } } "
            else:
                s = " INSERT DATA { " + gs + " } "
                L.debug("update query = " + s)
                self.conf['rdf.graph'].update(s)
        else:
            gr = self.conf['rdf.graph']
            if self.conf['rdf.source'] == 'ZODB':
                transaction.commit()
                transaction.begin()
            for x in g:
                gr.add(x)
            if self.conf['rdf.source'] == 'ZODB':
                transaction.commit()
                transaction.begin()

        # infer from the added statements
        # self.infer()

    def infer(self):
        """ Fire FuXi rule engine to infer triples """

        from FuXi.Rete.RuleStore import SetupRuleStore
        from FuXi.Rete.Util import generateTokenSet
        from FuXi.Horn.HornRules import HornFromN3
        # fetch the derived object's graph
        semnet = self.rdf
        rule_store, rule_graph, network = SetupRuleStore(makeNetwork=True)
        closureDeltaGraph = Graph()
        network.inferredFacts = closureDeltaGraph
        # build a network of rules
        for rule in HornFromN3('testrules.n3'):
            network.buildNetworkFromClause(rule)
        # apply rules to original facts to infer new facts
        network.feedFactsToAdd(generateTokenSet(semnet))
        # combine original facts with inferred facts
        for x in closureDeltaGraph:
            self.rdf.add(x)

    def add_reference(self, g, reference_iri):
        """
        Add a citation to a set of statements in the database

        :param triples: A set of triples to annotate
        """
        new_statements = Graph()
        ns = self.conf['rdf.namespace']
        for statement in g:
            statement_node = self._reify(new_statements, statement)
            new_statements.add(
                (URIRef(reference_iri),
                 ns['asserts'],
                    statement_node))

        self.add_statements(g + new_statements)

    def retract_statements(self, graph):
        """
        Remove a set of statements from the database.

        :param graph: An iterable of triples
        """
        self._remove_from_store_by_query(graph)

    def _remove_from_store_by_query(self, q):
        s = " DELETE WHERE {" + q + " } "
        L.debug("deleting. s = " + s)
        self.conf['rdf.graph'].update(s)

    def add_statements(self, graph):
        """
        Add a set of statements to the database.
        Annotates the addition with uploader name, etc

        :param graph: An iterable of triples
        """
        self._add_to_store(graph)

    def _reify(self, g, s):
        """
        Add a statement object to g that binds to s
        """
        n = self.conf['new_graph_uri'](s)
        g.add((n, RDF['type'], RDF['Statement']))
        g.add((n, RDF['subject'], s[0]))
        g.add((n, RDF['predicate'], s[1]))
        g.add((n, RDF['object'], s[2]))
        return n


class Data(Configuration):

    """
    Provides configuration for access to the database.

    Usually doesn't need to be accessed directly

    .. confval:: rdf.graph

        An RDFLib `~rdflib.ConjunctiveGraph`, possibly a `~rdflib.Dataset`. Configured
        according to :confval:`rdf.source` and any other variables used by the
        `.RDFSource` corresponding

    .. confval:: rdf.namespace

        Default namespace bound to an empty string in the the namespace manager,
        :confval:`rdf.namespace_manager`

    .. confval:: rdf.namespace_manager

        RDFLib Namespace Manager. Typically, this is generated automatically during a call
        to `init`

    .. confval:: rdf.namespace_manager.store

        RDFLib :doc:`store name <rdflib:plugin_stores>` specific to namespaces

    .. confval:: rdf.namespace_manager.store_conf

        Configuration for RDFLib store specified with
        :confval:`rdf.namespace_manager.store`

    .. confval:: transaction_manager.provider

        A `provider <.retrieve_provider>` for a transaction manager. Provider must resolve
        to a `callable` that accepts a `Data` instance.

    .. confval:: transaction_manager

        Transaction manager for RDFLib stores. Provided by
        :confval:`transaction_manager.provider` if that's defined. Should be passed to
        `~transaction.interfaces.IDataManager` instances within the scope of a given
        `Data` instance.

    .. confval:: rdf.source

        A string corresponding to a key in `.SOURCES`

    """

    def __init__(self, conf=None, **kwargs):
        """
        Parameters
        ----------
        conf : .Configuration
            The base configuration from which this configuration will be built. This
            configuration will be copied into this one, but no direct reference will be
            retained
        """
        super(Data, self).__init__(**kwargs)

        if conf is not None:
            self.copy(conf)
        else:
            self.copy(Configurable.default_config)
        self.namespace = Namespace("http://openworm.org/entities/")
        self.molecule_namespace = Namespace("http://openworm.org/entities/molecules/")
        self['rdf.namespace'] = self.namespace
        self['molecule_name'] = self._molecule_hash
        self['new_graph_uri'] = self._molecule_hash

        self._cch = None
        self._listeners = dict()

        tm_provider_name = self.get(TRANSACTION_MANAGER_PROVIDER_KEY, None)
        if tm_provider_name is not None:
            tm = retrieve_provider(tm_provider_name)(self)
        else:
            tm = transaction.ThreadTransactionManager()
            tm.explicit = True
        self[TRANSACTION_MANAGER_KEY] = tm

    @classmethod
    def load(cls, file_name):
        """ Load a file into a new Data instance storing configuration in a JSON format """
        return cls.open(file_name)

    @classmethod
    def open(cls, file_name):
        """ Load a file into a new Data instance storing configuration in a JSON format """
        return cls(conf=Configuration.open(file_name))

    @classmethod
    def process_config(cls, config_dict, **kwargs):
        """ Load a file into a new Data instance storing configuration in a JSON format """
        return cls(conf=Configuration.process_config(config_dict, **kwargs))

    def init(self):
        """ Open the configured database """
        self._init_rdf_graph()
        L.debug("opening %s", self.source)
        try:
            self.source.open()
        except OpenFailError as e:
            L.error('Failed to open the data source because: %s', e)
            raise

        nm_store = self.get(NAMESPACE_MANAGER_STORE_KEY, None)
        if nm_store is not None:
            # the graph here is just for the reference to the store, so we don't need the
            # extra stuff that comes with the "sources"
            nm_graph = Graph(self[NAMESPACE_MANAGER_STORE_KEY])
            nm_store_conf = self.get(NAMESPACE_MANAGER_STORE_CONF_KEY, None)
            # If there's no store conf, this store is assumed to be already "opened" upon
            # construction
            if nm_store_conf is not None:
                nm_graph.open(nm_store_conf)
            nm = _NamespaceManager(nm_graph)

        else:
            nm = _NamespaceManager(self['rdf.graph'])
        self[NAMESPACE_MANAGER_KEY] = nm
        self['rdf.graph'].namespace_manager = nm

        # A runtime version number for the graph should update for all changes
        # to the graph
        self['rdf.graph.change_counter'] = 0

        self['rdf.graph']._add = self['rdf.graph'].add
        self['rdf.graph']._remove = self['rdf.graph'].remove
        self['rdf.graph'].add = self._my_graph_add
        self['rdf.graph'].remove = self._my_graph_remove
        try:
            with self[TRANSACTION_MANAGER_KEY]:
                nm.bind("", self['rdf.namespace'])
        except Exception:
            L.warning("Failed to bind default RDF namespace %s", self['rdf.namespace'], exc_info=True)
        ACTIVE_CONNECTIONS.append(self)

    def openDatabase(self):
        self.init()

    init_database = init

    def _my_graph_add(self, triple):
        self['rdf.graph']._add(triple)

        # It's important that this happens _after_ the update otherwise anyone
        # checking could think they have the lastest version when they don't
        self['rdf.graph.change_counter'] += 1

    def _my_graph_remove(self, triple_or_quad):
        self['rdf.graph']._remove(triple_or_quad)

        # It's important that this happens _after_ the update otherwise anyone
        # checking could think they have the lastest version when they don't
        self['rdf.graph.change_counter'] += 1

    def destroy(self):
        """ Close a the configured database """
        graph = self.source.get()
        nm = self.get(NAMESPACE_MANAGER_KEY, None)
        if nm is not None and nm.graph is not graph:
            nm.graph.close(commit_pending_transaction=False)
        self.source.close()
        try:
            ACTIVE_CONNECTIONS.remove(self)
        except ValueError:
            L.debug("Attempted to close a database which was already closed")

    close = closeDatabase = destroy

    def _init_rdf_graph(self):
        # Set these in case they were left out
        self['rdf.source'] = self.get('rdf.source', 'default')
        self['rdf.store'] = self.get('rdf.store', 'default')
        self['rdf.store_conf'] = self.get('rdf.store_conf', 'default')
        source = SOURCES[self['rdf.source'].lower()](conf=self)
        self.source = source

        self.link('semantic_net_new', 'semantic_net', 'rdf.graph')
        self['rdf.graph'] = source
        return source

    def _molecule_hash(self, data):
        return URIRef(
            self.molecule_namespace[
                hashlib.sha224(
                    str(data)).hexdigest()])


class ContextChangedEvent(Event):
    pass


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


class RDFSource(Configurable, ConfigValue):
    """
    Base class for data sources.

    Alternative sources should derive from this class
    """

    def __init__(self, **kwargs):
        super(RDFSource, self).__init__(**kwargs)
        self.graph = False

    def get(self):
        if self.graph is False:
            raise Exception(
                "Must call openDatabase on Data object before using the database")
        return self.graph

    def close(self):
        if self.graph is False:
            return
        self.graph.close(commit_pending_transaction=False)
        self.graph = False

    def open(self):
        """ Called on ``owmeta_core.connect()`` to set up and return the rdflib graph.
        Must be overridden by sub-classes.
        """
        raise NotImplementedError()


def _rdf_literal_to_gp(x):
    return x.n3()


def _triples_to_bgp(trips):
    # XXX: Collisions could result between the variable names of different
    # objects
    g = " .\n".join(" ".join(_rdf_literal_to_gp(x) for x in y) for y in trips)
    return g


class SPARQLSource(RDFSource):

    """ Reads from and queries against a remote data store

        ::

            "rdf.source" = "sparql_endpoint"
    """

    def open(self):
        # XXX: If we have a source that's read only, should we need to set the
        # store separately??
        g0 = _Dataset('SPARQLUpdateStore', default_union=True)
        g0.open(tuple(self.conf['rdf.store_conf']))
        self.graph = g0
        return self.graph


class SleepyCatSource(RDFSource):

    """ Reads from and queries against a local Sleepycat database

        The database can be configured like::

            "rdf.source" = "Sleepycat"
            "rdf.store_conf" = <your database location here>
    """

    def open(self):
        import logging
        # XXX: If we have a source that's read only, should we need to set the
        # store separately??
        g0 = _Dataset('Sleepycat', default_union=True)
        self.conf['rdf.store'] = 'Sleepycat'
        g0.open(self.conf['rdf.store_conf'], create=True)
        self.graph = g0
        logging.debug("Opened SleepyCatSource")


class DefaultSource(RDFSource):

    """ Reads from and queries against a configured database.

        The default configuration.

        The database store is configured with::

            "rdf.source" = "default"
            "rdf.store" = <your rdflib store name here>
            "rdf.store_conf" = <your rdflib store configuration here>

        Leaving unconfigured simply gives an in-memory data store.
    """

    def open(self):
        self.graph = _Dataset(self.conf['rdf.store'], default_union=True)
        self.graph.open(self.conf['rdf.store_conf'], create=True)


class ZODBSourceOpenFailError(OpenFailError):
    def __init__(self, openstr, *args):
        super(ZODBSourceOpenFailError, self).__init__(
                f'Could not open the database file "{openstr}"',
                *args)
        self.openstr = openstr


class ZODBSource(RDFSource):

    """ Reads from and queries against a configured Zope Object Database.

        If the configured database does not exist, it is created.

        The database store is configured with::

            "rdf.source" = "ZODB"
            "rdf.store_conf" = <location of your ZODB database>

        Leaving unconfigured simply gives an in-memory data store.
    """

    def __init__(self, *args, **kwargs):
        super(ZODBSource, self).__init__(*args, **kwargs)
        self.conf['rdf.store'] = "ZODB"

    def open(self):
        self.path = self.conf['rdf.store_conf']
        openstr = os.path.abspath(self.path)

        try:
            fs = FileStorage(openstr)
        except IOError:
            L.exception("Failed to create a FileStorage")
            raise ZODBSourceOpenFailError(openstr)
        except LockError:
            # LockError doesn't give us the lock file name directly and I'm not going to
            # try parsing it out of the error message, but it contains useful info like
            # the process ID holding the lock, so we try to grab that for the user
            lockfile_name = f'{openstr}.lock'
            try:
                lockfile = open(lockfile_name, 'r')
                with lockfile:
                    lockfile_contents = lockfile.read()
            except Exception:
                L.debug("Unable to read lockfile")
            else:
                L.error("Lock file contents: %s", lockfile_contents)

            L.exception('Found database "%s" is locked when trying to open it. '
                    'The PID of this process: %s', openstr, os.getpid(), exc_info=True)
            raise DatabaseConflict(f'Database {openstr} locked')

        tm = self.conf[TRANSACTION_MANAGER_KEY]
        self.zdb = ZODB.DB(fs, cache_size=1600)
        self.conn = self.zdb.open(transaction_manager=tm)
        root = self.conn.root()

        if 'rdflib' not in root:
            store = plugin.get('ZODB', Store)()
            with tm:
                root['rdflib'] = store
        self.graph = _Dataset(root['rdflib'], default_union=True)
        self.graph.open(openstr)

    def close(self):
        if self.graph is False:
            return

        # Abort the current transaction (if there is one, I guess) since we can't close
        # our connection while joined to a transaction...
        try:
            transaction.abort()
        except NoTransaction:
            L.debug("Attempt to abort, but there was no active transaction")
        self.graph.close()
        self.conn.close()
        self.zdb.close()
        self.graph = False


class SQLSource(RDFSource):

    def __init__(self, *args, **kwargs):
        super(SQLSource, self).__init__(*args, **kwargs)
        self.conf['rdf.store'] = self.store_name

    def open(self):
        try:
            from rdflib_sqlalchemy import registerplugins
        except ImportError:
            raise OpenFailError('The rdflib-sqlalchemy package is not installed.'
                    ' You may need to install one of the extras for owmeta_core.'
                    ' For example, change "owmeta_core" in your setup.py or'
                    ' requirements.txt to "owmeta_core[postgres_source_pg8000]" and reinstall')
        registerplugins()

        store = plugin.get("SQLAlchemy", Store)(**self._initargs())
        self.graph = ConjunctiveGraph(store)
        cfg = self._openconfig()
        self.graph.open(cfg, create=True)

    def _initargs(self):
        a = self._initargs_augment()
        if not a or not isinstance(a, dict):
            return dict()
        return a

    def _openconfig(self):
        c = self.conf['rdf.store_conf']
        if isinstance(c, dict):
            c = dict(c)
            url = c.pop('url', None)
            if not url:
                raise OpenFailError('A "url" argument must be provided in config dict')
            c.pop('init_args', None)
            self.url = self._openurl(url)
            c['url'] = self.url
            return c
        else:
            self.url = self._openurl(c)
            return self.url

    def _openurl(self, url):
        return url

    def _initargs_augment(self):
        c = self.conf['rdf.store_conf']
        if isinstance(c, dict):
            initargs = self.conf['rdf.store_conf'].get('init_args', None)
            if initargs:
                return dict(initargs)


class SQLiteSource(SQLSource):
    store_name = 'sqlite'

    def _openurl(self, url):
        return 'sqlite:///' + url


class MySQLSource(SQLSource):
    store_name = 'mysql'


class PostgreSQLSource(SQLSource):
    store_name = 'postgresql'


SOURCES = {'sparql_endpoint': SPARQLSource,
           'sleepycat': SleepyCatSource,
           'default': DefaultSource,
           'zodb': ZODBSource,
           'sqlite': SQLiteSource,
           'mysql': MySQLSource,
           'postgresql': PostgreSQLSource}
'''
Table of possible sources for :confval:`rdf.source`
'''

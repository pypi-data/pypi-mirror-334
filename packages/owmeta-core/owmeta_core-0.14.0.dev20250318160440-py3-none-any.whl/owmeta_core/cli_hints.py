'''
Hints for the CLI wrapper that help mapping from the Python methods to command line
arguments.

:CLI_HINTS: hints accepted by `~.cli_command_wrapper.CLICommandWrapper`
'''

from .cli_common import METHOD_NAMED_ARG

CLI_HINTS = {
    'owmeta_core.command.OWM': {
        'commit': {
            (METHOD_NAMED_ARG, 'message'): {
                'names': ['--message', '-m'],
            },
        },
        'context': {
            (METHOD_NAMED_ARG, 'context'): {
                'nargs': '?',
                'names': ['context'],
            },
        },
        'imports_context': {
            (METHOD_NAMED_ARG, 'context'): {
                'nargs': '?',
                'names': ['context'],
            },
        },
        'clone': {
            (METHOD_NAMED_ARG, 'url'): {
                'names': ['url'],
            },
        },
        'translate': {
            (METHOD_NAMED_ARG, 'translator'): {
                'names': ['translator']
            },
            (METHOD_NAMED_ARG, 'data_sources'): {
                'nargs': '*',
                'names': ['data_sources'],
            },
        },
        'retract': {
            (METHOD_NAMED_ARG, 'subject'): {
                'names': ['subject']
            },
            (METHOD_NAMED_ARG, 'property'): {
                'names': ['property']
            },
            (METHOD_NAMED_ARG, 'object'): {
                'names': ['object']
            }
        },
        'say': {
            (METHOD_NAMED_ARG, 'subject'): {
                'names': ['subject']
            },
            (METHOD_NAMED_ARG, 'property'): {
                'names': ['property']
            },
            (METHOD_NAMED_ARG, 'object'): {
                'names': ['object']
            }
        },
        'save': {
            (METHOD_NAMED_ARG, 'module'): {
                'names': ['module']
            }
        },
        'non_interactive': {
            'names': ['--non-interactive', '-b']
        },
        'declare': {
            (METHOD_NAMED_ARG, 'python_type'): {
                'names': ['python_type']
            },
            (METHOD_NAMED_ARG, 'attributes'): {
                'names': ['attr'],
                'kvlist': True,
                'nargs': '*'
            },
        },
        'IGNORE': ['message', 'progress_reporter', 'prompt', 'connect', 'disconnect',
                'rdf', 'default_context', 'connected', 'cleanup_manager', 'own_rdf',
                'repository', 'transaction_manager']
    },
    'owmeta_core.command.OWMRegistryModuleAccessShow': {
        '__call__': {
            (METHOD_NAMED_ARG, 'module_accessor'): {
                'names': ['module_accessor'],
            },
        },
    },
    'owmeta_core.command.OWMRegistryModuleAccessDeclare': {
        'python_pip': {
            (METHOD_NAMED_ARG, 'package_name'): {
                'names': ['package_name'],
            },
            (METHOD_NAMED_ARG, 'package_version'): {
                'names': ['package_version'],
            },
            (METHOD_NAMED_ARG, 'module_names'): {
                'names': ['--module-name'],
                'action': 'append'
            },
        },
    },
    'owmeta_core.command.OWMContexts': {
        'list_imports': {
            (METHOD_NAMED_ARG, 'context'): {
                'names': ['context'],
            },
        },
        'list_importers': {
            (METHOD_NAMED_ARG, 'context'): {
                'names': ['context'],
            },
        },
        'bundle': {
            (METHOD_NAMED_ARG, 'context'): {
                'names': ['context'],
            },
        },
        'edit': {
            (METHOD_NAMED_ARG, 'context'): {
                'names': ['context'],
                'nargs': '?'
            },
            (METHOD_NAMED_ARG, 'list_formats'): {
                'nargs': '?'
            }
        },
        'rm': {
            (METHOD_NAMED_ARG, 'context'): {
                'names': ['context'],
                'nargs': '?'
            },
        },
        'add_import': {
            (METHOD_NAMED_ARG, 'importer'): {
                'names': ['importer'],
            },
            (METHOD_NAMED_ARG, 'imported'): {
                'names': ['imported'],
                'nargs': '+'
            },
        },
        'rm_import': {
            (METHOD_NAMED_ARG, 'importer'): {
                'names': ['importer'],
            },
            (METHOD_NAMED_ARG, 'imported'): {
                'names': ['imported'],
                'nargs': '*'
            },
        },
        'serialize': {
            (METHOD_NAMED_ARG, 'context'): {
                'names': ['context'],
                'nargs': '?'
            },
            (METHOD_NAMED_ARG, 'destination'): {
                'names': ['--destination', '-w']
            },
            (METHOD_NAMED_ARG, 'format'): {
                'names': ['--format', '-f']
            }
        },
    },
    'owmeta_core.command.OWMNamespace': {
        'bind': {
            (METHOD_NAMED_ARG, 'prefix'): {
                'names': ['prefix'],
            },
            (METHOD_NAMED_ARG, 'uri'): {
                'names': ['uri'],
            },
        },
    },
    'owmeta_core.commands.bundle.OWMBundleRemote': {
        'show': {
            (METHOD_NAMED_ARG, 'name'): {
                'names': ['name'],
            },
        },
        'remove': {
            (METHOD_NAMED_ARG, 'name'): {
                'names': ['name'],
            },
        }
    },
    'owmeta_core.commands.bundle.OWMBundleRemoteAdd': {
        '__call__': {
            (METHOD_NAMED_ARG, 'name'): {
                'names': ['name'],
            },
            (METHOD_NAMED_ARG, 'url'): {
                'names': ['url'],
            },
        },
    },
    'owmeta_core.commands.bundle.OWMBundleRemoteUpdate': {
        '__call__': {
            (METHOD_NAMED_ARG, 'name'): {
                'names': ['name'],
            },
            (METHOD_NAMED_ARG, 'url'): {
                'names': ['url'],
            },
        },
    },
    'owmeta_core.commands.bundle.OWMBundle': {
        'fetch': {
            (METHOD_NAMED_ARG, 'bundle_id'): {
                'names': ['bundle_id'],
            },
        },
        'load': {
            (METHOD_NAMED_ARG, 'input_file_name'): {
                'names': ['input'],
            },
        },
        'save': {
            (METHOD_NAMED_ARG, 'bundle_id'): {
                'names': ['bundle_id'],
            },
            (METHOD_NAMED_ARG, 'output'): {
                'names': ['output'],
            },
        },
        'install': {
            (METHOD_NAMED_ARG, 'bundle'): {
                'names': ['bundle'],
            },
        },
        'deregister': {
            (METHOD_NAMED_ARG, 'bundle_id'): {
                'names': ['bundle_id'],
            },
        },
        'register': {
            (METHOD_NAMED_ARG, 'descriptor'): {
                'names': ['descriptor'],
            },
        },
        'deploy': {
            (METHOD_NAMED_ARG, 'bundle_id'): {
                'names': ['bundle_id'],
            },
        },
        'checkout': {
            (METHOD_NAMED_ARG, 'bundle_id'): {
                'names': ['bundle_id'],
            },
        },
    },
    'owmeta_core.command.OWMSource': {
        'show': {
            (METHOD_NAMED_ARG, 'data_source'): {
                'names': ['data_source'],
            },
        },
        'derivs': {
            (METHOD_NAMED_ARG, 'data_source'): {
                'names': ['data_source'],
            },
        },
    },
    'owmeta_core.command.OWMTranslator': {
        'show': {
            (METHOD_NAMED_ARG, 'translator'): {
                'names': ['translator'],
            },
        },
        'create': {
            (METHOD_NAMED_ARG, 'translator_type'): {
                'names': ['translator_type'],
            },
        },
    },
    'owmeta_core.command.OWMConfig': {
        'set': {
            (METHOD_NAMED_ARG, 'key'): {
                'names': ['key'],
            },
            (METHOD_NAMED_ARG, 'value'): {
                'names': ['value'],
            },
        },
        'get': {
            (METHOD_NAMED_ARG, 'key'): {
                'names': ['key'],
            },
        },
        'delete': {
            (METHOD_NAMED_ARG, 'key'): {
                'names': ['key'],
            },
        },
    },
}

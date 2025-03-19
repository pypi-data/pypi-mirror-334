from contextlib import contextmanager
import impmagic


@impmagic.loader(
    {'module':'sys'}
)
@contextmanager
def ignore_site_packages_paths():
    paths = sys.path
    sys.path = list(filter(
        None,
        filter(lambda i: 'site-packages' not in i, sys.path)
    ))
    yield
    sys.path = paths

@impmagic.loader(
    {'module':'sys'},
    {'module':'inspect'}
)
@contextmanager
def ignore_module(module_name):
    original_module = sys.modules.copy()  # Récupérer le module original ou None
    for element in original_module:
        if element==module_name or element==module_name+".":
            del sys.modules[element]
    try:
        yield
    finally:
        if original_module:
            sys.modules = original_module 

@impmagic.loader(
    {'module':'sys'},
    {'module':'importlib', 'submodule': ['import_module']},
    {'module':'os.path', 'submodule': ['exists', 'isfile']}
)
def is_native_module(module):
    if module in ['pip', 'setuptools']:
        return True
    if exists(module+".py") or exists(module+".pyw"):
        return False
    else:
        if module in sys.builtin_module_names:
            return True
        with ignore_module(module):
            with ignore_site_packages_paths():
                try:
                    import_module(module)
                except ModuleNotFoundError:
                    return False
                except ImportError:
                    return False
                else:
                    return True
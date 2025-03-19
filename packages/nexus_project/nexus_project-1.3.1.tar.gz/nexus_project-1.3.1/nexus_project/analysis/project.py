import impmagic

class Find_modules:
    @impmagic.loader(
        {'module':'ast'},
        {'module': 'os.path', 'submodule': ['exists']},
        {'module': 'app.display', 'submodule': ['logs']}
    )
    def __init__(self, file, submodule=False):
        if exists(file):
            with open(file) as f:
                self.tree = ast.parse(f.read())
        else:
            logs(f"Fichier {file} introuvable", "critical")
            exit()
        self.result = []
        self.submodule=submodule

    @impmagic.loader(
        {'module':'ast'}
    )
    def get_variable(self, name):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                if isinstance(node.targets[0], ast.Name) and node.targets[0].id == name:
                    return node.value
            if isinstance(node, ast.For):
                target_node = node.target
                iter_node = node.iter
                if isinstance(target_node, ast.Name) and target_node.id == name:
                    if isinstance(iter_node, ast.Name):
                        data = self.get_variable(iter_node.id)
                        if isinstance(data, ast.Constant):
                            return data.value
                        else:
                            return self.get_value(data)

    @impmagic.loader(
        {'module':'ast'}
    )
    def get_value(self, data, result=None):
        try:
            if isinstance(data, ast.Constant):
                return data.value

            elif isinstance(data, ast.Tuple):
                result = ()
                for element in data.elts:
                    if isinstance(element, ast.Constant):
                        result = result + (element,)
                    else:
                        result = result + (self.get_value(element), )

            elif isinstance(data, ast.Dict):
                result = {}
                for i, value in enumerate(data.values):
                    if isinstance(value, ast.Constant):
                        result[data.keys[i].value] = value.value
                    else:
                        value = self.get_value(value)
                        result[data.keys[i].value] = value

            elif isinstance(data, ast.List):
                result = []
                for element in data.elts:
                    if isinstance(element, ast.Constant):
                        result.append(element.value)
                    else:
                        result.append(self.get_value(element))

            elif isinstance(data, ast.Subscript):
                key = self.get_value(data.slice)
                res_var = self.get_variable(data.value.id)
                
                result = []
                for el in res_var:
                    if el!=None and isinstance(el, dict):
                        result.append(el[key])
                    else:
                        result = res_var

            elif isinstance(data, ast.Name):
                res_var = self.get_variable(data.id)
                if isinstance(res_var, list) or isinstance(res_var, tuple):
                    result = []
                    for element in res_var:
                        if isinstance(element, str):
                            result.append(element)
                        else:
                            result.append(self.get_value(element))
                elif isinstance(res_var, str):
                    result = res_var
                else:
                    result = self.get_value(res_var)
            return result
        except:
            return None

    def add_module(self, name):
        if not name.startswith('__'):
            if not self.submodule and '.' in name:
                name = name.split(".")[0]

            if name not in self.result:
                self.result.append(name)

    @impmagic.loader(
        {'module':'ast'}
    )
    def search(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if hasattr(node.func, 'id') and node.func.id=='__import__' or node.func.id=="import_module":
                        res = self.get_value(node.args[0])
                        if isinstance(res, list):
                            for element in res:
                                self.add_module(element)
                        else:
                            if res!=None:
                                self.add_module(res)
                if isinstance(node.func, ast.Attribute):
                    if hasattr(node.func.value, 'id') and  (node.func.value.id=="importlib" and node.func.attr=="import_module"):
                        self.add_module(self.get_value(node.args[0]))
                    elif hasattr(node.func.value, 'id') and  (node.func.value.id=="impmagic" and node.func.attr=="loader"):
                        for element in node.args:
                            data = self.get_value(element)
                            if isinstance(data, dict) and 'module' in data:
                                if 'submodule' in data and isinstance(data['submodule'], list):
                                    for submodule in data['submodule']:
                                        self.add_module(data['module']+"."+submodule)
                                else:
                                    self.add_module(data['module'])

            elif isinstance(node, ast.Import):
                for name in node.names:
                    self.add_module(name.name)
            elif isinstance(node, ast.ImportFrom):
                self.add_module(node.module)

@impmagic.loader(
    {'module':'os.path', 'submodule': ['exists', 'isdir', 'isfile']},
    {'module':'glob', 'submodule': ['glob']},
    {'module':'package.check', 'submodule': ['is_native_module']},
)
def get_modules_from_project(files, recursive=True):
    data = {'interne':[], 'dependency':[], 'externe':[]}
    analysed = []
    search = True
    while search:
        new = []
        for file in files:
            if file not in analysed:
                analysed.append(file)
            a = Find_modules(file, submodule=False)
            a.search()
            for mod in a.result:
                if exists(mod) and isdir(mod):
                    if mod not in data['interne']:
                        data['interne'].append(mod)
                    if recursive:
                        for mod_file in glob(mod + '/**/*.py', recursive=True):
                            if mod_file not in analysed:
                                new.append(mod_file)

                elif exists(mod+".py") and isfile(mod+".py"):
                    if mod+".py" not in analysed and recursive:
                        new.append(mod+".py")
                    if mod not in data['interne']:
                        data['interne'].append(mod)
                elif exists(mod+".pyw") and isfile(mod+".pyw"):
                    if mod+".pyw" not in analysed and recursive:
                        new.append(mod+".pyw")
                    if mod not in data['interne']:
                        data['interne'].append(mod)
                else:
                    if is_native_module(mod):
                        if mod not in data['externe']:
                            data['externe'].append(mod)
                    else:
                        if mod not in data['dependency']:
                            data['dependency'].append(mod)

        if len(new)==0:
            search = False
        
        files = new

    return data


@impmagic.loader(
    {'module':'app.display', 'submodule': ['prompt']},
    {'module':'package.package', 'submodule': ['in_repo', 'get_alias', 'set_alias']}
)
#Liste les packages dont les noms d'install sont différents et sans alias
def check_realname(package, init=False):
    alias = get_alias(init)
    insert_alias = alias.copy()

    if package in alias:
        fnd = alias[package]
        if isinstance(fnd, str):
            return fnd
        else:
            data = {}
            if 'windows' in fnd:
                if in_repo(fnd['windows']):
                    data['windows'] = fnd['windows']
            if 'linux' in fnd:
                if in_repo(fnd['linux']):
                    data['linux'] = fnd['linux']

            if len(data):
                return data
    else:
        packagename = package
        while not in_repo(package):
            package = prompt(packagename)
            if package=="{exclude}":
                package = None
                break

        if package and packagename!=package:
            insert_alias[packagename] = package

    if alias!=insert_alias:
        set_alias(insert_alias)

    return package
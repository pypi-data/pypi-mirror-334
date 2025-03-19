import impmagic

class StructureCorrect:
    def __init__(self, projectfolder, exclude='dist'):
        self.projectfolder = projectfolder
        self.exclude = exclude

    @impmagic.loader( 
        {'module':'os'}, 
        {'module':'os.path', 'submodule': ['join']}
    )
    def init(self):            
        self.initial_files_dirs = set(join(dp, f) for dp, dn, filenames in os.walk(self.projectfolder) for f in filenames + dn)

    @impmagic.loader(
        {'module':'shutil'}, 
        {'module':'os'}, 
        {'module':'os.path', 'submodule': ['join', 'isdir', 'exists', 'abspath']}
    )
    def purge(self):
        final_files_dirs = set(join(dp, f) for dp, dn, filenames in os.walk(self.projectfolder) for f in filenames + dn)
        self.result = {'dirs':[], 'files':[]}
        exclude = join(abspath('.'), self.exclude)
        final_files_dirs = sorted(final_files_dirs)
        for file in final_files_dirs:
            if file not in self.initial_files_dirs:
                if not file.startswith(exclude):
                    print(file)
                    find = False
                    for element in self.result['dirs']:
                        if file.startswith(element):
                            find = True

                    if not find:
                        if isdir(file):
                            if not file.endswith(self.exclude):
                                shutil.rmtree(file)
                            else:
                                self.result['dirs'].append(file)
                        else:
                            if exists(file):
                                os.remove(file)
                                self.result['files'].append(file)


#Récupère une liste de fichiers et retourne une liste de chemin
@impmagic.loader(
    {'module':'glob', 'submodule': ['glob']}
)
def list_to_content(content_backup):
    result = []
    for element in content_backup:
        if len(element):
            if isinstance(element, str):
                if exists(element):
                    if isfile(element):
                        result.append(element)
                    elif isdir(element):
                        folder = glob(element+"/*")+glob(element+"/.*")
                        if len(folder):
                            res = list_to_content(folder)
                            if len(res):
                                result+=res
                        else:
                            #pour inclure les dossiers vide
                            result.append(element)
                else:
                    logs(f"{element} introuvable", "warning")
            else:
                res = list_to_content(element)
                if len(res):
                    result+=res
    return result



@impmagic.loader(
    {'module':'template.toml_format', 'submodule': ['DEFAULT_TOML']},
    {'module':'app.display', 'submodule': ['logs']},
    {'module':'os.path', 'submodule': ['exists', 'isfile', 'isdir']}
)
def list_projectfile(tfile):
    project_dir = tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section'])
    include_files = tfile.get_key(DEFAULT_TOML['include_files']['name'],DEFAULT_TOML['include_files']['section'])
    
    license_file = tfile.get_key(DEFAULT_TOML['license_file']['name'],DEFAULT_TOML['license_file']['section'])
    readme = tfile.get_key(DEFAULT_TOML['readme']['name'],DEFAULT_TOML['readme']['section'])
    changelog = tfile.get_key(DEFAULT_TOML['changelog']['name'],DEFAULT_TOML['changelog']['section'])

    content_backup = ['nexus.toml', '.package_alias', project_dir, include_files, license_file, readme, changelog]

    content = list_to_content(content_backup)

    return content


#Parse les fichiers du projet pour en faire un dictionnaire et compresse le contenu
@impmagic.loader(
    {'module':'brotli'},
    {'module':'hashlib'},
    {'module':'glob', 'submodule': ['glob']},
    {'module':'os.path', 'submodule': ['exists', 'isfile', 'isdir', 'basename']}
)
def dump_project(projectfolder):
    result = {}

    for file in glob(f"{projectfolder}/*"):
        if isdir(file):
            if basename(file)!="__pycache__":
                result[basename(file)] = dump_project(file)
        else:
            with open(file, 'rb') as f:
                content = f.read()

                result[basename(file)] = {
                    'hash': hashlib.sha256(content).hexdigest(),
                    'content': brotli.compress(content, quality=11).hex()
                }
    return result


@impmagic.loader(
    {'module':'hashlib'},
    {'module':'brotli'},
    {'module':'app.display', 'submodule': ['logs']},
    {'module':'os.path', 'submodule': ['exists', 'join']},
    {'module':'structure.check', 'submodule': ['get_root_project']}
)
def load_file(specific_file, deps, dest=None):
    if specific_file in deps:
        logs(f"Restauration du {specific_file}")

        if specific_file=='project_file':
            deps[specific_file]['name'] = "nexus.toml"

        if 'hash' in deps[specific_file]:
            if 'name' not in deps[specific_file]:
                logs(f"Le snap ne contient pas le nom du fichier {specific_file}", "critical")
                return

            if dest:
                sp_file = join(dest, deps[specific_file]['name'])
            else:
                sp_file = join(get_root_project(), deps[specific_file]['name'])
            inject = True

            if exists(sp_file):
                with open(sp_file, 'rb') as f:
                    hash_file =  hashlib.sha256(f.read()).hexdigest()
                    if hash_file==deps[specific_file]['hash']:
                        inject=False
                        logs(f"Fichier {specific_file} inchangé")

            if 'content' in deps[specific_file]:
                if inject:
                    with open(sp_file, 'wb') as f:
                        f.write(brotli.decompress(bytes.fromhex(deps[specific_file]['content'])))
            else:
                logs(f"Le snap ne contient pas le contenu du fichier {specific_file}")
        else:
            logs(f"Le snap ne contient pas le hash du fichier {specific_file}")


@impmagic.loader(
    {'module':'hashlib'},
    {'module':'brotli'},
    {'module':'os', 'submodule': ['mkdir']},
    {'module':'app.display', 'submodule': ['logs']},
    {'module':'os.path', 'submodule': ['exists', 'isfile', 'join']},
    {'module':'structure.check', 'submodule': ['get_root_project']}
)
def load_project(project_data, dest_dir):
    if not exists(dest_dir):
        mkdir(dest_dir)

    for namefile, element in project_data.items():
        sp_file = join(dest_dir, namefile)
        if 'hash' in element and 'content' in element:
            inject = True

            if exists(sp_file):
                with open(sp_file, 'rb') as f:
                    hash_file =  hashlib.sha256(f.read()).hexdigest()
                    if hash_file==element['hash']:
                        inject=False
                        logs(f"Fichier {sp_file} inchangé")

            if inject:
                logs(f"Restauration de {sp_file}")
                with open(sp_file, 'wb') as f:
                    f.write(brotli.decompress(bytes.fromhex(element['content'])))
        else:
            load_project(element, sp_file)


def tree_project(project_data):
    result = {}

    for namefile, element in project_data.items():
        if 'hash' in element and 'content' in element:
            result[namefile] = ''
        else:
            result[namefile] = tree_project(element)

    return result


def select_file_from_project(file, project_data):
    inject = {}

    if isinstance(file, str):
        file = file.replace("\\", "/").split("/") 
    
    if len(file):
        element = file.pop(0)

        if element in project_data:
            if isinstance(project_data[element], dict) and 'hash' in project_data[element]:
                inject[element] = project_data[element]
            
            elif isinstance(project_data[element], dict) and 'hash' not in project_data[element]:
                if len(file):
                    result = select_file_from_project(file, project_data[element])
                else:
                    result = project_data[element]

                if result:
                    inject[element] = result

            else:
                return None

    return inject


#Compare le code du projet actuel avec le code du snap
@impmagic.loader(
    {'module':'hashlib'}, 
    {'module':'glob', 'submodule': ['glob']},
    {'module':'os.path', 'submodule': ['isdir', 'join', 'basename']},
    {'module':'app.display', 'submodule': ['logs']}
)
def compare_snap_file(projectfolder, project_data, origin=None):
    if not origin:
        origin = projectfolder.replace("\\", "/")

    for file in glob(f"{projectfolder}/*"):
        if basename(file)!="__pycache__":
            if basename(file) in project_data:
                if isdir(file):
                    compare_snap_file(file, project_data[basename(file)], origin)
                else:
                    with open(file, 'rb') as f:
                        hash_file = hashlib.sha256(f.read()).hexdigest()

                    filename = file.replace("\\","/").replace(f'{origin}/', '')
                    
                    if project_data[basename(file)]['hash']==hash_file:
                        logs(f"Fichier {filename} inchangé")
                    else:
                        logs(f"Fichier {filename} modifié", "warning")
            else:
                logs(f"{join(projectfolder, file)} nouvellement créé", "warning")
import __main__
import impmagic


@impmagic.loader(
    {'module':'os', 'submodule':['mkdir']},
    {'module':'sys', 'submodule':['exit']},
    {'module':'app.display', 'submodule':['logs']}
)
def create_folder(name):
    try:
        mkdir(name)
    except FileExistsError:
        logs(f"Le répertoire {name} existe déjà", "error")
        exit()
    except PermissionError:
        logs(f"Vous n'avez pas la permission de créer le répertoire {{name}}.", "error")
        exit()
    except FileNotFoundError:
        logs(f"Le répertoire parent spécifié n'existe pas ou vous n'avez pas accès au répertoire {name}.", "error")
        exit()

@impmagic.loader(
    {'module':'sys', 'submodule':['exit']},
    {'module':'app.display', 'submodule':['logs']},
    {'module':'os.path', 'submodule':['exists']}
)
def create_file(filename, content=''):
    if exists(filename):
        raise FileExistsError(f"Le fichier {filename} existe déjà.")
        exit()
    try:
        with open(filename, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        logs(f"Le répertoire de destination du fichier {filename} n'existe pas.", "error")
        exit()
    except PermissionError:
        logs(f"Vous n'avez pas la permission d'écrire le fichier {filename}.", "error")
        exit()


@impmagic.loader(
    {'module':'template.toml_format', 'submodule':['DEFAULT_TOML']},
    {'module':'toml_nxs.toml', 'submodule':['TOML'], 'as':'TOMLnxs'},
    {'module':'os.path', 'submodule':['exists', 'join', 'splitext', 'expanduser', 'abspath']},
    {'module':'env_nxs.env', 'submodule':['create_environment', 'get_py_version']},
    {'module':'package.package', 'submodule':['dependency_to_list']},
    {'module':'template.readme', 'submodule':['README_TEMPLATE']},
    {'module':'sys_nxs.host', 'submodule':['path_rep']},
    {'module': 'template', 'submodule': ['default_conf']},
    {'module': 'repository.repo', 'submodule': ['Repo']},
    {'module': 'os', 'submodule': ['getcwd']},
    {'module':'sys'}
)
def create_project(project, data, argument, action):
    if action=='new':
        tfile = TOMLnxs(join(project,'nexus.toml'))
        tfile.new(data)
        projectfolder = join(project, tfile.get_key(DEFAULT_TOML['projectname']['name'], DEFAULT_TOML['projectname']['section']))
    elif action=='init':
        tfile = TOMLnxs('nexus.toml')
        tfile.new(data)
        projectfolder = tfile.get_key(DEFAULT_TOML['projectname']['name'], DEFAULT_TOML['projectname']['section'])
    
    create_folder(projectfolder)

    mainfile = tfile.get_key(DEFAULT_TOML['mainfile']['name'],DEFAULT_TOML['mainfile']['section'])
    if mainfile!=None:
        if mainfile!="__init__.py":
            if action=='new':
                create_file(join(projectfolder, mainfile))
            name, extension = splitext(mainfile)
            create_file(join(projectfolder, "__init__.py"), f"from .{name} import *")
        else:
            create_file(join(projectfolder, "__init__.py"))

    readmefile = tfile.get_key(DEFAULT_TOML['readme']['name'],DEFAULT_TOML['readme']['section'])
    if action=='new':
        create_file(join(project, readmefile), README_TEMPLATE.format(**{"projectname": tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section']),"description": tfile.get_key(DEFAULT_TOML['description']['name'],DEFAULT_TOML['description']['section'])}))
    elif action=='init' and not exists(readmefile):
        create_file(readmefile, README_TEMPLATE.format(**{"projectname": tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section']),"description": tfile.get_key(DEFAULT_TOML['description']['name'],DEFAULT_TOML['description']['section'])}))

    if 'license_file' in data and data['license_content']!=None:
        create_file(join(project, data['license_file']), data['license_content'])

    if not argument.noenv and (__main__.nxs.conf.load(val='virtualenvs.create', section='',default=default_conf.virtualenvs_create) or argument.env):
        #Nom du projet                    
        projectname = data['projectname']
        #Nettoyage du dossier env avant création                    
        clear_env = __main__.nxs.conf.load(val='virtualenvs.clear', section='',default=default_conf.virtualenvs_clear)
        if argument.clear:
            clear_env = True

        #Pré-installation des dépendances    
        if not hasattr(__main__.nxs, 'py_version'):
            __main__.nxs.py_version = get_py_version(sys.executable)   
        mdm_env = dependency_to_list(data['dependencies'])

        #Mise à jour de pip                    
        upgradepip_env = __main__.nxs.conf.load(val='virtualenvs.upgradepip', section='',default=default_conf.virtualenvs_upgradepip)
        if argument.upgradepip:
            upgradepip_env = True
        
        symlinks_env = __main__.nxs.conf.load(val='virtualenvs.symlinks', section='',default=default_conf.virtualenvs_symlinks)
        sitepackages_env = __main__.nxs.conf.load(val='virtualenvs.system-site-packages', section='',default=default_conf.virtualenvs_system_site_packages)
        proxy_env = __main__.nxs.conf.load(val='proxy', section='',default=default_conf.proxy)

        folder_env = __main__.nxs.conf.load(val='virtualenvs.foldername', section='',default=default_conf.virtualenvs_foldername)
        if hasattr(argument, 'envpath') and argument.envpath!=None:
            folder_env = argument.envpath

        if (argument.inproject and not argument.incache) or (not argument.inproject and not argument.incache and __main__.nxs.conf.load(val='virtualenvs.in-project', section='',default=default_conf.virtualenvs_in_project)):
            if action=='new':
                virtdir = join(project, folder_env, "default")
            elif action=='init':
                virtdir = join(folder_env, "default")
        else:
            #if os.path.isabs(path):
            cachedir = __main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)
            virtdir = join(expanduser(cachedir), folder_env, projectname, "default")
        
        venv_data = create_environment(virtdir, name=projectname, installmodule=mdm_env, clear=clear_env, upgradepip=upgradepip_env, symlinks=symlinks_env, sitepackages=sitepackages_env, proxy=proxy_env)
        
        for element in venv_data:
            tfile.edit_key(element, venv_data[element].replace(join(abspath('.'), project)+path_rep[0],"").replace("\\","/"), "venv.default")
        tfile.edit_key("default", True, "venv.default")

    if not argument.norepo and (__main__.nxs.conf.load(val='repo.create', section='',default=default_conf.repo_create) or argument.repo):
        if action=='new':
            repo = Repo(project, create=True)
        elif action=='init':
            repo = Repo(getcwd(), create=True)
        if __main__.nxs.conf.load(val='repo.branch_autocreate', section='',default=default_conf.repo_branch_autocreate):
            version = tfile.get_key(DEFAULT_TOML['version']['name'],DEFAULT_TOML['version']['section'])
            repo.switch_branch(version, create=True)


@impmagic.loader(
    {'module':'os.path', 'submodule':['join', 'expanduser']},
    {'module':'env_nxs.env', 'submodule':['create_environment', 'get_py_version']},
    {'module':'package.package', 'submodule':['dependency_to_list']},
    {'module':'sys_nxs.host', 'submodule':['path_rep']},
    {'module': 'template', 'submodule': ['default_conf']},
    {'module':'sys'}
)
def create_project_environment(envname, project, data, tfile, first=False, cache=False, prompt=None, clear=False, nocheck=False):
    #Nom du projet                    
    projectname = data['projectname']
    #Nettoyage du dossier env avant création                    
    clear_env = __main__.nxs.conf.load(val='virtualenvs.clear', section='',default=default_conf.virtualenvs_clear)
    if clear_env:
        clear = True

    #Pré-installation des dépendances    
    if not hasattr(__main__.nxs, 'py_version'):
        __main__.nxs.py_version = get_py_version(sys.executable)

    if 'dependencies' in data and data['dependencies']!=None and len(data['dependencies']): 
        mdm_env = dependency_to_list(data['dependencies'], nocheck=nocheck)
    else:
        mdm_env = []


    if mdm_env is None:
        exit()

    #Mise à jour de pip                    
    upgradepip_env = __main__.nxs.conf.load(val='virtualenvs.upgradepip', section='',default=default_conf.virtualenvs_upgradepip)
    
    symlinks_env = __main__.nxs.conf.load(val='virtualenvs.symlinks', section='',default=default_conf.virtualenvs_symlinks)
    sitepackages_env = __main__.nxs.conf.load(val='virtualenvs.system-site-packages', section='',default=default_conf.virtualenvs_system_site_packages)
    proxy_env = __main__.nxs.conf.load(val='proxy', section='',default=default_conf.proxy)

    folder_env = __main__.nxs.conf.load(val='virtualenvs.foldername', section='',default=default_conf.virtualenvs_foldername)

    cachedir = expanduser(__main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir))
    
    if cache==False and __main__.nxs.conf.load(val='virtualenvs.in-project', section='',default=default_conf.virtualenvs_in_project):
        virtdir = join(project, folder_env, envname)
    else:
        virtdir = join(cachedir, folder_env, projectname, envname)

    venv_data = create_environment(virtdir, name=envname, installmodule=mdm_env, clear=clear, upgradepip=upgradepip_env, symlinks=symlinks_env, sitepackages=sitepackages_env, proxy=proxy_env, prompt=prompt)
    
    for element in venv_data:
        if venv_data[element].startswith(cachedir):
            tfile.edit_key(element, venv_data[element].replace("\\","/"), "venv."+envname)
        elif project:
            tfile.edit_key(element, venv_data[element].replace(project+path_rep[0],"").replace("\\","/"), "venv."+envname)
        else:
            tfile.edit_key(element, venv_data[element].replace("\\","/"), "venv."+envname)
    
    #Ajoute default si c'est le premier environnement créé
    if first:
        tfile.edit_key("default", True, "venv."+envname)


@impmagic.loader(
    {'module':'datetime'},
    {'module':'analysis.project', 'submodule': ['get_modules_from_project']},
    {'module':'app.display', 'submodule': ['prompt', 'logs']}, 
    {'module':'template.toml_format', 'submodule': ['DEFAULT_TOML']},
    {'module':'structure.license', 'submodule': ['licenses_availables', 'get_license_content', 'get_license_fullname', 'license_exist', 'detect_license']},
    {'module':'toml_nxs.check.check', 'submodule': ['check_list', 'check_dependency_format']},
    {'module':'os.path', 'submodule': ['exists']}
)
def construct_new_data(nameproject, action):
    data = {}
    data['projectname'] = prompt("Nom du projet", nameproject)
    data['version'] = prompt("Version", DEFAULT_TOML['version']['default_value'])
    data['description'] = prompt("Description", DEFAULT_TOML['description']['default_value'])
    data['mainfile'] = prompt("Fichier principal", "__init__.py")
    if action=='init':
        if not exists(data['mainfile']):
            logs(f"Le fichier {data['mainfile']} n'existe pas", "critical")
            exit()
    data['authors'] = check_list(prompt("authors", DEFAULT_TOML['authors']['default_value']), "authors")
    data['maintainers'] = check_list(prompt("maintainers", DEFAULT_TOML['maintainers']['default_value']), "maintainers")

    if action=='init' and license_exist()!=False:
        license_file = license_exist()
        data['license'] = detect_license(license_file)
        data['license_content'] = None
        data['license_file'] = license_file
    else:
        data['license'] = prompt("license", DEFAULT_TOML['license']['default_value'])
        if licenses_availables(data['license']):
            license_content = get_license_content(data['license'])
            if '[year]' in license_content:
                year = prompt("date license", datetime.date.today().strftime("%Y"))
            if '[fullname]' in license_content:
                if len(data['authors'])>0:
                    author = prompt("author license", data['authors'][0])
                else:
                    author = prompt("author license")
            data['license_content'] = license_content.replace('[year]',year).replace('[fullname]', author)
            data['license_file'] = 'LICENSE'

            data['license'] =   (data['license'])

    if action=='new':
        data['dependencies'] = check_dependency_format(prompt("dependencies", DEFAULT_TOML['dependencies']['default_value']))
    else:
        module_project = get_modules_from_project([data['mainfile']])
        data['dependencies'] = check_dependency_format(module_project['dependency'])
        data['package'] = module_project['externe']+module_project['dependency']
        data['include'] = module_project['interne']

    return data
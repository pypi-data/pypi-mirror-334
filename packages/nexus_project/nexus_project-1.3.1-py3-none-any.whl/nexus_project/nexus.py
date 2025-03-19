import __main__
import impmagic
import sys
import os
# Action avant arrêt de l'application
import atexit
import signal

nexus_logo = "                                                            \n    @@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@       \n     @@%=::::::::::----=%@@            @@%+-----=*@@      \n       @+:::::::::::----=@@              @=----=@@         \n        @%::::::::::::---#@ @%+=+*%@      @=----@           \n          @+:::::::::::---+@  @@+---*@@   @+---+@           \n           @%::::::::::::---%@  @@+---+@@ @*---+@           \n             @=::::::::::.---+@   @@+---=@@*---+@           \n              @#::::::::::.:---%@   @@+---=+---+@           \n                @-:::::::::..---+@    @@-------+@           \n                 @*::::::::::.:---@@    @%=----+@           \n                  @@-:::::::::..---*@     @#---+@           \n       @@           @+::::::::::.:--=@@     @*-+@           \n      @@*@           @@-:::::::::.:---#@     @@*@           \n       @==%@           @+::::::::::.:--+@      @            \n       @=--=@@          @%::::::::::.:---%@                 \n       @=----+@           @=:::::::::::---*@                \n       @=------#@          @#::::::::::.:---@               \n       @=--------%@          @-:::::::::::---#@             \n       @=---+%----=@@         @+:::::::::::---+@            \n       @=---+@@%=---+@          %::::::::::::--=@           \n       @=---=@  @#=---*@         @=:::::::::::---%@         \n       @=---=@    @%=---*@        @=:::::::::::---*@        \n      @@=----#@     @%=---*@@     @-:::::::::::::--=@@      \n     @@==-----*@@     @%*+===*@ @%::::::::::::::::---+@@    \n   @%+===========#@        @@@#=:::::::::::::::::::::--=#@  \n   @@@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
nexus_ascii_name = "      ___           __      __   __   __        ___  __  ___ \n|\\ | |__  \\_/ |  | /__`    |__) |__) /  \\    | |__  /  `  |  \n| \\| |___ / \\ \\__/ .__/    |    |  \\ \\__/ \\__/ |___ \\__,  |  \n"

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

#Nettoyage du cache ou autres fichiers avant arrêt
__main__.ToDoClear = []

@impmagic.loader(
    {'module':'app.display', 'submodule': ['logs']},
    {'module':'os.path', 'submodule': ['basename']},
    {'module':'shutil', 'submodule': ['rmtree']}
)
def clear_nexus():
    for file in __main__.ToDoClear:
        logs(f"Suppression de l'environnement {basename(file)}")
        if os.path.exists(file) and os.path.isdir(file):
            rmtree(file)
        elif os.path.exists(file) and os.path.isfile(file):
            os.remove(file)

class Nexus:
    @impmagic.loader(
        {'module':'zpp_config', 'submodule': ['Config']},
        {'module':'shutil', 'submodule': ['copyfile']},
        {'module':'app.display', 'submodule': ['print_nxs']},
        {'module':'template', 'submodule': ['default_conf','color']},
        {'module':'os.path', 'submodule': ['abspath','expanduser','exists']}
    )
    def __init__(self):
        self.workspace = abspath('.')
        if os.name=="nt":
            self.ini_file = os.path.join(expanduser("~\\AppData\\Local\\Nexus\\.config"),"nexus.ini")
        else:
            self.ini_file = os.path.join(expanduser("~/.config/Nexus/.config"),"nexus.ini")
        if not exists(self.ini_file):
            print("Création du fichier de config")
            if os.name=="nt":
                default_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"template","default_ini")
            else:
                default_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"template","default_ini_lin")
            if exists(default_file):
                if not exists(os.path.dirname(self.ini_file)):
                    os.makedirs(os.path.dirname(self.ini_file), exist_ok=True)
                copyfile(default_file, self.ini_file)
            else:
                print("Fichier de conf impossible à générer", color=__main__.color["light_red"])
        self.license_cache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"license_cache.json")
        self.conf = Config(self.ini_file)

        if self.conf.load(val='logs.truecolor', section='',default=default_conf.logs_truecolor):
            __main__.color = color.truecolor
        else:
            __main__.color = color.classic

        self.metadata_source = self.conf.load(val='metadata.source', section='',default=default_conf.metadata_source)

        self.threadmax = self.conf.load(val='threadmax', section='',default=default_conf.threadmax)
    

    def help(self):
        DATA = {
            'PROJECT MANAGEMENT': {
                'new': "Création d'un nouveau projet",
                'init': "Initialisation d'un projet à partir de fichier existant",
                'clearcode': "Analyser la lisibilité du code", 
                'analyse': "Analyse statique de code",
                'securiscan': "Analyse de la sécurité du code",
                'compile': "Compilation du projet",
                'pack': "Création du package publiable",
                'publish': "Publication du package",
                'version': "Affichage/Changement de la version du projet",
                'config': "Affichage/Modification de la configuration de nexus",
                'provisioning': "Réserve le nom d'un package sur un repository",
                'measure': "Mesure de temps d'exécution d'une commande",
                'backup': "Sauvegarde du projet en cours",
                'project': "Afficher les informations du projet",
                'changelog': "Ajouter des informations au changelog",
                'licence': "Générer une licence",
                'entrypoint': "Ajouter des entrypoint",
            },
            'PACKAGE MANAGEMENT': {
                'search': "Recherche d'un package",
                'info': "Afficher les informations d'un package",
                'install': "Installation des dépendances",
                'uninstall': "Désinstallation des dépendances",
                'update': "Mise à jour des dépendances",
                'add': "Ajout de dépendances dans le projet",
                'remove': "Suppression de dépendances dans le projet",
                'alias': "Gestion des alias de package",
                'lock': "Lock les versions de package",
                'check': "Contrôle la compatibilité des dépendances",
                'snap': "Sauvegarde/Restauration de l'état des dépendances",
                'list': "Lister les packages installés",
                'cache': "Gestion du cache",
                'export': "Exporter les dépendances dans un requirement"
            },
            'ENVIRONMENT MANAGEMENT': {
                'env': "Gestion des environnements d'un projet",
                'sandbox': "Création d'un environnement temporaire",
                'template': "Gestion des templates",
                'run': "Lancement d'une commande ou du projet",
                'shell': "Démarrage du shell python"
            },
            'REPO': {
                'repo': "Action sur le repo",
                'branch': "Action sur les branches du repo",
                'reset': "Restauration depuis un commit",
                'restore': "Restaurer un fichier spécifique",
                'commit': "Commit le travail en cours",
                'tree': "Affiche l'arborescence d'un commit",
            }
        }
        #Stick Letters
        print(nexus_ascii_name)
        max_size = len(max(DATA, key=len))
        for section, data in DATA.items():
            print("\n"+section)
            for key, value in data.items():
                print(f"  {key}{' '*((max_size-len(key))+3)}{value}")

    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'sys_nxs.host', 'submodule': ['path_reg']}, 
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'structure.create', 'submodule': ['create_folder', 'create_project', 'construct_new_data']},
        {'module':'os.path', 'submodule': ['exists']}
    )
    def new(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs new"
        parse.set_description("Création d'un nouveau projet")
        parse.set_argument(longname="env", description="Créer un environnement virtuel", default=False)
        parse.set_argument(longname="noenv", description="Ne pas créer d'environnement virtuel", default=False)
        parse.set_argument(longname="clear", description="Nettoyer le répertoire de l'environnement si existant", default=False)
        parse.set_argument(longname="upgradepip", description="Mettre à jour pip à l'installation", default=False)
        parse.set_argument(longname="inproject", description="Créer l'environnement dans le projet", default=False)
        parse.set_argument(longname="incache", description="Créer l'environnement dans le cache", default=False)
        parse.set_argument(longname="envpath", description="Préciser le nom du répertoire de l'environnement", store="value", default=None)
        parse.set_argument(longname="repo", description="Créer le repo du projet", default=False)
        parse.set_argument(longname="norepo", description="Ne pas créer le repo du projet", default=False)
        parse.set_parameter("NAMEPROJECT", description="Nom du projet")
        parameter, argument = parse.load()

        if parameter!=None and len(parameter)>0:
            project = path_reg(parameter[0])
            try:
                #Création du dossier projet
                create_folder(project)
            except FileExistsError:
                logs("Le répertoire/fichier existe déjà", "error")
                sys.exit()
            except PermissionError:
                logs("Vous n'avez pas la permission de créer ce répertoire/fichier.", "error")
                sys.exit()
            except FileNotFoundError:
                logs("Le répertoire/fichier parent spécifié n'existe pas ou vous n'avez pas accès à ce répertoire/fichier.", "error")
                sys.exit()
            
            data = construct_new_data(parameter[0], 'new')
            create_project(project, data, argument, action='new')


    @impmagic.loader(
        {'module':'zpp_args'},
        {'module': 'subprocess', 'submodule': ['Popen', 'PIPE']},
        {'module': 'time', 'submodule': ['perf_counter']},
        {'module': 'datetime', 'submodule': ['timedelta']}
    )
    def measure(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs measure"
        parse.set_description("Mesure de temps d'exécution d'une commande")
        parse.set_argument("o",longname="out", description="Voir le retour de la commande", default=False)
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if len(parameter)>0:
                proc = Popen(parameter, shell=True, stdout=PIPE, stderr=PIPE)
                st = perf_counter()
                stdout, stderr = proc.communicate()
                
                et = perf_counter()

                if argument.out:
                    if len(stdout):
                        print(stdout.decode())
                    if len(stderr):
                        print(stderr.decode())
                    print("")

                duree = timedelta(seconds=(et - st))
                print(f" Days         : {duree.days}\n Hours        : {duree.seconds//3600}\n Minutes      : {duree.seconds%3600//60}\n Seconds      : {duree.seconds%60}\n Milliseconds : {duree.microseconds//1000}\n Ticks        : {duree.microseconds*10}")



    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'env_nxs.env', 'submodule': ['command_shell', 'get_executable']}, 
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']}, 
        {'module':'template.toml_format', 'submodule': ['DEFAULT_TOML']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module': 'sys_nxs.host', 'submodule': ['path_rep']},
        {'module':'app.display', 'submodule': ['logs']}, 
        {'module':'os', 'submodule': ['chdir']}, 
        {'module':'os.path', 'submodule': ['exists', 'join', 'dirname', 'split']}
    )
    def run(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs run"
        parse.set_description("Lancement d'une commande ou du projet")
        parse.set_argument("T",longname="time", description="Voir le temps d'exécution", default=False)
        parse.set_argument("s",longname="set", description="Initialiser les arguments à ajouter", store="value", default=" ")
        parse.set_argument("t",longname="test", description="Lancer en mode test", default=True)
        parse.set_argument("p",longname="prod", description="Lancer en mode prod", default=False)
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parse.disable_check()
        parameter, argument = parse.load()
        
        if parameter!=None and argument.set!=None:
            if is_nexus_project('run'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()

                if argument.set!=" ":
                    if argument.prod:
                        tfile.edit_key('prod', argument.set, "project.run")
                        logs("Argument prod initialisé")
                    elif argument.test:
                        tfile.edit_key('test', argument.set, "project.run")
                        logs("Argument test initialisé")
                else:
                    env_exe = get_executable(tfile, argument.env)
                    if env_exe!=None:
                        #arguments = " ".join(parameter)

                        if len(parameter)>0:
                            if exists(parameter[0]):
                                arguments = ["python"] + parameter
                            else:
                                code_folder = join(split(get_nexus_file())[0], tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section']))
                                chdir(code_folder)

                                file = tfile.get_key(DEFAULT_TOML['mainfile']['name'],DEFAULT_TOML['mainfile']['section'])

                                arguments = ["python", file.replace(path_rep[0], path_rep[1])] + parameter

                            command_shell(env_exe, arguments, timer=argument.time)

                        else:
                            code_folder = join(split(get_nexus_file())[0], tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section']))
                            chdir(code_folder)

                            file = tfile.get_key(DEFAULT_TOML['mainfile']['name'],DEFAULT_TOML['mainfile']['section'])

                            if argument.prod:
                                args = tfile.get_key("prod", "project.run")
                            elif argument.test:
                                args = tfile.get_key("test", "project.run")
                            cmd = "python "+file.replace(path_rep[0], path_rep[1])

                            if args!=None and len(args)>0:
                                command_shell(env_exe, cmd, args=args, timer=argument.time)
                            else:
                                command_shell(env_exe, cmd, timer=argument.time)

    
    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'subprocess'}, 
        {'module':'os.path', 'submodule': ['exists']}, 
        {'module':'env_nxs.env', 'submodule': ['get_executable']}, 
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']},
        {'module':'app.display', 'submodule': ['logs']}, 
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'}
    )
    def shell(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs shell"
        parse.set_description("Démarrage du shell python")
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project(''):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()

                cmd = get_executable(tfile, argument.env)
                print(cmd)
                if exists(cmd):
                    proc = subprocess.Popen([cmd], shell=True)
                    proc.communicate()
                else:
                    logs("L'environnement est introuvable", "warning")

    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'package.package', 'submodule': ['dependency_to_list', 'lock_package']}, 
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'install_pool', 'get_py_version', 'get_all_package']}, 
        {'module':'app.display', 'submodule': ['logs']},  
        {'module':'structure.check', 'submodule': ['get_nexus_file', 'is_nexus_project']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'re'},
        {'module':'os.path', 'submodule':['join', 'exists', 'isfile']},
        {'module':'template', 'submodule':['regex']}
    )
    def install(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs install"
        parse.set_description("Installation des dépendances")
        parse.set_argument("f", longname="force", description="Forcer l'installation des packages", default=False)
        parse.set_argument("n", longname="nocheck", description="Ne pas vérifier les conflits de dépendances", default=False)
        parse.set_argument("r", longname="requirements", description="Spécifier un fichier requirements", store="value", default=None)
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        #parse.set_argument(longname="root", description="Forcer l'installation en dehors de l'environnement")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('', True):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
            else:
                tfile = None

            cmd = get_executable(tfile, argument.env)
            if cmd!=None:
                if not hasattr(self, 'py_version'):
                    self.py_version = get_py_version(cmd)
                    #self.py_version = "3.4"

                if argument.requirements!=None:
                    file_r = abspath(argument.requirements)
                    if exists(file_r) and isfile(file_r):
                        with open(file_r, 'r') as f:
                            parameter = f.read().split("\n")


                if len(parameter)==0 and tfile!=None:
                    deps = tfile.get_key('dependencies','project')
                    
                    if deps!=None:
                        deps = lock_package(deps)
                        if argument.nocheck:
                            mdm_env = dependency_to_list(deps, nocheck=True)
                        else:
                            mdm_env = dependency_to_list(deps)

                        if len(mdm_env):
                            install_pool(cmd, mdm_env, force=argument.force)

                            #for package in mdm_env:
                            #    install_module(cmd, package, mdm_env[package], force=argument.force)
                    else:
                        logs("Aucun module a installer")
                else:
                    old = get_all_package(cmd)
                    deps = {}
                    for package in parameter:
                        package_compiled = re.compile(regex.package_regex)
                        package_match = package_compiled.search(package)
                        if package_match!=None:
                            name = package_match.group('name')
                            version = package_match.group('version')
                            if version==None:
                                version = "N.A"

                            if name in old:
                                if version!="N.A" and old[name]!=version:
                                    deps[name] = version
                                else:
                                    logs(f"{name} déjà installé")
                            else:
                                deps[name] = version

                    if len(deps):
                        old = get_all_package(cmd)
                        """
                        if tfile==None:
                            print(cmd)
                        else:
                            old = tfile.get_key('dependencies','project')
                            old = lock_package(old)
                        """
                        old = lock_package(old)

                        if old!=None:
                            deps.update(dict(old))

                        mdm_env = dependency_to_list(deps, force=argument.force)
                        if len(mdm_env):
                            #print(mdm_env)
                            new = list(set(list(dict(old).keys())).symmetric_difference(set(list(mdm_env.keys()))))

                            if 'windows' in new:
                                new.remove('windows')
                            if 'linux' in new:
                                new.remove('linux')

                            if len(new):
                                delta = {}
                                for package in new:
                                    if package in mdm_env:
                                        delta[package] = mdm_env[package]

                                #for package in new:
                                    #print(mdm_env[package])
                                install_pool(cmd, delta, force=argument.force)
            else:
                logs("L'exécutable Python est introuvable", "critical")

    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'os'},
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'remove_pool', 'get_py_version']}, 
        {'module':'app.display', 'submodule': ['logs']}, 
        {'module':'structure.check', 'submodule': ['get_nexus_file', 'is_nexus_project']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'}
    )
    def uninstall(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs uninstall"
        parse.set_description("Désinstallation des dépendances")
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        #parse.set_argument(longname="env", description="Préciser un environnement", store="value")
        #parse.set_argument(longname="root", description="Forcer l'installation en dehors de l'environnement")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('', True):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
            else:
                tfile = None

            cmd = get_executable(tfile, argument.env)
            if cmd!=None:
                if not hasattr(self, 'py_version'):
                    self.py_version = get_py_version(cmd)
                    #self.py_version = "3.4"
                if len(parameter)==0 and tfile!=None:
                    deps = tfile.get_key('dependencies','project')
                    if os.name=="nt":
                        deps = list(deps)+list(deps['windows'])
                    else:
                        deps = list(deps)+list(deps['linux'])
                    deps.remove("windows")
                    deps.remove("linux")

                    remove_pool(cmd, deps)
                else:
                    remove_pool(cmd, parameter)
            else:
                logs("L'exécutable Python est introuvable", "critical")

    @impmagic.loader(
        {'module':'__main__'}, 
        {'module':'zpp_args'}, 
        {'module':'package.package', 'submodule': ['dependency_to_list', 'lock_package', 'unversion_package', 'compare_version', 'get_possible_version', 'filter_update']}, 
        {'module':'env_nxs.env', 'submodule': ['create_temp_env','Context','get_env', 'upgrade_pool', 'install_pool', 'get_py_version', 'open_environment', 'clone_environment', 'get_all_package']}, 
        {'module':'app.display', 'submodule': ['logs']},  
        {'module':'structure.check', 'submodule': ['get_nexus_file', 'get_root_project', 'is_nexus_project']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'sys'},
        {'module':'re'},
        {'module':'os'},
        {'module':'template', 'submodule':['regex']},
        {'module':'os.path', 'submodule':['join', 'split']},
        {'module':'uuid', 'submodule': ['uuid4']},
    )
    def update(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs update"
        parse.set_description("Mise à jour des dépendances")
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parse.set_argument("d", longname="dryrun", description="Tester l'update sur un environnement isolé", default=None)
        parse.set_argument("f", longname="full", description="Met à jour l'ensemble des modules de l'environnement", default=None)

        parse.set_argument(longname="minor", description="Mettre à jour uniquement les versions mineur", default=None)
        parse.set_argument(longname="patch", description="Mettre à jour uniquement les versions patch", default=None)
        #parse.set_argument(longname="env", description="Préciser un environnement", store="value")
        #parse.set_argument(longname="root", description="Forcer l'installation en dehors de l'environnement")
        parse.set_argument(longname="bypasslock", description="Ignorer le fichier de lock", default=False)
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('', True):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
            else:
                tfile = None

            #Pour identifier si c'est un environnement sandbox créé
            new = False
            env_data = None

            if tfile!=None:
                env_data = get_env(tfile, argument.env, logs_env=False)

            if argument.env!=None and env_data==None:
                logs(f"Environnement {argument.env} introuvable", "error")
                return
            elif argument.env==None and env_data==None:
                cmd = sys.executable
            else:
                cmd = join(get_root_project(), env_data['env_exe'])

            
            if argument.dryrun:
                logs("Préparation de l'environnement de test")

                if cmd!=sys.executable:
                    return_code, selected = clone_environment(env_data, str(uuid4()), tfile)
                    __main__.ToDoClear.append(selected['env_dir'])
                    cmd = selected['env_exe']

                else:
                    name, pathenv = create_temp_env(upgradepip=False)
                    context = Context(pathenv, name)
                    cmd = context.env_exe
                    selected = {'env_dir': pathenv}
                    new = True

            if not hasattr(self, 'py_version'):
                self.py_version = get_py_version(cmd)

            if len(parameter)==0:
                deps=None
                actual =  get_all_package(cmd, clean_name=True)

                if argument.full:
                    deps = actual
                elif tfile!=None:
                    deps = tfile.get_key('dependencies','project')

                if deps!=None:
                    deps = unversion_package(deps)
                    deps = get_possible_version(deps, actual, argument.minor, argument.patch)

                    if not argument.bypasslock:
                        deps = lock_package(deps)

                    to_upgrade = dependency_to_list(deps)

                    to_upgrade = filter_update(actual, to_upgrade)

                    if len(to_upgrade):
                        if new:
                            install_pool(cmd, to_upgrade, force=True)
                        else:
                            upgrade_pool(cmd, to_upgrade, force=True)

                        logs("Mise à jour des modules terminées")
                        if argument.dryrun:
                            code_folder = join(split(get_nexus_file())[0], tfile.get_key("name","project"))
                            open_environment(selected['env_dir'], code_folder)
                    else:
                        logs("Aucun package à mettre à jour")

                else:
                    logs("Aucun module a installer")
            else:
                deps = {}
                actual =  get_all_package(cmd, clean_name=True)

                reg = re.compile(regex.package_regex)

                #Lister les packages a mettre à jour
                for pack in parameter:
                    matcher = reg.match(pack)
                    if matcher:
                        name = matcher.group('name')
                        version = matcher.group('version')

                        if name in actual:
                            if version!=None:
                                deps[name] = version
                            else:
                                deps[name] = "N.A"

                    else:
                        logs(f"Format invalide pour {pack}")

                for name, version in deps.items():
                    if not version.startswith("==") and not version.startswith(">=") and not version.startswith("<=") and not version.startswith("!=") and not version.startswith("^")  and not version.startswith(">") and not version.startswith("<"):
                        deps[name] = "=="+version

                deps = get_possible_version(deps, actual, argument.minor, argument.patch)

                mdm_env = dependency_to_list(deps)
                to_upgrade = filter_update(actual, mdm_env)

                upgrade_pool(cmd, to_upgrade, force=True)


            if not argument.dryrun and tfile!=None:
                deps_conf = tfile.get_key('dependencies','project')
                deps = get_all_package(cmd, refresh=True)

                for package in to_upgrade:
                    if package in deps:
                        if package in deps_conf:
                            if deps_conf[package]!="N.A":
                                operator_regex = re.compile(regex.segment_version)
                                match = operator_regex.match(deps_conf[package])
                                operator = match.group('operator')

                                if not compare_version(deps[package], operator, deps_conf[package].replace(operator, "")):
                                    tfile.edit_key(package, "=="+deps[package], "project.dependencies")
                        
                        elif os.name=="nt" and package in deps_conf['windows']:
                            if deps_conf['windows'][package]!="N.A":
                                operator_regex = re.compile(regex.segment_version)
                                match = operator_regex.match(deps_conf['windows'][package])
                                operator = match.group('operator')

                                if not compare_version(deps[package], operator, deps_conf['windows'][package].replace(operator, "")):
                                    tfile.edit_key(package, "=="+deps[package], "project.dependencies.windows")
                        
                        elif os.name!="nt" and package in deps_conf['linux']:
                            if deps_conf['linux'][package]!="N.A":
                                operator_regex = re.compile(regex.segment_version)
                                match = operator_regex.match(deps_conf['linux'][package])
                                operator = match.group('operator')

                                if not compare_version(deps[package], operator, deps_conf['linux'][package].replace(operator, "")):
                                    tfile.edit_key(package, "=="+deps[package], "project.dependencies.linux")


    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'zpp_color', 'submodule': ['fg', 'attr']}, 
        {'module':'package.package', 'submodule': ['search_package']}
    )
    def search(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs search"
        parse.set_description("Recherche d'un package")
        parse.set_argument(longname="strict", description="Recherche strict", default=False)
        parse.set_parameter("NAME", description="Nom du package")
        parameter, argument = parse.load()

        if parameter!=None and len(parameter)>0:
            result = search_package(parameter[0], argument.strict)
            
            for pack in result:
                print(f"{fg(__main__.color['cyan'])}{str(pack)}{attr(0)} ({fg(__main__.color['green'])}{result[pack]['version']}{attr(0)}) - {fg(__main__.color['dark_gray'])}{result[pack]['description']}{attr(0)}")

    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'package.package', 'submodule': ['info_package']}, 
        {'module':'os.path', 'submodule': ['isfile', 'exists']}, 
        {'module':'build_nxs.publish', 'submodule': ['get_metadata']},
        {'module':'env_nxs.env', 'submodule': ['get_py_version']}
    )
    def info(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs info"
        parse.set_description("Afficher les informations d'un package")
        parse.set_argument(longname="nodeps", description="Ne pas afficher l'arborescence de dépendances", default=False)
        parse.set_argument(longname="arbolvl", description="Déterminer le niveau d'arborescence", store="value", type="digit", default=2)
        parse.set_argument(longname="version", description="Afficher toutes les versions disponibles", default=False)
        parse.set_parameter("NAME", description="Nom du package")
        parameter, argument = parse.load()

        if parameter!=None and len(parameter)>0:
            if not hasattr(self, 'py_version'):
                self.py_version = get_py_version(sys.executable)

            for package in parameter:
                if exists(package) and isfile(package):
                    meta = get_metadata(package)
                    if meta!=None:
                        for key, value in meta.items():
                            print_nxs(f"{key}: ", nojump=True)
                            print(value)
                else:
                    info_package(package, noarbo=argument.nodeps, arbolvl=argument.arbolvl, list_version=argument.version)

    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'glob', 'submodule': ['glob']}, 
        {'module':'analysis', 'submodule': ['black']},
        {'module':'os.path', 'submodule': ['abspath', 'join']}
    )
    def clearcode(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs clearcode"
        parse.set_description("Analyser la lisibilité du code")
        parse.set_argument(longname="apply", description="Appliquer les modifications", default=False)
        parse.set_argument(longname="output", description="Appliquer les modifications sur un autre fichier", store="value", default=None)
        parse.set_argument("r", longname="recursive", description="Faire une recherche récursive", default=False)
        parse.set_argument(longname="fast", description="Faire une analyse rapide", default=False)
        parse.set_parameter("NAME", description="Nom du package")
        parameter, argument = parse.load()

        if parameter!=None:
            if len(parameter)==0:
                parameter = []
                if argument.recursive:
                    for file in glob(abspath('.') + '/**/*.py', recursive=True):
                        parameter.append(file.replace(join(abspath('.'),""),""))
                else:
                    for file in glob("*.py", recursive=False):
                        parameter.append(file)

            for file in parameter:
                black.analyse(file, apply=argument.apply, fileout=argument.output, fast=argument.fast)

    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'re'}, 
        {'module':'glob', 'submodule': ['glob']}, 
        {'module':'analysis', 'submodule': ['linter']}, 
        {'module':'app.display', 'submodule': ['logs', 'print_nxs']},
        {'module':'os.path', 'submodule': ['abspath', 'join']}
    )
    def code_analysis(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs analyse"
        parse.set_description("Analyse statique de code")
        parse.set_argument("e", longname="exclude", description="Code erreur à exclure", store="value", default=None)
        parse.set_argument("n", longname="onlynote", description="Afficher uniquement la note")
        parse.set_argument("r", longname="onlyreport", description="Afficher uniquement le rapport")
        parse.set_argument(longname="recursive", description="Faire une recherche récursive", default=False)
        parse.set_parameter("FILE", description="Fichier à analyser")
        parameter, argument = parse.load()

        if parameter!=None:
            if len(parameter)==0:
                parameter = []
                if argument.recursive:
                    for file in glob(abspath('.') + '/**/*.py', recursive=True):
                        parameter.append(file.replace(join(abspath('.'),""),""))
                else:
                    for file in glob("*.py", recursive=False):
                        parameter.append(file)

            for file in parameter:
                if argument.exclude!=None and argument.exclude!="":
                    reg = '^([CRWEF]{1}(\\d{4})?)(,[CRWEF]{1}(\\d{4})?)*$'
                    if not re.search(reg, argument.exclude):
                        logs("Code d'exclusion non valide", "error")
                        return
                else:
                    argument.exclude=""

                a = linter.Analyser(file,argument.exclude)
                a.load_report()
                if argument.onlyreport or (not argument.onlyreport and not argument.onlynote):
                    a.display_report()
                if argument.onlynote:
                    print_nxs(f"\n{file}""  \n  Global note: ", nojump=True)
                    print(a.get_note())

                if(not argument.onlyreport and not argument.onlynote):
                    print(f"\n  Global note: {a.get_note()}")

    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'glob', 'submodule': ['glob']}, 
        {'module':'analysis', 'submodule': ['bandit']}, 
        {'module':'app.display', 'submodule': ['print_nxs']},
        {'module':'os.path', 'submodule': ['abspath', 'join']}
    )
    def secure_analysis(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs securiscan"
        parse.set_description("Analyse de la sécurité du code")
        parse.set_argument("r", longname="recursive", description="Recherche de fichier récursive")
        parse.set_argument("e", longname="errors", description="Afficher les erreurs d'analyse")
        parse.set_argument("g", longname="globalmetric", description="Afficher les metrics regroupés")
        parse.set_argument("f", longname="filemetric", description="Afficher les metrics par fichier")
        parse.set_argument("m", longname="allmetric", description="Afficher toutes les metrics")
        parse.set_argument("d", longname="details", description="Afficher le détail des résultats")
        parse.set_argument("a", longname="all", description="Afficher toutes les informations")
        parse.set_argument("E", longname="exclude", description="Exclure des fichiers", store="value", default=None)
        parse.set_argument("s", longname="severity", description="Filtrer par niveau de severity", store="value", default=1, type="digit")
        parse.set_argument("c", longname="confidence", description="Filtrer par niveau de confidence", store="value", default=1, type="digit")

        parse.set_parameter("FILE", description="Fichier à analyser")
        parameter, argument = parse.load()

        if parameter!=None and argument!=None:
            if not argument.errors and not argument.globalmetric and not argument.filemetric and not argument.allmetric and not argument.details:
                argument.all = True

            if argument.exclude!=None:
                argument.exclude = argument.exclude(",")

            if argument.severity<1 or argument.severity>4:
                argument.severity = 1

            if argument.confidence<1 or argument.confidence>4:
                argument.confidence = 1

            if len(parameter)==0:
                parameter = []
                if argument.recursive:
                    for file in glob(abspath('.') + '/**/*.py', recursive=True):
                        parameter.append(file.replace(join(abspath('.'),""),""))
                else:
                    for file in glob("*.py", recursive=False):
                        parameter.append(file)

            for file in parameter:
                print_nxs(f"\n{file}")
                bs = BanditScan([file], exclude_file=argument.exclude, recursive=argument.recursive, severity=argument.severity, confidence=argument.confidence, show_errors=argument.errors, show_metrics= argument.allmetric, show_globalmetrics=argument.globalmetric, show_filemetrics=argument.filemetric, show_details=argument.details, show_all=argument.all)
                bs.run_scan()
                bs.output()

    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'shutil'},
        {'module':'structure.create', 'submodule': ['create_project', 'construct_new_data']},
        {'module':'analysis.project', 'submodule': ['check_realname']},
        {'module':'os.path', 'submodule': ['exists', 'join', 'split']}
    )
    def init(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs init"
        parse.set_description("Initialisation d'un projet à partir de fichier existant")
        parse.set_argument(longname="env", description="Créer un environnement virtuel", default=False)
        parse.set_argument(longname="noenv", description="Ne pas créé d'environnement virtuel", default=False)
        parse.set_argument(longname="clear", description="Nettoyer le répertoire de l'environnement si existant", default=False)
        parse.set_argument(longname="upgradepip", description="Mettre à jour pip à l'installation", default=False)
        parse.set_argument(longname="inproject", description="Créer l'environnement dans le projet", default=False)
        parse.set_argument(longname="incache", description="Créer l'environnement dans le cache", default=False)
        parse.set_argument(longname="envpath", description="Préciser le nom du répertoire de l'environnement", store="value", default=None)
        parse.set_argument(longname="repo", description="Créer le repo du projet", default=False)
        parse.set_argument(longname="norepo", description="Ne pas créer le repo du projet", default=False)
        parse.set_parameter("NAMEPROJECT", description="Nom du projet")
        parameter, argument = parse.load()

        if parameter!=None:
            #files = [parameter[0]]
            projectfolder = os.getcwd()
            projectname = split(projectfolder)[1]
            data = construct_new_data(projectname, 'init')

            #Dans la liste des dépendances, va vérifier si le paclage existe sinon cherche/demande le nom pypi du package
            if 'dependencies' in data:
                data_read = data['dependencies'].copy()
                for element in data_read:
                    element_func = check_realname(element, True)
                    if element_func!=element:
                        if isinstance(element_func, str):
                            data['dependencies'][element_func] = data['dependencies'][element]
                            del data['dependencies'][element]

                        elif isinstance(element_func, dict):
                            change = False
                            value = data['dependencies'][element]

                            if 'windows' in element_func:
                                if 'windows' not in data['dependencies']:
                                    data['dependencies']['windows'] = {}
                                data['dependencies']['windows'][element_func['windows']] = value
                                
                                if element in data['dependencies']:
                                    del data['dependencies'][element]

                            if 'linux' in element_func:
                                if 'linux' not in data['dependencies']:
                                    data['dependencies']['linux'] = {}
                                data['dependencies']['linux'][element_func['linux']] = value

                                if element in data['dependencies']:
                                    del data['dependencies'][element]

                            if change:
                                del data['dependencies'][element]                                

            create_project(data['projectname'], data, argument, action='init')

            project = data['projectname']
            shutil.move(data['mainfile'], join(project, data['mainfile']))
            for element in data['include']:
                if exists(element+".py"):
                    element += ".py"
                elif exists(element+".pyw"):
                    element += ".pyw"
                shutil.move(element, join(project, element))

    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'shutil'},
        {'module':'app.display', 'submodule': ['logs', 'print_nxs']}, 
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file', 'get_root_project']}, 
        {'module':'package.package', 'submodule': ['lock_package']},
        {'module':'template.toml_format', 'submodule': ['DEFAULT_TOML']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'structure.create', 'submodule': ['create_folder', 'create_project_environment']},
        {'module': 'env_nxs.env', 'submodule': ['is_valid_envdir', 'get_executable', 'open_environment', 'clone_environment', 'change_default', 'get_all_package']},
        {'module': 'template', 'submodule': ['default_conf']},
        {'module': 'os', 'submodule': ['chdir']},
        {'module': 'sys_nxs.host', 'submodule': ['path_rep']},
        {'module':'zpp_config', 'submodule': ['Config']},
        {'module':'os.path', 'submodule': ['abspath', 'exists', 'isabs', 'join', 'split', 'expanduser', 'isdir', 'dirname']}
    )
    def env(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs env"
        parse.set_description("Gestion des environnements d'un projet")
        parse.set_argument(longname="clone", description="Cloner un environnement", store="value", default=False)
        parse.set_argument(longname="disable", description="Désactiver l'environnement par défaut", default=False)
        parse.set_argument("o", longname="open", description="Ouvrir un environnement", default=False)
        parse.set_argument("l", longname="list", description="Lister les environnements virtuels", default=False)
        parse.set_argument("d", longname="default", description="Définir l'environnement par défaut", default=False)
        parse.set_argument("a", longname="add", description="Ajouter un environnement existant", default=False)
        parse.set_argument("n", longname="name", description="Spécifier le nom de l'environnement", default=None, store="value", category=" add")
        parse.set_argument("c", longname="create", description="Créer un environnement", default=False)
        parse.set_argument("r", longname="remove", description="Supprimer un environnement", default=False)
        parse.set_argument(longname="withoutdeps", description="Créer sans installer les dépendances", default=False, category=" create")
        parse.set_argument(longname="nocheck", description="Ne pas vérifier les conflits de dépendances", default=False, category=" create")
        parse.set_argument(longname="clear", description="Supprimer le répertoire de destination si pas vide", default=False, category=" create")
        parse.set_argument("C", longname="cache", description="Créer dans le cache", default=False, category=" create")
        parse.set_argument("p", longname="prompt", description="Spécifier le message du prompt", default=None, store="value", category=" create")
        parse.set_argument("m", longname="migrate", description="Migrer l'environnement dans le projet ou le cache", default=False)
        parse.set_argument("P", longname="listpackage", description="Lister les packages installés de l'environnement", default=False)
        parse.set_argument("i", longname="info", description="Afficher les informations de l'environnement", default=False)
        parse.set_argument("D", longname="dest", description="Spécifier un dossier de destination", default=None, store="value", category=" migration")
        parse.set_parameter("NAME", description="Nom de l'environnement")
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('env'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()

                if argument.open:
                    if len(parameter):
                        if 'venv' in tfile.doc:
                            find = False

                            for environment in tfile.doc['venv']:
                                name = environment
                                environment = tfile.doc['venv'][environment]
                                if parameter[0]==name:
                                    find=True
                                    env = environment

                            cmd = env['env_dir']
                            if not isabs(cmd):
                                cmd = join(get_root_project(), cmd)

                            if not find:
                                logs(f"L'environnement {parameter[0]} n'existe pas", "critical")
                            else:
                                if exists(join(get_root_project(), env['env_exe'])):
                                    code_folder = join(split(get_nexus_file())[0], tfile.get_key("name","project"))
                                    open_environment(cmd, code_folder)
                                else:
                                    logs("L'environnement est introuvable", "critical")

                        else:
                            logs("Aucun environnement configuré", "warning")
                    else:
                        logs("Aucun environnement spécifié", "critical")

                elif argument.clone:
                    if 'venv' in tfile.doc:
                        selected = None
                        if len(parameter):
                            if parameter[0] in tfile.doc['venv']:
                                selected = tfile.doc['venv'][parameter[0]]
                            else:
                                logs(f"Environnement {parameter[0]} introuvable", "warning")
                        else:
                            for env in tfile.doc['venv']:
                                name = env
                                env = tfile.doc['venv'][env]
                                if 'default' in env and env['default']==True:
                                    selected = env

                        if selected!=None:
                            return_code, venv_data = clone_environment(selected, argument.clone, tfile)

                            if return_code:
                                logs("Mise à jour du fichier projet")
                                for element in venv_data:
                                    tfile.edit_key(element, venv_data[element], "venv."+argument.clone)

                    else:
                        logs("Aucun environnement configuré", "warning")

                elif argument.disable:
                    if 'venv' in tfile.doc:
                        for env in tfile.doc['venv']:
                            name = env
                            env = tfile.doc['venv'][env]
                            if 'default' in env and env['default']==True:
                                tfile.edit_key('default', False, "venv."+name)
                                logs("Environnement par défaut désactive")
                    else:
                        logs("Aucun environnement configuré", "warning")

                elif argument.list:
                    if 'venv' in tfile.doc:
                        cachedir = expanduser(self.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)).replace(path_rep[1], path_rep[0])
                        for env in tfile.doc['venv']:
                            name = env
                            env = tfile.doc['venv'][env]
                            print_nxs(f" - {name}", nojump=True)
                            if exists(join(get_root_project(), env['env_exe'])):
                                if 'default' in env and env['default']==True:
                                    print_nxs(" (", nojump=True)
                                    print_nxs("default", color=__main__.color["yellow"], nojump=True)
                                    print_nxs(")", nojump=True)

                                if isabs(env['env_dir']) and env['env_dir'].replace(path_rep[1], path_rep[0]).startswith(cachedir):
                                    print_nxs(" (", nojump=True)
                                    print_nxs("cache", color=__main__.color["yellow"], nojump=True)
                                    print_nxs(")", nojump=True)
                            else:
                                print_nxs(" (", nojump=True)
                                print_nxs("not-found", color=__main__.color["red"], nojump=True)
                                print_nxs(")", nojump=True)
                            print("")
                    else:
                        logs("Aucun environnement configuré", "warning")

                elif argument.remove:
                    if len(parameter)>0:
                        if 'venv' in tfile.doc:
                            for env in tfile.doc['venv']:
                                name = env
                                env = tfile.doc['venv'][env]
                                if parameter[0]==name:
                                    env_dir = join(get_root_project(), env['env_dir'])
                                    if exists(env_dir):
                                        shutil.rmtree(env_dir)

                                    if tfile.delete_key(name, 'venv'):
                                        logs("L'environnement a été supprimé")
                                    else:
                                        logs("L'environnement n'a pas pu être supprimé", "critical")
                        else:
                            logs("Aucun environnement configuré", "warning")
                    else:
                        logs("Aucun environnement spécifié", "critical")

                elif argument.create:
                    if len(parameter)>0:
                        find = False
                        first = False

                        if 'venv' in tfile.doc:
                            for env in tfile.doc['venv']:
                                name = env
                                env = tfile.doc['venv'][env]
                                if parameter[0]==name:
                                    find=True
                        else:
                            first=True

                        if find:
                            logs(f"L'environnement {parameter[0]} existe déjà", "critical")
                        else:
                            data = {}
                            data['projectname'] = tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section'])
                            if argument.withoutdeps:
                                data['dependencies'] = {}
                            else: 
                                data['dependencies'] = tfile.get_key('dependencies','project')
                                data['dependencies'] = lock_package(data['dependencies'])
                            create_project_environment(parameter[0], get_root_project(), data, tfile, first, cache=argument.cache, prompt=argument.prompt, clear=argument.clear, nocheck=argument.nocheck)

                            if argument.default:
                                change_default(tfile, parameter[0])
                    else:
                        logs("Aucun environnement spécifié", "critical")

                elif argument.add:
                    if len(parameter)>0:
                        if argument.name!=None:
                            nameenv = argument.name
                        else:
                            nameenv = parameter[0]

                        find = False
                        if 'venv' in tfile.doc:
                            for env in tfile.doc['venv']:
                                name = env
                                env = tfile.doc['venv'][env]
                                if nameenv==name:
                                    find=True

                        if find:
                            logs(f"L'environnement {parameter[0]} existe déjà", "critical")
                        else:
                            virtdir = abspath(parameter[0])
                            if exists(virtdir) and isdir(virtdir):
                                context = is_valid_envdir(virtdir)
                                if context!=None:
                                    root_env = get_root_project()
                                    if context.env_dir.startswith(root_env):
                                        context.env_dir = context.env_dir.replace(root_env+path_rep[0], "")
                                        context.env_exe = context.env_exe.replace(root_env+path_rep[0], "")
                                        context.bin_path = context.bin_path.replace(root_env+path_rep[0], "")

                                    venv_data = {}
                                    venv_data['env_dir'] = context.env_dir
                                    venv_data['env_name'] = context.env_name 
                                    venv_data['env_exe'] = context.env_exe
                                    venv_data['bin_path'] = context.bin_path
                                    c = Config(context.cfg_path)
                                    data = c.load(val='version', section='',default="N.A")
                                    venv_data['version'] = data

                                    for element in venv_data:
                                        tfile.edit_key(element, venv_data[element].replace("\\","/"), "venv."+nameenv)
                                    tfile.edit_key("default", False, "venv."+nameenv)
                                    
                                    logs("Environnement ajouté")

                                    if argument.default:
                                        change_default(tfile, nameenv)
                                else:
                                    logs("Environnement non valide", "critical")
                            else:
                                logs("Le répertoire n'existe pas", "critical")
                    else:
                        logs("Aucun environnement spécifié", "critical")

                elif argument.migrate:
                    if len(parameter)>0:
                        if 'venv' in tfile.doc:
                            for env in tfile.doc['venv']:
                                name = env
                                env = tfile.doc['venv'][env]
                                if parameter[0]==name:
                                    if exists(join(get_root_project(), env['env_exe'])):
                                        chdir(get_root_project())
                                        env_folder = self.conf.load(val='virtualenvs.foldername', section='',default=default_conf.virtualenvs_foldername)
                                        env_dir = split(env['env_dir'])[1]
                                        fold = join(env_folder, env_dir)
                                        project_folder = split(get_nexus_file())[0]
                                        cachedir = expanduser(self.conf.load(val='cache-dir', section='',default=default_conf.cache_dir))
                                        origin = env['env_dir']
                                        logs("Migration en cours")
                                        migrate=False

                                        environment_dir = env['env_dir'].replace(path_rep[1], path_rep[0])
                                        if argument.dest!=None:
                                            fold = abspath(expanduser(argument.dest))


                                            shutil.move(environment_dir, fold)

                                            migrate=True

                                        elif isabs(environment_dir) and environment_dir.startswith(cachedir):
                                            shutil.move(environment_dir, join(project_folder, fold))
                                            migrate=True

                                        else:
                                            appname = tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section'])
                                            fold = join(cachedir,env_folder,appname,env['env_name'])

                                            shutil.move(environment_dir, fold)

                                            migrate=True

                                        if migrate==True:
                                            #Supprime si le répertoire d'origine est vide
                                            parent = split(env['env_dir'])[0]
                                            if not os.listdir(parent):
                                                os.rmdir(parent)

                                            logs("Application de la configuration")
                                            env_dir = env['env_dir'].replace(origin, fold).replace("\\","/")
                                            env_exe = env['env_exe'].replace(origin, fold).replace("\\","/")
                                            bin_path = env['bin_path'].replace(origin, fold).replace("\\","/")
                                            tfile.edit_key('env_dir', env_dir, "venv."+name)
                                            tfile.edit_key('env_exe', env_exe, "venv."+name)
                                            tfile.edit_key('bin_path', bin_path, "venv."+name)

                                            logs("Migration terminée")
                                    else:
                                        logs("L'environnement est introuvable", "critical")
                    else:
                        logs("Aucun environnement spécifié", "critical")
                
                elif argument.default:
                    if len(parameter)>0:
                        if 'venv' in tfile.doc:
                            change_default(tfile, parameter[0])
                        else:
                            logs("Aucun environnement configuré", "warning")
                    else:
                        logs("Aucun environnement spécifié", "critical")
                
                elif argument.listpackage:
                    if len(parameter):
                        envname = parameter[0]
                    else:
                        envname = None

                    cmd = get_executable(tfile, env_name=envname, logs_env=False)
                    if cmd!=None:
                        deps = get_all_package(cmd)

                        for name, version in deps.items():
                            print(f"{name}=={version}")

                elif argument.info:
                    if 'venv' in tfile.doc:
                        selected = None
                        if len(parameter):
                            if parameter[0] in tfile.doc['venv']:
                                selected = tfile.doc['venv'][parameter[0]]
                            else:
                                logs(f"Environnement {parameter[0]} introuvable", "warning")
                                return
                        else:
                            for env in tfile.doc['venv']:
                                name = env
                                env = tfile.doc['venv'][env]
                                if 'default' in env and env['default']==True:
                                    selected = env

                        if selected:
                            for key, value in selected.items():
                                print_nxs(f"{key}: ", nojump=True)
                                print(value)
                        else:
                            logs(f"Aucun environnement utilisable", "error")
                    else:
                        logs(f"Aucun environnement configuré", "warning")

                else:
                    if len(parameter):
                        envname = parameter[0]
                    else:
                        envname = None

                    cmd = get_executable(tfile, env_name=envname, logs_env=False)
                    if cmd!=None and cmd!=sys.executable:
                        env_dir = dirname(dirname(cmd))
                        code_folder = join(split(get_nexus_file())[0], tfile.get_key("name","project"))
                        open_environment(env_dir, code_folder)
                    elif cmd!=None and cmd==sys.executable:
                        logs("Aucun environnement par défaut configuré", "critical")
                    elif cmd==None and envname!=None:
                        logs(f"Environnement {envname} introuvable", "critical")


    @impmagic.loader(
        {'module':'zpp_args'},
        {'module': 'subprocess', 'submodule': ['Popen', 'PIPE']},
        {'module':'package.package', 'submodule': ['dependency_to_list']}, 
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'install_module', 'install_pool', 'get_py_version', 'get_package', 'installed_module', 'init_pip', 'create_temp_env', 'Context']}, 
        {'module':'app.display', 'submodule': ['logs']}, 
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']}, 
        {'module':'template.toml_format', 'submodule': ['DEFAULT_TOML']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'structure.check', 'submodule': ['get_root_project']}, 
        {'module':'os.path', 'submodule': ['abspath', 'join', 'split', 'dirname']}
    )
    def compile(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs compile"
        parse.set_description("Compilation du projet")
        parse.set_argument(longname="install", description="Installe ou met à jour un package introuvable", default=False)
        parse.set_argument(longname="nocheck", description="Désactiver le contrôle des dépendances", default=False)
        parse.set_argument(longname="dryrun", description="Affichage des informations de compilation", default=False)
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parse.set_argument(longname="isolate", description="Compiler à partir d'un environnement isolé", default=False)
        parse.set_argument(longname="debug", description="Afficher les détais de la compilation", default=False)
        #parse.set_parameter("NAME", description="Nom de l'environnement")
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('compile'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()

                project_folder = split(get_nexus_file())[0]
                code_folder = join(project_folder, tfile.get_key("name","project"))
                build_folder = join(project_folder, "build")

                mainfile = join(dirname(get_nexus_file()),tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section']),tfile.get_key(DEFAULT_TOML['mainfile']['name'],DEFAULT_TOML['mainfile']['section']))

                payload = join(abspath(split(__file__)[0]),'build_nxs','payload.py')

                #################################
                if argument.isolate:
                    name, pathenv = create_temp_env(upgradepip=True)
                    context = Context(pathenv, name)
                    env_exe = context.env_exe
                    argument.install = True
                else:
                    env_exe = get_executable(tfile, argument.env)

                if env_exe!=None:
                    if argument.dryrun:
                        installed_module(env_exe, "pygments", install=True)

                    else:
                        installed_module(env_exe, "chardet", install=True)
                        installed_module(env_exe, "wheel", install=True)
                    
                    installed_module(env_exe, "cx_Freeze", install=True)
                    installed_module(env_exe, "toml", install=True)
                    installed_module(env_exe, "impmagic", install=True)

                    """
                    if not get_package(env_exe, "pygments") and argument.dryrun:
                        install_module(env_exe, "pygments")

                    if not get_package(env_exe, "chardet") and not argument.dryrun:
                        install_module(env_exe, "chardet")

                    if not get_package(env_exe, "cx_Freeze") and not argument.dryrun:
                        install_module(env_exe, "cx_Freeze")
                    
                    if not get_package(env_exe, "toml"):
                        install_module(env_exe, "toml")

                    if not get_package(env_exe, "wheel") and not argument.dryrun:
                        install_module(env_exe, "wheel")

                    if not get_package(env_exe, "impmagic"):
                        install_module(env_exe, "impmagic")
                    """


                    if not argument.nocheck and not argument.dryrun:
                        logs("Contrôle de la présence des dépendances")
                        deps = tfile.get_key('dependencies','project')

                        if deps!=None:
                            if self.conf.load(val='virtualenvs.upgradepip', section='',default=default_conf.virtualenvs_upgradepip):
                                init_pip(env_exe)
                            if not hasattr(self, 'py_version'):
                                self.py_version = get_py_version(env_exe)

                            mdm_env = dependency_to_list(deps)
                            if len(mdm_env):
                                for package in mdm_env:
                                    version = get_package(env_exe, package)
                                    if not version or version.replace('==', '')!=mdm_env[package]['version']:
                                        res = installed_module(env_exe, package, mdm_env[package], install=argument.install)
                                        if res==False:
                                            logs(f"Module {package} non installé", "critical")
                                            if argument.install:
                                                install_pool(env_exe, mdm_env, force=True)
                                            else:
                                                exit()
                            else:
                                logs("Aucun module a installer")
                                
                else:
                    logs("L'exécutable Python est introuvable", "critical")
                    exit()

                logs("Lancement de la compilation")
                alias_file = join(get_root_project(), ".package_alias")

                if argument.dryrun:
                    argument_run = [env_exe, payload, get_nexus_file(), code_folder, build_folder, mainfile, alias_file, "dryrun"]
                else:
                    argument_run = [env_exe, payload, get_nexus_file(), code_folder, build_folder, mainfile, alias_file, "build"]

                #subprocess.run(argument_run)

                proc = Popen(argument_run, shell=True, stdout=PIPE, stderr=PIPE)
                stdout, stderr = proc.communicate()
                if argument.dryrun or argument.debug:
                    if len(stdout):
                        logs(stdout.decode())
                    
                    if len(stderr):
                        logs(stderr.decode(), "error")

                if len(stderr):
                    logs(f"Erreur lors de la compilation: {stderr}", "error")
                else:
                    logs("Compilation terminé", "success")
                #################################

    @impmagic.loader(
        {'module':'zpp_args'}, 
        {'module':'shutil'}, 
        {'module':'os'}, 
        {'module':'build_nxs.pack', 'submodule': ['build'], 'as': 'build_wheel'}, 
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']},
        {'module':'structure.structure', 'submodule': ['StructureCorrect']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'os.path', 'submodule': ['split']}
    )
    def pack(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs pack"
        parse.set_description("Création du package publiable")
        parse.set_argument(longname="windows", description="Package whl pour windows", default=False)
        parse.set_argument(longname="linux", description="Package whl pour linux", default=False)
        parse.set_argument(longname="sdist", description="Package .tar.gz", default=False)
        parse.set_argument("d", longname="dryrun", description="Affichage des informations de packaging", default=None)
        #parse.set_parameter("NAME", description="Nom de l'environnement")
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('pack'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()

                project_folder = split(get_nexus_file())[0]
                #print(project_folder)
                #includes = tfile.get_key("includes", "project.build")
                #include_files = tfile.get_key("include_files", "project.build")

                #Sauvegarde l'état et supprime les fichiers inutiles une fois fini
                sc = StructureCorrect(project_folder)
                sc.init()

                if argument.dryrun:
                    build_wheel(tfile, project_folder, typefile="sdist", dry_run=True)
                else:
                    if argument.sdist and not argument.windows and not argument.linux:
                        build_wheel(tfile, project_folder, typefile="sdist")

                    if argument.windows:
                        build_wheel(tfile, project_folder, "windows")
                        if argument.sdist:
                            build_wheel(tfile, project_folder, typefile="sdist")

                    elif argument.linux:
                        build_wheel(tfile, project_folder, "linux")
                        if argument.sdist:
                            build_wheel(tfile, project_folder, typefile="sdist")

                    elif not argument.windows and not argument.linux and not argument.sdist:
                        install_requires = tfile.get_key('dependencies','project').copy() if tfile.get_key('dependencies','project') is not None else None

                        if ('windows' in install_requires and len(install_requires['windows'])>1) or ('linux' in install_requires and len(install_requires['linux'])>1):
                            os.system("nxs pack --windows")
                            os.system("nxs pack --linux")
                        else:
                            build_wheel(tfile, project_folder)

                        build_wheel(tfile, project_folder, typefile="sdist")


                sc.purge()
                
    
    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file', 'get_root_project']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'re'},
        {'module':'app.display', 'submodule': ['prompt','logs', 'print_nxs']},
        {'module':'template', 'submodule':['regex']},
        {'module':'datetime', 'submodule':['datetime']},
        {'module':'os.path', 'submodule':['exists', 'join', 'dirname', 'isdir']},
        {'module': 'template', 'submodule': ['default_conf']},
        {'module':'repository.repo', 'submodule': ['Repo']},
        {'module':'package.package', 'submodule':['compare_version']}
    )
    def version(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs version"
        parse.set_description("Affichage/Changement de la version du projet")
        #parse.set_argument(longname="list", description="Lister les environnements virtuels", default=False)
        parse.set_parameter("VERSION", description="Numéro de version ou alias version (major/minor/patch)")
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('version'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
                actual = tfile.get_key('version','project')

                if len(parameter)>0:
                    version_regex = re.compile(regex.version)

                    actual_version = version_regex.match(actual)
                    if actual_version!=None:
                        new_version = version_regex.match(parameter[0])
                        if new_version!=None:
                            if compare_version(parameter[0], ">", actual):
                                new_version = parameter[0]
                            else:
                                logs("Mauvaise version", "critical")
                                exit()

                        else:
                            actual_major = int(actual_version.group('major'))
                            actual_minor = int(actual_version.group('minor'))
                            actual_patch = int(actual_version.group('patch'))

                            if parameter[0]=='major':
                                actual_major+=1
                                actual_minor=0
                                actual_patch=0
                            elif parameter[0]=='minor':
                                actual_minor+=1
                                actual_patch=0
                            elif parameter[0]=='patch':
                                actual_patch+=1
                            else:
                                logs("alias non valide", "critical")
                                exit()

                            new_version = f"{actual_major}.{actual_minor}.{actual_patch}"
                        
                        changelog = tfile.get_key('changelog','project.metadata')

                        if (changelog=="" or changelog==None):
                            changelog="changelog.md"

                        if self.conf.load(val='project.changelog', section='',default=default_conf.project_changelog):
                            changefile = join(dirname(get_nexus_file()),changelog)
                            if changelog!="":
                                data = ""
                                if not exists(changefile):
                                    tfile.edit_key('changelog', changelog, "project.metadata")
                                    data+="# Changelog\n"

                                data+=f"\n## [{new_version}] - {datetime.today().strftime('%Y-%m-%d')}\n"

                                description=None
                                print_nxs("Description du changement:")
                                while description!="":
                                    description = prompt("> ")
                                    if description!="":
                                        data+="- "+description+"\n"

                                with open(changefile, 'a') as f:
                                    f.write(data)

                        tfile.edit_key('version', new_version, "project")
                        print_nxs("Nouvelle version: ", nojump=True)
                        print_nxs(new_version, color=__main__.color["orange_1"])

                        if self.conf.load(val='repo_branch_autocreate', section='',default=default_conf.repo_branch_autocreate):               
                            git_path = join(get_root_project(), '.git')
                            if exists(git_path) and isdir(git_path):
                                repo = Repo(get_root_project())

                                status_code = repo.switch_branch(new_version, create=True)
                                if status_code:
                                    logs(f"Bascule sur la branche {new_version}")

                else:
                    logs(actual)


    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'re'},
        {'module':'template', 'submodule':['regex']},
        {'module':'package.check', 'submodule':['is_native_module']},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file', 'get_root_project']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'os.path', 'submodule': ['exists', 'isfile', 'isdir', 'join', 'abspath']},
        {'module':'package.package', 'submodule':['dependency_to_list']},
        {'module':'sys_nxs.host', 'submodule':['path_rep']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'install_pool', 'get_py_version', 'init_pip', 'get_all_package']}
    )
    def add(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs add"
        parse.set_description("Ajout de dépendances dans le projet")
        parse.set_argument(longname="windows", description="Ajouter les dépendances uniquement pour Windows", default=False)
        parse.set_argument(longname="linux", description="Ajouter les dépendances uniquement pour Linux", default=False)
        parse.set_argument(longname="install", description="Installe les dépendances", default=False)
        parse.set_argument(longname="force", description="Force l'installation", default=False)
        parse.set_argument("r", longname="requirements", description="Spécifier un fichier requirements", store="value", default=None)
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parse.set_parameter("PACKAGE", description="Nom du package")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('add'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
                actual = tfile.get_key('dependencies','project')
                new_deps = False
                new_files = False
                
                actual_packages = tfile.get_key('packages','project.build')
                actual_includes = tfile.get_key('includes','project.build')
                actual_include_files = tfile.get_key('include_files','project.build')
                #print(actual)
                version_regex = re.compile(regex.dependencies)

                if not argument.windows and not argument.linux:
                    temp = actual
                elif argument.linux and not argument.windows:
                    if not 'linux' in actual:
                        actual['linux'] = {}
                    temp = actual['linux']
                else:
                    if not 'windows' in actual:
                        actual['windows'] = {}
                    temp = actual['windows']

                if argument.requirements!=None:
                    file_r = abspath(argument.requirements)
                    if exists(file_r) and isfile(file_r):
                        with open(file_r, 'r') as f:
                            parameter = f.read().split("\n")

                projectfolder = join(get_root_project(), tfile.get_key('name','project'))

                for_install = {}
                for element in parameter:
                    if len(element):
                        #Contrôle si c'est un package interne
                        test_file = join(element.replace(".","/"))
                        if exists(element) and isfile(element) and not element.endswith('.py') and not element.endswith('.pyw'):
                            #actual_include_files
                            path_file = abspath(element)
                            if path_file.startswith(projectfolder):
                                path_file = path_file.replace(projectfolder+path_rep[0],'')
                                if path_file not in actual_include_files:
                                    actual_include_files.append(path_file)
                                    new_files = True
                        elif exists(test_file+".py") or exists(test_file+".pyw") or (exists(test_file) and isdir(test_file)):
                            if element not in actual_includes:
                                actual_includes.append(element)
                                new_deps=True
                        else:
                            matcher = version_regex.match(element)
                            if matcher!=None:
                                packagename = matcher.group(1)
                                if packagename.lower()!="windows" and packagename.lower()!="linux":
                                    version = matcher.group(2)
                                    if version==None:
                                        version="N.A"

                                    if packagename in temp and temp[packagename]!=version:
                                        logs(f"Changement de version pour la dépendances {packagename} ({temp[packagename]} -> {version})")
                                    temp[packagename] = version
                                    for_install[packagename] = version
                                    new_deps=True

                                else:
                                    logs(f"Nom de dépendances invalide: {element}")

                            else:
                                logs(f"Package {element} invalide", "warning")

                if new_deps:
                    mdm_env = dependency_to_list(temp)

                    if len(mdm_env):
                        new = {}
                        for element in temp:
                            if element not in mdm_env and element.lower()!='windows' and element.lower()!='linux':
                                pass
                            else:
                                new[element] = temp[element]

                                if element.lower()!='windows' and element.lower()!='linux' and not is_native_module(element):
                                    if element not in actual_packages:
                                        actual_packages.append(element)
                        if not argument.windows and not argument.linux:
                            actual = new
                        elif argument.linux and not argument.windows:
                            actual['linux'] = new
                        else:
                            actual['windows'] = new

                        tfile.edit_key('includes', actual_includes, "project.build")
                        tfile.edit_key('packages', actual_packages, "project.build")
                        tfile.edit_key('dependencies', actual, "project")
                        logs("Dépendances mises à jour")

                        if argument.install:
                            cmd = get_executable(tfile, argument.env)
                            if cmd!=None:
                                mdm_install = dependency_to_list(for_install)

                                if self.conf.load(val='virtualenvs.upgradepip', section='',default=default_conf.virtualenvs_upgradepip):
                                    init_pip(cmd)
                                #### ????????????????
                                if not hasattr(self, 'py_version'):
                                    self.py_version = get_py_version(cmd)
                                #### ????????????????

                                if len(mdm_install)>0:
                                    install_pool(cmd, mdm_install, force=argument.force)
                                else:
                                    logs("Aucun module a installer")
                            else:
                                logs("L'exécutable Python est introuvable", "critical")
                if new_files:
                    tfile.edit_key('include_files', actual_include_files, "project.build")
                    logs("Ajout des fichiers includes")

    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file', 'get_root_project']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'os.path', 'submodule': ['exists','isfile','abspath','join']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'sys_nxs.host', 'submodule':['path_rep']},
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'remove_pool']}
    )
    def remove(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs remove"
        parse.set_description("Suppression de dépendances dans le projet")
        parse.set_argument(longname="windows", description="Suppression pour Windows", default=False)
        parse.set_argument(longname="linux", description="Suppression pour Linux", default=False)
        parse.set_argument(longname="uninstall", description="Désinstalle les dépendances", default=False)
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parse.set_parameter("PACKAGE", description="Nom du package")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('remove'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
                actual = tfile.get_key('dependencies','project')
                actual_include_files = tfile.get_key('include_files','project.build')

                deleted = []
                deleted_files = False

                if not argument.windows and not argument.linux:
                    temp = actual
                elif argument.linux and not argument.windows:
                    if not 'linux' in actual:
                        actual['linux'] = {}
                    temp = actual['linux']
                else:
                    if not 'windows' in actual:
                        actual['windows'] = {}
                    temp = actual['windows']

                for element in parameter:
                    if element in temp:
                        deleted.append(element)
                        del temp[element]
                    if element in actual_include_files:
                        actual_include_files.remove(element)
                        deleted_files = True

                projectfolder = join(get_root_project(), tfile.get_key('name','project'))
                for element in parameter:
                    if exists(element) and isfile(element):
                        path_file = abspath(element)
                        if path_file.startswith(projectfolder):
                            path_file = path_file.replace(projectfolder+path_rep[0],'')
                            if path_file in actual_include_files:
                                actual_include_files.remove(path_file)
                                deleted_files = True

                if not argument.windows and not argument.linux:
                    actual = temp
                elif argument.linux and not argument.windows:
                    actual['linux'] = temp
                else:
                    actual['windows'] = temp
                tfile.edit_key('dependencies', actual, "project")

                if len(deleted)!=0:
                    actual_packages = tfile.get_key('packages','project.build')
                    actual_includes = tfile.get_key('includes','project.build')

                    for element in deleted:
                        if element in actual_packages:
                            actual_packages.remove(element)
                        if element in actual_includes:
                            actual_includes.remove(element)

                    tfile.edit_key('includes', actual_includes, "project.build")
                    tfile.edit_key('packages', actual_packages, "project.build")

                    logs("Dépendances mises à jour")

                if argument.uninstall:
                    if len(deleted)>0:
                        cmd = get_executable(tfile, argument.env)
                        if cmd!=None:
                            remove_pool(cmd, deleted)
                        else:
                            logs("L'exécutable Python est introuvable", "critical")
                    else:
                        logs("Aucun module a désinstaller")

                if deleted_files:
                    tfile.edit_key('include_files', actual_include_files, "project.build")
                    logs("Suppression des fichiers includes")

    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'os', 'submodule': ['chdir']},
        {'module':'os.path', 'submodule': ['join','split']},
        {'module':'package.package', 'submodule':['dependency_to_list', 'lock_package', 'get_all_requirement']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'get_all_package']},
        {'module':'analysis.project', 'submodule': ['get_modules_from_project', 'check_realname']}
    )
    def check(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs check"
        parse.set_description("Contrôle la compatibilité des dépendances")
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parse.set_parameter("PACKAGE", description="Nom du package")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('check'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
                actual = tfile.get_key('dependencies','project')
                actual = lock_package(actual)
                data = None

                deps = dependency_to_list(actual, force=True)
                logs("Analyse des dépendances terminée")
                #if deps!=None:
                project_folder = split(get_nexus_file())[0]
                code_folder = join(project_folder, tfile.get_key("name","project"))
                chdir(code_folder)

                data = get_modules_from_project([tfile.get_key("mainfile","project")])

                cmd = get_executable(tfile, argument.env)
                if exists(cmd):
                    logs("Vérification des dépendances inutiles")

                    list_installed = get_all_package(cmd)

                    used = list(set(deps.keys()).union(data['dependency']))

                    used = get_all_requirement(used)

                    used = [x.lower().replace("-", "_") for x in used]

                    for package_installed in list_installed:
                        if package_installed.lower().replace("-", "_") not in used:
                            logs(f"{package_installed} inutilisé", "warning")
                    
                    logs("Vérification des dépendances inutiles terminée")

                if data and 'dependency' in data:
                    logs("Analyse des nouvelles dépendances")
                    for element in data['dependency']:
                        element = check_realname(element)
                        if element:
                            if isinstance(element, str):
                                if element not in actual:
                                    logs(f"{element} non présent dans les dépendances", "warning")

                            elif isinstance(element, dict):
                                if 'windows' in element and 'windows' in actual:
                                    if element['windows'] not in actual['windows']:
                                        logs(f"{element['windows']} non présent dans les dépendances windows", "warning")
                                elif 'linux' in element and 'linux' in actual:
                                    if element['linux'] not in actual['linux']:
                                        logs(f"{element['linux']} non présent dans les dépendances linux", "warning")

                    logs("Analyse des nouvelles dépendances terminée")

                if data and 'externe' in data:
                    logs("Vérification des informations de build")
                    actual_packages = tfile.get_key('packages','project.build')
                    for element in data['externe']:
                        if element not in actual_packages:
                            logs(f"{element} non présent dans les packages de build", "warning")
                    logs("Analyse des informations packages terminée")
                
                if data and 'interne' in data:
                    logs("Analyse des informations includes")
                    actual_includes = tfile.get_key('includes','project.build')
                    for element in data['interne']:
                        if element not in actual_includes:
                            logs(f"{element} non présent dans les includes de build", "warning")
                    logs("Analyse des informations includes terminée")


    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'app.display', 'submodule': ['logs', 'print_nxs']},
        {'module':'shutil', 'submodule': ['copyfile']},
        {'module':'os', 'submodule': ['remove', 'name']}
    )
    def config_nexus(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs config"
        parse.set_description("Affichage/Modification de la configuration de nexus")
        parse.set_argument(longname="disable", description="Désactive le paramètre", default=False)
        parse.set_argument(longname="enable", description="Active le paramètre masqué", default=False)
        parse.set_argument(longname="reload", description="Recharger le fichier de config par défaut", default=False)
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            data = self.conf.load(section='')
            if len(parameter)==0 and not argument.reload:
                datacopy = data.copy()
                data = {}
                for key, value in datacopy.items():
                    if "." in key:
                        category = key.split(".")[0]
                    else:
                        category = "general"

                    if category not in data:
                        data[category] = {}

                    data[category][key] = value

                for cat, cat_info in data.items():
                    print_nxs(f"\n#{cat}", color=__main__.color['dark_gray'])
                    for key, value in cat_info.items():
                        print_nxs(f"{key}: ", nojump=True)
                        print_nxs(value, color=__main__.color['yellow'])

                """
                for key, value in data.items():
                    print_nxs(f"{key}: ", nojump=True)
                    print_nxs(value, color=__main__.color['yellow'])
                """

                is_disable = self.conf.disabled_line()
                if len(is_disable) and '' in is_disable:
                    is_disable = is_disable['']
                    print_nxs("\nParamètre désactivé:", color=__main__.color['red'])
                    for key, value in is_disable.items():
                        print_nxs(f"{key}: ", nojump=True)
                        print_nxs(value, color=__main__.color['yellow'])
            else:
                if argument.enable:
                    is_disable = self.conf.disabled_line()
                    if len(is_disable) and '' in is_disable:
                        is_disable = is_disable['']
                        if parameter[0] in is_disable:
                            self.conf.enable(parameter[0])
                            logs(f"{parameter[0]} activé")
                
                elif argument.disable:
                    if parameter[0] in data:
                        self.conf.disable(parameter[0])
                        logs(f"{parameter[0]} désactivé")

                elif argument.reload:
                    if exists(self.ini_file):
                        remove(self.ini_file)
                    if name=="nt":
                        default_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"template","default_ini")
                    else:
                        default_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"template","default_ini_lin")
                    if exists(default_file):
                        copyfile(default_file, self.ini_file)
                        logs("Fichier de conf rechargé")
                    else:
                        print("Fichier de conf impossible à générer", color=__main__.color["light_red"])

                elif len(parameter):
                    parameter[0] = parameter[0].lower()
                    if parameter[0] in data:
                        if isinstance(data[parameter[0]], bool):
                            if data[parameter[0]]==True:
                                self.conf.change(parameter[0], False)
                                logs(f"Passage de {parameter[0]} à False")  
                            else:
                                self.conf.change(parameter[0], True)    
                                logs(f"Passage de {parameter[0]} à True")  
                        if isinstance(data[parameter[0]], str):
                            if len(parameter)==2:
                                logs(f"Modification du paramètre {parameter[0]}")  
                                self.conf.change(parameter[0], parameter[1])
                        if isinstance(data[parameter[0]], int):
                            if len(parameter)==2 and parameter[1].isdigit():
                                logs(f"Modification du paramètre {parameter[0]}")  
                                self.conf.change(parameter[0], parameter[1])
                    else:
                        logs(f"Paramètre {parameter[0]} introuvable", "error")  



    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['get_nexus_file', 'get_root_project']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'os.path', 'submodule': ['exists','join','isdir']},
        {'module':'glob', 'submodule': ['glob']},
        {'module':'build_nxs.publish', 'submodule': ['Uploader']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'re'},
        {'module':'package.package', 'submodule':['compare_version']},
        {'module':'template', 'submodule':['regex']}
    )
    def publish(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs publish"
        parse.set_description("Publication du package")
        parse.set_argument(longname="url", description="Url du repository", default=None, store="value")
        #parse.set_argument(longname="enable", description="Active le paramètre masqué", default=False)
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:

            inproject = False
            if len(parameter):
                dist = parameter
            else:
                root = get_root_project()
                if root:
                    dist = [join(root, 'dist')]
                    inproject = True

                    tfile = TOMLnxs(get_nexus_file())
                    tfile.load_doc()
                else:
                    logs("Projet nexus introuvable", "critical")
                    exit()

            files = []
            for dist in dist:
                if exists(dist):
                    reg_match = re.compile(regex.pack_regex)
                    if isdir(dist):
                        content = glob(dist+"/*")
                    else:
                        content = glob(dist+"*")

                    for file in content:
                        find = reg_match.search(file)
                        if find:
                            if inproject:
                                packagename = find.group('packagename').replace("_","-")
                                version = find.group('version')
                                d = tfile.get_key('name','project').replace("_","-")
                                e = tfile.get_key('version','project')
                                if d==packagename and compare_version(version, "==", e):
                                    files.append(file)
                            else:
                                files.append(file)
                else:
                    logs(f"Répertoire {dist} introuvable", "critical")
            
            if len(files):
                cu = Uploader(files, argument.url)
                cu.connect()
                cu.upload()
            else:
                logs("Aucun package disponible", "warning")


    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'shutil', 'submodule': ['rmtree']},
        {'module':'glob', 'submodule': ['glob']},
        {'module':'os.path', 'submodule': ['abspath','exists']},
        {'module':'uuid', 'submodule': ['uuid4']},
        {'module':'build_nxs.pack', 'submodule': ['build_fake']},
        {'module':'structure.structure', 'submodule': ['StructureCorrect']},
        {'module':'build_nxs.publish', 'submodule': ['Uploader']},
        {'module':'package.package', 'submodule': ['latest_version']}
    )
    def provisioning(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs provisioning"
        parse.set_description("Réserve le nom d'un package sur un repository")
        parse.set_argument(longname="url", description="Url du repository", default=None)
        parse.set_parameter("PACKAGE", description="Nom de package")
        parameter, argument = parse.load()

        if parameter!=None:
            packagename = parameter[0]
            if latest_version(packagename)==None:
                print("disponible")
                foldername = str(uuid4())
                while exists(foldername):
                    foldername = uuid4()

                sc = StructureCorrect(abspath('.'), exclude=foldername)
                sc.init()
                build_fake(packagename, foldername)
                sc.purge()

                files = glob(foldername+"/*")
                if len(files):
                    cu = Uploader(files, argument.url)
                    cu.connect()
                    cu.upload()
                rmtree(foldername)
            else:
                logs(f"package {packagename} non disponible", "warning")

    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'zpp_color', 'submodule': ['fg', 'attr']},
        {'module':'package.package', 'submodule': ['in_repo', 'get_alias', 'set_alias']}
    )
    def alias(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs alias"
        parse.set_description("Gestion des alias de package")
        parse.set_argument('a', longname="add", description="Ajouter un alias", default=False)
        parse.set_argument('r', longname="remove", description="Supprimer un alias", default=False)
        parse.set_argument(longname="windows", description="Ajouter d'un alias uniquement pour Windows", default=False)
        parse.set_argument(longname="linux", description="Ajouter d'un alias uniquement pour Linux", default=False)
        parse.set_parameter("ALIAS", description="Nom de l'alias")
        parse.set_parameter("PACKAGE", description="Nom du package")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if argument.add and len(parameter)==2:
                    alias = get_alias()
                    if in_repo(parameter[1]):
                        change = False
                        if not argument.windows and not argument.linux:
                            if parameter[0] not in alias:
                                change = True
                                alias[parameter[0]] = parameter[1]
                            else:
                                logs(f"Alias {parameter[0]} déjà configuré sur {alias[parameter[0]]}", "error")
                        elif argument.windows and not argument.linux:
                            if parameter[0] not in alias:
                                alias[parameter[0]] = {}
                            if 'windows' in alias[parameter[0]]:
                                logs(f"Alias {parameter[0]} déjà configuré sur {alias[parameter[0]]['windows']}", "error")
                            else:
                                change = True
                                alias[parameter[0]]['windows'] = parameter[1]
                        elif not argument.windows and argument.linux:
                            if parameter[0] not in alias:
                                alias[parameter[0]] = {}
                            if 'linux' in alias[parameter[0]]:
                                logs(f"Alias {parameter[0]} déjà configuré sur {alias[parameter[0]]['linux']}", "error")
                            else:
                                change = True
                                alias[parameter[0]]['linux'] = parameter[1]

                        if change:
                            set_alias(alias)
                            logs(f"Alias {parameter[0]} ajouté")

                    else:
                        logs(f"Le module {parameter[1]} n'existe pas sur les repos", "error")
            
            if argument.remove and len(parameter)>=1:
                change = False
                alias = get_alias()
                for alias_name in parameter:
                    if alias_name in alias:
                        if not argument.windows and not argument.linux:
                            del alias[alias_name]
                            change = True
                        elif argument.windows and not argument.linux:
                            if 'windows' in alias[alias_name]:
                                del alias[alias_name]['windows']
                                change = True
                            else:
                                logs(f"Alias {alias_name} n'ont configurés pour Windows", "error")

                        elif not argument.windows and argument.linux:
                            if 'linux' in alias[alias_name]:
                                del alias[alias_name]['linux']
                                change = True
                            else:
                                logs(f"Alias {alias_name} n'ont configurés pour Linux", "error")
                        if len(alias[alias_name])==0:
                            del alias[alias_name]
                    else:
                        logs(f"Alias {alias_name} introuvable", "error")
        
                if change:
                    set_alias(alias)
                    logs(f"Alias supprimé")
            else:
                alias = get_alias()
                for alias_name, value in alias.items():
                    maxsize = len(max(alias, key=lambda x: len(x)))+1
                    if isinstance(value, str):
                        print(f"{fg(__main__.color['dark_gray'])}{alias_name : <{maxsize}}{attr(0)}: {value}")
                    if isinstance(value, dict):
                        print(f"{fg(__main__.color['dark_gray'])}{alias_name : <{maxsize}}{attr(0)}")
                        maxinter = len(max(value, key=lambda x: len(x)))
                        for e1, e2 in value.items():
                            print(f"  {fg(__main__.color['light_gray'])}{e1 : <{maxinter}}{attr(0)}: {e2}")

    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'package.package', 'submodule': ['get_package','build_cache']}
    )
    def test(self):
        #build_cache()
        print(get_package("poetry"))


    #Gestion des templates
    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'zpp_menu'},
        {'module':'yaml'},
        {'module':'re'},
        {'module':'app.display', 'submodule': ['logs', 'prompt', 'print_nxs', 'form']},
        {'module':'os.path', 'submodule': ['join', 'dirname', 'exists']},
        {'module':'package.package', 'submodule': ['get_package', 'dependency_to_list']},
        {'module':'template', 'submodule':['regex']}
    )
    def template(self):
        parse = zpp_args.parser(sys.argv[1:], error_lock=True)
        parse.command = "nxs template"
        parse.set_description("Gestion des templates")
        parse.set_argument("s", longname="set", description="Créer un template", store="value", default=None)
        parse.set_argument("g", longname="get", description="Afficher un template", store="value", default=None)
        parse.set_argument("e", longname="edit", description="Editer un template", store="value", default=None)
        parse.set_argument("l", longname="list", description="Lister les templates disponibles", default=False)
        parameter, argument = parse.load()

        if parameter!=None and argument!=None:
            template_file = join(dirname(self.ini_file), "sandbox.template")

            if not exists(template_file):
                open(template_file, "w").close()

            with open(template_file) as f:
                data_template = yaml.safe_load(f)
                if not data_template:
                    data_template = {}

            if argument.list:
                for temp_name, temp_info in data_template.items():
                    print_nxs(f"{temp_name}: ", nojump=True)
                    print_nxs(f"{len(temp_info)} packages", color=__main__.color['yellow'])


            elif argument.set:
                dependencies = []
                package_name = None

                while package_name!="":
                    package_name = prompt("Package name")
                    if len(package_name):
                        dependencies.append(package_name)

                for package in dependencies.copy():
                    package_compiled = re.compile(regex.package_regex)
                    package_match = package_compiled.search(package)
                    if package_match!=None:
                        name = package_match.group('name')
                        version = package_match.group('version')
                        info = get_package(name)
                        if not len(info):
                            logs(f"Le package {pack} n'existe pas", "error")
                            dependencies.remove(package)

                data_template[argument.set] = dependencies
                with open(template_file, "w") as f:
                    yaml.dump(data_template, f, allow_unicode=True)


            elif argument.get:
                if argument.get in data_template:
                    for line in data_template[argument.get]:
                        print_nxs(f"- {line}")
                else:
                    logs(f"Le template {argument.get} n'existe pas", "critical")
            
            elif argument.edit:
                if argument.edit in data_template:
                    package_list = data_template[argument.edit]
                    id_list = 0

                    while len(package_list)+2!=id_list:
                        id_list = zpp_menu.Menu("== Editeur de template ==", package_list+["= Ajouter", "= Sauvegarder", "= Quitter"], Pointer=">")
                        if len(package_list)+2!=id_list and len(package_list)+1!=id_list and len(package_list)!=id_list:
                            options = zpp_menu.Menu(f"== Edition de {package_list[id_list]} ==", ["Changement", "Suppression", "Retour"], Pointer=">")
                            if options==0:
                                new_value = form("Package", package_list[id_list])
                                if new_value!=package_list[id_list]:
                                    package_list[id_list] = new_value

                            elif options==1:
                                package_list.remove(package_list[id_list])
                                id_list = 0

                        elif len(package_list)==id_list:
                            package = input("Package: ")
                            if package not in data_template:
                                package_compiled = re.compile(regex.package_regex)
                                package_match = package_compiled.search(package)
                                if package_match!=None:
                                    name = package_match.group('name')
                                    version = package_match.group('version')
                                    info = get_package(name)
                                    if not len(info):
                                        logs(f"Le package {name} n'existe pas", "error")
                                        input("")
                                    else:
                                        data_template[argument.edit].append(package)

                        elif len(package_list)+1==id_list:
                            try:
                                with open(template_file, "w") as f:
                                    yaml.dump(data_template, f, allow_unicode=True)
                                logs("Template enregistré", "success")
                            except Exception as err:
                                logs(f"Erreur lors de l'enregistrement du template: {err}", "error")
                            
                            input("")
                else:
                    logs(f"Le template {argument.edit} n'existe pas", "critical")


    #Création d'un venv temporaire qui se détruit en sortant
    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'yaml'},
        {'module':'re'},
        {'module':'app.display', 'submodule': ['logs', 'prompt', 'print_nxs']},
        {'module':'os.path', 'submodule': ['join', 'dirname', 'exists']},
        {'module':'package.package', 'submodule': ['get_package', 'dependency_to_list']},
        {'module':'template', 'submodule':['regex']},
        {'module':'env_nxs.env', 'submodule': ['create_temp_env', 'Context', 'open_environment', 'install_pool']}
    )
    def sandbox(self):
        parse = zpp_args.parser(sys.argv[1:], error_lock=True)
        parse.command = "nxs sandbox"
        parse.set_description("Création d'un environnement temporaire")
        parse.set_argument("t", longname="template", description="Utiliser un template", store="value", default=None)
        parse.set_argument("s", longname="set_template", description="Créer un template", store="value", default=None)
        parse.set_argument("g", longname="get_template", description="Afficher un template", store="value", default=None)
        parse.set_argument("l", longname="list_template", description="Lister les templates disponibles", default=False)
        parameter, argument = parse.load()

        if parameter!=None and argument!=None:
            template_info = None

            if argument.template:
                template_file = join(dirname(self.ini_file), "sandbox.template")

                if not exists(template_file):
                    open(template_file, "w").close()

                with open(template_file) as f:
                    data_template = yaml.safe_load(f)
                    if not data_template:
                        data_template = {}

                if argument.template in data_template:
                    template_info = data_template[argument.template]
                else:
                    logs(f"Le template {argument.template} n'existe pas", "critical")
                    exit()

            name, pathenv = create_temp_env(upgradepip=False)
            context = Context(pathenv, name)

            if template_info:
                logs("Installation des dépendances")
                deps = {}
                for package in template_info:
                    package_compiled = re.compile(regex.package_regex)
                    package_match = package_compiled.search(package)
                    if package_match!=None:
                        name = package_match.group('name')
                        version = package_match.group('version')
                        if version==None:
                            version = "N.A"

                        deps[name] = version

                to_install = dependency_to_list(deps, force=True)

                if len(to_install):
                    install_pool(context.env_exe, to_install, force=True)

            open_environment(pathenv)


    #Sauvegarde le projet
    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']}, 
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'os', 'submodule': ['chdir']},
        {'module':'datetime', 'submodule': ['datetime']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'structure.structure', 'submodule': ['list_projectfile']},
        {'module':'zipfile', 'submodule': ['ZipFile', 'ZIP_LZMA']},
        {'module':'getpass', 'submodule': ['getpass']},
        {'module':'os.path', 'submodule': ['dirname', 'exists', 'abspath']}
    )
    def backup(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs backup"
        parse.set_description("Sauvegarde du projet en cours")
        parse.set_argument('q', longname="quality", description="Qualité du compression (1-9)", store="value", type="digit", default=9)
        parse.set_argument('o', longname="out", description="Fichier de sortie", default=None)
        parse.set_argument('f', longname="force", description="Forcer l'écriture sur le fichier de sortie", default=None)
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('backup'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()

                if not 1<=argument.quality<=9:
                    argument.quality=9
                    logs("Valeur de quality invalide. Initialisation à 9", "warning")

                if argument.out==None:
                    argument.out = "archive_"+datetime.today().strftime("%Y%m%d%H%M")+".zip"

                fileout = abspath(argument.out)
                if exists(fileout) and not argument.force:
                    logs(f"Le fichier {fileout} existe déjà", "critical")
                    return

                elif exists(fileout) and argument.force:
                    logs(f"Réecriture sur le fichier {fileout}", "warning")

                logs("Création de l'archive")
                #Déplacement à la racine du projet
                chdir(dirname(get_nexus_file()))

                content = list_projectfile(tfile)

                with ZipFile(fileout,'w',compression=ZIP_LZMA,allowZip64=True) as zf:
                    for file in content:
                        zf.write(file)
                
                logs(f"Archive {argument.out} créée")

    #Lock les versions de package
    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file', 'get_root_project']},
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'get_package_installed', 'filter_deps']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'os.path', 'submodule': ['join']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'}
    )
    def lock(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs lock"
        parse.set_description("Lock les versions de package")
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parse.set_parameter("PACKAGE", description="Nom des packages à lock")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('lock'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
                deps = tfile.get_key('dependencies','project')

                if deps!=None:
                    cmd = get_executable(tfile, argument.env)
                    if exists(cmd):
                        if len(parameter):
                            deps = filter_deps(parameter, deps)

                        lockable = get_package_installed(cmd, deps, {})

                        insert = {"dependencies": lockable}
                        tfile = TOMLnxs(join(get_root_project(), 'nexus.lock'))
                        tfile.dict_to_toml(insert)

                    else:
                        logs("L'environnement est introuvable", "warning")
                else:
                    logs("Aucunes dépendances configurées")


    #Afficher les informations du projet
    @impmagic.loader(
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']},
        {'module':'package.package', 'submodule': ['lock_package']}, 
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'zpp_color', 'submodule': ['fg', 'attr']}, 
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'toml_nxs.toml', 'submodule': ['read_data']}
    )
    def project(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs project"
        parse.set_description("Afficher les informations du projet")
        #parse.set_parameter("PACKAGE", description="Nom des packages à lock")
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('run'):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
                project = tfile.get_key('project')

                if project!=None:
                    model = {
                        'INFORMATIONS': {'model': ['name', 'version', 'description', 'mainfile', 'requires-python'], 'data': None},
                        'METADATA': {'model': ['authors', 'maintainers', 'license', 'keywords', 'classifiers', 'copyright'], 'data': 'metadata'},
                        'BUILD': {'model': ['includes', 'excludes', 'include_files', 'optimize', 'no_compress', 'GUI', 'icon'], 'data': 'build'},
                        'WHEEL': {'model': ['platform', 'entry_points'], 'data': 'wheel'}
                        #'dependencies': {'model': None, 'data': 'dependencies'},
                    }


                    for line, details in model.items():
                        if details['data']==None:
                            data = project.copy()
                        elif details['data'] is not None and details['data'] in project:
                            data = project[details['data']].copy()
                        else:
                            continue


                        print(f"\n[{fg(__main__.color['green'])}{line}{attr(0)}] ")
                        for element in details['model']:
                            if element in data and (isinstance(data[element], int) or isinstance(data[element], float) or len(data[element])):
                                if isinstance(data[element], str) or isinstance(data[element], int) or isinstance(data[element], float):
                                    print(f"{fg(__main__.color['dark_gray'])}{element}{attr(0)}: {data[element]} ")
                                elif isinstance(data[element], list):
                                    print(f"{fg(__main__.color['dark_gray'])}{element}{attr(0)}: {list(data[element])} ")
                                else:
                                    print(f"{fg(__main__.color['dark_gray'])}{element}{attr(0)}:")
                                    read_data(data[element], "  ")

                    if 'dependencies' in project:
                        deps = lock_package(project['dependencies'])
                        print(f"\n[{fg(__main__.color['green'])}DEPENDENCIES{attr(0)}] ")
                        for element, value in deps.items():
                            if isinstance(value, str):
                                if value!='N.A':
                                    print(f"  {fg(__main__.color['dark_gray'])}{element}{attr(0)} ({value}) ")
                                else:
                                    print(f"  {fg(__main__.color['dark_gray'])}{element}{attr(0)}")
                            else:
                                if len(value):
                                    print(f"  {element}")
                                    for el, vl in value.items():
                                        if vl!='N.A':
                                            print(f"    {fg(__main__.color['dark_gray'])}{el}{attr(0)} ({vl}) ")
                                        else:
                                            print(f"    {fg(__main__.color['dark_gray'])}{el}{attr(0)}")

    @impmagic.loader(
        {'module':'sys'},
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_root_project']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'repository.repo', 'submodule': ['Repo']},
        {'module':'os.path', 'submodule': ['exists', 'isdir', 'join']}
    )
    def branch(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs branch"
        parse.set_description("Action sur les branches du repo")
        parse.set_argument('a', longname="add", description="Ajouter une branche", store="value", default=None)
        parse.set_argument('d', longname="delete", description="Supprimer une branche", store="value", default=None)
        parse.set_argument('s', longname="switch", description="Switch sur une autre branche", store="value", default=None)
        parse.set_argument('r', longname="rename", description="Renommer une branche", store="value", default=None)
        parse.set_argument('m', longname="merge", description="Merge les branches", store="value", default=None)
        parse.set_argument('c', longname="create", description="Créer la branche si inexistante", default=False, category="switch")
        parse.set_argument('S', longname="source", description="Choisir la branche source", store="value", default=None, category="add")
        parse.set_argument('C', longname="commit", description="Choisir le commit de départ", store="value", default='HEAD', category="add")
        parse.set_argument('D', longname="dest", description="Choisir la branche de destination", store="value", default=None, category="merge")
        #parse.set_parameter("ACTION", description="Nom des packages à lock")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project(''):
                git_path = join(get_root_project(), '.git')
                if exists(git_path) and isdir(git_path):
                    repo = Repo(get_root_project())

                    if argument.add:
                        status_code = repo.add_branch(argument.add, source_branch=argument.source, commit_id=argument.commit)
                        if status_code:
                            logs(f"Branche {argument.add} créée")

                    elif argument.delete:
                        status_code = repo.delete_branch(argument.delete)
                        if status_code:
                            logs(f"Branche {argument.delete} supprimée")

                    elif argument.switch:
                        status_code = repo.switch_branch(argument.switch, create=argument.create)
                        if status_code:
                            logs(f"Bascule sur la branche {argument.switch}")

                    elif argument.rename:
                        if len(parameter):
                            dest = parameter[0]
                        else:
                            dest = input("Nouvea nom: ")

                        status_code = repo.rename_branch(argument.rename, dest)
                        if status_code:
                            logs(f"Branche {argument.rename} renommée en {dest}")

                    elif argument.merge:
                        status_code = repo.merge_branch(argument.merge, target_branch=argument.dest)
                        if status_code:
                            if argument.dest:
                                logs(f"Branche {argument.merge} merge dans la branche {argument.dest}")
                            else:
                                logs(f"Branche {argument.merge} merge dans la branche {repo.get_active_branch()}")

                    else:
                        active = repo.get_active_branch()
                        for br in repo.list_branch():
                            if br==active:
                                print(f"* {br}")
                            else:
                                print(f"  {br}")
                else:
                    logs("Vous n'êtes pas dans un repo","critical")

    @impmagic.loader(
        {'module':'sys'},
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_root_project']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'repository.repo', 'submodule': ['Repo']},
        {'module':'shutil', 'submodule': ['rmtree']},
        {'module':'os.path', 'submodule': ['exists', 'isdir', 'join']}
    )
    def repo_nexus(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs repo"
        parse.set_description("Action sur le repo")
        parse.set_argument('s', longname="status", description="Afficher le statut du repo", default=False)
        parse.set_argument('l', longname="log", description="Afficher les logs du repo", default=False)
        parse.set_argument('o', longname="oneline", description="Afficher les logs sur une ligne", default=False, category="log")
        parse.set_argument('i', longname="init", description="Initialiser le repo", default=False)
        parse.set_argument('p', longname="purge", description="Supprimer le repo", default=False)
        #parse.set_parameter("ACTION", description="Nom des packages à lock")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project(''):
                git_path = join(get_root_project(), '.git')
                if exists(git_path) and isdir(git_path):
                    repo = Repo(get_root_project())

                    if argument.status:
                        repo.status()

                    elif argument.log:
                        repo.log(argument.oneline)

                    elif argument.purge:
                        try:
                            rmtree(git_path)
                            logs("Repo supprimé")
                        except Exception as err:
                            logs(f"Impossible de supprimer le repo:\n{err}", "error")

                elif argument.init:
                    repo = Repo(get_root_project(), create=True)
                    if repo:
                        logs("Repo créé")

                else:
                    logs("Vous n'êtes pas dans un repo", "critical")

    @impmagic.loader(
        {'module':'sys'},
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_root_project']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'repository.repo', 'submodule': ['Repo']},
        {'module':'os.path', 'submodule': ['exists', 'isdir', 'join']}
    )
    def reset(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs reset"
        parse.set_description("Reset un repo")
        parse.set_argument(longname="hard", description="Reset hard", default=False)
        parse.set_argument(longname="soft", description="Reset soft", default=False)
        parse.set_argument(longname="mixed", description="Reset mixed", default=False)
        parse.set_parameter("COMMIT", description="ID du commit cible")
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project(''):
                git_path = join(get_root_project(), '.git')
                if exists(git_path) and isdir(git_path):
                    if argument.hard and not argument.soft and not argument.mixed:
                        mode = "hard"
                    elif argument.soft and not argument.hard and not argument.mixed:
                        mode = "soft"
                    elif argument.mixed and not argument.hard and not argument.soft:
                        mode = "mixed"
                    else:
                        logs("Mode invalid", "error")
                        exit()

                    repo = Repo(get_root_project())
                    repo.reset(parameter[0], mode=mode)

                else:
                    logs("Vous n'êtes pas dans un repo", "critical")

    @impmagic.loader(
        {'module':'sys'},
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_root_project']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'repository.repo', 'submodule': ['Repo']},
        {'module':'os.path', 'submodule': ['exists', 'isdir', 'join', 'basename']}
    )
    def restore(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs restore"
        parse.set_description("Restaurer un fichier spécifique depuis le repo")
        parse.set_argument("d", longname="dest", description="Fichier/répertoire de destination", default=None, store="value")
        parse.set_argument("c", longname="commit", description="Spécifier l'id du commit", default="HEAD", store="value")
        parse.set_parameter("FILE", description="Fichier à restaurer")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None and len(parameter):
            if is_nexus_project(''):
                git_path = join(get_root_project(), '.git')
                if exists(git_path) and isdir(git_path):
                    repo = Repo(get_root_project())

                    for file in parameter:
                        logs(f"Restauration de {file}")

                        if argument.dest!=None and exists(argument.dest) and isdir(argument.dest):
                            dest = join(argument.dest, basename(file))
                        elif argument.dest!=None and exists(argument.dest):
                            logs(f"La destination {argument.dest} existe déjà")
                            exit()
                        elif argument.dest!=None and not exists(argument.dest):
                            dest = argument.dest
                        else:
                            dest = None

                        repo.restore(file, dest=argument.dest, commit_id=argument.commit)

                else:
                    logs("Vous n'êtes pas dans un repo", "critical")

    @impmagic.loader(
        {'module':'sys'},
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_root_project']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'repository.repo', 'submodule': ['Repo']},
        {'module':'os.path', 'submodule': ['exists', 'isdir', 'join', 'basename']}
    )
    def commit(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs commit"
        parse.set_description("Commit le travail en cours")
        parse.set_argument("m", longname="message", description="Spécifier le message de commit", default=None, store="value")
        parse.set_argument("b", longname="branch", description="Spécifier la branche", default=None, store="value")
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project(''):
                git_path = join(get_root_project(), '.git')
                if exists(git_path) and isdir(git_path):
                    repo = Repo(get_root_project())

                    if not argument.message:
                        message = input("Message de commit: ")
                    else:
                        message = argument.message

                    commit = repo.git_add_and_commit(commit_message=message, branch_name=argument.branch)
                    if commit!=None:
                        logs(f"Commit effectué: {commit}")
                else:
                    logs("Vous n'êtes pas dans un repo", "critical")

    #Affiche l'arborescence d'un commit
    @impmagic.loader(
        {'module':'sys'},
        {'module':'zpp_args'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_root_project']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'os.path', 'submodule': ['join', 'isdir']},
        {'module':'repository.repo', 'submodule': ['Repo']}
    )
    def tree(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs tree"
        parse.set_description("Affiche l'arborescence d'un commit")
        parse.set_argument("c", longname="commit", description="Spécifier l'id du commit", default="HEAD", store="value")
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project(''):
                git_path = join(get_root_project(), '.git')
                if exists(git_path) and isdir(git_path):
                    repo = Repo(get_root_project())

                    repo.tree(argument.commit)

                else:
                    logs("Vous n'êtes pas dans un repo", "critical")


    @impmagic.loader(
        {'module':'__main__'}, 
        {'module':'zpp_args'}, 
        {'module':'sys'},
        {'module':'json'},
        {'module':'brotli'},
        {'module':'hashlib'},
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'get_all_package', 'remove_pool', 'install_pool', 'upgrade_pool']}, 
        {'module':'app.display', 'submodule': ['logs', 'prompt', 'print_nxs']},  
        {'module':'app.tree', 'submodule': ['tree']},
        {'module':'structure.check', 'submodule': ['get_nexus_file', 'get_root_project', 'is_nexus_project']},
        {'module':'structure.create', 'submodule': ['create_project_environment']},
        {'module':'structure.structure', 'submodule': ['dump_project', 'load_file', 'load_project', 'tree_project', 'select_file_from_project', 'compare_snap_file']},
        {'module':'package.package', 'submodule': ['dependency_to_list', 'lock_package']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'template.toml_format', 'submodule': ['DEFAULT_TOML']},
        {'module':'os.path', 'submodule':['join', 'exists']},
        {'module':'uuid', 'submodule': ['uuid4']},
        {'module':'datetime', 'submodule': ['datetime']}
    )
    def snap(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs snap"
        parse.set_description("Sauvegarde/Restauration de l'état des dépendances")
        parse.set_argument("e", longname="env", description="Spécifier l'environnement source", store="value", default=None)
        parse.set_argument("f", longname="file", description="Spécifier le fichier snap", store="value", default="snap.json")
        parse.set_argument("i", longname="info", description="Afficher les informations d'un snap", default=False)
        parse.set_argument("d", longname="dest", description="Spécifier le répertoire de destination lors de la restauration", store="value", default=None)
        parse.set_argument(longname="full", description="Faire un snap full", default=False)
        parse.set_argument(longname="restore", description="Restaurer un snapshot", default=False)
        parse.set_argument(longname="force", description="Forcer la restauration", default=False)
        parse.set_argument(longname="compare", description="Comparer la configuration actuelle et le snap", default=False)
        parse.set_argument(longname="snapfile", description="Spécifier le fichier/répertoire à restaurer", store="value", default=None, category="restore")
        parse.set_argument(longname="only_env", description="Restaurer uniquement l'environnement", default=None, category="restore")
        parse.set_argument(longname="only_file", description="Restaurer uniquement les fichiers", default=None, category="restore")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if is_nexus_project('', True):
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
            else:
                tfile = None

            cmd = get_executable(tfile, argument.env)
            if cmd!=None:
                if argument.restore:
                    with open(argument.file) as json_file:
                        deps = json.load(json_file)

                    new = True
                    if argument.dest:
                        sp_file = join(argument.dest, "nexus.toml")
                    else:
                        if not get_root_project():
                            logs("Vous n'êtes pas dans un projet nexus. Ajouter -d pour préciser le chemin", "critical")
                            return
                        sp_file = join(get_root_project(), "nexus.toml")

                    if exists(sp_file):
                        new = False

                    if not argument.only_env:
                        if argument.only_file:
                            file_list = ['project_file']
                        else:
                            file_list = ['project_file', 'changelog', 'readme', 'license_file']
                        
                        for specific_file in file_list:
                            load_file(specific_file, deps=deps, dest=argument.dest)
                            

                    tfile_resto = TOMLnxs(get_nexus_file())
                    tfile_resto.load_doc()

                    #Création de l'environnement uniquement si c'est un nouveau fichier nexus.toml
                    if not argument.only_file:
                        if new:
                            if 'venv' in tfile_resto.doc:
                                selected_name = None
                                logs("Purge des anciens environnements")
                                for env in tfile_resto.doc['venv']:
                                    name = env
                                    env = tfile_resto.doc['venv'][env]
                                    if 'default' in env and env['default']==True:
                                        selected_name = name
                                    tfile_resto.delete_key(name, 'venv')

                                if selected_name:
                                    logs("Restauration de l'environnement par défaut")
                                    data = {}
                                    data['projectname'] = tfile_resto.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section']) 
                                    data['dependencies'] = tfile_resto.get_key('dependencies','project')
                                    data['dependencies'] = lock_package(data['dependencies'])

                                    create_project_environment(selected_name, get_root_project(), data, tfile_resto, first=True, nocheck=True)

                        else:
                            cmd = get_executable(tfile_resto, argument.env)
                            deps_env = get_all_package(cmd)

                            deps_packages = [x.lower().replace("-", "_") for x in deps['packages']]

                            to_remove = []
                            for package, version in deps_env.items():
                                if package.lower().replace("-", "_") not in deps_packages:
                                    to_remove.append(package)
                                else:
                                    package_name = None
                                    for element in deps['packages']:
                                        if element.lower().replace("-", "_")==package.lower().replace("-", "_"):
                                            package_name = element
                                            break

                                    if package_name:    
                                        if version==deps['packages'][package_name]:
                                            del deps['packages'][package_name]

                            if len(to_remove):
                                logs("Suppression des dépendances inutiles")
                                remove_pool(cmd, to_remove)

                            if len(deps['packages']):
                                to_install = {}
                                to_update = {}

                                for package, version in deps['packages'].items():
                                    if package in deps_env:
                                        to_update[package] = "=="+version
                                    else:
                                        to_install[package] = "=="+version

                                if len(to_install):
                                    logs("Installation des dépendances")
                                    to_install = dependency_to_list(to_install, force=argument.force)
                                    if len(to_install):
                                        install_pool(cmd, to_install, force=argument.force)

                                if len(to_update):
                                    logs("Mise à jour des dépendances")
                                    to_update = dependency_to_list(to_update, force=argument.force)
                                    if len(to_update):
                                        upgrade_pool(cmd, to_update, force=argument.force)

                    if len(deps['project_data']) and not argument.only_env:
                        if len(parameter):
                            project_data = {}
                            for par in parameter:
                                inject = select_file_from_project(par, deps['project_data'])
                                if inject and len(inject):
                                    project_data.update(inject)
                                else:
                                    logs(f"{par} non trouvé", "critical")
                        else:
                            project_data = deps['project_data']

                        if len(project_data):
                            load_project(project_data, join(get_root_project(), tfile_resto.get_key('name','project')))

                elif argument.info:
                    with open(argument.file) as json_file:
                        deps = json.load(json_file)

                    for element in ['name', 'date', 'commentaire', 'type', 'version projet']:
                        if element in deps:
                            print_nxs(f"{element.capitalize()}: ", nojump=True)
                            print_nxs(deps[element], color=__main__.color['yellow'])

                    if 'packages' in deps:
                        print_nxs(f"Packages: ", nojump=True)
                        print_nxs(len(deps['packages']), color=__main__.color['yellow'])

                    if 'project_data' in deps and len(deps['project_data']):
                        print_nxs(f"Content: ")
                        tree(tree_project(deps['project_data']))

                elif argument.compare:
                    if not get_root_project():
                        logs("Vous n'êtes pas dans un projet nexus. Ajouter -d pour préciser le chemin", "critical")
                        return
                    sp_file = join(get_root_project(), "nexus.toml")

                    deps_installed = get_all_package(cmd)

                    with open(argument.file) as json_file:
                        snap_content = json.load(json_file)

                    logs("Comparaison des packages")

                    for package in deps_installed:
                        if package in snap_content['packages']:
                            if snap_content['packages'][package]==deps_installed[package]:
                                logs(f"Package {package} dans la bonne version")
                            else:
                                logs(f"Package {package} mis à jour: {snap_content['packages'][package]} => {deps_installed[package]}", "warning")
                            del snap_content['packages'][package]

                        else:
                            logs(f"Package {package} nouvellement installé", "warning")

                    if len(snap_content['packages']):
                        for package in snap_content['packages']:
                            logs(f"Package {package} désinstallé", "warning")


                    logs("")
                    logs("Comparaison des fichiers du projet")

                    for element in ['nexus.toml', 'changelog', 'readme', 'license_file']:
                        if element=='nexus.toml':
                            element_config = element
                            element = 'project_file'
                        else:
                            element_config = tfile.get_key(element, 'project.metadata')

                        if element_config:
                            sp_file_path = join(get_root_project(), element_config)

                            if exists(sp_file_path):
                                with open(sp_file_path, 'rb') as f:
                                    hash_file = hashlib.sha256(f.read()).hexdigest()

                                if element in snap_content:
                                    if 'hash' in snap_content[element]:
                                        if snap_content[element]['hash']==hash_file:
                                            logs(f"Fichier {element} inchangé")
                                        else:
                                            logs(f"Fichier {element} changé", "warning")
                                    else:
                                        logs(f"Le snap ne contient pas le hash de {element}", "error")

                                else:
                                    logs(f"Fichier {element} nouvellement créé", "warning")

                    logs("")
                    logs("Comparaison du projet")

                    projectfolder = join(get_root_project(), tfile.get_key('name','project'))

                    compare_snap_file(projectfolder, snap_content['project_data'])


                else:
                    try:
                        deps = get_all_package(cmd)

                        name = prompt("Snapshot name")
                        if not len(name):
                            name = str(uuid4())

                        commentaire = prompt("Commentaire")

                        if argument.full:
                            type_snap = "full"
                        else:
                            type_snap = "partial"

                        data = {
                            "name": name,
                            "date": datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
                            "commentaire": commentaire,
                            "version projet": tfile.get_key('version','project'),
                            "type": type_snap,
                            "packages": deps
                        }

                        if argument.full:
                            logs("Récupération du projet")
                            projectfolder = join(get_root_project(), tfile.get_key('name','project'))

                            data['project_data'] = dump_project(projectfolder)

                        logs("Récupération de la configuration du projet")
                        sp_file = join(get_root_project(), "nexus.toml")

                        if exists(sp_file):
                            with open(sp_file, 'rb') as f:
                                content = f.read()
                                data['project_file'] = {
                                    'hash': hashlib.sha256(content).hexdigest(),
                                    'content': brotli.compress(content, quality=11).hex()
                                }
                        else:
                            logs("Le fichier de configuration du projet n'a pas été trouvé", "warning")


                        for specific_file in ['changelog', 'readme', 'license_file']:
                            sp_file = tfile.get_key(specific_file,'project.metadata')
                            if not (sp_file=="" or sp_file==None):
                                logs(f"Récupération du {specific_file}")
                                sp_file_path = join(get_root_project(), sp_file)

                                if exists(sp_file_path):
                                    with open(sp_file_path, 'rb') as f:
                                        content = f.read()
                                        data[specific_file] = {
                                            'name': sp_file,
                                            'hash': hashlib.sha256(content).hexdigest(),
                                            'content': brotli.compress(content, quality=11).hex()
                                        }

                        with open(argument.file, "w") as outfile:
                            json.dump(data, outfile, indent = 4)

                            logs("Snap créé", "success")

                    except Exception as err:
                        logs(f"Erreur lors de la création du snap: {err}", "critical")


    @impmagic.loader(
        {'module':'__main__'}, 
        {'module':'zpp_args'}, 
        {'module':'sys'},
        {'module':'json'},
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'get_all_package', 'remove_pool', 'install_pool', 'upgrade_pool']},
        {'module':'package.package', 'submodule': ['dependency_to_list', 'unversion_package', 'filter_update']}, 
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'structure.check', 'submodule': ['get_nexus_file', 'get_root_project']},
        {'module':'package.package', 'submodule': ['dependency_to_list']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'os.path', 'submodule':['join']}
    )
    def pip_freeze(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs list"
        parse.set_description("Lister les packages installés")
        parse.set_argument("r", longname="root", description="Package sur l'environnement root", default=False)
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", default=None)
        parse.set_argument("o", longname="outdated", description="Afficher uniquement les packages qui ont une mise à jour disponible", default=False)
        parse.set_argument("u", longname="upgradable", description="Afficher avec les mises à jour disponible", default=False)
        parameter, argument = parse.load()

        if parameter!=None:
            if argument.root:
                cmd = get_executable(None, env_name=None, logs_env=False)
            else:
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
                cmd = get_executable(tfile, env_name=argument.env, logs_env=False)
                #cmd = get_executable(tfile, env_name=None, logs_env=False)

            if cmd!=None:
                to_upgrade = {}

                if argument.outdated or argument.upgradable:
                    deps = get_all_package(cmd)

                    if deps!=None:
                        deps_temp = unversion_package(deps)
                        to_upgrade = dependency_to_list(deps_temp)

                        if argument.outdated:
                            to_upgrade = filter_update(deps, to_upgrade)
                else:
                    deps = get_all_package(cmd)

                for name, version in deps.items():
                    if name in to_upgrade and to_upgrade[name]['version']!=version:
                        print(f"{name}=={version} ({to_upgrade[name]['version']})")
                    elif not argument.outdated:
                        print(f"{name}=={version}")


    @impmagic.loader(
        {'module':'__main__'}, 
        {'module':'zpp_args'},
        {'module': 'sys_nxs.host', 'submodule': ['path_rep']},
        {'module':'os.path', 'submodule': ['join', 'expanduser', 'getsize', 'exists', 'isfile']},
        {'module':'cache', 'submodule': ['management']},
        {'module':'app.display', 'submodule': ['logs', 'bytes2human', 'print_nxs']}
    )
    def cache_nexus(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs cache"
        parse.set_description("Gestion du cache Nexus")
        parse.set_argument("l", longname="list", description="Afficher le contenu du cache", default=False)
        parse.set_argument("r", longname="remove", description="Supprimer un package du cache", default=False)
        parse.set_argument("a", longname="add", description="Ajouter un package dans le cache", default=False)
        parse.set_parameter("PACKAGE_NAME", description="Nom des packages")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if argument.list:
                data = management.list_cache()

                if len(data):
                    for package, version in data.items():
                        print_nxs(f"{package}: ", nojump=True)
                        print_nxs(', '.join(version), color=__main__.color['yellow'])
            elif argument.remove:
                for element in parameter:
                    management.remove_from_cache(element)

            elif argument.add:
                for element in parameter:
                    management.add_to_cache(element)

            else:
                data = management.list_cache()

                if data:
                    total_package = 0
                    total_version = 0

                    for pack, ver in data.items():
                        total_package +=1
                        total_version += len(ver)

                    cachefile = join(expanduser(__main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)).replace(path_rep[1], path_rep[0]), 'repo_cache.db')

                    print_nxs(f"Size: ", nojump=True)
                    print_nxs(bytes2human(getsize(cachefile)), color=__main__.color['yellow'])

                    print_nxs(f"Total Package: ", nojump=True)
                    print_nxs(total_package, color=__main__.color['yellow'])
                    
                    print_nxs(f"Total Version: ", nojump=True)
                    print_nxs(total_version, color=__main__.color['yellow'])


    @impmagic.loader(
        {'module':'pkg_resources'}, 
        {'module':'app.display', 'submodule': ['print_nxs']},  
    )
    def about(self):
        print(nexus_logo)
        print(nexus_ascii_name)

        print_nxs(f"Author: ", nojump=True)
        print_nxs("ZephyrOff", color=__main__.color['yellow'])
        
        print_nxs(f"Version: ", nojump=True)
        print_nxs(pkg_resources.get_distribution('nexus_project').version, color=__main__.color['yellow'])


    @impmagic.loader(
        {'module':'__main__'}, 
        {'module':'zpp_args'}, 
        {'module':'app.display', 'submodule': ['logs', 'prompt']},  
        {'module':'structure.check', 'submodule': ['get_nexus_file']},
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'os.path', 'submodule': ['exists', 'isfile']},
    )
    def changelog(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs changelog"
        parse.set_description("Ajouter des informations dans le changelog")
        #parse.set_argument("l", longname="list", description="Afficher le contenu du cache", default=False)
        parameter, argument = parse.load()

        if parameter!=None:
            tfile = TOMLnxs(get_nexus_file())
            tfile.load_doc()
            changelog = tfile.get_key('changelog','project.metadata')

            if (changelog=="" or changelog==None):
                changelog="changelog.md"

            if exists(changelog) and isfile(changelog):
                with open(changelog, 'r') as f:
                    content = f.read()

                content_size = len(content)

                if not content.endswith('\n'):
                    content+="\n"

                description=None
                print_nxs("Description du changement:")
                while description!="":
                    description = prompt("> ")
                    if description!="":
                        content+="- "+description+"\n"

                if len(content)!=content_size:
                    with open(changelog, 'w') as f:
                        f.write(content)

            else:
                logs(f"Fichier {changelog} introuvable", "error")


    @impmagic.loader(
        {'module':'__main__'}, 
        {'module':'zpp_args'}, 
        {'module':'app.display', 'submodule': ['logs']},  
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']},
        {'module':'env_nxs.env', 'submodule': ['get_executable', 'get_all_package']}, 
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'os.path', 'submodule': ['exists', 'isfile']}
    )
    def export(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs export"
        parse.set_description("Exporter les dépendances dans un requirement")
        parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        parse.set_argument("o", longname="out", description="Spécifier le fichier de sortie", store="value", default="requirements.txt")
        #parse.set_argument("l", longname="list", description="Afficher le contenu du cache", default=False)
        parameter, argument = parse.load()

        if parameter!=None:
            tfile = TOMLnxs(get_nexus_file())
            tfile.load_doc()
            
            env_exe = get_executable(tfile, argument.env)

            if tfile.get_key('dependencies','project')!=None:
                #Pour être équivalent du clean_name
                deps_project = {}
                for pack, pack_info in tfile.get_key('dependencies','project').items():
                    deps_project[pack.replace("-", "_")] = {"real_name": pack ,"version": pack_info}
                    #deps_project[pack.replace("-", "_").lower()] = {"real_name": pack ,"version": pack_info}

                deps = get_all_package(env_exe, clean_name=True)

                requirements = []
                for package_name, package_info in deps.items():
                    if package_name in deps_project:
                        requirements.append(f"{deps_project[package_name]['real_name']}=={package_info}")

                if len(requirements):
                    if not exists(argument.out) and not isfile(argument.out):
                        with open(argument.out, "w") as f:
                            f.write("\n".join(requirements))

                    else:
                        logs(f"Le fichier {argument.out} existe déjà", "error")
                else:
                    logs("Aucun package à mettre dans le requirements", "warning")
            else:
                logs("Aucune dépendance dans le fichier de configuration du projet", "warning")


    @impmagic.loader(
        {'module':'__main__'}, 
        {'module':'zpp_args'},
        {'module':'datetime'}, 
        {'module':'os'}, 
        {'module':'os.path', 'submodule': ['exists', 'join']},
        {'module':'app.display', 'submodule': ['logs', 'prompt']},
        {'module':'structure.license', 'submodule': ['get_license_content']},
        {'module':'structure.create', 'submodule': ['create_file']},
        {'module':'structure.check', 'submodule': ['get_root_project']},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']}, 
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
    )
    def licence(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs licence"
        parse.set_description("Générer une licence")
        parse.set_parameter("LICENCE TYPE", description="Préciser le type de licence")
        #parse.set_argument("e", longname="env", description="Spécifier l'environnement", store="value", default=None)
        #parse.set_argument("o", longname="out", description="Spécifier le fichier de sortie", store="value", default="requirements.txt")
        #parse.set_argument("l", longname="list", description="Afficher le contenu du cache", default=False)
        parameter, argument = parse.load()

        if parameter!=None:
            if len(parameter):
                license_content = get_license_content(parameter[0])
                if '[year]' in license_content:
                    year = prompt("date license", datetime.date.today().strftime("%Y"))
                if '[fullname]' in license_content:
                    if is_nexus_project('run', nolog=True) and get_nexus_file(log=False, _break=False):
                        tfile = TOMLnxs(get_nexus_file())
                        tfile.load_doc()
                        authors = tfile.get_key("authors", "project.metadata")

                        if len(authors):
                            author = prompt("author license", authors[0])
                        else:
                            author = prompt("author license")
                    else:
                        author = prompt("author license")
                license_content = license_content.replace('[year]',year).replace('[fullname]', author)

                root_project = get_root_project()
                if not root_project:
                    root_project = os.getcwd()

                license_file = join(root_project, 'LICENSE')

                if not exists(license_file):
                    create_file(license_file, license_content)
                else:
                    logs("Le fichier de licence existe déjà", "error")
            else:
                logs("Type de licence non renseigné", "critical")

    @impmagic.loader(
        {'module':'__main__'}, 
        {'module':'zpp_args'},
        {'module':'os'},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'structure.check', 'submodule': ['get_root_project']},
        {'module':'structure.check', 'submodule': ['is_nexus_project', 'get_nexus_file']}, 
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
        {'module':'template.toml_format', 'submodule': ['DEFAULT_TOML']},
    )
    def entrypoint(self):
        parse = zpp_args.parser(sys.argv[1:])
        parse.command = "nxs entrypoint"
        parse.set_description("Ajouter un v")
        parse.set_parameter("ENTRYPOINT_NAME", description="Préciser le nom de l'entrypoint")
        parse.set_parameter("MODULE_NAME", description="Préciser le nom du module")
        parse.set_parameter("FUNCTION_NAME", description="Préciser le nom de la fonction")
        parse.disable_check()
        parameter, argument = parse.load()

        if parameter!=None:
            if len(parameter):
                if is_nexus_project('run', nolog=True) and get_nexus_file(log=False, _break=False):
                    tfile = TOMLnxs(get_nexus_file())
                    tfile.load_doc()

                    projectname = tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section'])

                    if len(parameter)==1:
                        module_name = projectname
                        function_name = "main"
                    else:
                        if len(parameter)==3:
                            module_name = parameter[1]
                            function_name = parameter[2]
                        else:
                            logs("Arguments manquants", "error")
                            return

                    entry = f"{parameter[0]} = {module_name}:{function_name}"

                    os.chdir(get_root_project())

                    mod = impmagic.get(f"{module_name}.{function_name}")
                    if callable(mod):
                        try:
                            p = tfile.get_key("console_scripts","project.wheel.entry_points")
                            if not p:
                                p = []
                            p.append(entry)
                            tfile.edit_key("console_scripts", p, "project.wheel.entry_points")
                            logs(f"Entrypoint ajouté", "success")
                        
                        except Exception as err:
                            logs(f"Erreur lors du l'ajout de l'entrypoint: {err}", "error")
                    else:
                        logs("L'entrypoint n'est pas valide", "error")


    def switch(self):
        if len(sys.argv)>1:
            match sys.argv[1]:
                case "new":
                    self.new()
                case "run":
                    self.run()
                case "shell":
                    self.shell()
                case "install":
                    self.install()
                case "uninstall":
                    self.uninstall()
                case "update":
                    self.update()
                case "search":
                    self.search()
                case "info":
                    self.info()
                case "clearcode":
                    self.clearcode()
                case "analyse":
                    self.code_analysis()
                case "securiscan":
                    self.secure_analysis()
                case "init":
                    self.init()
                case "env":
                    self.env()
                case "compile":
                    self.compile()
                case "pack":
                    self.pack()
                case "version":
                    self.version()
                case "add":
                    self.add()
                case "remove":
                    self.remove()
                case "check":
                    self.check()
                case "config":
                    self.config_nexus()
                case "publish":
                    self.publish()
                case "provisioning":
                    self.provisioning()
                case "alias":
                    self.alias()
                case "sandbox":
                    self.sandbox()
                case "test":
                    self.test()
                case "measure":
                    self.measure()
                case "backup":
                    self.backup()
                case "lock":
                    self.lock()
                case "project":
                    self.project()
                case "branch":
                    self.branch()
                case "repo":
                    self.repo_nexus()
                case "reset":
                    self.reset()
                case "restore":
                    self.restore()
                case "commit":
                    self.commit()
                case "tree":
                    self.tree()
                case "snap":
                    self.snap()
                case "list":
                    self.pip_freeze()
                case "cache":
                    self.cache_nexus()
                case "about":
                    self.about()
                case "changelog":
                    self.changelog()
                case "export":
                    self.export()
                case "licence":
                    self.licence()
                case "entrypoint":
                    self.entrypoint()
                case "template":
                    self.template()
                case _:
                    self.help()
        else:
            self.help()

def handler_signal(signal_num, frame):
    atexit._run_exitfuncs()

def main():
    atexit.register(clear_nexus)
    signal.signal(signal.SIGINT, handler_signal)

    __main__.nxs = Nexus()
    __main__.nxs.switch()


#6545

#METTRE A JOUR LA DOC RETYPE
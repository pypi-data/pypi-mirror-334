import __main__
import impmagic


#Création du context
class Context:
    @impmagic.loader(
        {'module':'sys_nxs.host', 'submodule': ['path_rep']},
        {'module':'os.path', 'submodule': ['dirname']},
        {'module': 'sys'}
    )
    def __init__(self, virtdir, virtname = None, prompt=None):
        self.env_dir = virtdir
        if virtname==None:
            name = virtdir.split(path_rep[0])
            self.env_name = name[len(name)-1]
        else:
            self.env_name = virtname

        if prompt!=None:
            self.prompt = f'({prompt}) '
        else:
            self.prompt = f'({self.env_name}) '

        self.executable = sys.executable
        self.python_dir = dirname(sys.executable)
        self.python_exe = sys.executable.replace(self.python_dir,"").replace(path_rep[0],"")
        if sys.platform == 'win32':
            self.bin_name = 'Scripts'
            self.lib_path = virtdir + path_rep[0] +'Lib'
            self.inc_path = virtdir + path_rep[0] +'Include'
        else:
            self.bin_name = 'bin'
            self.lib_path = virtdir + path_rep[0] +'lib'
            self.inc_path = virtdir + path_rep[0] +'include'
        self.bin_path = virtdir + path_rep[0] +self.bin_name
        self.env_exe = self.bin_path + path_rep[0] + self.python_exe
        self.env_exec_cmd = self.env_exe
        self.cfg_path = virtdir + path_rep[0] + 'pyvenv.cfg'

@impmagic.loader(
    {'module':'os.path', 'submodule': ['exists','isfile','isdir']}
)
def is_valid_envdir(envdir):
    context = Context(envdir)

    for directory in [context.lib_path,context.bin_path]:
        if not exists(directory) or not isdir(directory):
            return None

    for file in [context.env_exe,context.cfg_path]:
        if not exists(file) or not isfile(file):
            return None

    return context
    


#Récupérer le chemin de l'exécutable (root ou de l'environnement default)
@impmagic.loader(
    {'module':'sys'},
    {'module':'os.path', 'submodule': ['join', 'exists', 'isfile', 'isabs']},
    {'module':'app.display', 'submodule': ['logs']},
    {'module': 'sys_nxs.host', 'submodule': ['path_rep']},
    {'module':'structure.check', 'submodule': ['get_root_project']}
)
def get_executable(tfile=None, env_name=None, root=True, logs_env=True):
    if tfile==None:
        return sys.executable

    env_exe=None
    if 'venv' in tfile.doc:
        for env in tfile.doc['venv']:
            name = env
            env = tfile.doc['venv'][env]
            #Prend le default si aucun env est spécifié
            if env_name==None and 'default' in env and env['default']==True:
                env_exe = env['env_exe']
                break
            elif env_name!=None and name==env_name:
                env_exe = env['env_exe']
                break

    if env_exe!=None:
        if logs_env:
            logs("Run in env ")

        if isabs(env_exe):
            executable = env_exe.replace(path_rep[1], path_rep[0])
        else:
            executable = join(get_root_project(), env_exe).replace(path_rep[1], path_rep[0])

        if exists(executable) and isfile(executable):
            return executable
        else:
            if logs_env and env_name==None:
                logs(f"Environnement {name} introuvable", "error")
            elif logs_env and env_name!=None:
                logs(f"Environnement {env_name} introuvable", "error")
            return
    elif env_name!=None and env_exe==None:
        if logs_env:
            logs(f"Environnement {env_name} introuvable", "error")
        return
    elif env_exe==None and root==True:
        if logs_env:
            logs("Run in main python")
        return sys.executable
    else:
        return

#Récupérer les informations de l'environnement (root ou de l'environnement default)
def get_env(tfile, env_name=None, root=True, logs_env=True):
    env_exe=None
    if 'venv' in tfile.doc:
        for env in tfile.doc['venv']:
            name = env
            env = tfile.doc['venv'][env]
            #Prend le default si aucun env est spécifié
            if env_name==None and 'default' in env and env['default']==True:
                env_exe = env
                break
            elif env_name!=None and name==env_name:
                env_exe = env
                break

    if env_exe!=None:
        return env
    elif env_exe==None and root==True:
        return None
    else:
        return None


#Check si le package est déjà installé
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'re', 'submodule': ['compile']},
    {'module':'sys_nxs.host', 'submodule': ['path_rep']},
    {'module':'template.regex', 'submodule': ['dependencies']}
)
def get_package(env_exe, namemodule):
    env_exe = env_exe.replace(path_rep[1], path_rep[0])

    reg = compile(dependencies)
    module = reg.match(namemodule)
    namemodule = module.group(1)
    namemodule = namemodule.lower().replace("-","_")
    #namemodule = namemodule.replace("-","_")

    #Vérifie si le retour commande pip freeze existe déjà (pour éviter de l'appeler plusieurs fois)
    if not hasattr(__main__.nxs, 'already_installed'):
        #cmd = [env_exe, '-c', 'from pip._internal.operations import freeze;print("\\n".join([ package for package in freeze.freeze()]));']
        #cmd = [env_exe, '-c', 'from pkg_resources import working_set;print("\\n".join([package.project_name + "==" + package.version for package in working_set]))']
        cmd = [env_exe, '-m', 'pip', 'freeze']
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        __main__.nxs.already_installed = stdout
    else:
        stdout = __main__.nxs.already_installed

    for pack in stdout.decode().split("\r\n"):
        if pack!="":
            pack = pack.lower()
            module_installed = reg.match(pack.replace("-","_"))
            if module_installed!=None and namemodule==module_installed.group(1):
                return module_installed.group(2)
    return False


#Retourne la liste des packages installés
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'re', 'submodule': ['compile']},
    {'module':'sys_nxs.host', 'submodule': ['path_rep']},
    {'module':'template.regex', 'submodule': ['dependencies']}
)
def get_all_package(env_exe, refresh=False, clean_name=False):
    env_exe = env_exe.replace(path_rep[1], path_rep[0])
    stdout = []
    #Vérifie si le retour commande pip freeze existe déjà (pour éviter de l'appeler plusieurs fois)
    if refresh or not hasattr(__main__.nxs, 'already_installed'):
        cmd = [env_exe, '-m', 'pip', 'freeze']
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        __main__.nxs.already_installed = stdout
    else:
        stdout = __main__.nxs.already_installed
    
    stdout = stdout.decode('utf-8').split("\r\n")
    result = {}

    for pack in stdout:
        if len(pack):
            pack = pack.split("==")
            if len(pack)>1:
                if clean_name:
                    #result[pack[0].replace("-", "_").lower()] = pack[1]
                    result[pack[0].replace("-", "_")] = pack[1]
                else:
                    result[pack[0]] = pack[1]

    return result
    

#Récupérer la version de pip installé
@impmagic.loader(
    {'module':'subprocess'}
)
def get_pip_version(env_exe):
    cmd = [env_exe, '-m', 'pip', '--version']
    proc = subprocess.run(cmd, stdout=subprocess.PIPE)
    version = proc.stdout.decode().strip().split()[1]
    return version

#Installe la dernière version de pip si nécessaire
@impmagic.loader(
    {'module':'app.display', 'submodule': ['logs']},
    {'module':'package', 'submodule': ['package']}
)
def init_pip(env_exe):
    latest_pip = package.latest_version('pip')
    if latest_pip!=None:
        version_pip = get_pip_version(env_exe)
        if version_pip!=None:
            if not package.compare_version(latest_pip, "==", version_pip):
                logs("Nouvelle version de pip détectée", "warning")
                logs("Mise à jour de pip")
                upgrade_module(env_exe, "pip", force=True)
        else:
            logs("Pip n'est pas installé", "critical")
    else:
        logs("Impossible de trouver la version de pip", "critical")

#Parse des arguments envoyés
def arg_parse(string):
        array = []

        if len(string)>=1:
            arg = ""
            lock = None
            if isinstance(string, list):
                string = " ".join(string)
            for i,caracter in enumerate(string):
                if (caracter=="'" or caracter=='"') and (lock==None or caracter==lock):
                    if lock==None:
                        lock=caracter
                    else:
                        array.append(arg)
                        arg=""
                        lock=None
                else:
                    if caracter==" " and lock!=None:
                        arg+=caracter
                    elif caracter==" " and len(arg)>=1 and lock==None:
                        array.append(arg)
                        arg=""
                    elif caracter!=" ":
                        arg+=caracter
                        if i==len(string)-1:
                            array.append(arg)
                            arg=""
        return array


#Appel d'une commande dans un environnement
@impmagic.loader(
    {'module':'subprocess'},
    {'module': 'time', 'submodule': ['perf_counter']},
    {'module': 'datetime', 'submodule': ['timedelta', 'time']},
)
def command_shell(env_exe, command, args=None, timer=False):
    if isinstance(command, list):
        if command[0]=="python":
            command.pop(0)

        cmd = [env_exe] + command
    else:
        if command.startswith("python "):
            cmd = [env_exe, command.replace("python ","")]
        else:
            cmd = [env_exe, '-c', command]

    if args!=None and len(args)>0:
        if isinstance(args, str):
            cmd = cmd+arg_parse(args)
        if isinstance(args, list):
            cmd = cmd+args
    
    if timer:
        proc = subprocess.Popen(cmd, shell=True)
        
        st = perf_counter()
        proc.communicate()

        et = perf_counter()
        duree = timedelta(seconds=(et - st))
        print(f" Days          : {duree.days}\n Hours        : {duree.seconds//3600}\n Minutes      : {duree.seconds%3600//60}\n Seconds      : {duree.seconds%60}\n Milliseconds : {duree.microseconds//1000}\n Ticks        : {duree.microseconds*10}")
    else:
        proc = subprocess.Popen(cmd, shell=True)
        proc.communicate()
    '''    
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = proc.stdout.readline().decode("utf-8").strip()
        if output == "":
            break
        logs(output)

    for output in proc.stderr.readlines():
        logs(output.decode("utf-8").strip(), "error")
    '''

#Récupérer la version de python
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'sys_nxs.host', 'submodule': ['path_rep']}
)
def get_py_version(env_exe):
    cmd = [env_exe.replace(path_rep[1], path_rep[0]), '-c', 'import platform; print(platform.python_version())']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if len(stdout)!=0:
        return stdout.decode().rstrip()
    else:
        return 0

#Récupérer le sys.path de python
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'sys_nxs.host', 'submodule': ['path_rep']}
)
def get_py_syspath(env_exe):
    cmd = [env_exe.replace(path_rep[1], path_rep[0]), '-c', 'import sys; print ("\\n".join(sys.path));']
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if len(stdout)!=0:
        lines = stdout.decode('utf-8').splitlines()
        return list(filter(bool, lines))
    else:
        return []


#Vérifie si un module est installé
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'chardet'},
    {'module':'app.display', 'submodule': ['logs']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def installed_module(env_exe, namemodule, details=None, proxy=None, install=False):
    if proxy==None:
        proxy = __main__.nxs.conf.load(val='proxy', section='',default=default_conf.proxy)
        if proxy=="":
            proxy=None

    if namemodule!="pip" and namemodule!="setuptools":
        find = get_package(env_exe, namemodule)

        if not find:
            proc = subprocess.Popen([env_exe, '-c', f'"import pkg_resources; pkg_resources.get_distribution(\'{namemodule}\').version"'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            if not len(stderr) and len(stdout):
                return True

        if find!=False:
            find = find.replace("==","")
            if not details or find==details['version']:
                #logs(f"Module {namemodule} déjà installé dans la bonne version", "warning")
                return True
            else:
                if find in details['compatible']:
                    #logs(f"Module {namemodule} déjà installé dans une version compatible ({find})", "warning")
                    return True
                else:
                    logs(f"Module {namemodule} installé dans une version non compatible ({find})", "error")
                    if install==True:
                        logs("Mise à jour forcée du module", "warning")
                        res = upgrade_module(env_exe, namemodule, version=details['version'],force=True)
                        return res
                    else:
                        return False

    if install==True:
        logs(f"Installation du module {namemodule}")
        if details!=None:
            cmd = [env_exe, '-m', 'pip', 'install', namemodule+"=="+details['version']]
        else:
            cmd = [env_exe, '-m', 'pip', 'install', namemodule]
        if proxy!=None:
            cmd.append('--proxy='+proxy)

        full_log = __main__.nxs.conf.load(val='logs.full', section='',default=default_conf.logs_full)
        
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            output = proc.stdout.readline().decode("utf-8").strip()
            if output == "":
                break
            if full_log:
                logs(output)


        #Pour éviter les erreurs sur un pip pas à jour
        d_error = False
        stderrr = proc.stderr.read()
        if stderrr!=None:
            if chardet.detect(stderrr)['encoding']!=None and "A new release of pip available" not in stderrr.decode(chardet.detect(stderrr)['encoding']).strip():
                proc.stderr.seek(0)
                for output in proc.stderr.readlines():
                    if len(output)>0 and d_error==False:
                        logs(f"ERREUR: Module {namemodule} non installé\nMessage d'erreur: {output.decode()}", "error")
                        d_error=True

                    if full_log:
                        logs(output.decode("utf-8").strip(), "error")

        if d_error==True:
            return False
        else:
            return True
    else:
        return False

#Installation de package en multithread si enable
@impmagic.loader(
    {'module':'concurrent.futures', 'as': 'worker'},
    {'module':'sys_nxs.host', 'submodule': ['path_rep']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def install_pool(env_exe, installmodule, proxy=None, force=False):
    env_exe = env_exe.replace(path_rep[1], path_rep[0])
    if __main__.nxs.conf.load(val='threading', section='',default=default_conf.threading):
        threads = []

        with worker.ThreadPoolExecutor(max_workers=__main__.nxs.threadmax) as executor:
            futures = []
            for package in installmodule:
                details = None
                if isinstance(installmodule, dict):
                    details = installmodule[package]

                futures.append(executor.submit(install_module, env_exe, package, details, proxy, force))
            
            worker.wait(futures)

    else:
        for package in installmodule:
            install_module(env_exe,package, details=installmodule[package], proxy=proxy, force=force)


#Installation d'un module dans un environnement
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'chardet'},
    {'module':'app.display', 'submodule': ['logs']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def install_module(env_exe, namemodule, details=None, proxy=None, force=False):
    if proxy==None:
        proxy = __main__.nxs.conf.load(val='proxy', section='',default=default_conf.proxy)
        if proxy=="":
            proxy=None

    if namemodule!="pip" and namemodule!="setuptools":
        find = get_package(env_exe, namemodule)

        if find!=False:
            find = find.replace("==","")
            if details:
                if find==details['version']:
                    logs(f"Module {namemodule} déjà installé dans la bonne version", "warning")
                else:
                    if find in details['compatible']:
                        logs(f"Module {namemodule} déjà installé dans une version compatible ({find})", "warning")
                    else:
                        logs(f"Module {namemodule} installé dans une version non compatible ({find})", "error")

                    if force==True:
                        logs("Mise à jour forcée du module", "warning")
                        upgrade_module(env_exe, namemodule, version=details['version'],force=True)
            else:
                logs(f"Module {namemodule} déjà installé", "warning")

            return
    
    logs(f"Installation du module {namemodule}")
    if details!=None:
        cmd = [env_exe, '-m', 'pip', 'install', namemodule+"=="+details['version']]
    else:
        cmd = [env_exe, '-m', 'pip', 'install', namemodule]
    if proxy!=None:
        cmd.append('--proxy='+proxy)
    """
    cache_dir = pipcache("pip")
    if cache_dir!=None and os.path.exists(cache_dir):
        cmd.append('--cache-dir='+cache_dir)
    """

    full_log = __main__.nxs.conf.load(val='logs.full', section='',default=default_conf.logs_full)
    
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = proc.stdout.readline().decode("utf-8").strip()
        if output == "":
            break
        if full_log:
            logs(output)

    d_error = False
    #Pour éviter les erreurs sur un pip pas à jour
    stderrr = proc.stderr.read()
    if stderrr!=None:
        if chardet.detect(stderrr)['encoding']!=None and "A new release of pip available" not in stderrr.decode(chardet.detect(stderrr)['encoding']).strip():
            proc.stderr.seek(0)
            for output in proc.stderr.readlines():
                if len(output)>0 and d_error==False:
                    logs(f"ERREUR: Module {namemodule} non installé\nMessage d'erreur: {output.decode()}", "error")
                    d_error=True

                if full_log:
                    logs(output.decode("utf-8").strip(), "error")


#Suppression d'un module en multithread si enable
@impmagic.loader(
    {'module':'concurrent.futures', 'as': 'worker'},
    {'module':'sys_nxs.host', 'submodule': ['path_rep']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def remove_pool(env_exe,namemodule):
    env_exe = env_exe.replace(path_rep[1], path_rep[0])
    if __main__.nxs.conf.load(val='threading', section='',default=default_conf.threading):
        threads = []

        with worker.ThreadPoolExecutor(max_workers=__main__.nxs.threadmax) as executor:
            futures = []
            for package in namemodule:
                futures.append(executor.submit(remove_module, env_exe, package))
            worker.wait(futures)

    else:
        for package in namemodule:
            remove_module(env_exe,package)

#Suppression d'un module dans un environnement
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'app.display', 'submodule': ['logs']}
)
def remove_module(env_exe,namemodule):
    if get_package(env_exe, namemodule)==False:
        logs(f"Module {namemodule} non installé", "warning")
        return
    
    cmd = [env_exe, '-m', 'pip', 'uninstall', '-y', namemodule]
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if len(stdout)!=0:
        logs(f"Module {namemodule} supprimé")
    else:
        logs(f"ERREUR: Module {namemodule} non supprimé\nMessage d'erreur: {stderr.decode()}", "error")


#Installation de package en multithread si enable
@impmagic.loader(
    {'module':'concurrent.futures', 'as': 'worker'},
    {'module':'sys_nxs.host', 'submodule': ['path_rep']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def upgrade_pool(env_exe, installmodule, proxy=None, force=False):
    env_exe = env_exe.replace(path_rep[1], path_rep[0])
    if __main__.nxs.conf.load(val='threading', section='',default=default_conf.threading):
        threads = []

        with worker.ThreadPoolExecutor(max_workers=__main__.nxs.threadmax) as executor:
            futures = []
            for package in installmodule:
                details = None
                if isinstance(installmodule, dict):
                    details = installmodule[package]
                    futures.append(executor.submit(upgrade_module, env_exe, package, details['version'], proxy, force))

            worker.wait(futures)

    else:
        for package in installmodule:
            upgrade_module(env_exe,package, installmodule[package]['version'], proxy=proxy, force=force)
    
#Upgrade d'un module dans un environnement
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'chardet'},
    {'module':'app.display', 'submodule': ['logs']},
    {'module':'sys_nxs.host', 'submodule': ['path_rep']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def upgrade_module(env_exe, namemodule, version=None, proxy=None, force=False, reinstall=False):
    logs(f"Mise à jour du module {namemodule}")

    env_exe = env_exe.replace(path_rep[1], path_rep[0])

    if version!=None:
        for_install = namemodule+"=="+version
    else:
        for_install = namemodule

    find = get_package(env_exe, namemodule)
    if find!=False:
        find = find.replace("==","")
        if version!=None and find==version:
            logs(f"Module {namemodule} déjà installé dans la bonne version")
            return True

    if proxy==None:
        proxy = __main__.nxs.conf.load(val='proxy', section='',default=default_conf.proxy)
        if proxy=="":
            proxy=None

    if namemodule!="pip" and namemodule!="setuptools":
        if get_package(env_exe, namemodule)==False:
            logs(f"Module {namemodule} non installé", "warning")
            return

    cmd = [env_exe, '-m', 'pip', 'install', for_install, '--upgrade']
    if proxy!=None:
        cmd.append('--proxy='+proxy)

    if force==True:
        cmd.append('--force')
    
    if reinstall==True:
        cmd.append('--force-reinstall')

    full_log = __main__.nxs.conf.load(val='logs.full', section='',default=default_conf.logs_full)

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = proc.stdout.readline().decode("utf-8").strip()
        if output == "":
            break
        if full_log:
            logs(output)

    d_error = False
    #Pour éviter les erreurs sur un pip pas à jour
    stderrr = proc.stderr.read()
    if stderrr!=None:
        if chardet.detect(stderrr)['encoding']!=None and "A new release of pip available" not in stderrr.decode(chardet.detect(stderrr)['encoding']).strip():
            proc.stderr.seek(0)
            for output in proc.stderr.readlines():
                if len(output)>0 and d_error==False:
                    logs(f"ERREUR: Module {namemodule} non mis à jour\nMessage d'erreur: {proc.stderr.readlines()}", "error")
                    d_error=True

                if full_log:
                    logs(output.decode("utf-8").strip(), "error")

    if d_error==False:
        logs(f"Module {namemodule} mis à jour")
        return True

    return False

#Créer un environnement dans le cache
@impmagic.loader(
    {'module':'__main__'},
    {'module':'uuid', 'submodule': ['uuid1']},
    {'module': 'template', 'submodule': ['default_conf']},
    {'module':'os.path', 'submodule': ['expanduser','join']}
)
def create_temp_env(installmodule=None, upgradepip=True):
    name = str(uuid1())
    cachedir = join(expanduser(__main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)), name)
    __main__.ToDoClear.append(cachedir)
    create_environment(cachedir, name=name, installmodule=None, upgradepip=upgradepip, prompt="temp-"+name)

    return name, cachedir


#Création d'un environnement
@impmagic.loader(
    {'module':'sys_nxs.host', 'submodule': ['path_rep']},
    {'module':'zpp_config', 'submodule': ['Config']},
    {'module':'os.path', 'submodule': ['exists', 'isdir']},
    {'module':'os'},
    {'module':'virtualenv'},
    {'module':'app.display', 'submodule': ['logs']},
    {'module':'sys_nxs.host', 'submodule': ['path_reg']},
    {'module': 'template', 'submodule': ['default_conf']},
    {'module':'sys'}
)
def create_environment(virtdir, name=None, installmodule=None, clear=False, upgradepip=True, symlinks=False, sitepackages=False, proxy=None, prompt=None):
    if proxy==None:
        proxy = __main__.nxs.conf.load(val='proxy', section='',default=default_conf.proxy)
        if proxy=="":
            proxy=None
    if name!=None:
        logs(f"Environnement {name}")
    else:
        logs(f"Environnement {virtdir}")

    logs("Création du contexte")
    virtdir = path_reg(virtdir)
    context = Context(virtdir, name, prompt=prompt)

    args = []
    args.append("--no-download")
    args.append("--no-periodic-update")
    #args.append("--no-setuptools")
    #args.append("--no-pip")
    #args.append("--no-wheel")

    if not symlinks:
        args.append("--always-copy")
    
    if sitepackages:
        args.append("--system-site-packages")

    if clear:
        args.append("--clear")

    if prompt is not None:
        args.extend(["--prompt", prompt])

    #args.append("--python")
    #args.append("PATHPYTHON")
    args.append(context.env_dir)

    if clear==False and exists(virtdir) and isdir(virtdir) and len(os.listdir(virtdir))!=0:
        logs("Le dossier n'est pas vide", "warning")
        sys.exit()
    
    logs("Création de l'environnement")
    try:
        virtualenv.cli_run(args)
    except Exception as err:
        logs(err, "error")

    if not exists(context.bin_path) or not exists(context.lib_path):
        logs("ERREUR: Le dossier de l'environnement n'a pas été créé", "error")
        sys.exit()
    
    if not exists(context.cfg_path):
        logs("ERREUR: Le fichier de config n'a pas été créé", "error")
        sys.exit()
    
    if not exists(context.env_exe):
        logs("ERREUR: L'exécutable n'a pas été copié", "error")
        sys.exit()
    
    if not exists(context.bin_path+path_rep[0]+"activate"):
        logs("ERREUR: Les scripts d'activation n'ont pas été créé", "error")
        sys.exit()

    if os.name=='nt':
        pipname = 'pip.exe'
    else:
        pipname = 'pip'
    if not exists(context.bin_path+path_rep[0]+pipname):
        logs("ERREUR: Pip n'a pas été installé", "error")
        sys.exit()

    if upgradepip:
        logs("Recherche de mise à jour")
        upgrade_module(context.env_exe,"pip", proxy=proxy)
        upgrade_module(context.env_exe,"setuptools", proxy=proxy)

    if installmodule!=None:
        if isinstance(installmodule, str):
            installmodule = installmodule.split(",")

        install_pool(context.env_exe, installmodule, None, proxy)

    logs("Environnement créé")

    venv_data = {}
    venv_data['env_dir'] = context.env_dir 
    venv_data['env_name'] = context.env_name 
    venv_data['env_exe'] = context.env_exe
    venv_data['bin_path'] = context.bin_path
    c = Config(context.cfg_path)
    data = c.load(val='version', section='',default="N.A")
    venv_data['version'] = data

    return venv_data

#Suppression d'un environnement
@impmagic.loader(
    {'module':'os.path', 'submodule': ['exists']},
    {'module':'shutil', 'submodule': ['rmtree']},
    {'module':'app.display', 'submodule': ['logs']}
)
def remove_environment(virtdir):
    if exists(virtdir):
        logs("Suppresion d'un dossier d'environnement")
        try:
            rmtree(virtdir)
        except PermissionError:
            logs("ERREUR: Autorisation refusée pour supprimer le dossier d'environnement", "error")
        except Exception as err:
            logs(f"Error: {err}", "error")
    else:
        logs("Le dossier d'environnement n'existe pas", "error")

#Ouvrir l'environnement
@impmagic.loader(
    {'module':'sys_nxs.host', 'submodule': ['path_rep']},
    {'module':'os.path', 'submodule': ['exists', 'isdir']},
    {'module':'os', 'submodule': ['name', 'environ']},
    {'module':'subprocess'},
    {'module':'pexpect'},
    {'module':'app.display', 'submodule': ['logs']},
    {'module':'sys_nxs.host', 'submodule': ['path_reg', 'path_rep', 'get_os']},
    {'module':'sys'}
)
def open_environment(virtdir, projectfolder="", shell=False):
    context = Context(path_reg(virtdir))

    if exists(context.bin_path) and isdir(context.bin_path):
        if shell:
            cmd = context.env_exe
        else:
            OSType = get_os()
            if OSType=='cmd' or OSType=='cmd.exe':
                activate_file='activate.bat'
                if exists(context.bin_path+path_rep[0]+activate_file):
                    cmd = ['cmd', '/k']
                    target = ""
                    ### Add alias CMD
                    if projectfolder!="":
                        target+=f"doskey cdproject=cd {projectfolder} & "
                    else:
                        target+=f"doskey cdproject=echo "+"Le dossier de projet n'est pas configuré"+" & "
                    target+=f"doskey shellenv={context.env_exe} & "
                    target+=f'doskey help=echo "'+"cdproject  se déplacer dans le dossier du projet`nshellenv   accéder au shell python`ndeactivate    sortir de l'environnement"+'" & '
                    ### END Add alias
                    target+="pushd "+context.bin_path.replace(path_rep[1], path_rep[0])+" & .\\"+activate_file+" & popd"
                    cmd.append(target)
                else:
                    logs("ERREUR: Le script d'activation n'existe pas", "error")
                    sys.exit()

            elif OSType=='powershell.exe' or name=='nt':
                activate_file='activate.ps1'
                if exists(context.bin_path+path_rep[0]+activate_file):
                    cmd = ['powershell', '-NoExit', '-Command']
                    target = ""
                    ### Add alias PS1
                    """
                    """
                    if projectfolder!="":
                        target+='function cdproject{cd "'+projectfolder+'"}; '
                    else:
                        target+='function cdproject{Write-Host '+"Le dossier de projet n`'est pas configuré"+'}; '
                    target+='function shellenv{'+context.env_exe+'}; '
                    target+='function help{Write-Host "'+"cdproject  se déplacer dans le dossier du projet`nshellenv   accéder au shell python`ndeactivate    sortir de l'environnement"+'"}; '
                    ### END Add alias
                    target+='. "'+context.bin_path+path_rep[0]+activate_file+'"'

                    cmd.append(target)
                else:
                    logs("ERREUR: Le script d'activation n'existe pas", "error")
                    sys.exit()
            
            else:
                activate_file='activate'
                if exists(context.bin_path+path_rep[0]+activate_file):

                    cmd = []
                    target = ""
                    ### Add alias Linux
                    """
                    if projectfolder!="":
                        target+=f"alias cdproject=\'cd {projectfolder}\' && "
                    else:
                        target+="alias cdproject=\'echo "+"Le dossier de projet n'est pas configuré"+"\' && "
                    target+=f"alias shellenv='{context.env_exe}' && "
                    target+=f'alias help=\'echo -e "'+"cdproject  se déplacer dans le dossier du projet\nshellenv   accéder au shell python\ndeactivate    sortir de l'environnement"+'"\' && '
                    ### END alias Linux
                    target+=". "+context.bin_path+path_rep[0]+activate_file
                    cmd.append(target)
                    """

                    target=". "+context.bin_path+path_rep[0]+activate_file

                    shell = environ.get('SHELL')
                    interact = pexpect.spawn(shell, ['-i'])
                    interact.sendline(target)
                    interact.interact(escape_character=None)

                    interact.close()
                    return
                else:
                    logs("ERREUR: Le script d'activation n'existe pas", "error")
                    sys.exit()

        subprocess.call(cmd, shell=True)
    else:
        logs("ERREUR: Dossier d'environnement introuvable", "error")


@impmagic.loader(
    {'module':'__main__'},
    {'module':'shutil'},
    {'module':'app.display', 'submodule': ['logs']}, 
    {'module':'structure.check', 'submodule': ['get_root_project']}, 
    {'module':'template.toml_format', 'submodule': ['DEFAULT_TOML']},
    {'module': 'template', 'submodule': ['default_conf']},
    {'module': 'os', 'submodule': ['chdir']},
    {'module': 'sys_nxs.host', 'submodule': ['path_rep']},
    {'module':'os.path', 'submodule': ['exists', 'isabs', 'join', 'split', 'expanduser', 'dirname']}
)
def clone_environment(env, dest_env, tfile, sandbox=False):
    if exists(join(get_root_project(), env['env_exe'])):
        chdir(get_root_project())

        if exists(dest_env):
            logs("Le répertoire de destination existe déjà", "warning")
            return False, {}
        env_folder = __main__.nxs.conf.load(val='virtualenvs.foldername', section='',default=default_conf.virtualenvs_foldername)
        cachedir = expanduser(__main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)).replace(path_rep[1], path_rep[0])
        env_dir = split(env['env_dir'])[1]
        logs(f"Clonage en cours de l'environnement {env['env_name']}")

        environment_dir = env['env_dir'].replace(path_rep[1], path_rep[0])

        if isabs(environment_dir) and environment_dir.startswith(cachedir):
            appname = tfile.get_key(DEFAULT_TOML['projectname']['name'],DEFAULT_TOML['projectname']['section'])

            parent = dirname(join(cachedir,env_folder,appname,env_dir))
            source = join(cachedir,env_folder,appname,env_dir)
        else:
            parent = dirname(environment_dir)
            source = environment_dir

        dest = join(parent, dest_env)
        shutil.copytree(source, dest)

        venv_data = {}
        venv_data['env_dir'] = dest.replace(path_rep[0], path_rep[1])
        venv_data['env_name'] = dest_env
        venv_data['env_exe'] = env['env_exe'].replace(env['env_dir'], dest).replace(path_rep[0], path_rep[1])
        venv_data['bin_path'] = env['bin_path'].replace(env['env_dir'], dest).replace(path_rep[0], path_rep[1])
        venv_data['version'] = env['version']

        
        fixup_scripts(source, dest, get_py_version(env['env_exe']), venv_data['bin_path'])
        fix_symlink_if_necessary(source, dest)

        #Reinstallation de pip pour le link sur le nouvel environnement
        pipversion = get_pip_version(venv_data['env_exe'])
        upgrade_module(venv_data['env_exe'], 'pip', version=pipversion, reinstall=True)


        logs("Environnement cloné")
        return True, venv_data
    else:
        logs("L'environnement est introuvable", "critical")

    return False, {}

#Fonction récursive pour faire la liste des packages installés dans l'env en fonction des dépendances du fichier toml
#ATTENTION NE PREND EN COMPTE QUE LES PATH DE PROFONDEUR 1
@impmagic.loader(
    {'module':'os'}
)
def get_package_installed(cmd, deps, lockable, path=None):
    if path!=None and path not in lockable:
        lockable[path]={}

    for package in deps:
        if package!="windows" and package!="linux":
            a = get_package(cmd, package)
            if a==False:
                logs(f"{package} non installé", "warning")
            else:
                version = a.replace("==","")

                if path!=None:
                    lockable[path][package]=version
                else:
                    lockable[package]=version

        elif package=="windows" and os.name=="nt":
            lockable = get_package_installed(cmd, deps['windows'], lockable, "windows")
        elif package=="linux" and os.name!="nt": 
            lockable = get_package_installed(cmd, deps['linux'], lockable, "linux")
    return lockable


#Filtrer le dictionnaire de dépendances à partir d'une liste 
@impmagic.loader(
    {'module':'tomlkit'}
)
def filter_deps(filtre, deps):
    for package, value in deps.copy().items():
        if package=='windows' or package=='linux':
            res = filter_deps(filtre, value)
            if len(res):
                deps[package] = res
            
            if not len(deps[package]):
                del deps[package]
        elif package not in filtre:
            del deps[package]

    return deps

@impmagic.loader(
    {'module':'app.display', 'submodule': ['logs']}
)
def change_default(tfile, env_name):
    last = None
    for env in tfile.doc['venv']:
        name = env
        env = tfile.doc['venv'][env]
        if 'default' in env and env['default']==True:
            last = name

    for env in tfile.doc['venv']:
        name = env
        env = tfile.doc['venv'][env]
        if env_name==name:
            tfile.edit_key('default', True, "venv."+name)
            if last!=None:
                tfile.edit_key('default', False, "venv."+last)
            logs("Environnement par défaut modifié")


## Fixing function from virtualenv-clone
## https://github.com/edwardgeorge/virtualenv-clone
def _dirmatch(path, matchwith):
    matchlen = len(matchwith)
    if (path.startswith(matchwith)
        and path[matchlen:matchlen + 1] in [os.sep, '']):
        return True
    return False

@impmagic.loader(
    {'module':'itertools'},
    {'module':'os', 'submodule': ['walk', 'remove', 'symlink']},
    {'module':'os.path', 'submodule': ['join', 'islink', 'realpath']}
)
def fix_symlink_if_necessary(src_dir, dst_dir):
    for dirpath, dirnames, filenames in walk(dst_dir):
        for a_file in itertools.chain(filenames, dirnames):
            full_file_path = join(dirpath, a_file)
            if islink(full_file_path):
                target = realpath(full_file_path)
                if target.startswith(src_dir):
                    new_target = target.replace(src_dir, dst_dir)
                    remove(full_file_path)
                    symlink(new_target, full_file_path)


@impmagic.loader(
    {'module':'itertools'},
    {'module':'re'},
    {'module':'os', 'submodule': ['walk']},
    {'module':'os.path', 'submodule': ['join', 'islink', 'isfile']}
)
def fixup_scripts(old_dir, new_dir, version, bin_dir):
    #bin_dir = join(new_dir, env_bin_dir)
    root, dirs, files = next(walk(bin_dir))
    pybinre = re.compile(r'pythonw?([0-9]+(\.[0-9]+(\.[0-9]+)?)?)?$')

    for file_ in files:
        filename = join(root, file_)
        #Changement le chemin du venv dans les scripts activate
        if file_ == 'activate' or file_.startswith('activate.'):

            with open(filename, 'rb') as f:
                data = f.read().decode('utf-8')

            data = data.replace(old_dir, new_dir)
            with open(filename, 'wb') as f:
                f.write(data.encode('utf-8'))

        #Relink des liens symboliques
        elif islink(filename):
            fixup_link(filename, old_dir, new_dir)

        #Remplacement des shebang
        elif isfile(filename):
            fixup_script_(root, file_, old_dir, new_dir, version)


@impmagic.loader(
    {'module':'os.path', 'submodule': ['join', 'normcase', 'abspath']}
)
def fixup_script_(root, file_, old_dir, new_dir, version):
    old_shebang = '#!%s/bin/python' % normcase(abspath(old_dir))
    new_shebang = '#!%s/bin/python' % normcase(abspath(new_dir))

    filename = join(root, file_)
    with open(filename, 'rb') as f:
        if f.read(2) != b'#!':
            # no shebang
            return
        f.seek(0)
        lines = f.readlines()

    if not lines:
        return

    def rewrite_shebang(version=None):
        shebang = new_shebang
        if version:
            shebang = shebang + version
        shebang = (shebang + '\n').encode('utf-8')
        with open(filename, 'wb') as f:
            f.write(shebang)
            f.writelines(lines[1:])

    try:
        bang = lines[0].decode('utf-8').strip()
    except UnicodeDecodeError:
        return

    short_version = bang[len(old_shebang):]

    if not bang.startswith('#!'):
        return
    elif bang == old_shebang:
        rewrite_shebang()
    elif (bang.startswith(old_shebang) and bang[len(old_shebang):] == version):
        rewrite_shebang(version)
    elif (bang.startswith(old_shebang) and short_version and bang[len(old_shebang):] == short_version):
        rewrite_shebang(short_version)
    else:
        return


@impmagic.loader(
    {'module':'os', 'submodule': ['readlink', 'symlink', 'rename']},
    {'module':'os.path', 'submodule': ['join', 'dirname', 'abspath', 'isabs']}
)
def fixup_link(filename, old_dir, new_dir, target=None):
    if target is None:
        target = readlink(filename)

    origdir = dirname(abspath(filename)).replace(new_dir, old_dir)
    if not isabs(target):
        target = abspath(join(origdir, target))
        rellink = True
    else:
        rellink = False

    if _dirmatch(target, old_dir):
        if rellink:
            target = target[len(origdir):].lstrip(os.sep)
        else:
            target = target.replace(old_dir, new_dir, 1)

    tmpfn = "%s.new" % filename
    symlink(target, tmpfn)
    rename(tmpfn, filename)

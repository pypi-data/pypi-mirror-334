import __main__
import impmagic

"""
import xmlrpc.client
client = xmlrpc.client.ServerProxy('https://pypi.org/pypi')
client.package_releases('py-cpuinfo')
client.release_data('py-cpuinfo', '0.1.3')
client.list_packages()
"""

#A REFAIRE
def build_cache():
    import xmlrpc.client
    client = xmlrpc.client.ServerProxy(f'{__main__.nxs.metadata_source}/pypi')
    
    print("Récupération de la liste")
    packages = client.list_packages()
    maxd = len(packages)

    print("Construction")
    i=1
    for package in packages:
        print(f"{i}/{maxd} - {package}")
        get_package(package)
        i+=1

#Récupération les informations d'un package
@impmagic.loader(
    {'module':'json'},
    {'module':'sys_nxs.connect', 'submodule':['get']},
    {'module':'cache.sqlite', 'submodule':['Cache']},
    {'module': 'template', 'submodule': ['default_conf']},
    {'module': 'sys_nxs.host', 'submodule': ['path_rep']},
    {'module':'os.path', 'submodule': ['split', 'expanduser', 'join']}
)
def get_package_information(package_name, version):
    cachefile = join(expanduser(__main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)).replace(path_rep[1], path_rep[0]), 'repo_cache.db')

    dbcache = Cache(cachefile)

    result = dbcache.search(package_name, version)

    if len(result):
        return result[0]

    else:
        url = f"{__main__.nxs.metadata_source}/pypi/{package_name}/{version}/json"

        response = get(url)
        if response.status_code == 200:
            insert_data = {}
            data = response.json()
            info = data['info']

            informations = ['name', 'version', 'summary', 'author', 'maintainer', 'license', 'home_page', 'requires_python', 'requires_dist', 'vulnerabilities']

            for inf in informations:
                if inf in info and info[inf]!=None and len(info[inf])>0:
                    if isinstance(info[inf], list):
                        insert_data[inf] = json.dumps(info[inf])
                    else:
                        insert_data[inf] = info[inf]
                else:
                    insert_data[inf] = ""

            dbcache.add(insert_data.copy())

            return insert_data


#Récupération des informations d'un package
@impmagic.loader(
    {'module':'concurrent.futures', 'as': 'worker'},
    {'module':'sys_nxs.connect', 'submodule':['get']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def get_package(package_name, version=None):
    if version!=None:
        return get_package_information(package_name, version)
    else:
        releases = get_versionlist_package(package_name)
        
        result = []
        if __main__.nxs.conf.load(val='threading', section='',default=default_conf.threading):
            with worker.ThreadPoolExecutor(max_workers=__main__.nxs.threadmax) as executor:
                futures = [executor.submit(get_package_information, package_name, release) for release in releases]

                worker.wait(futures)

                result = [future.result() for future in futures]


        else:
            for release in releases:
                result.append(get_package_information(package_name, release))

        return result


#Récupération des la liste des requirements
@impmagic.loader(
    {'module':'concurrent.futures', 'as': 'worker'},
    {'module': 'template', 'submodule': ['default_conf']}
)
def get_all_requirement(used, i=0):
    if i>__main__.nxs.conf.load(val='project.deep_search', section='',default=default_conf.project_deep_search):
        return used

    if __main__.nxs.conf.load(val='threading', section='',default=default_conf.threading):
        with worker.ThreadPoolExecutor(max_workers=__main__.nxs.threadmax) as executor:
            futures = [executor.submit(run_all_requirement, used_package, used, i) for used_package in used.copy()]

            worker.wait(futures)

            for future in futures:
                used = list(set(used).union(future.result()))
    else:
        for used_package in used.copy():
            requirement_package = run_all_requirement(used_package, used, i)
            used = list(set(used).union(requirement_package))

    return used


def run_all_requirement(used_package, used, i):
    v = get_versionlist_package(used_package)
    if len(v):
        try:
            requirements = get_requirement(used_package, v[-1])
            if len(requirements):
                # Créer une liste avec les éléments de liste2 qui ne sont pas dans liste1
                resultat = [x for x in list(requirements.keys()) if x not in used]

                used = list(set(used).union(list(requirements.keys())))

                req = get_all_requirement(resultat, i+1)
                if len(req):
                    used = list(set(used).union(req))
        except:
            pass
    return used


#Récupération de la liste des dépendances d'un package
@impmagic.loader(
    {'module':'os'},
    {'module':'re'},
    {'module':'json'},
    {'module':'sys_nxs.connect', 'submodule':['get']},
    {'module':'template', 'submodule':['regex']},
    {'module':'cache.direct', 'submodule':['DirectCache']}
)
def get_requirement(package_name, version, test=False):
    cache = DirectCache()
    data = cache.get("package_info", package_name)

    if data==None:
        data = get_package_information(package_name, version)
        if data==None:
            return {}

        cache.set("package_info", package_name, data)
    dependencies = data['requires_dist']
    if dependencies==None:
        return {}
    else:
        package_compiled = re.compile(regex.package_regex)
        python_version_compiled = re.compile(regex.python_version_regex)
        sys_platform_compiled = re.compile(regex.sys_platform_regex)
        extra_compiled = re.compile(regex.extra_regex)
        operator_regex = re.compile(regex.segment_version)

        result = {}

        try:
            dependencies = json.loads(dependencies)
        except:
            pass

        for deps in list(dependencies):
            package = package_compiled.search(deps)
            if package!=None:
                name = package.group('name')
                version = package.group('version')
                #print(f"Name: {package.group('name')}\nVersion: {package.group('version')}")
                
                pyver = python_version_compiled.search(deps)
                if pyver!=None and hasattr(__main__.nxs, 'py_version'):
                    pyversion = pyver.group('python_version')
                    pyversion = pyversion.replace("'","").replace(" ","")
                    match = operator_regex.match(pyversion)
                    if match:
                        operator = match.group('operator')
                        target_major = match.group('major')
                        target_minor = match.group('minor')
                        target_patch = match.group('patch')

                        target = target_major
                        if target_minor!=None:
                            target+= "."+target_minor
                        if target_patch!=None:
                            target+= "."+target_patch

                        if not compare_version(__main__.nxs.py_version, operator, target):
                            continue

                    #print(f"Pyversion: {pyversion}")

                platf = sys_platform_compiled.search(deps)
                if platf!=None:
                    if platf.group('platform').lower().startswith('win') and os.name!='nt':
                        continue
                    #print(f"platform: {platf.group('platform')}")

                extra = extra_compiled.search(deps)
                if extra!=None:
                    if extra.group('extra')=="test" and test==False:
                        continue
                    #print(f"extra: {extra.group('extra')}")

                if name!=None:
                    result[name] = {}
                    if version!=None:
                        result[name]['version'] = version
                    else:
                        result[name]['version'] = 'N.A'

        #return dependencies
        #print(result)
        return result
    return {}

#Vérifie la compatibilité du module avec les autres modules a installer
@impmagic.loader(
    {'module':'template', 'submodule':['regex']},
    {'module':'re'}
)
def get_conflit_package(name, dictionary, element=None):
    if element is None or 'compatibility' not in element or not element['compatibility']:
        return dictionary

    version = element['compatibility'][-1]
    operator_regex = re.compile(regex.segment_version)
    
    # Recherche des dépendances du package
    requirements = get_requirement(name, version)

    for package_name, requirement in requirements.items():
        if requirement['version'] == 'N.A':
            compatible_version = get_compatible_versions(package_name, ">=0.0.0")
        else:
            number_regex = re.compile(regex.dissociate_version)
            compatible_version = None

            for match in number_regex.finditer(requirement['version']):
                dep_version = match.group()
                match = operator_regex.match(dep_version)

                possible = get_compatible_versions(package_name, dep_version)
                if compatible_version is None:
                    compatible_version = set(possible)
                else:
                    compatible_version.intersection_update(possible)

            if package_name in dictionary:
                conflit = all(ver not in compatible_version for ver in dictionary[package_name]['compatibility'])

                if conflit:
                    if 'conflicts' not in dictionary[name]:
                        dictionary[name]['conflicts'] = []
                    dictionary[name]['conflicts'].append(f"{package_name} ({requirement})")
                    if len(element['compatibility']) > 1:
                        element['compatibility'].pop()
                        dictionary[name]['compatibility'] = element['compatibility']

    return dictionary




#Récupère un dictionnaire (du toml) et une dictionnaire avec les versions compatibles
@impmagic.loader(
    {'module':'template', 'submodule':['regex']},
    {'module':'app.display', 'submodule':['logs']},
    {'module': 'template', 'submodule': ['default_conf']},
    {'module':'package.check', 'submodule':['is_native_module']},
    {'module':'re'}
)
def dependency_to_list(dictionary, force=False, nocheck=False):
    full_log = __main__.nxs.conf.load(val='logs.full', section='',default=default_conf.logs_full)
    result = {}
        #result = []

    logs("Analyse des dépendances")
    """
    {'module':'cache.direct', 'submodule':['DirectCache']}
    cache = DirectCache()
    cache.set("version_package", package_name, result)
    """
    logs("Téléchargement des informations")
    pull_package_informations(dictionary)
    #exit()

    dictionary = construct_dependencies(dictionary)

    if not nocheck:
        #Analyse les dépendances
        version_regex = re.compile(regex.dependencies)
        logs(f"Recherche de conflit")
        for name, element in dictionary.items():
            dictionary = get_conflit_package(name, dictionary, element)


    #Construct la liste des modules à installer avec la version la plus récente compatible
    for element in dictionary:
        if dictionary[element]['compatibility']==None:
            if not is_native_module(element):
                logs(f"Module {element} non disponible", "error")
        else:
            if 'conflicts' in dictionary[element].keys():
                logs(f"Aucune version compatible pour le module {element}\nConflits avec les packages:\n  - {'  - '.join(dictionary[element]['conflicts'])}", "warning")
                if not force:
                    return None
            else:
                if len(dictionary[element]['compatibility'])>0:
                    result[str(element)] = {}
                    #Récupération de la version la plus récente
                    result[str(element)]['version'] = max(dictionary[element]['compatibility'], key=lambda x: [int(i) for i in x.split('.')])
                    result[str(element)]['compatible'] = dictionary[element]['compatibility']
                    #result.append(str(element)+"=="+dictionary[element]['compatibility'].pop())
                else:
                    logs(f"Aucune version compatible pour le module {element}", "warning")

    return result


#Télécharge les informations des packages
@impmagic.loader(
    {'module':'app.display', 'submodule':['logs']},
    {'module':'concurrent.futures', 'as': 'worker'},
    {'module':'os'}
)
def pull_package_informations(dictionary, result=None):
    with worker.ThreadPoolExecutor(max_workers=__main__.nxs.threadmax) as executor:
        futures = []
        for key, value in dictionary.items():
            futures.append(executor.submit(thread_pull, key, value))
        worker.wait(futures)


def thread_pull(key, value):
    if isinstance(value, dict):
        if key=="windows" and os.name=="nt":
            result = thread_pull(value, result)
        elif key=="linux" and os.name!="nt":
            result = thread_pull(value, result)
        elif key!="windows" and key!="linux":
            result = thread_pull(value, result)

    else:
        v = get_versionlist_package(key)
        if len(v):
            requirements = get_requirement(key, v[-1])
            if len(requirements):
                for requirement in requirements:
                    get_versionlist_package(requirement)  



#Construct un dictionnaire contenant chaque package avec une liste de version compatible
@impmagic.loader(
    {'module':'app.display', 'submodule':['logs']},
    {'module':'functools', 'submodule':['reduce']},
    {'module': 'template', 'submodule': ['default_conf']},
    {'module':'os'}
)
def construct_dependencies(dictionary, result=None):
    full_log = __main__.nxs.conf.load(val='logs.full', section='',default=default_conf.logs_full)

    if result==None:
        result = {}

    for key, value in dictionary.items():
        if isinstance(value, dict):
            if key=="windows" and os.name=="nt":
                result = construct_dependencies(value, result)
            elif key=="linux" and os.name!="nt":
                result = construct_dependencies(value, result)
            elif key!="windows" and key!="linux":
                result = construct_dependencies(value, result)

        else:
            """
            if full_log:
                logs(f"Analyse de {key}")
            """
            if value=="N.A":
                compatible_version = get_compatible_versions(key, ">=0.0.0")
            else:
                if ',' in value:
                    compatible_version = []
                    for ver in value.split(","):
                        compatible_version.append(get_compatible_versions(key, ver))

                    common_versions = reduce(set.intersection, [set(versions) for versions in compatible_version])
                    compatible_version = sorted(common_versions, key=lambda x: tuple(map(int, x.split('.'))))
                else:
                    compatible_version = get_compatible_versions(key, value)

            if key in result.keys():
                if result[key]['compatibility']!=None:
                    for ver in result[key]['compatibility']:
                        if ver not in compatible_version:
                            result[key]['compatibility'].remove(ver)
                else:
                    logs(f"Package {key} non compatible", "warning")
            else:
                result[key] = {}
                result[key]['compatibility'] = compatible_version
    return result

#Retourne la liste des versions disponibles d'un package
@impmagic.loader(
    {'module':'sys_nxs.connect', 'submodule':['get']},
    {'module':'cache.direct', 'submodule':['DirectCache']}
)
def get_versionlist_package(package_name):
    cache = DirectCache()
    info = cache.get("version_package", package_name)

    if info!=None:
        return info

    result = []

    headers = {"Accept": "application/vnd.pypi.simple.v1+json"}
    #print("aaaaaaa")
    #import requests
    response = get(f"{__main__.nxs.metadata_source}/simple/{package_name}/", headers=headers)
    #print(info.text)
    #url = f"https://pypi.org/pypi/{package_name}/json"
    #response = get(url)
    if response.status_code == 200:
        data = response.json()
        releases = data["versions"]
        for version in releases:
            result.append(version)

    cache.set("version_package", package_name, result)
    return result


@impmagic.loader(
    {'module':'template', 'submodule':['regex']},
    {'module':'re'}
)
def get_compatible_versions(package, version=None):
    # Récupérer la liste des versions disponibles
    releases = get_versionlist_package(package)

    if len(releases)>0:
        if version==None:
            return releases

        # Liste qui va stocker les versions compatibles
        compatible_versions = []

        # Séparer l'opérateur de comparaison et la version cible
        operator_regex = re.compile(regex.segment_version)
        if not version.startswith("==") and not version.startswith(">=") and not version.startswith("<=") and not version.startswith("!=") and not version.startswith("^")  and not version.startswith(">") and not version.startswith("<"):
            version = "=="+version

        if " " in version:
            version = version.replace(" ", "")

        match = operator_regex.match(version)
        operator = match.group('operator')
        target_major = match.group('major')
        target_minor = match.group('minor')
        target_patch = match.group('patch')

        target = target_major
        if target_minor!=None:
            target+= "."+target_minor
        if target_patch!=None:
            target+= "."+target_patch
        """
        # Convertir les parties de la version cible en entiers
        if target_major!=None:
            target_major = int(target_major)
        if target_minor!=None:
            target_minor = int(target_minor)
        if target_patch!=None:
            target_patch = int(target_patch)
        """

        # Parcourir toutes les versions disponibles
        for v in releases:
            # Extraire les différentes parties de la version en utilisant l'expression régulière
            if compare_version(v, operator, target):
                compatible_versions.append(v)

        return compatible_versions

@impmagic.loader(
    {'module':'template', 'submodule':['regex']},
    {'module':'re'}
)
def compare_version(v, operator, target):
    version_regex = re.compile(regex.version)

    target_version = version_regex.match(target)
    if target_version!=None:
        #match_release = release_version.groups()

        target_major = target_version.group('major')
        target_minor = target_version.group('minor')
        target_patch = target_version.group('patch')
        # Convertir les parties de la version en entiers
        if target_major!=None:
            target_major = int(target_major)
        if target_minor!=None:
            target_minor = int(target_minor)
        if target_patch!=None:
            target_patch = int(target_patch)
        release_version = version_regex.match(v)
        if release_version!=None:
            #match_release = release_version.groups()
            major = release_version.group('major')
            minor = release_version.group('minor')
            patch = release_version.group('patch')
            # Convertir les parties de la version en entiers
            if major!=None:
                major = int(major)
            if minor!=None:
                minor = int(minor)
            if patch!=None:
                patch = int(patch)

            # Vérifier si la version est compatible en utilisant l'opérateur de comparaison
            if operator == '>=' and (major > target_major or (minor!=None and target_minor!=None and (target_patch==None or patch==None) and major == target_major and minor >= target_minor) or (minor!=None and patch!=None and target_minor!=None and target_patch!=None and major == target_major and minor > target_minor) or (patch!=None and target_patch!=None and major == target_major and minor == target_minor and patch >= target_patch)):
                return True
            elif operator == '>' and (major > target_major or (minor!=None and target_minor!=None and major == target_major and minor > target_minor) or (target_patch!=None and major == target_major and minor == target_minor and patch > target_patch)):
                return True
            elif operator == '<' and (major < target_major or (minor!=None and target_minor!=None and major == target_major and minor < target_minor) or (target_patch!=None and major == target_major and minor == target_minor and patch < target_patch)):
                return True
            elif operator == '<=' and (major < target_major or (minor!=None and target_minor!=None and (target_patch==None or patch==None) and major == target_major and minor <= target_minor) or (minor!=None and patch!=None and target_minor!=None and target_patch!=None and major == target_major and minor < target_minor) or (patch!=None and target_patch!=None and major == target_major and minor == target_minor and patch <= target_patch)):
                return True
            elif operator == '^' and major == target_major:
                return True
            elif operator == '==' and major == target_major and (target_minor is None or minor == target_minor) and (target_patch is None or patch == target_patch):
                return True
            elif operator == '!=' and (major != target_major or minor != target_minor or patch != target_patch):
                return True
    return False


@impmagic.loader(
    {'module':'sys_nxs.connect', 'submodule':['get']},
    {'module':'html5lib.html5parser', 'submodule':['parse']}
)
def search_package(query, strict=None):
        url = f"{__main__.nxs.metadata_source}/"
        
        results = {}

        search = {"q": query}
        response = get(url+"search", params=search)

        content = parse(response.content, namespaceHTMLElements=False)
        for result in content.findall(".//*[@class='package-snippet']"):
            name_element = result.find("h3/*[@class='package-snippet__name']")
            version_element = result.find("h3/*[@class='package-snippet__version']")

            if name_element is None or version_element is None or not name_element.text or not version_element.text:
                continue

            description_element = result.find("p[@class='package-snippet__description']")
            if description_element is not None and description_element.text:
                description = description_element.text
            else:
                description = ""

            try:
                name = name_element.text
                if strict==True and (query not in name and query.replace("_","-") not in name):
                    continue
                results[name] = {}
                results[name]['version'] = version_element.text
                results[name]['description'] = description.strip()
            except:
                pass

        return results

#Vérifie si un package est disponible dans les repos
@impmagic.loader(
    {'module':'sys_nxs.connect', 'submodule':['get']}
)
def in_repo(package_name):
    url = f"{__main__.nxs.metadata_source}/pypi/{package_name}/json"
    response = get(url)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False

#Récupérer les informations d'un package
@impmagic.loader(
    {'module':'subprocess'},
    {'module':'re'},
    {'module':'sys_nxs.connect', 'submodule':['get']},
    {'module':'app.display', 'submodule':['logs', 'print_nxs']},
    {'module':'structure.check', 'submodule':['in_project', 'get_nexus_file']},
    {'module':'toml_nxs.toml', 'submodule':['TOML'], 'as': 'TOMLnxs'},
    {'module': 'sys_nxs.host', 'submodule': ['path_rep']},
    {'module': 'os.path', 'submodule': ['exists']},
    {'module':'env_nxs.env', 'as':'env'},
    {'module':'template', 'submodule':['regex']}
)
def info_package(package_name, noarbo=False, arbolvl=1, list_version=None):
    package_compiled = re.compile(regex.package_regex)
    package_match = package_compiled.search(package_name)
    if package_match!=None:
        package_name = package_match.group('name')
        version = package_match.group('version')

        if version!=None:
            version = version.replace("==","")
            url = f"{__main__.nxs.metadata_source}/pypi/{package_name}/{version}/json"
        else:
            url = f"{__main__.nxs.metadata_source}/pypi/{package_name}/json"
        
        response = get(url)
        if response.status_code == 200:
            data = response.json()
            info = data['info']

            print_nxs("Name: ", nojump=True)
            print(info['name'])
            if 'version' in info and info['version']!=None and len(info['version'])>0:
                print_nxs("Version: ", nojump=True)
                print(info['version'])
            if 'summary' in info and info['summary']!=None and len(info['summary'])>0:
                print_nxs("Description: ", nojump=True)
                print(info['summary'])
            if 'author' in info and info['author']!=None and len(info['author'])>0:
                print_nxs("Author: ", nojump=True)
                print(info['author'])
            if 'license' in info and info['license']!=None and len(info['license'])>0:
                print_nxs("License: ", nojump=True)
                print(info['license'])
            if 'home_page' in info and info['home_page']!=None and len(info['home_page'])>0:
                print_nxs("Homepage: ", nojump=True)
                print(info['home_page'])

            if not noarbo:
                res = get_requirement(package_name, info['version'])

                if len(res)>0:
                    print_nxs("Dependencies: ")
                    tree_dependencies(res, max=len(res), lvl_max=arbolvl)
                else:
                    print_nxs("Dependencies: ", nojump=True)
                    print("No dependencies")

            #print(res)

            print_nxs("Vulnerabilities: ", nojump=True)
            vuln = data['vulnerabilities']
            if len(vuln)>0:
                print(vuln)
            else:
                print("No vulnerabilities")

            print_nxs("Install: ", nojump=True)
            if in_project():
                tfile = TOMLnxs(get_nexus_file())
                tfile.load_doc()
            else:
                tfile = None

            env_exe = env.get_executable(tfile, logs_env=False)
            if env_exe!=None:
                env_exe = env_exe.replace(path_rep[1], path_rep[0])
                if exists(env_exe):
                    cmd = [env_exe, '-c', 'import pkg_resources; print(pkg_resources.get_distribution("'+package_name+'").location)']
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = proc.communicate()

                    if len(stdout):
                        cmd = [env_exe, '-c', 'import pkg_resources; print(pkg_resources.get_distribution("'+package_name+'")._version)']
                        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout_version, stderr_version = proc.communicate()

                        if len(stdout_version):
                            if stdout_version.rstrip().decode()==info['version']:
                                print("is installed")
                            else:
                                print(f"is installed in another version ({stdout_version.rstrip().decode()})")
                            
                            print_nxs("Location: ", nojump=True)
                            print(stdout.rstrip().decode())
                        else:
                            print("not installed")
                    else:
                        print("not installed")

            if list_version:
                print_nxs("Version available: ")
                for release, rel_info in data['releases'].items():
                    if len(rel_info):
                        print(f"  {release} ({rel_info[0]['upload_time'].replace('T',' ')})")
                    else:
                        print(f"  {release}")

        elif response.status_code == 404:
            logs("package not found", "error")

#Récupérer la dernière version disponible d'un package
@impmagic.loader(
    {'module':'sys_nxs.connect', 'submodule':['get']}
)
def latest_version(package_name):
    url = f"{__main__.nxs.metadata_source}/pypi/{package_name}/json"
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        info = data['info']

        if 'version' in info and len(info['version'])>0:
            return info['version']
    return None

#Vérifie si le package a des vulnérabilités
@impmagic.loader(
    {'module':'sys_nxs.connect', 'submodule':['get']}
)
def is_vulnerable(packages):
    url = f"{__main__.nxs.metadata_source}/pypi/{packages}/json"
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data['vulnerabilities'])>0:
            return True
    return False

#Affichage de l'arbre de dependance
@impmagic.loader(
    {'module':'app.display', 'submodule':['print_nxs']}
)
def tree_dependencies(packages, lvl=0, lvl_max=1, max=1, arbo=[]):
    i=1
    for package, info in packages.items():
        print_pattern(i, max, arbo)
        if is_vulnerable(package):
            print_nxs(" "+package, color=__main__.color['dark_gray'], nojump=True)
            print_nxs(" (vuln)", color=__main__.color['red'])
        else:
            print_nxs(" "+package, color=__main__.color['dark_gray'])

        if info['version']=="N.A":
            info['version']=">=0.0"
        compatible_version = get_compatible_versions(package, info['version'])

        if compatible_version and len(compatible_version):
            res = get_requirement(package, compatible_version[-1])

            if len(res)>0 and lvl<lvl_max:
                if i==max-1:
                    new_arbo = arbo+['   ']
                else:
                    new_arbo = arbo+['│  ']
                tree_dependencies(res, lvl+1, max=len(res), lvl_max=lvl_max, arbo=new_arbo)
        i+=1

def print_pattern(index, max, arbo):
    arbo = "".join(arbo)
    if index==max-1:
        print(f"{arbo}└─", end="")
    else:
        print(f"{arbo}├─", end="")


#Cherche dans les alias
@impmagic.loader(
    {'module':'json', 'submodule': ['load']},
    {'module':'structure.check', 'submodule': ['get_root_project']},
    {'module':'app.display', 'submodule':['logs']},
    {'module':'os.path', 'submodule': ['exists', 'isfile', 'join', 'abspath']}
)
def get_alias(init=False):
    if init:
        file = abspath('.package_alias')
    else:
        root_project = get_root_project()
        if root_project is False:
            file = '.package_alias'
        else:
            file = join(get_root_project(), '.package_alias')

    if exists(file) and isfile(file):
        try:
            #logs("Chargement des alias de package")
            with open(file) as file:
                return load(file)
        except:
            logs("Fichier corrompu", "warning")
            return {}
    else:
        return {}


#Sauvegarde les alias
@impmagic.loader(
    {'module':'json', 'submodule': ['dump']},
    {'module':'structure.check', 'submodule': ['get_root_project']},
    {'module':'os.path', 'submodule': ['exists', 'isfile', 'join']}
)
def set_alias(data):
    root_project = get_root_project()
    if root_project is False:
        file = '.package_alias'
    else:
        file = join(get_root_project(), '.package_alias')

    with open(file, 'w') as file:
        return dump(data, file, indent=4)

@impmagic.loader(
    {'module':'tomlkit'}
)
def dependency_to_lock(deps, lockfile):
    for package, version in deps.copy().items():
        if isinstance(version, tomlkit.items.Table):
            if package in lockfile:
                deps[package] = dependency_to_lock(version, lockfile[package])
        else:
            if package in lockfile:
                deps[package] = "=="+lockfile[package]   
    return deps


@impmagic.loader(
    {'module':'structure.check', 'submodule': ['get_root_project']}, 
    {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'},
    {'module':'os.path', 'submodule':['join', 'exists']}
)
def lock_package(deps):
    #Si fichier de lock existe
    lock = join(get_root_project(), 'nexus.lock')
    if exists(lock):
        lockfile = TOMLnxs(join(get_root_project(), 'nexus.lock'))
        lockfile.load_doc()
        lock_deps = lockfile.get_key('dependencies')
        if lock_deps!=None:
            deps = dependency_to_lock(deps, lock_deps)

    return deps

#Récupère le dictionnaire des dépendances et enlève les obligations de versions pour tous les packages où uniquement ceux dans name
@impmagic.loader(
    {'module':'tomlkit'}
)
def unversion_package(deps, name=None):
    result = {}
    for element, value in deps.items():
        if isinstance(value, tomlkit.items.Table):
            value = unversion_package(value, name)
            result[element] = value
        else:
            if name==None or (name!=None and name==element):
                result[element] = "N.A"
            else:
                result[element] = value

    return result


#Trouver la version suivante à mettre à jour
@impmagic.loader(
    {'module':'re'},
    {'module':'template', 'submodule':['regex']},
    {'module':'os'}
)
def get_possible_version(deps, actual, minor=False, patch=False):
    #Passage en l'ensemble des noms en lower() pour faciliter la recherche
    actual = [x.lower() for x in actual]

    to_return = {}
    reg_version = re.compile(regex.version)

    for package_name, info in deps.items():
        if package_name=="windows":
            if os.name=="nt":
                win = get_possible_version(info, actual, minor, patch)
                to_return.update(win)
        elif package_name=="linux":
            if os.name!="nt":
                lin = get_possible_version(info, actual, minor, patch)
                to_return.update(lin)
        else:
            if info=="N.A":
                releases = get_versionlist_package(package_name)

                if not minor and not patch:
                    to_return[package_name] = releases[-1]
                else:
                    valid_release = None
                    #match = reg_version.match(actual[package_name.lower()])
                    match = reg_version.match(actual[package_name.lower()])
                    actual_major = match.group('major')
                    actual_minor = match.group('minor')
                    actual_patch = match.group('patch')

                    for release_version in releases:
                        match = reg_version.match(release_version)
                        if match:
                            release_major = match.group('major')
                            release_minor = match.group('minor')
                            release_patch = match.group('patch')

                            if minor:
                                if actual_major==release_major:
                                    valid_release=release_version
                            elif patch:
                                if actual_major==release_major and actual_minor==release_minor:
                                    valid_release=release_version

                    if valid_release==None:
                        valid_release = actual[package_name.lower()]

                    to_return[package_name] = valid_release
            else:
                to_return[package_name] = info

    return to_return


#Retourne uniquement les packages dont la version à changer
def filter_update(actual, deps):
    #Passage en l'ensemble des noms en lower() pour faciliter la recherche
    c_actual = actual.copy()
    actual = {}
    for name, info in c_actual.items():
        actual[name.lower()] = info


    for package_name, package_info in deps.copy().items():
        if package_name.lower() in actual and package_info['version']==actual[package_name.lower()]:
            del deps[package_name]

    return deps
import impmagic

@impmagic.loader(
    {'module':'sys_nxs.connect', 'submodule':['get']}
)
def list_all_licenses():
    response = get("https://api.github.com/licenses")
    result = {}

    if response.status_code==200:
        licenses = response.json()
        for license in licenses:
            response = get(license['url'])
            if response.status_code==200:
                licenses_content = response.json()
                result[license['key']] = {}
                result[license['key']]['key'] = license['key']
                result[license['key']]['name'] = license['name']
                result[license['key']]['license'] = licenses_content['body']
    return result

@impmagic.loader(
    {'module':'__main__'},
    {'module':'os.path', 'submodule':['exists']},
    {'module':'json', 'submodule':['load', 'dump']}
)
def get_data_licenses():
    if exists(__main__.nxs.license_cache_file):
        with open(__main__.nxs.license_cache_file) as json_file:
            licenses = load(json_file)
    else:
        licenses = list_all_licenses()
        with open(__main__.nxs.license_cache_file, 'w') as json_file:
            dump(licenses, json_file)
    return licenses

@impmagic.loader(
    {'module':'Levenshtein'}
)
def detect_license(file):
    with open(file) as f:
        content = f.read()

    licenses = get_data_licenses()

    for license in licenses:
        license = licenses[license]
        distance = Levenshtein.distance(content, license['license'])
        similarity = 1 - (distance / max(len(content), len(license['license'])))
        if (similarity * 100)>95:
            return license['name']

    return False


def licenses_availables(name):
    licenses = get_data_licenses()

    for license in licenses:
        license = licenses[license]
        if name==license['name'] or name==license['key']:
            return True
    return False


@impmagic.loader(
    {'module':'app.display', 'submodule':['print_nxs', 'prompt']}
)
def get_license_content(name):
    licenses = get_data_licenses()

    if sum(1 for lic in licenses.keys() if name in lic)>1:
        options = [lic for lic in licenses.keys() if name in lic]
        choice = "0"
        while not choice.isdigit() or int(choice)<=0 or int(choice) >len(options):
            print_nxs("Plusieurs licences disponibles. Veuillez choisir la bonne:")
            for i, name in enumerate(options):
                print_nxs(f"{i+1}. {name}")
            choice = prompt("Choix: ")

        name = options[int(choice)-1]

    for license in licenses:
        license = licenses[license]
        if name==license['name'] or name==license['key']:
            return license['license']
    return False


def get_license_fullname(name):
    licenses = get_data_licenses()

    for license in licenses:
        license = licenses[license]
        if name==license['name'] or name==license['key']:
            return license['name']
    
    return False

@impmagic.loader(
    {'module':'glob', 'submodule':['glob']}
)
def license_exist():
    for file in glob('*'):
        if file.startswith('LICENSE'):
            return file
    return False
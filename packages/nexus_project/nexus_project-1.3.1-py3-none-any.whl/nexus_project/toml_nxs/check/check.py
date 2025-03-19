import impmagic

#Convertis un str en liste, contrôle les regex associés pour valider le format et sortie en dict
@impmagic.loader(
    {'module':'template.toml_format', 'submodule':['DEFAULT_TOML']},
    {'module':'re', 'submodule':['match']}
)
def check_list(value, name):
    if isinstance(value, str):
        value = value.split(",")

    result = {}
    if 'regex' in DEFAULT_TOML[name]:
        for element in value:
            if match(DEFAULT_TOML[name]["regex"], element):
                result.append(element)

        return result
    else:
        return value

#Formate une liste de dépendance en dictionnaire
@impmagic.loader(
    {'module':'template.regex', 'submodule':['dependencies']},
    {'module':'re', 'submodule':['match']}
)
def check_dependency_format(value):
    if isinstance(value, str):
        value = value.split(",")
    elif isinstance(value, dict):
        return value

    result = {}
    for package in value:
        matchs = match(dependencies, package)
        if matchs!=None:
            package_name = matchs.group(1)
            version = matchs.group(2)
            if version==None:
                version = "N.A"

            result[package_name]=version

    return result
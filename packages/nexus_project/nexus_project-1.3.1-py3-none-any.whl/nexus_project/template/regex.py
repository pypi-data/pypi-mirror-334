
#Vérifie que c'est une version de projet
project_version = r"^\d+\.\d+\.\d+$"

#Vérifie si c'est un fichier .py ou .pyw
valid_file = r"^[\w]+\.(py|pyw)$"

#Vérifie le format de la version python
python_version = r"^(>=\s*\d+\.\d+(\.\d+)?)(\s*(,\s*)?(<=|>=|!=|==|<|>)\s*\d+\.\d+(\.\d+)?(\.\d+)?)*$"

#Permet de séparer le package et la version avec le format package!=version
#dependencies = r'^([a-zA-Z0-9_.-]+)((>=|!=|<|>|<=|\^|==)\s*\d+\.\d+(\.\d+)?)?$'
dependencies = r'^([a-zA-Z0-9_.-]+)((>=|!=|<=|<|>|\^|==)\s*\d+(\.\d+(\.\d+)?)?)?$'

#Extraire mineure, majeur et patch d'une version
version = r'^(?P<major>\d+)(\.(?P<minor>\d+))?(\.(?P<patch>\d+))?$'


#Sépare le comparateur et les versions
segment_version = r'(?P<operator>>=|!=|<|>|<=|\^|==)(?P<major>\d+)(\.(?P<minor>\d+))?(\.(?P<patch>\d+))?'

#Modèle de requirement
package_regex = r"(?P<name>^([a-zA-Z0-9_.-]+))\s?\(?(?P<version>(>=|!=|<=|<|>|\^|==)\s*\d+(\.\d+){0,2},?\s?((>=|!=|<=|<|>|\^|==)\s*\d+(\.\d+){0,2})*)?"
info_package_regex = r"(?P<name>^([a-zA-Z0-9_.-]+))\s?\(?(?P<operator>>=|!=|<=|<|>|\^|==)?(?P<version>\s*\d+(\.\d+){0,2},?\s?((==)\s*\d+(\.\d+){0,2})*)?"
python_version_regex = r"(python_version\s+(?P<python_version>[<>=]+\s*[^\s()]+))"
sys_platform_regex = r"sys_platform\s*[<>=]+\s*'(?P<platform>([^']+))'"
extra_regex = r"(extra\s*[<>=]+\s*'(?P<extra>([^']+))')"
dissociate_version = r"((>=|!=|<=|<|>|\^|==)\s*\d+(\.\d+){0,2})"

#authors
author_regex = r"(.*)\s*<([^@]+@[^@]+\.[^@]+?)>"

#Contrôle le nom d'un fichier wheel/tar
pack_regex = r"(?P<packagename>[a-zA-Z0-9._-]+)-(?P<version>\d+\.\d+\.\d+)(-[a-zA-Z0-9_]+){0,3}\.(tar\.gz|whl)$"

#Vérifie si c'est un uuid
uuid_regex = r"^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$"
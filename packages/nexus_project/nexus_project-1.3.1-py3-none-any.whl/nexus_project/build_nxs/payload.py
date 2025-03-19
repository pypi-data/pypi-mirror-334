from cx_Freeze import setup, Executable
import os, sys
import toml
import json
import impmagic
from glob import glob
import re

def replace_by_alias(package_list, alias_file):
    try:
        with open(alias_file) as file:
            alias = load(file)

        for package_name, package_info in package_list.copy().items(): 
            if package_name in alias:
                print(package_name)
                fnd = alias[package]
                if isinstance(fnd, str):
                    package_list[fnd] = package_info
                else:
                    if os.name=="nt" and 'windows' in fnd:
                        package_list[fnd['windows']] = package_info
                    elif os.name!="nt" and 'linux' in fnd:
                        package_list[fnd['linux']] = package_info

                del package_list[package_name]

    finally:
        return package_list


def cat_(content):
    from tempfile import NamedTemporaryFile
    from json import dumps
    import pygments.lexers as lexers
    from pygments.formatters import TerminalTrueColorFormatter
    from pygments import highlight

    BUF_SIZE = 65536

    f = NamedTemporaryFile()
    f.write(dumps(content, indent=4).encode())
    f.seek(0)

    try:
        lex = lexers.get_lexer_by_name('json')
        formatter = TerminalTrueColorFormatter(style="monokai")
        
        while True:
            line = f.readline() 
            if not line:
                break
            else:
                print(highlight(line, lex, formatter),end="")
        f.close()
    except:
        with open(file, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE).decode('utf-8', 'ignore').translate({ord('\u0000'): None})
                if not data:
                    break
                print(data)


def load_key(config, section, entry):
    section_split = section.split(".")

    section = config
    for sec in section_split:
        section = section.get(sec, {})

    entry = section.get(entry, None)

    return entry


#Recherche dans les site-packages si le nom du répertoire est différent
def find_real_package_name(package_name):
    if impmagic.get(package_name):
        return package_name

    else:
        for sys_path in sys.path:
            if os.path.isdir(sys_path):
                for file in glob(f"{sys_path}/*"):
                    matcher = re.match(package_dist, os.path.basename(file))
                    if matcher:
                        if matcher.group("name").lower()==package_name:
                            return matcher.group("name")
    return package_name


#Recherche dans les site-packages si le nom du répertoire est différent
def find_package_name(package_name):
    if impmagic.get(package_name):
        return package_name

    else:
        for sys_path in sys.path:
            if os.path.isdir(sys_path):
                for file in glob(f"{sys_path}/*"):
                    matcher = re.match(package_dist, os.path.basename(file))
                    if matcher:
                        if matcher.group("name").lower()==package_name:
                            top_level_file = os.path.join(file, 'top_level.txt')
                            if os.path.exists(top_level_file):
                                with open(top_level_file) as f:
                                    lines = f.read().splitlines()
                                    return next((line for line in lines if not line.startswith('_')), package_name)
    return package_name


code_folder = sys.argv[2]
destination = sys.argv[3]
mainfile = sys.argv[4]
alias_file = sys.argv[5]
action = sys.argv[6]

#Pour recupérer le nom du package depuis le répertoire dist-info
package_dist = r"(?P<name>^([a-zA-Z0-9_.]+))?\-(?P<version>\d+(\.\d+){0,2})*\.dist-info"


with open(sys.argv[1], "r") as f:
    config = toml.load(f)


#fol = os.path.abspath('.')
fol = os.path.abspath(os.path.split(__file__)[0])
sys.path.remove(fol)
sys.path.append(code_folder)

os.chdir(code_folder)

#################################### SET BUILD #####################################
build_exe_options = {}
options = ["packages","includes","excludes","optimize","no_compress"]
for option in options:
    option_data = load_key(config, 'project.build', option)
    if option_data!=None:
        if isinstance(option_data, list) and len(option_data)==0:
            continue

        if option=="includes":
            option_data = replace_by_alias(option_data, alias_file)
            c_option_data = option_data
            option_data = []
            for line in c_option_data:
                option_data.append(find_package_name(line))

        build_exe_options[option] = option_data

build_exe_options['build_exe'] = destination

#################################### EXECUTABLE ####################################
#For GUI Windows
base = load_key(config, 'project.build', 'GUI')
if base==True and sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None
#base='Console'

copyright = load_key(config, 'project.metadata', 'copyright')
if copyright=="":
    copyright=None

icon = load_key(config, 'project.build', 'icon')
if icon=="":
    icon=None

executables = [(Executable(mainfile, copyright=copyright, base=base, icon=icon))]
####################################################################################

setD = []
infos = ['name', 'version', 'description']
for info in infos:
    key = load_key(config, 'project', info)
    if key!=None:
        setD.append(key)
    else:
        print(f"Erreur avec la clé {info}")
        exit()

# On appelle la fonction setup
if action=="build":
    sys.argv = ['payload.py', 'build']
    #sys.argv[1]='build'
    setup(
        name = setD[0],
        version = setD[1],
        description = setD[2],
        options={"build_exe": build_exe_options},
        executables = executables,
    )
else:
    setup = {'name': setD[0], 'version': setD[1], 'description': setD[2], 'options': build_exe_options, 'executables': {'mainfile': mainfile, 'copyright': copyright, 'base': base, 'icon': icon}}
    cat_(setup)
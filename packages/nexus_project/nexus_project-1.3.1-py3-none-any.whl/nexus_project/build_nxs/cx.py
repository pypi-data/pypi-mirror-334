import impmagic

@impmagic.loader(
    {'module': 'cx_Freeze', 'submodule': ['setup', 'Executable']},
    {'module': 'os', 'submodule': ['chdir']},
    {'module': 'os.path', 'submodule': ['abspath']},
    {'module': 'sys', 'submodule': ['path', 'platform', 'argv']}
)
def compile(tfile, projectfolder, code_folder, destination, mainfile):
    fol = abspath('.')
    path.remove(fol)
    path.append(code_folder)
    
    chdir(code_folder)

    #################################### SET BUILD #####################################
    build_exe_options = {}
    options = ["packages","includes","excludes","optimize","no_compress"]
    for option in options:
        option_data = tfile.get_key(option,'project.build')
        if option_data!=None:
            if isinstance(option_data, list) and len(option_data)==0:
                continue
            build_exe_options[option] = option_data

    build_exe_options['build_exe'] = destination

    #################################### EXECUTABLE ####################################
    #For GUI Windows
    base = tfile.get_key('GUI','project.build')
    if base==True and platform == "win32":
        base = "Win32GUI"
    else:
        base = None
    #base='Console'

    copyright = tfile.get_key('copyright','project.metadata')
    if copyright=="":
        copyright=None

    icon = tfile.get_key('icon','project.build')
    if icon=="":
        icon=None

    executables = [(Executable(mainfile,copyright=copyright,base=base,icon=icon))]
    ####################################################################################

    # On appelle la fonction setup
    argv[1]='build'
    setup(
        name = tfile.doc['project']['name'],
        version = tfile.doc['project']['version'],
        description = tfile.doc['project']['description'],
        options={"build_exe": build_exe_options},
        executables = executables,
    )
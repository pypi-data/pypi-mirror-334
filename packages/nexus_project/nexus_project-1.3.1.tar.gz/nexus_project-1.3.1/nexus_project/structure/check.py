import impmagic

#Controle que la clé sont présente et qu'elles respectent les regex
@impmagic.loader(
    {'module':'toml_nxs.toml', 'submodule':['TOML'], 'as':'TOMLnxs'},
    {'module':'template.toml_format', 'submodule':['DEFAULT_TOML']},
    {'module':'re', 'submodule':['match']},
    {'module':'app.display', 'submodule':['logs']}
)
def is_nexus_project(command, nolog=False):
	if in_project():
		parameter_mandatory = []
		if command=='run':
			parameter_mandatory = ['projectname', 'mainfile']
		elif command=='version':
			parameter_mandatory = ['version']
		elif command=='project':
			parameter_mandatory = ['project']
		elif command=='lock':
			parameter_mandatory = ['dependencies']
		elif command=='env':
			parameter_mandatory = ['projectname']
		elif command=='add' or command=='remove':
			parameter_mandatory = ['dependencies', 'package', 'include', 'include_files']
		elif command=='check':
			parameter_mandatory = ['dependencies', 'mainfile', 'package', 'include']
		elif command=='backup':
			parameter_mandatory = ['projectname','include_files','license_file','readme']
		elif command=='pack' or command=='compile':
			parameter_mandatory = ['version','mainfile','projectname']
		elif command=='pack':
			parameter_mandatory = ['projectname','version','description','authors','maintainers','keywords', 'classifiers','platforms','homepage','documentation','changelog']

		tfile = TOMLnxs(get_nexus_file())
		tfile.load_doc()

		for param in parameter_mandatory:
			res = tfile.get_key(DEFAULT_TOML[param]['name'], DEFAULT_TOML[param]['section'])
			if res==None:
				logs(f"Clé {DEFAULT_TOML[param]['name']} non trouvée", "warning")
				return False
			else:
				if "regex" in DEFAULT_TOML[param] and not isinstance(res, dict):
					if not match(DEFAULT_TOML[param]["regex"], res):
						logs(f"Clé {DEFAULT_TOML[param]['name']} non valide", "warning")
						return False
		return True
	else:
		if not nolog:
			logs("Vous n'êtes pas dans un projet","critical")
	return False

@impmagic.loader(
    {'module':'os.path', 'submodule':['abspath', 'exists', 'join', 'dirname']},
    {'module':'app.display', 'submodule':['logs']},
    {'module':'sys', 'submodule':['exit']},
    {'module':'template', 'submodule':['default_conf']},
    {'module':'__main__'} 
)
def get_nexus_file(log=True, _break=True):
	deep = __main__.nxs.conf.load(val='project.deep_search', section='',default=default_conf.project_deep_search)

	folder = abspath('.')

	i=0
	while i!=deep:
		file = join(folder,'nexus.toml')
		if exists(file):
			return file
		else:
			folder = dirname(folder)
		i+=1
	
	if log:
		logs("Aucun fichier nexus.toml trouvé", "critical")

	if _break:
		exit()


@impmagic.loader(
    {'module':'os.path', 'submodule':['abspath', 'exists', 'join', 'dirname']},
    {'module':'template', 'submodule':['default_conf']},
    {'module':'__main__'}
)
def in_project(deep = None):
	if deep==None:
		deep = __main__.nxs.conf.load(val='project.deep_search', section='',default=default_conf.project_deep_search)

	folder = abspath('.')

	i=0
	while i!=deep:
		file = join(folder,'nexus.toml')
		if exists(file):
			return True
		else:
			folder = dirname(folder)
		i+=1
	
	return False


@impmagic.loader(
    {'module':'os.path', 'submodule':['abspath', 'exists', 'join', 'dirname']},
    {'module':'template', 'submodule':['default_conf']},
    {'module':'__main__'}
)
def get_root_project(deep = None):
	if deep==None:
		deep = __main__.nxs.conf.load(val='project.deep_search', section='',default=default_conf.project_deep_search)

	folder = abspath('.')

	i=0
	while i!=deep:
		file = join(folder,'nexus.toml')
		if exists(file):
			return folder
		else:
			folder = dirname(folder)
		i+=1
	
	return False
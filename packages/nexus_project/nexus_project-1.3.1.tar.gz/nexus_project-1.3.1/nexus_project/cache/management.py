import impmagic
import __main__

@impmagic.loader(
	{'module':'json'},
	{'module':'app.display', 'submodule':['logs']},
	{'module':'cache.sqlite', 'submodule':['Cache']},
	{'module': 'template', 'submodule': ['default_conf']},
	{'module': 'sys_nxs.host', 'submodule': ['path_rep']},
	{'module':'os.path', 'submodule': ['join', 'expanduser', 'exists', 'isfile']}
)
def list_cache():
	cachefile = join(expanduser(__main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)).replace(path_rep[1], path_rep[0]), 'repo_cache.db')

	if exists(cachefile) and isfile(cachefile):
		dbcache = Cache(cachefile)
		result = {}

		for lines in dbcache.select_all():
			line = []

			for index in ['name', 'version', 'requires_python', 'requires_dist', 'summary', 'author', 'maintainer', 'license', 'home_page', 'vulnerabilities']:
				try:
					converted = json.loads(getattr(lines, index))
					setattr(lines, index, converted)
				except Exception as err:
					pass

			if lines.name not in result:
				result[str(lines.name)] = [lines.version]
			else:
				result[str(lines.name)].append(lines.version)

		sorted_keys = sorted(result.keys())
		sorted_data = {key: result[key] for key in sorted_keys}

		return sorted_data
	else:
		logs("Cache vide")
		return {}


@impmagic.loader(
	{'module':'json'},
	{'module':'app.display', 'submodule':['logs']},
	{'module':'cache.sqlite', 'submodule':['Cache']},
	{'module': 'template', 'submodule': ['default_conf']},
	{'module': 'sys_nxs.host', 'submodule': ['path_rep']},
	{'module':'os.path', 'submodule': ['join', 'expanduser', 'exists', 'isfile']},
	{'module':'re'},
	{'module':'template', 'submodule':['regex']},
)
def remove_from_cache(package_name):
	cachefile = join(expanduser(__main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)).replace(path_rep[1], path_rep[0]), 'repo_cache.db')

	if exists(cachefile) and isfile(cachefile):
		dbcache = Cache(cachefile)

		package_compiled = re.compile(regex.info_package_regex)
		package_match = package_compiled.search(package_name)

		if package_match!=None:
			package_name = package_match.group('name')
			operator = package_match.group('operator')
			version = package_match.group('version')

			if version!=None:
				if operator:
					dbcache.remove_package(package_name, version, operator)
				else:
					dbcache.remove_package(package_name, version)
			else:
				dbcache.remove_package(package_name)
		else:
			logs("Format de nom invalide", "critical")
	else:
		logs("Cache vide")
		return {}


@impmagic.loader(
	{'module':'re'},
	{'module':'template', 'submodule':['regex']},
	{'module':'app.display', 'submodule': ['logs']},
	{'module':'package.package', 'submodule': ['get_package_information', 'get_versionlist_package', 'compare_version']},
	{'module':'cache.sqlite', 'submodule':['Cache']},
	{'module': 'template', 'submodule': ['default_conf']},
	{'module':'os.path', 'submodule': ['join', 'expanduser']},
	{'module': 'sys_nxs.host', 'submodule': ['path_rep']},
)
def add_to_cache(package_name):
	cachefile = join(expanduser(__main__.nxs.conf.load(val='cache-dir', section='',default=default_conf.cache_dir)).replace(path_rep[1], path_rep[0]), 'repo_cache.db')
	dbcache = Cache(cachefile)

	package_compiled = re.compile(regex.info_package_regex)
	package_match = package_compiled.search(package_name)

	if package_match!=None:
		package_name = package_match.group('name')
		operator = package_match.group('operator')
		version = package_match.group('version')

		versionlist = get_versionlist_package(package_name)

		version_added = []

		#Stocke les versions dans le cache pour éviter d'afficher un message pour les versions déjà en cache
		version_already_in_cache = []
		for line in dbcache.search(package_name):
			version_already_in_cache.append(line['version'])

		
		if version!=None:
			if operator:	
				for vers in versionlist:
					if compare_version(vers, operator, version):
						get_package_information(package_name, vers)
						version_added.append(vers)
			else:
				get_package_information(package_name, version)
				version_added.append(version)
		else:
			for vers in versionlist:
				get_package_information(package_name, vers)
				version_added.append(vers)

		if len(version_added):
			for vers in version_added:
				if vers not in version_already_in_cache:
					result = dbcache.search(package_name, version=vers)

					if result:
						logs(f"Ajout de {package_name}=={vers}")

		else:
			logs("Aucune version trouvée")
	else:
		logs("Format de nom invalide", "critical")
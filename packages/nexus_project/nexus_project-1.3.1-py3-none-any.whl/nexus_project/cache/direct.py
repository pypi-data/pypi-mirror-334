import __main__
import impmagic

class DirectCache:
	def __init__(self):
		if not hasattr(__main__.nxs, 'cache'):
			__main__.nxs.cache = {}

	def get(self, type_cache, name):
		name = name.lower().replace("-","_")

		if type_cache not in __main__.nxs.cache.keys():
			return None
		else:
			if name in __main__.nxs.cache[type_cache]:
				return __main__.nxs.cache[type_cache][name]
			else:
				return None

	def set(self, type_cache, name, content):
		name = name.lower().replace("-","_")

		if type_cache not in __main__.nxs.cache.keys():
			__main__.nxs.cache[type_cache] = {}

		__main__.nxs.cache[type_cache][name] = content
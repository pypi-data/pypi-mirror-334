import sqlite3
import json
import os
import impmagic

class Cache:
    @impmagic.loader(
        {'module': 'cache.model','submodule': ['Table']},
        {'module': 'pony.orm','submodule': ['Database']},
        {'module': 'os.path','submodule': ['exists', 'isdir', 'dirname']},
        {'module': 'os','submodule': ['makedirs']},
    )
    def __init__(self, nom_base_de_donnees):
        self.orm = Database()
        Table(self.orm)

        if not exists(dirname(nom_base_de_donnees)) or not isdir(dirname(nom_base_de_donnees)):
            makedirs(dirname(nom_base_de_donnees))

        self.orm.bind(provider='sqlite', filename=nom_base_de_donnees, create_db=True)
        self.orm.generate_mapping(create_tables=True)


    @impmagic.loader(
        {'module':'app.display', 'submodule': ['logs']},
        {'module': 'pony.orm','submodule': ['db_session']},
    )
    def add(self, element):
        try:
            with db_session:
                self.orm.PackageCache(**element)

                return True
        except Exception as err:
            logs(err, "critical")
            return False


    @impmagic.loader(
        {'module': 'pony.orm','submodule': ['db_session']},
    )
    def remove_by_id(self, element_id):
        try:
            with db_session:
                element = self.orm.PackageCache.get(id=element_id)
                if element:
                    element.delete()
                    return True
                return False

        except Exception as err:
            logs(err, "critical")
            return False


    @impmagic.loader(
        {'module': 'pony.orm','submodule': ['db_session', 'select']},
        {'module':'app.display', 'submodule': ['logs']},
        {'module':'package.package', 'submodule': ['compare_version']}, 
    )
    def get_package_from_cache(self, package_name, version, operator):
        try:
            query = select(element for element in self.orm.PackageCache)

            query = query.filter(lambda element: element.name == package_name.lower().replace("-", "_"))

            if version and operator:
                results = []
                for element in query:
                    if compare_version(element.version, operator, version):
                        results.append(element)
                return results
            else:
                return query[:]

        except Exception as err:
            logs(err, "critical")
            return []

    @impmagic.loader(
        {'module': 'pony.orm','submodule': ['db_session', 'select']},
        {'module':'app.display', 'submodule': ['logs']},
    )
    def remove_package(self, package_name, version=None, operator="=="):
        try:
            with db_session:
                extract = self.get_package_from_cache(package_name, version, operator)

                if extract:
                    for line in extract:
                        line.delete()
                        logs(f"Package {package_name}=={line.version} supprimé")

                else:
                    logs("Aucun élément trouvé")

        except Exception as err:
            logs(err, "critical")
            return False


    @impmagic.loader(
        {'module': 'json'},
        {'module': 'pony.orm','submodule': ['db_session', 'select']},
        {'module':'app.display', 'submodule': ['logs']},
    )
    def search(self, package_name, version=None, operator="=="):
        result = []

        with db_session:
            extract = self.get_package_from_cache(package_name, version, operator)

        if extract:
            for line in extract:
                for index in ['name', 'version', 'requires_python', 'requires_dist', 'summary', 'author', 'maintainer', 'license', 'home_page', 'vulnerabilities']:
                    try:
                        converted = json.loads(getattr(line, index))
                        setattr(line, index, converted)
                    except Exception as err:
                        pass

                insert = {'name': line.name,'version': line.version,'requires_python': line.requires_python,'requires_dist': line.requires_dist,'summary': line.summary,'author': line.author,'maintainer': line.maintainer,'license': line.license,'home_page': line.home_page, 'vulnerabilities': line.vulnerabilities}
                result.append(insert)

        
        return result


    @impmagic.loader(
        {'module': 'pony.orm','submodule': ['db_session', 'select']},
        {'module':'app.display', 'submodule': ['logs']},
    )
    def select_all(self):
        try:
            with db_session:
                #log = __main__.orm_deploy.Argos_Server.get(name_server=self.hostname)
                query = select(log for log in self.orm.PackageCache)[:]
                return query
        except Exception as err:
            logs(err, "critical")
            return []

from pony.orm import Required, Optional, PrimaryKey


def Table(db, type_db="sqlite"):
    #Modèle pour le stockage de logs des workers de mise à jour
    class PackageCache(db.Entity):
        id = PrimaryKey(int, auto=True)
        name = Required(str)
        version = Required(str)
        requires_python = Optional(str)
        requires_dist = Optional(str)
        summary = Optional(str)
        author = Optional(str)
        maintainer = Optional(str)
        license = Optional(str)
        home_page = Optional(str)
        vulnerabilities = Optional(str)

import impmagic

def add_key(dictionary, key_string, value):
    # Séparation des différents éléments du string
    elements = key_string.split(".")
    # Ajout de la clé au dictionnaire à l'aide de la méthode update
    current_dict = dictionary
    for element in elements[:-1]:
        current_dict = current_dict.setdefault(element, {})
    current_dict.update({elements[-1]: value})
    return dictionary


class TOML:
    def __init__(self, file):
        self.file = file

    @impmagic.loader(
        {'module':'tomlkit'},
        {'module':'os.path', 'submodule':['exists']}
    )
    def load_doc(self):
        if exists(self.file):
            with open(self.file, 'r') as f:
                self.doc = tomlkit.parse(f.read())
        else:
            self.doc = tomlkit.document()

    def get_key(self, key, section=None):
        if hasattr(self, "doc"):
            if section is None:
                #Cas où section est None (éléments sans section)
                return self.doc.get(key, None)

            #return self.doc[section].get(key, None)

            section_levels = section.split('.')
    
            # Parcours de chaque niveau de section
            current_section = self.doc
            for level in section_levels:
                # Récupération de la sous-section correspondante
                current_section = current_section.get(level, None)
                if current_section is None:
                    # Si la sous-section n'existe pas, on retourne None
                    return None
            
            # Récupération de la valeur de la clé dans la section cible
            return current_section.get(key, None)

        return None

    @impmagic.loader(
        {'module':'tomlkit'}
    )
    def dict_to_toml(self, data):
        self.doc = tomlkit.document()

        for key, value in data.items():
            if isinstance(value, dict):
                table = tomlkit.table()
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, dict):
                        subtable = tomlkit.table()
                        for subsubkey, subsubvalue in subvalue.items():
                            subtable.add(subsubkey, subsubvalue)
                        table.add(subkey, subtable)
                    else:
                        table.add(subkey, subvalue)
                self.doc.add(key, table)
            else:
                self.doc.add(key, value)

        self.write(self.doc)

    @impmagic.loader(
        {'module':'template.toml_format', 'submodule':['DEFAULT_TOML']},
        {'module':'structure.license', 'submodule':['licenses_availables']},
        {'module':'re', 'submodule':['match']}
    )
    def new(self, data_user):
        data = {}
        for block in DEFAULT_TOML:
            value = None
            if block in data_user:
                #Condition spécial pour les licenses
                if block=="license":
                    if licenses_availables(data_user[block]):
                        value = data_user[block]
                else:
                    if isinstance(data_user[block], DEFAULT_TOML[block]["type"]):
                        if DEFAULT_TOML[block]["type"]==str and "regex" in DEFAULT_TOML[block]:
                            if match(DEFAULT_TOML[block]["regex"], data_user[block]):
                                value = data_user[block]
                        else:
                            value = data_user[block]

            if value==None:
                value = DEFAULT_TOML[block]["default_value"]

            data = add_key(data, DEFAULT_TOML[block]["section"]+"."+DEFAULT_TOML[block]["name"], value)

        #data = ast.literal_eval(TOML_TEMPLATE.format(**data))

        self.dict_to_toml(data)

    def edit_key(self, key, value, section):
        if hasattr(self, 'doc'):
            self.load_doc()

        sections = section.split('.')  
        current_section = self.doc
        for s in sections:
            if s not in current_section:
                current_section.add(s, {})
            current_section = current_section[s]
        if key not in current_section:
            current_section.add(key, 'default value')

        """
        # Vérification de l'existence de la section et de la clé
        if section not in self.doc:
            self.doc.add(section, {})
        if key not in self.doc[section]:
            self.doc[section].add(key, 'default value')

        # Modification de la valeur de la clé
        self.doc[section][key] = value
        """
        current_section[key] = value

        self.write(self.doc)

    def delete_key(self, key, section):
        if hasattr(self, 'doc'):
            self.load_doc()

        sections = section.split('.')
        current_section = self.doc

        # Parcours des niveaux de section
        for s in sections:
            # Vérification de l'existence de la section
            if s not in current_section:
                return False  # La section n'existe pas, retourne False
            current_section = current_section[s]

        # Vérification de l'existence de la clé
        if key not in current_section:
            return False  # La clé n'existe pas, retourne False

        # Suppression de la clé
        del current_section[key]

        self.write(self.doc)  # Écriture des modifications dans le fichier
        return True


    def write(self, data):
        data = data.as_string()

        while "\n\n\n" in data:
            data = data.replace("\n\n\n","\n")

        if "]\n[" in data:
            data = data.replace("]\n[","]\n\n[")

        with open(self.file, 'w') as f:
            f.write(data)


def read_data(data, pattern=""):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) or isinstance(value, dict):
                print(f"{pattern}{key}:")
                read_data(value, pattern+"  ")
            elif isinstance(value, str):
                print(f"{pattern}{key}: {value}")
    elif isinstance(data, list):
        print(f"{pattern}{list(data)}")
        """
        for element in data:
            if isinstance(element, list) or isinstance(element, dict):
                read_data(element, pattern+"  ")
            elif isinstance(element, str):
                print(f"{pattern}{element}")
        """
    elif isinstance(data, str):
        print(f"{pattern}{data}")
    elif isinstance(data, int) or isinstance(data, float):
        print(f"{pattern}{data}")

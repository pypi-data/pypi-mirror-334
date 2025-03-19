TOML_TEMPLATE= """\
{{
    "project": {{
        "name": "{projectname}",
        "version": "{version}",
        "description": "{description}",
        "mainfile": "{mainfile}",
        "requires-python": "{pythonversion}",
        "metadata": {{
            "authors": {authors},
            "maintainers": {maintainers},
            "readme": "{readme}",
            "changelog": "{changelog}",
            "license": "{license}",
            "license_file": "{license_file}",
            "keywords": {keywords},
            "classifiers": {classifiers},
            "copyright": "{copyright}"
        }},
        "dependencies": {{
            "windows": {dependencies_win},
            "linux": {dependencies_linux},
        }},
        "build": {{
            "packages": {package},
            "includes": {include},
            "excludes": {exclude},
            "include_files": {include},
            "optimize": {optimize},
            "no_compress": {compress},
            "GUI": {gui},
            "icon": "{icon}"
        }},
        "wheel": {{
            "platforms": "{platforms}",
            "entry_points": {{
                "console_scripts": "{console_scripts}"
            }}
        }},
        "urls": {{
            "homepage": "{homepage}",
            "documentation": "{documentation}",
            "changelog": "{changelog}"
        }}
    }}
}}
"""
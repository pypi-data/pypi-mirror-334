import impmagic

@impmagic.loader(
    {'module': 'glob', 'submodule': ['glob']},
    {'module': 'os.path', 'submodule': ['exists', 'join', 'isfile', 'isdir']}
)
def construct_pack_data(element, pack_data, codefolder, deep=False):
      file = join(codefolder, element)
      if deep==False and exists(file+".py") and isfile(file+".py"):
            pack_data.append(file.replace(codefolder+path_rep[0],'')+".py")
      elif deep==False and exists(file+".pyw") and isfile(file+".pyw"):
            pack_data.append(file.replace(codefolder+path_rep[0],'')+".pyw")
      elif exists(join(codefolder, element)):
            pack_data.append(element+path_rep[0]+"*")
            for content in glob(join(codefolder, element)+path_rep[0]+"*"):
                  if not content.endswith('__pycache__') and isdir(content):
                        pack_data = construct_pack_data(content.replace(codefolder+path_rep[0],''), pack_data, codefolder, deep=True)
      return pack_data


def construct_platform(dictionary):
      list_package = []
      for package, version in dictionary.items():
            if version!="N.A":
                  list_package.append(package+version)
            else:
                  list_package.append(package)

      return list_package

@impmagic.loader(
    {'module': 'setuptools'},
    {'module': 'os', 'submodule': ['chdir']},
    {'module': 'os', 'submodule': ['name'], 'as':'system_name'},
    {'module': 'os.path', 'submodule': ['exists', 'join', 'isfile']},
    {'module': 'sys'},
    {'module': 'sys_nxs.host', 'submodule': ['path_rep']},
    {'module': 'template.regex', 'submodule': ['author_regex']},
    {'module': 're', 'submodule': ['match']}
)
def build(tfile, projectfolder, version=None, typefile="bdist_wheel", dry_run=False):
      projectname = tfile.get_key('name','project')
      ## README FILE
      long_desc = tfile.get_key('readme','project.metadata')
      if long_desc!="" and exists(long_desc):
            long_desc = open(join(projectfolder, long_desc)).read()
            description_type = 'text/markdown'
      else:
            long_desc = None
            description_type = None

      ## URL INFORMATION
      url = tfile.get_key('homepage','project.urls')
      if url=="":
            url = None

      project_urls = {}
      doc = tfile.get_key('documentation','project.urls')
      if doc!="":
            project_urls['Documentation'] = doc

      changelog = tfile.get_key('changelog','project.urls')
      if changelog!="":
            project_urls['Changelog'] = changelog

      if len(project_urls)==0:
            project_urls={}

      #OTHER OPTIONS
      console_script = tfile.get_key('console_scripts','project.wheel.entry_points')
      if len(console_script)==0:
            entry_points = None
      else:
            entry_points = {
              'console_scripts': console_script,
            }

      platform = tfile.get_key('platforms','project.wheel')
      if platform=="":
            platform = "ALL"

      license = tfile.get_key('license','project.metadata')
      if license=="":
            license=None


      author = tfile.get_key('authors','project.metadata')
      if len(author)>0:
            new = ""
            for element in author:
                  if match(author_regex, element):
                        if new=="":
                              new = element
                        else:
                              new += ", "+element
            author = new
      else: 
            author=None

      maintainer = tfile.get_key('maintainers','project.metadata')
      if len(maintainer)>0:
            new = ""
            for element in maintainer:
                  if match(author_regex, element):
                        if new=="":
                              new = element
                        else:
                              new += ", "+element
            maintainer = new
      else: 
            maintainer=None
      
      includes = tfile.get_key("includes", "project.build")
      include_files = tfile.get_key("include_files", "project.build")
      includable = includes+include_files
      codefolder = join(projectfolder,tfile.get_key('name','project'))
      pack_data = []
      for element in includable:
            pack_data = construct_pack_data(element, pack_data, codefolder)

      if len(pack_data)==0:
            package_data = {}
      else:
            package_data = {}
            package_data[projectname] = pack_data

      if version=="windows":
            platform="win_amd64"
      elif version=="linux":
            platform="manylinux2010_x86_64"

      install_requires = tfile.get_key('dependencies','project').copy() if tfile.get_key('dependencies','project') is not None else None

      if install_requires==None or len(install_requires)==0:
            install_requires=None
      else:
            if version=='windows' and 'windows' in install_requires:
                  requires_platform = install_requires.copy()
                  for element, element_version in install_requires['windows'].items():
                        if element not in install_requires:
                              requires_platform[element] = element_version
                  install_requires = requires_platform

            elif version=='linux' and 'linux' in install_requires:
                  requires_platform = install_requires.copy()
                  for element, element_version in install_requires['linux'].items():
                        if element not in install_requires:
                              requires_platform[element] = element_version
                  install_requires = requires_platform

            if "windows" in install_requires:
                  install_requires.remove('windows')
            if "linux" in install_requires:
                  install_requires.remove('linux')


      chdir(projectfolder)
      #exit()
      #setup.py sdist bdist_wheel --dist-dir=dist
      argument = ['pack.py', typefile, "--dist-dir=dist"]
      if platform!="ALL":
            argument.append("--plat-name="+platform)

      sys.argv = argument

      if install_requires!=None:
            install_requires = construct_platform(install_requires)


      if dry_run:
            from app.display import cat_setup

            if long_desc!=None:
                  long_desc = "-- CONTENT FILE --"

            setup = {'name':projectname,
                  'version': tfile.get_key('version','project'),
                  'author': author,
                  'maintainer': maintainer,
                  'keywords': " ".join(tfile.get_key('keywords','project.metadata')),
                  'classifiers': tfile.get_key('classifiers','project.metadata'),
                  'packages': [tfile.get_key('name','project')],
                  'description': tfile.get_key('description','project'),
                  'long_description': long_desc,
                  'long_description_content_type': description_type,
                  'url': url,
                  'project_urls': project_urls,
                  'entry_points': entry_points,
                  'install_requires': install_requires,
                  'package_data': package_data,
                  'platforms':platform,
                  'license':license}

            cat_setup(setup)

      else:
            setuptools.setup(name=projectname,
                  version=tfile.get_key('version','project'),
                  author=author,
                  maintainer=maintainer,
                  keywords = " ".join(tfile.get_key('keywords','project.metadata')),
                  classifiers = tfile.get_key('classifiers','project.metadata'),
                  packages=[tfile.get_key('name','project')],
                  description=tfile.get_key('description','project'),
                  long_description = long_desc,
                  long_description_content_type=description_type,
                  url = url,
                  project_urls=project_urls,
                  entry_points = entry_points,
                  install_requires = install_requires,
                  package_data=package_data,
                  platforms = platform,
                  license=license)



@impmagic.loader(
    {'module': 'setuptools', 'submodule': ['setup']},
    {'module': 'sys'}
)
def build_fake(projectname, foldername):
      #setup.py sdist bdist_wheel --dist-dir=dist
      sys.argv = ["pack.py", "sdist", "--dist-dir="+foldername]
      setup(name=projectname,
            version="0.0.0")
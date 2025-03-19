import impmagic

class Repo:
	@impmagic.loader(
		{'module':'pygit2', 'submodule': ['Repository', 'Signature', 'init_repository']},
		{'module':'os.path', 'submodule': ['abspath']}
	)
	def __init__(self, repo_path, branch_name=None, create=True):
		self.repo_path = abspath(repo_path)

		try:
			self.repo = Repository(self.repo_path)
		except:
			if create:
				self.repo = init_repository(self.repo_path)
			else:
				return

		try:
			self.author = self.repo.default_signature
			self.committer = self.repo.default_signature
		except:
			self.author = Signature("nxs_default", "nxs_default@example.com")
			self.committer = Signature("nxs_default", "nxs_default@example.com")

		#Si nouveau projet, initialiser la branche master
		if create and branch_name==None:
			self.init_master()

		if branch_name==None:
			branch_name = self.get_active_branch()

		if branch_name not in self.list_branch():
			if not len(list(self.repo.references)):
				self.init_master()
			
			if branch_name!="master":
				self.add_branch(branch_name)
		
		self.branch_name = branch_name

	def commit_exist(self, commit_id):
		try:
			self.repo.revparse_single(commit_id)
			return True
		except:
			return False

	#Liste les branches disponibles
	def list_branch(self, local=False, remote=False):
		if (not local and not remote) or (local and remote):
			return list(self.repo.branches)

		if local and not remote:
			return list(self.repo.branches.local)

		if remote and not local:
			return list(self.repo.branches.remote)

	#Récupérer la liste des branches avec les informations
	@impmagic.loader(
		{'module':'pygit2'},
		{'module':'datetime', 'submodule': ['datetime']}
	)
	def get_branch_info(self, local=False, remote=False):
		infos = {}
		active_branch = self.get_active_branch()

		for branch_name in self.list_branch(local, remote):
			branch = self.repo.branches[branch_name]
			commit = branch.peel(pygit2.Commit)

			if active_branch==branch_name:
				active = True
			else:
				active = False

			infos[branch_name] = {
				'last_commit_id': commit.hex,
				'last_commit_message': commit.message,
				'last_commit_author': f'{commit.author.name} <{commit.author.email}>',
				'last_commit_committer': f'{commit.committer.name} <{commit.committer.email}>',
				'last_commit_date': str(datetime.fromtimestamp(commit.commit_time)),
				'parents': commit.parents,
				'parent_ids': commit.parent_ids,
				'active_branch': active,
			}

		return infos

	#Récupérer la liste des commits
	@impmagic.loader(
		{'module':'pygit2'},
		{'module':'datetime', 'submodule': ['datetime']}
	)
	def get_commit_info(self):
		infos = {}

		# Parcourir tous les commits du dépôt
		for commit in self.repo.walk(self.repo.head.target, pygit2.GIT_SORT_TIME | pygit2.GIT_SORT_TOPOLOGICAL):
			# Obtenir les références associées au commit
			commit_refs = []
			for ref_name in self.repo.listall_references():
				ref = self.repo.lookup_reference(ref_name)
				if ref.target.hex == commit.id.hex:
					commit_refs.append(ref_name)
			commit_refs = ', '.join(commit_refs)


			# Afficher les informations du commit
			commit_refs = commit_refs.replace('refs/heads/', '')

			infos[commit.hex] = {
				'commit_id': commit.id,
				'commit_hash': str(commit.id)[:7],
				'commit_message': commit.message,
				'commit_message_resume': commit.message.strip().split('\n')[0],
				'commit_author': f'{commit.author.name} <{commit.author.email}>',
				'commit_committer': f'{commit.committer.name} <{commit.committer.email}>',
				'commit_time': str(datetime.fromtimestamp(commit.commit_time)),
				'commit_refs': commit_refs,
				'parent_ids': commit.parent_ids,
			}

		return infos

	@impmagic.loader(
		{'module':'pygit2'},
		{'module':'app.display', 'submodule': ['print_nxs']}
	)
	def log(self, oneline=False):
		commit = self.repo.head.peel(pygit2.Commit)

		for commit, info in self.get_commit_info().items():
			if info['commit_id'] == self.repo.head.target:
				info['commit_refs'] = "HEAD -> "+info['commit_refs']

			if oneline:
				if len(info['commit_refs']):
					print(f"{info['commit_hash']} ({info['commit_refs']}) {info['commit_message_resume']}")
				else:
					print(f"{info['commit_hash']} {info['commit_message_resume']}")
			else:
				if len(info['commit_refs']):
					print(f"\ncommit: {info['commit_id']} ({info['commit_refs']})")
				else:
					print(f"\ncommit: {info['commit_id']}")

				if len(info['parent_ids']):
					print(f"Parents: {', '.join([str(element)[:7] for element in info['parent_ids']])}")

				print(f"Author: {info['commit_author']}")

				if info['commit_author']!=info['commit_committer']:
					print(f"Committer: {info['commit_committer']}")

				print(f"Date: {info['commit_time']}")

				print(f"Message: {info['commit_message']}")


	#Récupérer le nom de la branche active
	def get_active_branch(self):
		return self.repo.head.shorthand

	#Création d'un ref
	def add_ref(self, branch_name):
		tree = self.repo.TreeBuilder().write()

		commit_oid = self.repo.create_commit(None, self.author, self.committer, "Commit initial", tree, [])
		branch_ref = self.repo.create_reference(self.get_ref(branch_name), commit_oid)

	#Renvoie la référence de branche
	def get_ref(self, branch_name):
		return f"refs/heads/{branch_name}"

	#Création de la première branche
	def init_master(self):
		tree = self.repo.TreeBuilder().write()

		# Créer le commit initial avec l'arbre vide
		commit_oid = self.repo.create_commit('HEAD', self.author, self.committer, "Commit initial", tree, [])


	#Ajoute une branche au repo (à partir du master, d'une autre branche ou d'un commit spécifique)
	@impmagic.loader(
		{'module':'pygit2'},
		{'module':'app.display', 'submodule': ['logs']}
	)
	def add_branch(self, branch_name, source_branch=None, commit_id='HEAD'):
		if source_branch!=None and not self.get_active_branch()==source_branch:
			status_code = self.switch_branch(source_branch)
			if not status_code:
				return

		if branch_name in self.list_branch():
			logs(f"La branche {branch_name} existe déjà", "error")
			return False

		if not self.commit_exist(commit_id):
			logs("Commit ID invalid", "error")
			exit()

		try:
			commit = self.repo.revparse_single(commit_id).peel(pygit2.Commit)
			self.repo.create_branch(branch_name, commit)
			return True
		except Exception as err:
			logs(err, "error")
			return False

	#Supprimer une branche au repo
	@impmagic.loader(
		{'module':'app.display', 'submodule': ['logs']}
	)
	def delete_branch(self, branch_name):
		self.check_branch(branch_name)
		try:
			self.repo.branches.delete(branch_name)
			return True
		except Exception as err:
			logs(err, "error")
			return False

	#Switch sur une nouvelle branche
	@impmagic.loader(
		{'module':'app.display', 'submodule': ['logs']}
	)
	def switch_branch(self, branch_name, create=False):
		if branch_name in self.repo.branches:
			self.repo.checkout(self.get_ref(branch_name))
			self.branch_name = branch_name
			return True
		elif branch_name not in self.repo.branches:
			if create:
				logs(f"Création de la branche {branch_name}", "info")
				self.add_branch(branch_name)
				self.repo.checkout(self.get_ref(branch_name))
				self.branch_name = branch_name
				return True
			else:
				logs(f"La branche {branch_name} n'existe pas", "error")
				return False

	#Renommer une branche
	@impmagic.loader(
		{'module':'app.display', 'submodule': ['logs']}
	)
	def rename_branch(self, branch_name, new_branch_name):
		self.check_branch(branch_name)

		if new_branch_name in self.list_branch():
			logs(f"La branche {new_branch_name} existe déjà", "error")

		try:
			ref = self.repo.lookup_reference(self.get_ref(branch_name))
			ref.rename(self.get_ref(new_branch_name))
			return True
		except Exception as err:
			logs(err, "error")
			return False

	#Fusionner deux branches
	@impmagic.loader(
		{'module':'pygit2'},
		{'module':'app.display', 'submodule': ['logs']}
	)
	def merge_branch(self, source_branch, target_branch=None):
		try:
			self.check_branch(source_branch)

			if not target_branch:
				target_branch = self.get_active_branch()

			if not self.get_active_branch()==target_branch:
				status_code = self.switch_branch(target_branch)
				if not status_code:
					return

			source_ref = self.repo.branches[source_branch]

			source_commit = source_ref.peel(pygit2.Commit)

			index = self.repo.merge(source_commit.id)

			# Créer un nouvel objet de commit avec l'index fusionné
			signature = self.author
			merge_commit_id = self.repo.create_commit(
				self.get_ref(target_branch), signature, signature,
				"Merge: {} into {}".format(source_branch, target_branch),
				self.repo.index.write_tree(), [self.repo.head.target, source_commit.id]
			)
			# Mettre à jour la branche cible pour pointer vers le nouveau commit de fusion
			#target_ref.set_target(merge_commit_id)
			return True
		except Exception as err:
			logs(err, "error")
			return False


	#Retourne le hash de l'objet
	@impmagic.loader(
		{'module':'os.path', 'submodule': ['exists', 'isfile']}
	)
	def hash_object(self, file_path):
		if exists(file_path) and isfile(file_path):
			with open(file_path, 'rb') as file:
				file_content = file.read()

				# Créer un objet blob à partir du contenu du fichier
				blob_oid = self.repo.create_blob(file_content)

				return str(blob_oid)

	#Vérifie si la branche existe, sinon quitte
	@impmagic.loader(
		{'module':'app.display', 'submodule': ['logs']}
	)
	def check_branch(self, branch_name):
		if branch_name not in self.list_branch():
			logs(f"La branche {branch_name} n'existe pas", "error")
			exit()

	#Afficher le statut du repo
	@impmagic.loader(
		{'module':'pygit2'},
		{'module':'app.display', 'submodule': ['print_nxs']}
	)
	def status(self):
		for name, branch in self.get_branch_info().items():
			if branch['active_branch']:
				print(f"Active branch: {name}")
				print(f"Last commit:")
				print(f"   Id:{branch['last_commit_id']}")
				if len(branch['parent_ids']):
					print(f"   Parents: {', '.join([str(element)[:7] for element in branch['parent_ids']])}")
				print(f"   Date: {branch['last_commit_date']}")
				print(f"   Author: {branch['last_commit_author']}")
				if branch['last_commit_author']!=branch['last_commit_committer']:
					print(f"   Committer: {branch['last_commit_committer']}")
				print(f"   Message: {branch['last_commit_message']}")


		status_file = {'modified': [], 'deleted': [], 'new': [], 'conflicted': [], 'not_commited': []}
		# Afficher les fichiers modifiés dans l'espace de travail
		status = self.repo.status()
		for file in status:
			if status[file] == pygit2.GIT_STATUS_WT_MODIFIED:
				status_file['modified'].append(file)

			elif status[file] == pygit2.GIT_STATUS_WT_DELETED:
				status_file['deleted'].append(file)

			elif status[file] == pygit2.GIT_STATUS_WT_NEW:
				status_file['new'].append(file)

			elif status[file] == pygit2.GIT_STATUS_CONFLICTED:
				status_file['conflicted'].append(file)

			elif status[file] == pygit2.GIT_STATUS_INDEX_NEW or status[file] == pygit2.GIT_STATUS_INDEX_MODIFIED:
				status_file['not_commited'].append(file)


		# Afficher les fichiers modifiés dans l'espace de travail
		if len(status_file['modified']):
			file = '\n   '.join(status_file['modified'])
			print(f"\nChanges not staged for commit:\n   {file}")

		# Afficher les fichiers supprimés dans l'espace de travail
		if len(status_file['deleted']):
			file = '\n   '.join(status_file['deleted'])
			print(f"\nDeleted files:\n   {file}")

		# Afficher les fichiers non suivis
		if len(status_file['new']):
			file = '\n   '.join(status_file['new'])
			print(f"\nUntracked files:\n   {file}")

		# Afficher les fichiers en conflit
		if len(status_file['conflicted']):
			file = '\n   '.join(status_file['conflicted'])
			print(f"\nConflicted files:\n   {file}")

		# Afficher les fichiers ajoutés à l'index
		if len(status_file['not_commited']):
			file = '\n   '.join(status_file['not_commited'])
			print(f"\nChanges to be committed:\n   {file}")



	#Ajoute à l'index l'ensemble des modifications et commit
	def git_add_and_commit(self, commit_message="", branch_name=None):
		if not branch_name:
			branch_name = self.branch_name

		self.check_branch(branch_name)

		try:
			# Ajouter tous les modifications à l'index
			self.repo.index.add_all()
			#Ecrit l'index
			self.repo.index.write()
		except Exception as err:
			logs(f"Indexation impossible: \n{err}", "error")
			return None


		#Lecture de l'arbre de l'index
		tree = self.repo.index.write_tree()

		#Obtention de l'objet ref de la branche
		branch_ref = self.repo.lookup_reference(self.get_ref(branch_name))

		#Obtention de l'objet commit de la branche
		branch_commit = self.repo[branch_ref.target]

		try:
			#Création du commit
			commit_oid = self.repo.create_commit(self.get_ref(branch_name), self.author, self.committer, commit_message, tree, [branch_commit.id])
		except Exception as err:
			logs(f"Commit impossible: \n{err}", "error")
			return None

		# Récupérer l'identifiant du nouveau commit
		commit = self.repo.get(commit_oid)
		
		return commit.hex

	#Restauration depuis un commit
	@impmagic.loader(
		{'module':'pygit2'},
		{'module':'app.display', 'submodule': ['logs']}
	)
	def reset(self, commit_id, mode="hard"):
		if not self.commit_exist(commit_id):
			logs("Commit ID invalid", "error")
			exit()

		mode_list = {"soft": pygit2.GIT_RESET_SOFT, "hard": pygit2.GIT_RESET_HARD, "mixed": pygit2.GIT_RESET_MIXED}
		if mode in mode_list:
			try:
				self.repo.reset(commit_id, mode_list[mode])
			except Exception as err:
				logs(err, "error")
		else:
			print("Mode invalid")


	#Restaurer un fichier spécifique
	@impmagic.loader(
		{'module':'os', 'submodule': ['getcwd', 'chdir']},
		{'module':'os.path', 'submodule': ['relpath', 'abspath', 'split']},
		{'module':'app.display', 'submodule': ['logs']}
	)
	def restore(self, file, dest=None, commit_id='HEAD'):
		if not self.commit_exist(commit_id):
			logs("Commit ID invalid", "error")
			exit()

		init = None
		if self.repo_path not in getcwd():
			logs("You are outside the repo folder. Moving to the root of the repo", "info")
			init = getcwd()
			chdir(self.repo_path)

		file_path = relpath(abspath(file), self.repo_path)

		# Obtenir le contenu du fichier à partir du commit
		commit = self.repo.revparse_single(commit_id)

		file_array = list(split(file))
		#Suppression du champ vide si on cherche pas dans un dossier
		if "" in file_array:
			file_array.remove('')
		blob = self.search_file_from_commit_tree(commit.tree, file_array)
		
		if init and dest:
			chdir(init)
			file_out = abspath(dest)
		elif dest:
			file_out = abspath(dest)
		else:
			file_out = file_path

		#Si on veut restaurer un dossier entier
		if isinstance(blob, pygit2.Tree):
			self.restore_folder(blob, file_out)
		else:
			if blob!=None:
				# Récupérer le contenu du blob
				content = self.repo[blob.id].data.decode('utf-8')
			else:
				logs(f"File {file_path} not found", "error")
				return False

			try:
				# Écrire le contenu du fichier dans l'arborescence de travail
				with open(file_out, 'w') as file:
					file.write(content)
			except Exception as err:
				logs(err, "error")
				return False

			return True

	#Recherche un fichier à travers l'arborescence d'un commit
	@impmagic.loader(
		{'module':'pygit2'}
	)
	def search_file_from_commit_tree(self, commit_tree, file_array):
		for entry in commit_tree:
			if entry.name==file_array[0]:
				file_array.pop(0)
				if len(file_array):
					if isinstance(entry, pygit2.Tree):
						return self.search_file_from_commit_tree(entry, file_array)
				else:
					return self.repo[entry.id]
		return None

	#Restauration d'un dossier git complet
	@impmagic.loader(
		{'module':'os', 'submodule': ['mkdir']},
		{'module':'os.path', 'submodule': ['join', 'exists', 'isdir']}
	)
	def restore_folder(self, commit_tree, dest):
		if not exists(dest) or not dest:
			mkdir(dest)

		for entry in commit_tree:
			if isinstance(entry, pygit2.Tree):
				self.restore_folder(entry, join(dest, entry.name))
			else:
				content = self.repo[entry.id].data.decode('utf-8')

				try:
					# Écrire le contenu du fichier dans l'arborescence de travail
					with open(join(dest, entry.name), 'w') as file:
						file.write(content)
				except Exception as err:
					logs(err, "error")
					return False
		return None

	@impmagic.loader(
		{'module':'os', 'submodule': ['getcwd', 'chdir']},
		{'module':'os.path', 'submodule': ['relpath', 'abspath']}
	)
	def tree(self, commit_id='HEAD'):
		if not self.commit_exist(commit_id):
			logs("Commit ID invalid", "error")
			exit()

		init = None
		if self.repo_path not in getcwd():
			logs("You are outside the repo folder. Moving to the root of the repo", "info")
			init = getcwd()
			chdir(self.repo_path)

		# Obtenir le contenu du fichier à partir du commit
		commit = self.repo.revparse_single(commit_id)

		self.tree_display(commit.tree)

	@impmagic.loader(
		{'module':'pygit2'}
	)
	def tree_display(self, commit_tree, lvl=0, arbo_display=[]):
		for i, entry in enumerate(commit_tree):
			if isinstance(entry, pygit2.Tree):
				print_pattern(i, len(commit_tree), arbo_display)
				print(entry.name)
				if i==len(commit_tree)-1:
					new_arbo = arbo_display+['   ']
				else:
					new_arbo = arbo_display+['│  ']

				self.tree_display(entry, lvl+1, arbo_display=new_arbo)
			else:
				print_pattern(entry.name, len(commit_tree), arbo_display)
				print(entry.name)

def print_pattern(index, max, arbo):
	arbo = "".join(arbo)
	if index==max-1:
		print(f"{arbo}└─", end="")
	else:
		print(f"{arbo}├─", end="")
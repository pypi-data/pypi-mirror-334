import impmagic


@impmagic.loader(
	{'module':'app.display', 'submodule': ['print_nxs']},
)
def print_pattern(index, max, arbo):
	arbo = "".join(arbo)
	if index==max-1:
		print_nxs(f"{arbo}└─", end="")
	else:
		print_nxs(f"{arbo}├─", end="")

	
@impmagic.loader(
	{'module':'app.display', 'submodule': ['print_nxs']},
)
def tree(content, lvl=0, arbo_display=["  "]):
	arbo = []

	for i, rep in content.items():
		if isinstance(rep, dict):
			arbo.append({'name': i, 'type': 'dir', 'content': rep})
		else:
			arbo.append({'name': i, 'type': 'file'})

	arbo = sorted(arbo, key=lambda x: x['name'])
	arbo = sorted(arbo, key=lambda x: x['type'])
	#arbo = sorted(arbo, key=lambda x: x['type'], reverse=True)
	
	for i, element in enumerate(arbo):
		if i==len(content)-1:
			print_nxs(f"{''.join(arbo_display)}└─", nojump=True)
		else:
			print_nxs(f"{''.join(arbo_display)}├─", nojump=True)

		if element['type']=='dir':
			print_nxs(f"{element['name']}", color='magenta')
			if i==len(content)-1:
				new_arbo = arbo_display+['   ']
			else:
				new_arbo = arbo_display+['│  ']

			tree(element['content'], lvl+1, arbo_display=new_arbo)
		else:
			print_nxs(f"{element['name']}", color='yellow')
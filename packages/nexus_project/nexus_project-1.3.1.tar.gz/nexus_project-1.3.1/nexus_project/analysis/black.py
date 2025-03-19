import impmagic

@impmagic.loader(
    {'module':'black', 'submodule': ['FileMode', 'format_file_contents']},
    {'module':'black.report', 'submodule': ['NothingChanged']},
    {'module':'difflib', 'submodule': ['unified_diff']},
    {'module':'os.path', 'submodule': ['exists']},
    {'module':'Levenshtein'}
)
def analyse(filename, apply=False, fileout=None, fast=False):
    if exists(filename):
        with open(filename) as f:
            content = f.read()

            try:
                mode = FileMode()
                out = format_file_contents(content, fast=fast, mode=mode)
                
                result = ""
                for line in unified_diff(content.splitlines(), out.splitlines(), lineterm='', fromfile=filename, tofile='ClearCode', n=1):
                    if line.startswith("@@") and line.endswith("@@"):
                        result+="\n\n"+line+"\n"
                    else:
                        result+=line+"\n"
                
                cat_content(result)
                
                distance = Levenshtein.distance(content, out)
                similarity = 1 - (distance / max(len(content), len(out)))
                print("\nTaux de similarité: {:.2f}%\n".format(similarity * 100))

            except NothingChanged:
                print(f"Fichier {filename} déjà optimisé\n")

        if apply:
            if fileout==None:
                fileout = filename

            with open(fileout, 'w') as f:
                f.write(out)

    else:
        print(f"Fichier {filename} introuvable\n")



@impmagic.loader(
    {'module': 'pygments.lexers','submodule': None, 'as':'lexers'},
    {'module': 'pygments.formatters','submodule': ['TerminalTrueColorFormatter']},
    {'module': 'pygments','submodule': ['highlight']}
)
def cat_content(file):
    BUF_SIZE = 65536

    try:
        lex = lexers.guess_lexer(file)
        formatter = TerminalTrueColorFormatter(style='monokai')
        
        print(highlight(file, lex, formatter),end="")
    except:
        data = file.decode('utf-8', 'ignore').translate({ord('\u0000'): None})
        print(data)
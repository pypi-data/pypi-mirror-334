import __main__
import impmagic

@impmagic.loader(
    {'module': 'zpp_color', 'submodule': ['fg', 'attr']}
)
def prompt(name, default=None):
	default_display = default
	if (isinstance(default_display, list) or isinstance(default_display, dict)) and len(default_display)==0:
		default_display = ""
	if default!=None:
		inp = input(f"{fg(__main__.color['cyan'])}{name} [{fg('green')}{default_display}{fg(__main__.color['cyan'])}]: {attr(0)}")
		if inp=="":
			return default
	else:
		inp = input(f"{fg(__main__.color['cyan'])}{name}: {attr(0)}")
	return inp


@impmagic.loader(
    {'module': 'pynput.keyboard', 'submodule': ['Controller']}
)
def form(name, default=None):
	print(f"{default}: ", end="")
	if default:
		keyboard = Controller()
		keyboard.type(default)
	return input()


@impmagic.loader(
    {'module': 'zpp_color', 'submodule': ['fg', 'attr']},
    {'module': 'datetime', 'submodule': ['datetime']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def logs(message, lvl='info', nodate=None):
	if __main__.nxs.conf.load(val='logs.display', section='',default=default_conf.logs_display):
		if lvl=='logs':
			color = __main__.color['light_gray']
		elif lvl=='info':
			color = __main__.color['cyan']
		elif lvl=='warning':
			color = __main__.color['yellow']
		elif lvl=='error':
			color = __main__.color['red']
		elif lvl=='critical':
			color = __main__.color['light_red']
		elif lvl=='valid' or lvl=='success':
			color = __main__.color['green']
		
		if nodate==False or (nodate==None and __main__.nxs.conf.load(val='logs.date', section='',default=default_conf.logs_date)):
			date = datetime.now().strftime("%Y/%m/%d - %H:%M:%S.%f")
			print(f"{fg(__main__.color['dark_gray'])}[{date}] - {attr(0)}{fg(color)}{message}{attr(0)}")
		else:
			print(f"{fg(color)}{message}{attr(0)}")

@impmagic.loader(
    {'module': 'zpp_color', 'submodule': ['fg', 'attr']}
)
def print_nxs(message, color=None, nojump=False):
	if color==None:
		color = __main__.color['cyan']
	
	if nojump:
		print(f"{fg(color)}{message}{attr(0)}", end="")
	else:
		print(f"{fg(color)}{message}{attr(0)}")


@impmagic.loader(
    {'module': 'tempfile','submodule': ['NamedTemporaryFile']},
    {'module': 'json','submodule': ['dumps']},
    {'module': 'pygments.lexers','submodule': None, 'as':'lexers'},
    {'module': 'pygments.formatters','submodule': ['TerminalTrueColorFormatter']},
    {'module': 'pygments','submodule': ['highlight']}
)
def cat_setup(content):
    BUF_SIZE = 65536

    f = NamedTemporaryFile()
    f.write(dumps(content, indent=4).encode())
    f.seek(0)

    try:
        lex = lexers.get_lexer_by_name('json')
        formatter = TerminalTrueColorFormatter(style="monokai")
        
        while True:
            line = f.readline() 
            if not line:
                break
            else:
                print(highlight(line, lex, formatter),end="")
        f.close()
    except:
        with open(file, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE).decode('utf-8', 'ignore').translate({ord('\u0000'): None})
                if not data:
                    break
                print(data)

def bytes2human(n):
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.1f%s' % (value, s)
	return "%sB" % n
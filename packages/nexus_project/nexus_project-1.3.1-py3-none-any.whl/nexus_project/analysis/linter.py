import impmagic


class Analyser():
    @impmagic.loader(
        {'module':'pylint.lint', 'submodule': ['Run']}
    )
    def __init__(self, filename, exclude=""):
        self.init_reporter()

        Run([f'--disable={exclude}',filename], reporter=self.reporter, exit=False)

    @impmagic.loader(
        {'module':'pylint.reporters', 'submodule': ['JSONReporter']},
        {'module':'io', 'submodule': ['StringIO']}
    )
    def init_reporter(self):
        self.out_stream = StringIO()
        self.reporter = JSONReporter(self.out_stream)

    @impmagic.loader(
        {'module':'json', 'submodule': ['load']}
    )
    def load_report(self):
        self.out_stream.seek(0)
        js = load(self.out_stream)

        self.report = {}
        for rep in js:
            if rep['path'] not in self.report:
                self.report[rep['path']] = {}

            if rep['type'] not in self.report[rep['path']]:
                self.report[rep['path']][rep['type']] = []

            self.report[rep['path']][rep['type']].append(f'{rep["message-id"]: <6} - {rep["line"]}:{rep["column"]} - {rep["message"]}')

    @impmagic.loader(
        {'module':'app.display', 'submodule': ['print_nxs']}
    )
    def display_report(self):
        if hasattr(self, "report"):
            for file in self.report:
                print_nxs(f"\n{file}")
                for type_e in self.report[file]:
                    print(f"  {type_e}")
                    for el in self.report[file][type_e]:
                        print(f"     {el}")

    def get_note(self):
        if hasattr(self, "reporter"):
            return f"{round(self.reporter.linter.stats.global_note, 2)}/10"

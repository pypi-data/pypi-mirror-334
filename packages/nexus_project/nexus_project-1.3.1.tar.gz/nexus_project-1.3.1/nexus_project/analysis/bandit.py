import impmagic
import __main__

class BanditScan():
    @impmagic.loader(
        {'module':'bandit.core', 'submodule': ['constants']},
        {'module':'bandit.core', 'submodule': ['config'], 'as': 'b_config'},
        {'module':'bandit.core', 'submodule': ['manager'], 'as': 'b_manager'},
    )
    def __init__(self, file, exclude_file=None, recursive=True, severity=1, confidence=1, show_errors=False, show_metrics= False, show_globalmetrics=False, show_filemetrics=False, show_details=False, show_all=True):
        self.recursive = recursive
        self.show_errors = show_errors
        self.show_metrics = show_metrics
        self.show_globalmetrics = show_globalmetrics
        self.show_filemetrics = show_filemetrics
        self.show_details = show_details
        self.show_all = show_all

        self.sev_level = constants.RANKING[severity - 1]
        self.conf_level = constants.RANKING[confidence - 1]

        b_conf = b_config.BanditConfig(config_file=None)

        profile = {}
        profile["include"] = set(b_conf.get_option("tests") or [])
        profile["exclude"] = set(b_conf.get_option("skips") or [])

        self.b_mgr = b_manager.BanditManager(b_conf,None,False,profile=profile,verbose=False,quiet=False,ignore_nosec=False)

        if exclude_file is None:
            exclude_file = ",".join(constants.EXCLUDE)
        else:
            exclude_file = ",".join(exclude_file)

        self.b_mgr.discover_files(file, self.recursive, exclude_file)

    @impmagic.loader(
        {'module':'zpp_ManagedFile', 'submodule': ['ManagedFile']},
        {'module':'json', 'submodule': ['load']}
    )
    def run_scan(self):
        self.b_mgr.run_tests()

        file = ManagedFile(closable=False)

        self.b_mgr.output_results(3,self.sev_level,self.conf_level,file,'json',None)

        file.seek(0)
        self.result = load(file)

    @impmagic.loader(
        {'module':'zpp_color', 'submodule': ['fg', 'attr']}
    )
    def output(self):
        if self.show_errors or self.show_all:
            errors = self.result['errors']
            if len(errors)==0:
                print(f"\n{fg(__main__.color['yellow'])}Errors:{attr(0)} No error notify")
            else:
                errors = "\n".join(errors)
                print(f'Errors: {errors}')

        metrics = self.result['metrics']
        if self.show_metrics or self.show_globalmetrics or self.show_all:
            print(f"\n{fg(__main__.color['yellow'])}Metrics total:{attr(0)}")
            metric = metrics['_totals']
            for line in metric:
                print(f"  {line}: {metric[line]}")
        if self.show_metrics or self.show_filemetrics or self.show_all:
            print(f"\n{fg(__main__.color['yellow'])}Metrics by file:{attr(0)}")
            for metric in metrics:
                if metric!='_totals':
                    print(f"- {metric}")
                    cont = metrics[metric]
                    for line in cont:
                        print(f"  {str(line)}: {cont[line]}")

        if self.show_details or self.show_all:
            print(f"\n{fg(__main__.color['yellow'])}Details:{attr(0)}",end="")
            details = self.result['results']
            for detail in details:
                print(f"\n {fg(__main__.color['dark_gray'])}filename:{attr(0)} {detail['filename']}")
                print(f" {fg(__main__.color['dark_gray'])}test name:{attr(0)} {detail['test_name']}")
                print(f" {fg(__main__.color['dark_gray'])}confidence lvl:{attr(0)} {detail['issue_confidence']}")
                print(f" {fg(__main__.color['dark_gray'])}severity lvl:{attr(0)} {detail['issue_severity']}")
                print(f" {fg(__main__.color['dark_gray'])}issue:{attr(0)} {detail['issue_text']}")
                print(f" {fg(__main__.color['dark_gray'])}issue cwe:{attr(0)} {detail['issue_cwe'].get('link','')}")
                print(f" {fg(__main__.color['dark_gray'])}line:{attr(0)} {detail['line_number']}")
                print(f" {fg(__main__.color['dark_gray'])}column:{attr(0)} {detail['col_offset']}")
                code = "   "+detail['code'].replace("\n","\n   ")
                print(f" {fg(__main__.color['dark_gray'])}code:{attr(0)} \n{code}")
            print("")
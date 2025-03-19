import __main__
import impmagic

@impmagic.loader(
    {'module':'requests'},
    {'module':'zpp_config', 'submodule':['Config']},
    {'module': 'template', 'submodule': ['default_conf']}
)
def get(url, params=None, headers=None):
    proxy = __main__.nxs.conf.load(val='proxy', section='',default=default_conf.proxy)
    if proxy!=None and len(proxy):
        proxies = {
            "http": proxy,
            "https": proxy
        }

    else:
        proxies = None

    response = requests.get(url, proxies=proxies, params=params, headers=headers)

    return response
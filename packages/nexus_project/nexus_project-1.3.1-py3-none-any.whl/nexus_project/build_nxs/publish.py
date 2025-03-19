import impmagic

@impmagic.loader(
    {'module':'app.display', 'submodule': ['logs']}
)
def get_type(file):
    if file.endswith(".whl"):
        return "bdist_wheel"
    elif file.endswith(".tar.gz"):
        return "sdist"
    else:
        logs("Unknown distribution format", "critical")
        exit()

@impmagic.loader(
    {'module':'pkginfo'}
)
def get_metadata(file):
    file_type = get_type(file)

    meta = None
    if file_type=='bdist_wheel':
        pkg_info = pkginfo.Wheel(file)
        meta = pkg_info.__dict__
    elif file_type=='sdist':
        pkg_info = pkginfo.SDist(file)
        meta = pkg_info.__dict__

    return meta

#Uploader adapted from the project Poetry https://github.com/python-poetry/poetry
class Uploader:
    @impmagic.loader(
        {'module':'__main__'},
        {'module': 'template', 'submodule': ['default_conf']}
    )
    def __init__(self, files, url=None):
        self.files = files

        if url==None:
            self.url = __main__.nxs.conf.load(val='publish.url', section='',default=default_conf.publish_url)
        else:
            self.url = url

    @impmagic.loader(
        {'module':'getpass', 'submodule':['getpass']}
    )
    def connect(self):
        self._username = __main__.nxs.conf.load(val='publish.username', section='',default='')
        if self._username=='':
            self._username = input("Username: ")
        self._password = getpass('Password: ')

    @impmagic.loader(
        {'module':'requests_toolbelt', 'submodule':['user_agent']}
    )
    def get_user_agent(self):
        agent: str = user_agent("nexus", "0.5.0")
        return agent

    @impmagic.loader(
        {'module':'requests', 'submodule':['adapters']},
        {'module':'urllib3', 'submodule':['util']}
    )
    def get_adapter(self):
        retry = util.Retry(connect=5, total=10, allowed_methods=["GET"], status_forcelist=[500, 501, 502, 503])
        return adapters.HTTPAdapter(max_retries=retry)

    @impmagic.loader(
        {'module':'requests'}
    )
    def make_session(self):
        session = requests.session()
        auth = self.get_auth()
        if auth is not None:
            session.auth = auth

        session.headers["User-Agent"] = self.get_user_agent()
        for scheme in ("http://", "https://"):
            session.mount(scheme, self.get_adapter())

        return session

    def get_auth(self):
        if self._username is None or self._password is None:
            return None
        return (self._username, self._password)

    def upload(self):
        cert = True
        client_cert = None
        self.session = self.make_session()
        self.session.verify = str(cert) if not isinstance(cert, bool) else cert

        if client_cert:
            self.session.cert = str(client_cert)

        try:
            for file in self.files:
                self._upload_file(file)
        finally:
            self.session.close()

    @impmagic.loader(
        {'module':'hashlib'}
    )
    def post_data(self, file):
        file_type = get_type(file)

        if hasattr(hashlib, "blake2b"):
            blake2_256_hash = hashlib.blake2b(digest_size=256 // 8)

        md5_hash = hashlib.md5()
        sha256_hash = hashlib.sha256()
        with open(file, "rb") as fp:
            for content in iter(lambda: fp.read(8192), b""):
                md5_hash.update(content)
                sha256_hash.update(content)

                if hasattr(hashlib, "blake2b"):
                    blake2_256_hash.update(content)

        md5_digest = md5_hash.hexdigest()
        sha2_digest = sha256_hash.hexdigest()
        blake2_256_digest = None
        if hasattr(hashlib, "blake2b"):
            blake2_256_digest = blake2_256_hash.hexdigest()

        meta = get_metadata(file)

        in_meta = [
            ["name","name"],
            ["version","version"],
            ["metadata_version","metadata_version"],
            ["summary","summary"],
            ["home_page","home_page"],
            ["author","author"],
            ["author","author"],
            ["author_email","author_email"],
            ["maintainer","maintainer"],
            ["maintainer_email","maintainer_email"],
            ["license","license"],
            ["description","description"],
            ["description_content_type","description_content_type"],
            ["keywords","keywords"],
            ["platform","platform"],
            ["classifiers","classifiers"],
            ["download_url","download_url"],
            ["supported_platform","supported_platform"],
            ["provides","provides"],
            ["requires","requires"],
            ["obsoletes","obsoletes"],
            ["project_urls","project_urls"],
            ["provides_dist","provides_dist"],
            ["obsoletes_dist","obsoletes_dist"],
            ["requires_dist","requires_dist"],
            ["requires_external","requires_external"],
            ["requires_python","requires_python"]
        ]

        data = {
            "filetype": file_type,
            "pyversion": "source",
            "comment": None,
            "md5_digest": md5_digest,
            "sha256_digest": sha2_digest,
            "blake2_256_digest": blake2_256_digest
        }
        for m in in_meta:
            if m[1] in meta:
                data[m[0]] = meta[m[1]]

        if "name" in data and "version" in data and "filetype" in data and "pyversion" in data:
            return data
        else:
            print("Donnée manquante")
            exit()

    @impmagic.loader(
        {'module':'os.path', 'submodule':['isfile']},
        {'module':'requests'},
        {'module':'requests.exceptions', 'submodule':['ConnectionError', 'HTTPError']},
        {'module':'requests_toolbelt.multipart', 'submodule':['MultipartEncoder', 'MultipartEncoderMonitor']}
    )
    def _upload_file(self,file):
        if not isfile(file):
            print(f"Archive ({file}) does not exist")
            exit()

        data = self.post_data(file)
        data.update({":action": "file_upload","protocol_version": "1"})

        data_to_send = self._prepare_data(data)

        with open(file, "rb") as fp:
            ####
            if "\\" in file:
                file = file.split("\\")
                file = file[len(file)-1]
            ####
            data_to_send.append(("content", (file, fp, "application/octet-stream")))
            encoder = MultipartEncoder(data_to_send)
            monitor = MultipartEncoderMonitor(encoder)

            resp = None
            try:
                resp = self.session.post(
                    self.url,
                    data=monitor,
                    allow_redirects=False,
                    headers={"Content-Type": monitor.content_type},
                    timeout=15,
                )
                if resp is None or 200 <= resp.status_code < 300:
                    print(f"{file} uploaded")
                elif resp.status_code == 301:
                    print("Redirects are not supported")
                    exit()
                elif self._is_file_exists_error(resp):
                    print(f"File {file} already exists")
                else:
                    resp.raise_for_status()
            except (requests.ConnectionError, requests.HTTPError) as e:
                print(e)
                exit()

    def _prepare_data(self, data):
        data_to_send = []
        for key, value in data.items():
            if not isinstance(value, (list, tuple)):
                data_to_send.append((key, value))
            else:
                for item in value:
                    data_to_send.append((key, item))

        return data_to_send

    def _is_file_exists_error(self, response):
        status = response.status_code
        reason = response.reason.lower()
        text = response.text.lower()
        reason_and_text = reason + text

        return (
            status == 409
            or (status == 400 and "already exist" in reason_and_text)
            or (status == 400 and "updating asset" in reason_and_text)
            or (status == 403 and "overwrite artifact" in reason_and_text)
            or (status == 400 and "already been taken" in reason_and_text)
        )
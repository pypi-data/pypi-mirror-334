from requests import get
from os import path


class Download:

    def __init__(self, file_name, link, install_path) -> None:
        self.file = file_name
        self.link = link
        self.install_path = install_path
    
    def get_install_path(self) -> str:
        return self.install_path
    
    def create_file(self):
        local = self.install_path
        c = path.join(local, self.file)

        with open(c, "wb") as o:
            o.write(self.get_file())

    def get_file(self) -> bytes:
        w = get(self.link)
        json = w.json()
        link = json["assets"][0]["browser_download_url"]
        return get(link).content

    def get_name(self) -> str:
        return self.file

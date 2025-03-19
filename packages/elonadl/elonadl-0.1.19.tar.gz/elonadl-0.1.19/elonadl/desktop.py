import winshell
from os.path import join


class Desktop:

    def __init__(self, name, path, version, exe, description):
        self.name = name
        self.path = path
        self.version = version
        self.exe = exe
        self.description = description

    def create_shortcut(self):
        desktop = winshell.desktop()
        with winshell.shortcut(join(desktop, self.name + ' ' + self.version + ".lnk")) as shortcut:
            shortcut.path = self.path + self.version + '\\' + self.exe
            shortcut.icon_location = self.path + self.version + '\\' + self.exe, 0
            shortcut.description = self.description + self.version

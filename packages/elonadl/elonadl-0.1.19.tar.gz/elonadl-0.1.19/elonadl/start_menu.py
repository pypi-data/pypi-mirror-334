import os
from elonadl import SHORTCUT_NAME
from win32com.client import Dispatch
from pathlib import Path

class StartMenu:

    def __init__(self, install_path, current_version, folder_name, use_all_users=False):
        self.install_path = install_path
        self.current_version = current_version
        self.folder_name = folder_name + self.current_version

        
        if use_all_users:
            self.program_data = os.environ.get('PROGRAMDATA')
            self.start_menu_path = Path(self.program_data) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
        else:
            self.start_menu_path = Path(os.path.expanduser('~')) / 'AppData' / 'Roaming' / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
        
        self.folder_path = self.start_menu_path / self.folder_name
        
    def create_directory(self):
        try:
            if not self.folder_path.exists():
                self.folder_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {self.folder_path}")
            else:
                print(f"Directory already exists: {self.folder_path}")
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    def create_shortcut(self, shortcut_name=SHORTCUT_NAME):
        try:
            if not Path(self.install_path).exists():
                print(f"Error: Install path does not exist: {self.install_path + self.current_version}")
                return False
                
            if not self.create_directory():
                return False

            shortcut_path = self.folder_path / f"{shortcut_name + self.current_version}.lnk"
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = self.install_path
            shortcut.WorkingDirectory = str(Path(self.install_path).parent)
            shortcut.save()
            
            print(f"Created shortcut: {shortcut_path}")
            return True
        except Exception as e:
            print(f"Error creating shortcut: {e}")
            return False
    
    def remove_shortcut(self, shortcut_name="Elona Plus Custom-GX"):
        try:
            shortcut_path = self.folder_path / f"{shortcut_name + self.current_version}.lnk"
            if shortcut_path.exists():
                shortcut_path.unlink()
                print(f"Removed shortcut: {shortcut_path}")
                return True
            else:
                print(f"Shortcut does not exist: {shortcut_path}")
                return False
        except Exception as e:
            print(f"Error removing shortcut: {e}")
            return False
    
    def remove_directory(self):
        try:
            if self.folder_path.exists():
                # Check if the directory is empty
                if any(self.folder_path.iterdir()):
                    print(f"Directory is not empty: {self.folder_path}")
                    return False
                
                self.folder_path.rmdir()
                print(f"Removed directory: {self.folder_path}")
                return True
            else:
                print(f"Directory does not exist: {self.folder_path}")
                return False
        except Exception as e:
            print(f"Error removing directory: {e}")
            return False
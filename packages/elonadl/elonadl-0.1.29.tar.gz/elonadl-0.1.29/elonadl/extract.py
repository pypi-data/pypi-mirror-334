import elonadl as elona
from zipfile import ZipFile
from os import path, listdir, rename
from re import findall


class Extract:

    def __init__(self, file_name, install_path) -> None:
        self.file_name = file_name
        self.install_path = install_path

    def extract_zip(self):
        local = self.install_path
        c = path.join(local, self.file_name)

        with ZipFile(c) as z:
            z.extractall(local)

    def find_latest_version(self):
        t = listdir(path=self.install_path)
        n = "elonaplus"
        self.p = list()

        for x in t:
            h = findall(n + "[0-9].[0-9][0-9]", x)
            if h:
                self.p.append(x)

        if not self.p:
            print("No Elona+ directory found.")
            exit()
        
        result = path.join(self.install_path, max(self.p) + '\\')

        return result

    def scrape_version(self):
        t = listdir(path=self.install_path)
        n = elona.SHORTCUT_NAME
        u = list()

        for x in t:
            h = findall(n + "[0-9].[0-9][0-9]", x)
            if h:
                u.append(x)

        return max(u)[18:22]
    
    def rename_directory(self):
        dir = max(self.p)
    
        try:
            rename(path.join(self.install_path, dir), 
            path.join(self.install_path, elona.SHORTCUT_NAME + dir[9:13]))
        except FileExistsError as e:
            print(f"DIRECTORY NAME: {elona.BASE_ELONA_DIR + dir[9:13]}")
            cleaner = elona.cleanup.Cleanup(main_game=elona.ELONA_FILE_NAME, 
                                            mod=elona.CGX_FILE_NAME, base_dir=f"{elona.BASE_ELONA_DIR + dir[9:13]}")
            cleaner.execute()
            print(f"Error: {e}")
            print("The current vesion already exists in the directory. Exiting.")
            exit()
        except Exception as e:
            print(f"Error: {e}")
            exit()
            
        return path.join(self.install_path 
                + '\\' + elona.SHORTCUT_NAME)
import elonadl as elona
import os
import shutil

class Cleanup:

    def __init__(self, main_game, mod, base_dir, path=None):
        self.path = path or os.getenv('APPDATA')
        self.game = main_game
        self.mod = mod
        self.base_dir = base_dir
        if not self.path:
            raise ValueError("APPDATA environment variable not found and no path provided.")
        
        self.files_to_delete = [self.mod, self.game, self.base_dir]
        
    def find_targets(self) -> dict:
        results = {
            "files": [],
            "directories": []
        }
        
        for file_name in self.files_to_delete:
            file_path = os.path.join(self.path, file_name)
            if os.path.isfile(file_path):
                results["files"].append(file_path)
                
        for item in os.listdir(self.path):
            item_path = os.path.join(self.path, item)
            if (os.path.isdir(item_path) and item.startswith(elona.BASE_CGX_DIR) 
                or os.path.isdir(item_path) and item.startswith(elona.BASE_ELONA_DIR)):
                results["directories"].append(item_path)
                
        return results
    
    def delete_items(self, targets):
        for file_path in targets["files"]:
            try:
                os.remove(file_path)
            except OSError:
                pass
                
        for dir_path in targets["directories"]:
            try:
                shutil.rmtree(dir_path)
            except OSError:
                pass
    
    def execute(self, dry_run=False):
        targets = self.find_targets()
        
        if dry_run:
            return
        
        self.delete_items(targets)
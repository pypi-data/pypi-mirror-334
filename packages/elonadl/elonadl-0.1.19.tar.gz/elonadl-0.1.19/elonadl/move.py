import os
import shutil

class Move:
    
    def __init__(self, source_path, destination):
        self.source_path = source_path
        self.destination = destination
       
    def find_elona_directory(self) -> list:
        elona_dirs = []
        for item in os.listdir(self.source_path):
            item_path = os.path.join(self.source_path, item)
            if os.path.isdir(item_path) and item.startswith('Elona+'):
                elona_dirs.append(item_path)
               
        return elona_dirs
   
    def create_destination_directory(self):
        dest_path = os.path.join(self.source_path, self.destination)
       
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            print(f"Created destination directory: {dest_path}")
       
        return dest_path
   
    def move_files(self, elona_dir, dest_path) -> int:
        count = 0
       
        for item in os.listdir(elona_dir):
            source_item = os.path.join(elona_dir, item)
            dest_item = os.path.join(dest_path, item)
           
            try:
                if os.path.isfile(source_item):
                    shutil.copy2(source_item, dest_item)
                    count += 1
                elif os.path.isdir(source_item):

                    if os.path.exists(dest_item):
  
                        files_copied = self._merge_directories(source_item, dest_item)
                        count += files_copied
                    else:

                        shutil.copytree(source_item, dest_item)
                        count += 1 
            except (shutil.Error, OSError) as e:
                print(f"Error moving {source_item}: {e}")
               
        return count
    
    def _merge_directories(self, source_dir, dest_dir) -> int:
        files_copied = 0
        
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            dest_item = os.path.join(dest_dir, item)
            
            try:
                if os.path.isfile(source_item):
                    shutil.copy2(source_item, dest_item)
                    files_copied += 1
                elif os.path.isdir(source_item):
                    # Create destination subdirectory if it doesn't exist
                    if not os.path.exists(dest_item):
                        os.makedirs(dest_item)
                    
                    # Recursively merge subdirectories
                    sub_files_copied = self._merge_directories(source_item, dest_item)
                    files_copied += sub_files_copied
            except (shutil.Error, OSError) as e:
                print(f"Error merging {source_item}: {e}")
        
        return files_copied
   
    def execute(self) -> dict:
        results = {
            "elona_dirs_found": [],
            "files_moved": 0,
            "success": False
        }
       
        elona_dirs = self.find_elona_directory()
       
        if not elona_dirs:
            print("No directories starting with 'Elona+' found.")
            return results
       
        results["elona_dirs_found"] = elona_dirs
       
        dest_path = self.create_destination_directory()
       
        total_moved = 0
        for elona_dir in elona_dirs:
            print(f"Moving files from {elona_dir} to {dest_path}")
            moved = self.move_files(elona_dir, dest_path)
            total_moved += moved
            print(f"Moved {moved} items from {os.path.basename(elona_dir)}")
       
        results["files_moved"] = total_moved
        results["success"] = total_moved > 0
       
        print(f"Operation complete. Moved {total_moved} items in total.")
        return results
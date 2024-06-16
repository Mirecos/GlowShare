import os
import json
import io
from datetime import datetime
import base64
from threading import local
from src.classes.RemoteClient.RemoteClient import RemoteClient

class FileManager():

    def __init__(self, client : RemoteClient) -> None:
        self.client = client
        pass


    # Represents a directory to a dictionary
    def map_directory(self, path, path_from_root="", is_local=True  ) -> dict[str, io.BufferedReader]:
        result = {}
        if is_local:
            # Local scan
            files = os.listdir(path)
            for file in files:
                fp = os.path.join(path, file)
                if file == '.gitignore':
                    continue
                
                if os.path.isfile(fp):
                    with open(fp, "r") as f:
                        content = base64.b64encode(f.buffer.read()).decode()
                        result[os.path.join(path_from_root, file)] = content
                else:
                    subdir_result = self.map_directory(os.path.join(path, file), os.path.join(path_from_root, file))
                    result = {**result, **subdir_result}
            
        else:
            # Remote scan
            files = self.client.list_dir(path)
            for file in files:
                fp_from_root = os.path.join(path_from_root, file)
                if file == '.gitignore':
                    continue
                if self.client.is_file(fp_from_root):
                    result[os.path.join(path_from_root, file)] = self.client.get_file_content(fp_from_root)
                else:
                    subdir_result = self.map_directory(os.path.join(path, file), fp_from_root, is_local)
                    result = {**result, **subdir_result}
                
        return result

    def compare_directories(self, local : dict[str, io.BufferedReader], remote : dict[str, io.BufferedReader]):
        created_files = []
        modified_files = []
        deleted_files = []
        unchanged_files = []

        local_files_list = list(local)
        remote_files_list = list(remote)

        for path in local_files_list:
            if path in remote_files_list: 
                # file exist in remote, check content
                if local[path] == remote[path]:
                    # Same files
                    unchanged_files.append(path)
                else :
                    modified_files.append(path)

                remote_files_list.remove(path)
            else: 
                # Not in remote, so new file
                created_files.append(path)
        deleted_files = remote_files_list

        return {
            "Created": created_files,
            "Modified": modified_files,
            "Deleted": deleted_files,
            "Unchanged": unchanged_files
        }


    def reset_directory_to(self, representation: dict[str, io.BufferedReader]):

        return
            
    def overwrite_local_from_remote(self, path_from_root, local_path):

        fp = os.path.join(local_path, path_from_root)
        print(fp)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "a") as f :
            content = self.client.get_file_content(path_from_root)
            f.write(base64.b64encode(content).decode())

    def take_snapshot(self, path) -> None:
        fn = datetime.today().strftime('%Y-%m-%d_%H-%M-%S.json')
        snapshot = self.map_directory(path)
        with open(os.path.join('snapshots', fn), 'x') as f:
            json.dump(snapshot, f)

    def revert_snapshot(self):
        pass
    

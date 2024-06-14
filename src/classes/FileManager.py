import os
from diff_match_patch import diff_match_patch
import json
from datetime import datetime

class FileManager():

    def __init__(self) -> None:
        pass


        # Represents a directory to a dictionary
    def map_directory(self, path, path_from_root="./") -> dict:
        result = {}
        files = os.listdir(path)

        for file in files:
            fp = os.path.join(path, file)

            if os.path.isfile(fp):
                with open(fp, "r") as f: 
                    content = f.read()
                    result[os.path.join(path_from_root, file)] = content

            else:
                subdir_result = self.map_directory(os.path.join(path, file), os.path.join(path_from_root, file))
                result = {**result, **subdir_result}

        return result


    def compare_directories(self, local : dict, remote : dict):
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


    def take_snapshot(self, path) -> None:
        fn = datetime.today().strftime('%Y-%m-%d_%H-%M-%S.json')
        snapshot = self.map_directory(path)
        with open(os.path.join('snapshots',fn), 'x') as f:
            json.dump(snapshot, f)

    def save_snapshot(self):
        pass
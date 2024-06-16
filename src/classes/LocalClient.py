import os
import shutil
from src.utils import clear
from src.classes.FileManager import FileManager
from src.classes.RemoteClient.LocalRemoteClient import LocalRemoteClient

class LocalClient():


    def __init__(self, cwd, local_path, remote_path) -> None:
        self.fm = FileManager(LocalRemoteClient('./data_remote/'))
        self.cwd = cwd
        self.local_path = local_path
        self.remote_path = remote_path
        self.changes = {}



    def __compare(self) -> dict:
        local_content = self.fm.map_directory(os.path.join(self.cwd, self.local_path))
        remote_content = self.fm.map_directory(os.path.join(self.cwd, self.remote_path), is_local=False)
        return self.fm.compare_directories(local_content, remote_content)



    # Compare local with remote and print results
    def status(self):
        result = self.__compare()
        print("FileManager has found the following differences :")
        print("Modified files :")
        for changed in result["Modified"]:
            print(f"- {changed}")
        print("Deleted files :")
        for deleted in result["Deleted"]:
            print(f"- {deleted}")
        print("Created files :")
        for created in result["Created"]:
            print(f"- {created}")



    # fetch remote changes to local
    def fetch(self):
        self.changes = self.__compare()



    # pull content from fetched changes
    def pull(self):
        if self.changes == {}: 
            print("Your files are already up to date. You might need to fetch before pulling files.")
            return
        self.fm.take_snapshot(self.local_path)
        result = self.changes
        for path_from_root in result["Deleted"]:
            self.fm.overwrite_local_from_remote(path_from_root, self.local_path)
        for path_from_root in result["Modified"]:
            self.fm.overwrite_local_from_remote(path_from_root, self.local_path)
        self.changes = {}



    # push changes and content to remote
    def push(self):
        pass



    def handle_input(self):
        cmd = input("What to do ?")
        match cmd:
            case "pull":
                print("Pulling from remote...")
                self.pull()
            case "push":
                print("Pushig to remote...")
                self.push()
            case "stat":
                print("Comparing from remote...")
                self.status()
            case "fetch":
                print("Fetching from remote...")
                self.fetch()
            case "test":
                repr = self.fm.map_directory(os.path.join(self.cwd, self.remote_path))
                self.fm.reset_current_files_to(repr)
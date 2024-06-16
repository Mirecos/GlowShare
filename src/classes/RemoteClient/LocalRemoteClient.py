'''

    A local remote client manage files fully locally on your machine.
    The remote is simply a directory on your computer

'''
import os
import base64
from src.classes.RemoteClient.RemoteClient import RemoteClient 

class LocalRemoteClient(RemoteClient):

    def __init__(self, local_path) -> None:
        super().__init__()
        self.local_path=local_path




    def get_path(self, file):
        return os.path.join(self.local_path, file)


    def get_file_content(self, file_from_root) -> bytes:
        fp = self.get_path(file_from_root)
        with open(fp, "r") as f:
            return f.buffer.read()

    def set_file_content(self, file_from_root, content : bytes):
        fp = self.get_path(file_from_root)
        with open(fp, "x") as f:
            f.write(content)
    
    def is_file(self, file_from_root):
        fp = self.get_path(file_from_root)
        return os.path.isfile(fp)
    
    def list_dir(self, path):
        return os.listdir(path)
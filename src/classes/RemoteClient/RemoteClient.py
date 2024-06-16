from abc import ABC, abstractmethod
from importlib import metadata

class RemoteClient(ABC):

    def __init__(self) -> None:
        super().__init__()


    @abstractmethod
    def get_file_content(self, file_from_root) -> bytes:
        pass


    @abstractmethod
    def set_file_content(self, file_from_root, content):
        pass


    @abstractmethod
    def is_file(self, file_from_root) -> bool:
        pass
    
    @abstractmethod
    def list_dir(self, path):
        pass

from logging import Logger
from watchdog.events import LoggingEventHandler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Tracker(LoggingEventHandler):

    def __init__(
            self,
            path : str ,
            logger: Logger | None = None
            ) -> None:
        super().__init__(logger)

        self.path = path
        self.changes_log = {}
        logging.info(f'Start watching directory {path!r}')




    def dispatch(self, event):
        print(self.changes_log)



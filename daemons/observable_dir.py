import os
import typing as typ
import time
from enum import Enum
import pathlib
from collections import deque
import attr
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from .watcher import ObservableMixin, Event
from ..attrs_serializable import AttrsSerializable as Serializable


class FileEventType(Enum):
    FILE_ADDED    = "file_added"
    FILE_MODIFIED = "file_modified"
    FILE_DELETED  = "file_deleted"


@attr.s(auto_attribs=True, hash=False)
class ObservableDirectory(ObservableMixin, FileSystemEventHandler, Serializable):
    root: pathlib.Path = None
    events: deque = attr.ib(factory=deque)

    def changes(self) -> typ.List[Event]:
        res = list(self.events)
        self.events.clear()
        return res

    def on_any_event(self, wd_event: FileSystemEvent):

        self.logger.debug(wd_event)

        # Ignore directories
        if wd_event.is_directory:
            return

        fp = wd_event.src_path
        event_type = None
        sleep_time = 0.0

        # if wd_event.event_type == "created" and event_data.endswith(".zip"):
        #     logger.debug("Found a zipped archive")
        #     event_type = DicomEventType.FILE_ADDED
        #     sleep_time = 1.0  # Wait 1 sec for file to settle

        if wd_event.event_type == "created":
            self.logger.debug("Found a new file")
            event_type = FileEventType.FILE_ADDED
            sleep_time = 0.2  # Wait 0.2 secs for file to settle

        # Assigned an event type, so wait until file is stable
        if event_type:
            # Poll for a while until file is stable
            size = os.stat(fp).st_size
            prev_size = size - 1
            while size > prev_size:
                time.sleep(sleep_time)  # No change in this long
                prev_size = size
                size = os.stat(fp).st_size
            self.logger.debug("Final file size: {}".format(size))

            e = Event(
                event_type=event_type,
                data={"fp": fp}
            )
            self.logger.debug(f'Accepting file-creation event {e}')
            self.events.append(e)

        else:
            self.logger.debug('Rejecting non-creation event {}'.format(wd_event))

    def poll_events(self):

        self.logger.debug(f"Starting to poll for changes in {self.root}")
        observer = Observer()
        receiver = self

        observer.schedule(receiver, str(self.root), recursive=True)
        observer.start()

        self.logger.debug("Spawned observer and returning")

        # self.proc = observer  # For kill on __del__

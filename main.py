import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ProjectWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'The file {event.src_path} was modified')

    def on_created(self, event):
        print(f'The file {event.src_path} was created! Nice')

    def on_deleted(self, event):
        print(f'The file {event.src_path} was created! D:')

    def on_moved(self, event):
        print(f'The file {event.src_path} was moved? :O')


def startup_message():
    print('Welcome to PyConstructor v0.1')
    print('This program will handle running you\'re pre-defined build steps every time you hit save')


if __name__ == "__main__":
    startup_message()

    fileHandler = ProjectWatcher()
    observer = Observer()
    observer.schedule(fileHandler, path='/Users/rhysjohns/Code/Python/PyConstructor/test_dir', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

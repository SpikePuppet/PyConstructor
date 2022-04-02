import shlex
import subprocess
import time
import sys
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ProjectWatcher(FileSystemEventHandler):
    commands = []

    def __init__(self, commands):
        self.commands = commands

    @staticmethod
    def run_commands():
        for index in range(0, len(commands)):
            command_items = shlex.split(commands[index], posix=False)
            if ">" in command_items:
                command_items.remove(">")
                print(command_items[-1])
                with open(command_items[-1]) as fd:
                    result = subprocess.run(command_items, stdout=fd)
            else:
                result = subprocess.run(command_items, capture_output=True, text=True)
                print(result.stdout)

    def on_modified(self, event):
        print(f'The file {event.src_path} was modified')
        self.run_commands()

    def on_created(self, event):
        print(f'The file {event.src_path} was created! Nice')
        self.run_commands()

    def on_deleted(self, event):
        print(f'The file {event.src_path} was created! D:')
        self.run_commands()

    def on_moved(self, event):
        print(f'The file {event.src_path} was moved? :O')
        self.run_commands()

    def execute_observer_options(self):
        pass


def startup_message():
    print('Welcome to PyConstructor v0.1')
    print('This program will handle running you\'re pre-defined build steps every time you hit save')


def read_yaml():
    with open('sample-observer-config.yml') as fileHandle:
        data = yaml.load(fileHandle, Loader=yaml.FullLoader)

    return data[0]['observer']['execute']


if __name__ == "__main__":
    directory_to_be_monitored = sys.argv[1]
    recursive = sys.argv[2]
    startup_message()
    commands = read_yaml()

    fileHandler = ProjectWatcher(commands)
    observer = Observer()
    observer.schedule(fileHandler, path=directory_to_be_monitored, recursive=recursive)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

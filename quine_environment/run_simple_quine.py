import argparse
import atexit
import threading
from quine_dashboard import QuineDashboard
from simple_quine_simulation import random_selection
from quine_logger import log


class QuineInfo:
    def __init__(self):
        self.root_hash = None
        self.quine_dict = {}


def run_in_thread(quine_info, quine_file):
    running_lock = threading.Lock()

    def stop_running():
        print('stop running')
        nonlocal running_lock
        running_lock.acquire()

    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(stop_running)

    log.info('Starting thread for quine simulation')
    print('Starting thread for quine simulation')
    quine_thread = threading.Thread(target=random_selection, args=(quine_info, quine_file, running_lock,))
    quine_thread.setDaemon(True)
    quine_thread.start()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('quine', type=str, help='Quine to multiply')

    args = parser.parse_args()
    return args.quine


def main():
    quine_file = parse_args()

    quine_info = QuineInfo()

    run_in_thread(quine_info, quine_file)
    QuineDashboard(quine_info)


if __name__ == '__main__':
    main()

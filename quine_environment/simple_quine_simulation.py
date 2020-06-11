import hashlib
import random
import subprocess
import tempfile
from quine_logger import log
from collections import deque


class Quine:
    def __init__(self, code: str, livable: bool, parent=None):
        self.code = code
        self.hash = hash_quine(code)
        self.livable = livable
        self.parent = parent
        self.children = set()

    def __repr__(self):
        return f"(livable:{self.livable}, parent:{self.parent}, children:{','.join([c for c in self.children])})"


def hash_quine(quine_content: str):
    hash_object = hashlib.sha256(quine_content.encode())
    return hash_object.hexdigest()


def quine_generator(quine_dict: dict, semaphore):
    tmp_file_name = tempfile.NamedTemporaryFile(delete=False)
    living_quine_hash = deque(maxlen=100)
    living_quine_hash.append(list(quine_dict.values())[0].hash)
    while not semaphore.locked():
        # select quine
        quine_hash = random.choice(list(living_quine_hash))
        parent_quine = quine_dict[quine_hash]

        with open(tmp_file_name.name, 'w') as file:
            file.write(parent_quine.code)

        tmp_quine_result = subprocess.run(['python3', tmp_file_name.name], stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL, text=True)
        new_quine_code = tmp_quine_result.stdout

        new_quine = Quine(new_quine_code, tmp_quine_result.returncode == 0, parent_quine.hash)

        if new_quine.livable and new_quine.hash not in living_quine_hash:
            living_quine_hash.append(new_quine.hash)
        yield parent_quine, new_quine


def random_selection(quine_info, quine_file, semaphore):
    log.info('Starting random selection')
    with open(quine_file, 'r') as file:
        data = file.read()
    quine = Quine(data, True)

    quine_info.root_hash = quine.hash
    quine_info.quine_dict[quine.hash] = quine

    for parent_quine, child_quine in quine_generator(quine_info.quine_dict, semaphore):
        if child_quine.hash not in quine_info.quine_dict:
            quine_info.quine_dict[child_quine.hash] = child_quine
            parent_quine.children.add(child_quine.hash)

            print(len(quine_info.quine_dict))

    print("Quine generation finished !")

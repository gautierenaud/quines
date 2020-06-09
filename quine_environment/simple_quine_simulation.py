import hashlib
import random
import subprocess
import tempfile
from quine_logger import log


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


def quine_generator(quine_dict, semaphore):
    tmp_file_name = tempfile.NamedTemporaryFile(delete=False)
    while not semaphore.locked():
        # select quine
        quine_hash = random.choice(list(quine_dict))
        parent_quine = quine_dict[quine_hash]

        with open(tmp_file_name.name, 'w') as file:
            file.write(parent_quine.code)

        tmp_quine_result = subprocess.run(['python3', tmp_file_name.name], stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL, text=True)
        new_quine_code = tmp_quine_result.stdout

        yield parent_quine, Quine(new_quine_code, tmp_quine_result.returncode == 0, parent_quine.hash)


def random_selection(quine_info, quine_file, semaphore):
    log.info('Starting random selection')
    with open(quine_file, 'r') as file:
        data = file.read()
    quine = Quine(data, True)

    print(quine_info)
    quine_info.root_hash = quine.hash
    quine_info.quine_dict[quine.hash] = quine
    print(quine_info)

    for parent_quine, child_quine in quine_generator(quine_info.quine_dict, semaphore):
        if child_quine.hash not in quine_info.quine_dict:
            quine_info.quine_dict[child_quine.hash] = child_quine
            parent_quine.children.add(child_quine.hash)

            print(len(quine_info.quine_dict))

    print("Quine generation finished !")

import argparse
import hashlib
import random
import subprocess
import tempfile

import test_plotly
from draw_tree import buchheim


class Quine:
    def __init__(self, code: str, livable: bool, parent=None):
        self.code = code
        self.hash = hash_quine(code)
        self.livable = livable
        self.parent = parent
        self.children = set()

    def __repr__(self):
        return f"(livable:{self.livable}, parent:{self.parent}, children:{','.join([c for c in self.children])})"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('quine', type=str, help='Quine to multiply')

    args = parser.parse_args()
    return args.quine


def hash_quine(quine_content: str):
    hash_object = hashlib.sha256(quine_content.encode())
    return hash_object.hexdigest()


def quine_generator(quine_dict, number):
    tmp_file_name = tempfile.NamedTemporaryFile(delete=False)
    for i in range(number):
        # select quine
        quine_hash = random.choice(list(quine_dict))
        parent_quine = quine_dict[quine_hash]

        with open(tmp_file_name.name, 'w') as file:
            file.write(parent_quine.code)

        tmp_quine_result = subprocess.run(['python3', tmp_file_name.name], stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL, text=True)
        new_quine_code = tmp_quine_result.stdout

        yield parent_quine, Quine(new_quine_code, tmp_quine_result.returncode == 0, parent_quine.hash)


def get_plottable_tree(root_hash, quine_dict):
    raw_tree = create_tree(root_hash, quine_dict)
    return buchheim(raw_tree)


def random_selection(quine_dict):
    root_quine = list(quine_dict.values())[0]
    for parent_quine, child_quine in quine_generator(quine_dict, 100):
        if child_quine.hash not in quine_dict:
            quine_dict[child_quine.hash] = child_quine
            parent_quine.children.add(child_quine.hash)

    print("Quine generation finished !")
    first_tree = get_plottable_tree(root_quine.hash, quine_dict)
    test_plotly.QuineTreeDash(first_tree)


class Tree:
    def __init__(self, hash, parent, livable):
        self.hash = hash
        self.parent = parent
        self.livable = livable
        self.children = []

    def __repr__(self):
        return self.hash


def create_tree(hash, quine_dict):
    node = Tree(hash, None, quine_dict[hash].livable)
    for child_hash in quine_dict[hash].children:
        node.children.append(create_tree(child_hash, quine_dict))

    return node


def print_tree(tree):
    print(tree.tree)
    for child in tree.children:
        print_tree(child)


def main():
    quine_file = parse_args()

    quine_dict = dict()

    with open(quine_file, 'r') as file:
        data = file.read()
    quine = Quine(data, True)

    quine_dict[quine.hash] = quine

    random_selection(quine_dict)

    print(f"{len(quine_dict)} items")


if __name__ == '__main__':
    main()

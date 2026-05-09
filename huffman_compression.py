"""
Module for Huffman binary encoding/decoding.
"""

from __future__ import annotations


class HuffmanBinaryTree:
    """
    Representation of a binary tree for Huffman encoding/decoding.
    self.left represents 0 and self.right represents 1 for the encoding and decoding process.
    A leaf is represented by a tree that satisfies self.left is None and self.right is None.

    Representation Invariants:
        - self.char is not None and self.freq is not None
        - (self.left is None) == (self.right is None)
        - if self.left is None and self.right is None (i.e. self is a leaf node),
          then len(self.char) == 1
        - if self is an internal node,
          then self.char == self.left.char + self.right.char and self.freq == self.left.freq + self.right.freq
    """

    char: str
    freq: int
    left: HuffmanBinaryTree | None
    right: HuffmanBinaryTree | None
    _string: str

    def __init__(self, char: str, freq: int,
                 left: HuffmanBinaryTree = None, right: HuffmanBinaryTree = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return self._generate_string(0)

    def _generate_string(self, d: int) -> str:
        """

        :param d:
        :return:
        """
        str_so_far = f"{"  " * d}--{self.char}--{self.freq}"

        # Replace new line characters with the literal
        str_so_far = str_so_far.replace("\n", "\\n") + "\n"

        # Base case: self is a leaf node
        if self.left is None and self.right is None:
            return str_so_far

        # Recursive: get the hashes for the subtrees
        return f"{str_so_far}{self.left._generate_string(d + 1)}{self.right._generate_string(d + 1)}"

    def combine(self, other: HuffmanBinaryTree) -> HuffmanBinaryTree:
        """
        Combine two binary trees as the subtrees in a new binary tree.

        :param other: the binary tree to combine with this one
        :return: the binary tree that contains self and other as subtrees
        """
        return HuffmanBinaryTree(self.char + other.char, self.freq + other.freq, self, other)

    def generate_encoding_dict(self) -> dict[str, str]:
        """
        Create an encoding dictionary for this tree.

        :return: a mapping of string characters to binary codes
        """
        encoding_dict = {}
        self._generate_encoding_dict_helper(encoding_dict, "")
        return encoding_dict

    def _generate_encoding_dict_helper(self, encoding_dict: dict[str, str], str_so_far: str) -> None:
        """
        Helper method for generating an encoding dictionary for this tree. Mutating method.

        :param encoding_dict: encoding dictionary so far
        :param str_so_far: binary encoding so far
        :return: None
        """
        # Base case: we've reached a leaf node
        if len(self.char) == 1:
            encoding_dict[self.char] = str_so_far

        # Recursive: call it on the subtrees
        else:
            self.left._generate_encoding_dict_helper(encoding_dict, str_so_far + "0")
            self.right._generate_encoding_dict_helper(encoding_dict, str_so_far + "1")


# ---------- ENCODING ----------
def huffman_encode(s: str) -> tuple[str, HuffmanBinaryTree]:
    """
    Encode the given string using Huffman compression with two passes.

    :param s: string to encode
    :return: tuple of the encoded string along with the corresponding encoding/decoding tree
    """
    if s == "":
        return "", HuffmanBinaryTree("", 0)

    # First pass: construct a binary tree for the string
    tree = generate_encoding_tree(s)

    # Second pass: do the encoding
    return encode(s, tree), tree


def generate_encoding_tree(s: str) -> HuffmanBinaryTree:
    """
    Generate a tree corresponding to the frequencies of the characters in the string.

    :param s: string for which the tree should be generated
    :return: encoding/decoding tree
    """
    freq_list = generate_frequency_nodes(s)

    while len(freq_list) > 1:
        node2 = freq_list.pop()
        node1 = freq_list.pop()

        new_node = node1.combine(node2)

        freq_list.append(new_node)
        freq_list.sort(key=lambda node: node.freq, reverse=True)

        # insert_keeping_sort(freq_list, new_node, lambda node: node.freq)

    # Only one node left, which is the entire tree
    return freq_list[0]


def generate_frequency_nodes(s: str) -> list[HuffmanBinaryTree]:
    """
    Generate a list of leaf nodes with frequencies based on the given string.

    :param s: string for which the nodes should be generated
    :return: list of leaf nodes
    """
    # Store a dictionary with characters as keys and values being nodes
    freq_dict = {}
    for c in s:
        if c in freq_dict:
            freq_dict[c].freq += 1
        else:
            freq_dict[c] = HuffmanBinaryTree(c, 1)

    freq_list = list(freq_dict.values())
    freq_list.sort(key=lambda node: node.freq, reverse=True)  # Sort by frequency

    return freq_list


def encode(s: str, tree: HuffmanBinaryTree) -> str:
    """
    Encode the given string using the given tree.

    :param s: string to be encoded
    :param tree: tree to use for encoding
    :return: encoded string
    """
    # Generate characters and their encoding
    encoding_dict = tree.generate_encoding_dict()

    # Encode
    encoded = ""
    for c in s:
        encoded += encoding_dict[c]

    return encoded


# ---------- DECODING ----------
def huffman_decode(s: str, tree: HuffmanBinaryTree) -> str:
    """
    Decode the given string using Huffman compression with the given tree.

    Preconditions:
    - all(c == "0" or c == "1" for c in s)

    :param s: string to be decoded
    :param tree: tree to use for decoding
    :return: decoded string
    """
    decoded = []

    while len(s) > 0:
        new_char, s = decode_next_char(s, tree)
        decoded.append(new_char)

        print(f"    Binary characters remaining: {len(s)}")

    return "".join(decoded).replace("\\n", "\n")


def decode_next_char(s: str, curr_node: HuffmanBinaryTree) -> tuple[str, str]:
    """
    Decode the next character (located at the beginning) of the encoded string.

    :param s: string to be decoded
    :param curr_node: current node in a tree to use for decoding
    :return: tuple of the decoded character, and the remaining string to be decoded
    """
    # Base case: at a leaf node
    if curr_node.left is None and curr_node.right is None:
        return curr_node.char, s

    # Recursive: continue down the tree
    elif s[0] == "0":
        return decode_next_char(s[1:], curr_node.left)
    else:  # s[0] == "1"
        return decode_next_char(s[1:], curr_node.right)

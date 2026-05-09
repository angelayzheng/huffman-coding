"""
Module for Huffman binary encoding/decoding.
"""

from __future__ import annotations


class HuffmanBinaryTree:
    """
    Representation of a binary tree for Huffman encoding/decoding.
    self.zero represents 0 and self.one represents 1 for the encoding and decoding process.
    A leaf is represented by a tree that satisfies self.zero is None and self.one is None.

    Representation Invariants:
        - self.char is not None and self.freq is not None
        - (self.zero is None) == (self.one is None)
        - if self.zero is None and self.one is None (i.e. self is a leaf node),
          then len(self.char) == 1
        - if self is an internal node,
          then self.char == self.zero.char + self.one.char and self.freq == self.zero.freq + self.one.freq
    """

    char: str
    freq: int
    zero: HuffmanBinaryTree | None
    one: HuffmanBinaryTree | None
    _string: str

    def __init__(self, char: str, freq: int,
                 zero: HuffmanBinaryTree = None, one: HuffmanBinaryTree = None):
        self.char = char
        self.freq = freq
        self.zero = zero
        self.one = one

    def __str__(self) -> str:
        return self._generate_string(0)

    def _generate_string(self, d: int) -> str:
        """
        Generate a string representation of this tree.

        :param d: depth of current call
        :return: string representation
        """
        str_so_far = f"{"  " * d}--{self.char}--{self.freq}"

        # Replace new line characters with the literal
        str_so_far = str_so_far.replace("\n", "\\n") + "\n"

        # Base case: self is a leaf node
        if self.zero is None and self.one is None:
            return str_so_far

        # Recursive: get the hashes for the subtrees
        return f"{str_so_far}{self.zero._generate_string(d + 1)}{self.one._generate_string(d + 1)}"

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
            self.zero._generate_encoding_dict_helper(encoding_dict, str_so_far + "0")
            self.one._generate_encoding_dict_helper(encoding_dict, str_so_far + "1")


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
def huffman_decode(s: list[int], tree: HuffmanBinaryTree) -> str:
    """
    Decode the given string using Huffman compression with the given tree.

    Preconditions:
    - all(c == "0" or c == "1" for c in s)

    :param s: string to be decoded
    :param tree: tree to use for decoding
    :return: decoded string
    """
    decoded = [None] * tree.freq
    i = 0

    curr_node = tree
    for bit in s:
        if bit: # 1
            curr_node = curr_node.one
        else:  # 0
            curr_node = curr_node.zero
        if curr_node.zero is None:
            decoded[i] = curr_node.char
            i += 1
            curr_node = tree

    return "".join(decoded).replace("\\n", "\n")

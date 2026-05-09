"""
Module to read/write from files with Huffman compression.
"""

from huffman_compression import HuffmanBinaryTree, huffman_encode, huffman_decode


def encode_io(input_file: str, output_file: str, tree_file: str) -> None:
    """
    Read the given file and save the encoded text and tree.

    :param input_file: file to read text from
    :param output_file: file to save encoded binary to
    :param tree_file: file to save tree to
    :return: None
    """
    print("-------- ENCODING STARTED --------")

    with open(input_file, "r", encoding='utf-8') as file:
        content = file.read()
        print(f"Finished reading text from '{input_file}'. Number of characters: {len(content)}")

    encoded, tree = huffman_encode(content)
    print(f"Finished encoding. Number of binary characters: {len(encoded)}")

    len_padding = 8 - len(encoded) % 8  # Get the number of zeros to pad
    print(f"Length of padding: {len_padding}")
    encoded = f"{len_padding:08b}" + "0" * len_padding + encoded  # Add padding to front of string
    byte_data = int(encoded, 2).to_bytes(len(encoded) // 8, byteorder='big')  # Convert to bytes

    with open(output_file, "wb") as file:
        file.write(byte_data)
        print(f"Encoded binary written to '{output_file}'.")

    with open(tree_file, "w", encoding='utf-8') as file:
        file.write(str(tree))
        print(f"Encoding tree written to '{tree_file}'.")

    print("-------- ENCODING FINISHED --------")


def decode_io(input_file: str, output_file: str, tree_file: str) -> None:
    """
    Read the given file and tree file and save the decoded text.

    :param input_file: file to read encoded binary from
    :param output_file: file to save decoded text to
    :param tree_file: file to read tree from
    :return: None
    """
    print("-------- DECODING STARTED --------")

    with open(input_file, "rb") as file:
        binary_data = file.read()
        content = "".join(f"{byte:08b}" for byte in binary_data)

    # Remove padding from the start
    len_padding = int(content[:8], 2)  # Get length of padding
    print(f"Detected length of padding: {len_padding}")
    content = content[8 + len_padding:]  # Remove padding byte and the padding
    print(f"Finished reading binary data from '{input_file}'. Number of binary characters: {len(content)}")

    tree = read_tree_from_file(tree_file)
    print(f"Finished reading encoding tree from '{tree_file}'.")

    print("Started decoding.")
    decoded = huffman_decode(content, tree)
    print("Finished decoding.")

    with open(output_file, "w", encoding='utf-8') as file:
        file.write(decoded)
        print(f"Decoded text written to '{output_file}'.")

    print("-------- DECODING FINISHED --------")


def read_tree_from_file(tree_file: str) -> HuffmanBinaryTree:
    """
    Read a tree from the given file.

    Preconditions:
        - tree_file is a valid hash of a HuffmanBinaryTree

    :param tree_file: file to read tree from
    :return: constructed tree
    """
    with open(tree_file, "r", encoding='utf-8') as file:
        content = file.read().splitlines()

    # Create list of tuples containing line depths and nodes
    data = []
    for i in range(0, len(content)):
        data.append((depth_of_line(content[i]),
                     HuffmanBinaryTree(get_char_from_line(content[i]), get_freq_from_line(content[i]))))

    return construct_tree(data, 0)


def construct_tree(data: list[tuple[int, HuffmanBinaryTree]], curr_d: int) -> HuffmanBinaryTree | None:
    """
    Create a tree from node and depth data.

    :param data: list of tuples containing corresponding depths and nodes
    :param curr_d: current depth to look for
    :return: the constructed tree
    """
    # Base case: next node is not at the current depth. Then we have gone too far, so return None
    if len(data) == 0 or data[0][0] < curr_d:
        return None

    # Recursive:
    # Get the node
    curr_tree = data[0][1]
    data.pop(0)

    # Get the left subtree
    curr_tree.left = construct_tree(data, curr_d + 1)

    # Get the right subtree
    curr_tree.right = construct_tree(data, curr_d + 1)

    return curr_tree


def depth_of_line(line: str) -> int:
    """
    Get the depth of a line of tree data, corresponding to the length of the
    starting whitespace divided by 2.

    :param line: one line from a tree file
    :return: the depth of the given line
    """
    i = 0
    while i < len(line):
        if line[i] != " ":
            return i // 2
        i += 1

    return -1


def get_char_from_line(line: str) -> str:
    """
    Get the character(s) portion of a line of tree data.

    :param line: one line from a tree file
    :return: the character(s) for this node
    """
    no_spaces = line.lstrip()

    assert no_spaces[:2] == "--"

    if no_spaces[2] == "-":
        return "-" + no_spaces.split("-")[3]
    else:
        return no_spaces.split("-")[2]


def get_freq_from_line(line: str) -> int:
    """
    Get the frequency portion of a line of tree data.

    :param line: one line from a tree file
    :return: the frequency for this node
    """
    return int(line.split("-")[-1])

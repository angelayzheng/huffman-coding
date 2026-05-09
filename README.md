# Huffman Coding

After being challenged to do so by my friend, I wrote a Python module that implements the [Huffman coding algorithm](https://en.wikipedia.org/wiki/Huffman_coding), completed on April 30, 2026. You can read more about what I did in my [blog post](https://angelazheng.ca/projects/huffman-coding/).

*Note: I committed everything over a week after I completed this, which is why the entire commit history is compressed in time.*

## How to Use

- Clone the repository.
- Run the `runner.py` file (one way is to run `python runner.py` in the terminal).
- It will prompt you to enter the file path to the input file to be encoded. For example, `data/pride-and-prejudice.txt`.
- It will prompt you to enter the file path to the output file, which will be saved after decoding. For example, `data/pride-and-prejudice_decoded.txt`.
- After it finishes, you should also see the encoded file `inputfilepath.bin` and `inputfilepath.tree` saved in the same directory.

Alternatively, you can also manually use the `encode_io` and `decode_io` functions in `huffman_io.py`.
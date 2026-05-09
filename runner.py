import sys

from huffman_io import encode_io, decode_io

print("-------- HUFFMAN CODING --------")

print("Input file path:")
input_file = sys.stdin.readline().strip()

print("Output file path:")
output_file = sys.stdin.readline().strip()

encode_io(input_file, f"{input_file}.bin", f"{input_file}_tree.txt")
decode_io(f"{input_file}.bin", output_file, f"{input_file}_tree.txt")
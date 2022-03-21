import random
import sys
from HeaderReader import read_header

in_rom = open(sys.argv[1], "rb")
#out_rom = open(sys.argv[1].split(".")[0] + "_out." + sys.argv[1].split(".")[1], "wb")
output = open("output.txt", "w")

split_filename = sys.argv[1].split("\\")
output.write("----- " + split_filename[len(split_filename)-1] + " -----")

output.write(read_header(in_rom.read(16)))
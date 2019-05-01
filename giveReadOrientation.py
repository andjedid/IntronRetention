import sys 
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()
file = args.file

resfile = open(file.split(".bed")[0] + ".orientation.bed","w")

dico_reads = {}

with open(file) as f1:
	for line in f1:

		items = line.split("\t")
		read_info = items[3].strip()
		orientation = int(read_info.split("/")[1])
		name = read_info.split("/")[0]
		
		if orientation == 2:
			strand = items[5].strip()
			dico_reads[name] = strand


with open(file) as f1:
	for line in f1:
		items = line.split("\t")
		read_info = items[3].strip()
		name = read_info.split("/")[0]
		new_line = ""
		for i in range(0,5):
			new_line += items[i] + "\t"
		new_line = new_line + dico_reads[name] + "\n"
		resfile.write(new_line)
		


print("generated file: " + file.split(".bed")[0] + ".orientation.bed")

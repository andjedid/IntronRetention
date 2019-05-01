import sys 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--aligner", "-a", type=str, required=True)
args = parser.parse_args()
file = args.file
aligner = args.aligner
resfile = open(file.strip().split(".bed")[0] + ".uniqueMappedReads.bed","w")


with open(file, "r") as f1:
	for line in f1:
		items = line.split("\t")
		mapq = int(items[4].strip())
		if aligner == "tophat":
			if mapq == 50: 
				resfile.write(line)
				query_start = int(items[1])
				query_end = int(items[2])
		elif aligner == "star":
			if mapq == 60: #using Eric's pipeline 
				resfile.write(line)
		else:
			print("specify an aligner, please.")
			sys.exit(-1)

print("generated file: " + file.strip().split(".bed")[0] + ".uniqueMappedReads.bed")	
sys.exit(0)	

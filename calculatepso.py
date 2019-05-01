import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--jcnfile", "-j", type=str, required=True)
parser.add_argument("--borderfile", "-i", type=str, required=True)
args = parser.parse_args()



jcn_file = args.jcnfile
border_file =  args.borderfile
resfile = open(border_file.strip().split("_intron.counts")[0] + "_pso.counts","w")

dico_border_span = {}
with open(border_file, "r") as f1:
	for line in f1:
		items = line.split("\t")
		chrm = items[0]

		pos = int(items[3].split(".")[-2])
		name =  items[3].split(".")[1]
		strand = items[5]
		count = int(items[-1].strip())

		if chrm not in dico_border_span:
			dico_border_span[chrm] = {}

		dico_border_span[chrm][pos] = (count, name)



dico_jcn = {}
with open(jcn_file, "r") as f1:
	for line in f1:

		items = line.split("\t")
		chrm_jcn = items[0]

		if chrm_jcn in dico_border_span:
			#print items
			start_jcn = int(items[1]) - 1
			end_jcn = int(items[2]) + 1

			count_jcn = int(items[6].strip())
			count_pos1 = 'NA'
			count_pos2 = 'NA'
			LEFT_OK = False
			RIGHT_OK = False
			if start_jcn in dico_border_span[chrm_jcn]:
				count_pos1 = float(dico_border_span[chrm_jcn][start_jcn][0])
				LEFT_OK = True

			if end_jcn in dico_border_span[chrm_jcn]:
				count_pos2 = float(dico_border_span[chrm_jcn][end_jcn][0])
				RIGHT_OK = True
			
			if (LEFT_OK == True and RIGHT_OK == True):
				name_gene = dico_border_span[chrm_jcn][end_jcn][1]
				mean_pos = (count_pos1 + count_pos2)/2

				if (mean_pos + float(count_jcn) != 0):
					pso = float(count_jcn)/(mean_pos + float(count_jcn))
				else:
					pso = 'NA'
			else:
				name_gene = "Unknown"
				pso = 'NA'

			#print name_gene
			newline = name_gene + "\t" + chrm_jcn +  "\t" + str(start_jcn) + "\t" + str(end_jcn) + "\t" + str(count_jcn) + "\t" + str(count_pos1) + "\t" + str(count_pos2) + "\t" +  str(pso) + "\n"
			resfile.write(newline)





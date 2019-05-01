import os, sys, argparse, re, glob


parser = argparse.ArgumentParser()
parser.add_argument("--intron_bed",
                  help="path to the file containing the border coordinates of introns.")
parser.add_argument("--bed_dir", 
                  help="directory where are located the bed files")
parser.add_argument("--jcn_dir", 
                  help="directory where are located the jcn files (SJ.out.tab of star)")
parser.add_argument("--samples", 
                  help="sample names (separated with a comma).")
parser.add_argument("--genome", 
                  help="ex : mm10, hg19")
parser.add_argument("--path_result", 
                  help="result directory")
parser.add_argument("--aligner", 
                  help="star (only star for the moment)")


args = parser.parse_args()


intron_bed = args.intron_bed
bed_dir = args.bed_dir
jcn_dir = args.jcn_dir
genome = args.genome
path_result = args.path_result
aligner = args.aligner


#test
intron_bed = "/project/6007495/adjedid/references/mm10/eric_gtf/borders_of_introns_of_the_genes_2.sorted.bed"
bed_dir = "/project/6007495/adjedid/resources/splicing_pipeline/retained_introns/github/test"
jcn_dir = "/project/6007495/adjedid/resources/splicing_pipeline/retained_introns/github/test"
samples="E9-0-1-50000,E9-0-2-50000"
genome = "mm10"
path_result = '/project/6007495/adjedid/resources/splicing_pipeline/retained_introns/github/test/result'
aligner = "star"

dico_samples = {}
samples=samples.split(",")
for sample in samples:
	files = os.listdir(bed_dir)
	sample_bed = glob.glob(bed_dir + "**/" + sample + "*.bed")
	sample_jcn = glob.glob(jcn_dir + "**/" + sample + "*SJ.out.tab")
	dico_samples[sample] = (sample_bed, sample_jcn)


#1. Create bed from bam file
for sample in samples:

	bed_file = dico_samples[sample][0][0]
	print(bed_file)
	#filter the unique mapped reads
	bed_file2 = bed_file.split(".bed")[0] + ".uniqueMappedReads.bed"
	
	command = "python keepUniqMappedReads.py --file " + bed_file + " --aligner " + aligner
	os.system(command)
	
	#change the strand of the read for the read orientation  
	bed_file3 = bed_file2.split(".bed")[0] + ".orientation.bed"
	command = "python giveReadOrientation.py --file " + bed_file2
	os.system(command)
	
	bed_file4 = bed_file3.split(".bed")[0] + ".sorted.bed"
	command = "sortBed -i " + bed_file3 + " > " + bed_file4 
	os.system(command)

	#count the number of reads mapping completely the intron borders
	resfile = path_result + "/" + sample + "_intron.counts"
	command = "bedtools map -o count -f 1 -s -a " + intron_bed + " -b " + bed_file4 + " > " + resfile
	os.system(command)
	

	jcnfile = dico_samples[sample][1][0]
	command = "python calculatepso.py --jcnfile " +  jcnfile + " --borderfile " + resfile
	os.system(command)
	sys.exit(0)

	

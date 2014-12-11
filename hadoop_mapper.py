import sys
from operator import itemgetter

# Dictionary "chrom id: [start_line, endline]"
# For chromosome fragments line distribution in the 'gene' file
LINE_IDX_4_CHROM = {}

class Frag2GeneMap(object):
	def __init__(self, gene_file_name, frag_file):
		self.gene_file_name = gene_file_name
		self.frag_file = frag_file

	# 'gene' file line index for each type of chromosome
	def lineIdx4ChromId(self):
		global LINE_IDX_4_CHROM
		chromId = ''
		geneFile = self.getGeneFile()
		for line in geneFile:
			words = line.strip().split()
			# Chrom id located at 2nd column
			if words[1] == chromId:
				endline = int(words[0]) - 1
				LINE_IDX_4_CHROM[chromId][1] = endline
			else:
				chromId = words[1]
				line_num = int(words[0]) - 1
				LINE_IDX_4_CHROM[chromId] = [line_num, line_num]

	# Compare chromosome fragment to each gene
	# Each line has TWO fragments, here for ONE fragment
	def frag2gene(self, chrom_id, frag_start_val, frag_end_val):
		
		# Line index for one type of chromosome in 'gene' file
		startline = LINE_IDX_4_CHROM[chrom_id][0]
		endline = LINE_IDX_4_CHROM[chrom_id][1]
		
		# List for 'Overlapped' gene
		genelist = []

		# Read 'gene' file
		geneFile = self.getGeneFile()
		
		for i, line in enumerate(geneFile): 

			if startline <= i <= endline:

				gene_words = line.strip().split()
				# If 'strand' of this gene is '+', start position on the left
				if gene_words[2] == '+':
					gene_start_val = gene_words[3]
					gene_end_val = gene_words[4]

					if not gene_end_val <= frag_start_val and not gene_start_val >= frag_end_val:
						genelist.append([gene_words[0], gene_start_val])
				# 'strand' is '-', start on the left
				elif gene_words[2] == '-':
					gene_start_val = gene_words[4]
					gene_end_val = gene_words[3]

					if not gene_start_val <= frag_start_val and not gene_end_val >= frag_end_val:
						genelist.append([gene_words[0], gene_start_val])

				else:
					raise ValueError("Gene mark wrong. Neithr + nor -.")
		self.fileClose(geneFile)
		return genelist

	# Read 'gene' file
	def getGeneFile(self):
		return open(self.gene_file_name, 'r')

	def fileClose(self, geneFile):
		geneFile.close()

	# Compare distances from midvalue of chromosome and gene's start
	# Pick the closest gene
	def genePick(self, midVal, genelist):
		d_val_list = []
		for i in genelist:
			d_val_list.append(abs(int(i[1]) - midVal))
		i, value = min(enumerate(d_val_list), key = itemgetter(1))
		return genelist[i][0]


	def start(self):
		# Read 'input' file
		fragFile = self.frag_file
		# Each line in 'input' file
		for line in fragFile:
			words = line.strip().split()
			# Each line has two chromosome fragments
			# Determine if two parts are overlapped by some gene, and get those gene
			genelist_1 = self.frag2gene(words[0], words[1], words[2])
			genelist_2 = self.frag2gene(words[3], words[4], words[5])

			if genelist_1 and genelist_2:
				midVal1 = (int(words[2]) - int(words[1])) / 2
				midVal2 = (int(words[5]) - int(words[4])) / 2
				gen1 = self.genePick(midVal1, genelist_1)
				gen2 = self.genePick(midVal2, genelist_2)
				# Generate result and print
				print "%s:%s\t%d" % (gen1, gen2, 1)
				


if __name__ == '__main__':
	# stdin way input 'input' file
	fragFile = sys.stdin
	
	frag2genemap = Frag2GeneMap('gene', fragFile)
	frag2genemap.lineIdx4ChromId()
	frag2genemap.start()



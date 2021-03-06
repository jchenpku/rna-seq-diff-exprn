#!/usr/local/bin/python2.7
# encoding: utf-8
"""
get_transcript_coverage.py

Created by Olga Botvinnik on 2012-03-19.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.

Example run: ~/get_transcript_coverage.py -abed ~/mm9_ensembl-genes_single-exon.merged.stranded.bed -abam 100ng-1_sino.bam
"""
import pybedtools
import HTSeq
import itertools

#################################################################
# CommandLine
#################################################################
class CommandLine(object) :
	'''
	Handle the command line, usage and help requests.

	CommandLine uses argparse, now standard in 2.7 and beyond. 
	it implements a standard command line argument parser with various 
	argument options,
	a standard usage and help, and an error termination 
	mechanism do-usage_and_die.

	attributes:
	myCommandLine.args is a dictionary which includes each of the available 
	command line arguments as
	myCommandLine.args['option'] 
	
	methods:
	do_usage_and_die()
	prints usage and help and terminates with an error.
	'''
	
	def __init__(self, inOpts=None) :
		'''
		CommandLine constructor.
		Implements a parser to interpret the command line argv string using 
		argparse.
		'''
		
		import argparse
		self.parser = \
			    argparse.ArgumentParser(\
			description = '''Finds the
		coverage of each feature in the 
		gff file, in the sam file.''',	
			add_help = True, #default is True 
			prefix_chars = '-', 
			usage = '''%(prog)s
			-asam <SAM FILE> 
			-o <OUTPUT PREFIX>'''
			# -agff <GFF FILE>'''  
			)
		# self.parser.add_argument("bam", action="store", help="input bam file")
		self.parser.add_argument(\
			'-asam', '--sam-file', \
			action = 'store',
			help='input sam file', required=True) 
		self.parser.add_argument(\
			"-o", "--output-prefix", \
			action="store",
			help='''output prefix for *.wig
			and other files''', required=True)
		# self.parser.add_argument('-agff', '--gff-file', action = 'store',
		# 	help='input bed')
		if inOpts is None :
			self.args = vars(\
				self.parser.parse_args())
		else :
			self.args = vars(\
				self.parser.parse_args(inOpts))


	def __del__ (self) :
		'''
		CommandLine destructor.
		'''
		# do something if needed to clean up before leaving
		pass   

	def do_usage_and_die (self, str) :
		'''
		If a critical error is encountered, where it is suspected that the 
		program is not being called with consistent parameters or data, this
		method will write out an error string (str), then terminate execution 
		of the program.
		'''
		import sys
		print >>sys.stderr, str
		self.parser.print_usage()
		return 2

class Usage(Exception):
	'''
	Used to signal a Usage error, evoking a usage statement and eventual exit 
	when raised.
	'''
	def __init__(self, msg):
		self.msg = msg

		
#################################################################
# Main
# Here is the main program
# 
#
#################################################################
def main(cl=None):
	'''
	Implements the Usage exception handler that can be raised from anywhere 
	in process.  

	'''
	if cl is None:
		cl = CommandLine()
	else :
		cl = CommandLine(['-r'])

	try:
		print cl.args  # print the parsed argument string
		alignment_file = HTSeq.SAM_Reader(cl.args["sam_file"])
		
		# Get coverage for the whole genome
		cvg = HTSeq.GenomicArray( "auto", stranded=False, typecode='i' )
		for alngt in alignment_file:
			if alngt.aligned:
				cvg[ alngt.iv ] += 1
				
		# Write a "Wiggle" file for genome browser viewing
		cvg.write_bedgraph_file(cl.args["output_prefix"]+".wig")
				
		# Now need to iterate over every gene/transcript and get the
		# per-transcript coverage
		# gtf_file = HTSeq.GFF_Reader("/home/pvcastro/reference_known_genes.gtf")
		
	except Usage, err:
	   cl.do_usage_and_die(err.msg)

if __name__ == "__main__":
	main();
	raise SystemExit
	
# To test, uncomment below:
# import HTSeq
# alignment_file = HTSeq.BAM_Reader("/home/obot/single-cell/mapped/Sample_3/run2/accepted_hits_rmdup.bam")
# cvg = HTSeq.GenomicArray( "auto", stranded=False, typecode='i' )
# for alngt in alignment_file:
# 	if alngt.aligned:
# 		cvg[ alngt.iv ] += 1
# gtf_file = HTSeq.GFF_Reader("/home/pvcastro/reference_known_genes.gtf")
# for feature in itertools.islice( gtf_file, 10 ):
# 	iv = str(feature.iv)
# 	chrom = iv.split(":")[0]
# 	start = int(iv.split("[")[1].split(",")[0])
# 	stop = int(iv.split(",")[1].split(")")[0])
# 	print list(cvg[HTSeq.GenomicInterval(chrom, start, stop)])
# 	# print numpy.histogram(list(cvg[HTSeq.GenomicInterval(chrom, start, stop)]),
# 	# 	bins=100)
	

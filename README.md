# ESS - Epigenetic signature software
Searches for imprinting defects and other allelic imbalance patterns from long read data by comparing a case to a collection of controls.

1: Extract methylation data from bam files with methylartist (https://github.com/adamewing/methylartist):

	methylartist wgmeth -b {bam} -r {ref} -f {ref}.fai  --motif CG --mod m --primary_only -p {cores} -q 0 --phased --dss

The input bam file should be phased using software such as whatshap.

2: convert methylartist dss files to bed

	bash convert_bed.sh {prefix}

requires tabix, the script assumes that the dss output is named the following way:

	{prefix}.happlotagged.m.phase_0.DSS.txt
	{prefix}.happlotagged.m.phase_1.DSS.txt

The output is a tabix indexed bed file named

	{prefix}.bed.gz

3: setup the controls:
generate a text file listing the path to the control bed files. I recomend storing the control bed files in a folder

	ls control/*bed.gz > controls.txt

4: run ess.py

	ess.py {case}.bed.gz controls.txt praderwilli.txt > {case}.results.txt

The {case}.bed.gz file is generated according to step (2). controls.txt is generated accorfing to (2). The praderwilli.txt is a bed file listing the regions of interest (such as promoters of known imprinting genes).





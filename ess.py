import numpy
import pysam
import sys
import scipy.stats as st

regions_file=sys.argv[3]
regions={}
for region in open(regions_file):
	content=region.strip().split()
	regions[content[-1]]=[content[0],int(content[1]),int(content[2])]

control_files=sys.argv[2]
controls=[]
for control in open(control_files):
	controls.append(control.strip())

case_bed=pysam.TabixFile(sys.argv[1])
case={}
print("region,chromosome,start,end,epigenetic_imbalance_ratio,CI_control_epigenetic_imbalance_ratios,Significant,Zscore,epigenetic_imbalance_ratios")
for region in regions:
	chr=regions[region][0]
	start=regions[region][1]
	end=regions[region][2]

	diff_case=[]
	positions=set([])
	for row in case_bed.fetch(chr,start,end):
		c=row.split("\t")
		if c[3] == "[]" or c[4] == "[]":
			continue
		positions.add(int(c[1]))
		diff_case.append( abs(float(c[3].split(":")[-1])-float(c[4].split(":")[-1])) )

	#print(diff_case)
	control_medians=[]
	for control in controls:
		control_bed=pysam.TabixFile(control)
		diff_control=[]
		for row in control_bed.fetch(chr,start,end):
			c=row.split("\t")
			if c[3] == "[]" or c[4] == "[]":
				continue
			if int(c[1]) not in positions:
				continue
			diff_control.append( abs(float(c[3].split(":")[-1])-float(c[4].split(":")[-1])) )

		
		control_medians.append(numpy.median(diff_control))
		control_bed.close()

	median_case=numpy.median(diff_case)
	control_signals='|'.join(map(str,control_medians))
	ci=st.t.interval(alpha=0.95, df=len(control_medians)-1, loc=numpy.mean(control_medians), scale=st.sem(control_medians)) 
	zscore=(median_case-numpy.average(control_medians))/numpy.std(control_medians)

	significant="No"
	if median_case < ci[0] or median_case > ci[1]:
		significant="Yes"
	print(f"{region},{chr},{start},{end},{median_case},({ci[0]},{ci[1]}),{significant},{zscore},({control_signals})")

import sys

positions={}

p1=f"{sys.argv[1]}.happlotagged.m.phase_0.DSS.txt"
p2=f"{sys.argv[1]}.happlotagged.m.phase_1.DSS.txt"

first=True

chromosomes=[]

for line in open(p1):
	if first:
		first=False
		continue

	content=line.strip().split()
	content[1]=int(content[1])

	if not content[0] in positions:
		positions[content[0]]={}
		chromosomes.append(content[0])
	if not content[1] in positions[content[0]]:
		positions[content[0]][content[1]]=[[],[]]

	positions[content[0]][content[1]][0]=f"{content[2]}:{content[3]}:{float(content[3])/float(content[2])}"

first=True
for line in open(p2):
	if first:
		first=False
		continue

	content=line.strip().split()
	content[1]=int(content[1])

	if not content[0] in positions:
		positions[content[0]]={}
	if not content[1] in positions[content[0]]:
		positions[content[0]][content[1]]=[[],[]]

	positions[content[0]][content[1]][1]=f"{content[2]}:{content[3]}:{float(content[3])/float(content[2])}"

for chromosome in chromosomes:
	for pos in sorted(positions[chromosome]):
		print(f"{chromosome}\t{pos-1}\t{pos}\t{positions[chromosome][pos][0]}\t{positions[chromosome][pos][1]}")

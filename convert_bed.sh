python bed_from_DSS.py $1 > $1.bed
bgzip $1.bed
tabix -p bed $1.bed.gz

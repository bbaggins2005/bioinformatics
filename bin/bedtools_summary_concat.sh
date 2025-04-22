#!/usr/bin/env bash
# name:		bedtools_summary_concat.sh
# author:	Reece Chae
# description:	Concatenate bedtools summary output into one tsv

SUMMARYDATA_DIR=$1
mapfile -t CHROM_LIST <<EOF
chr1:1
chr2:2
chr3:3
chr4:4
chr5:5
chr6:6
chr7:7
chr8:8
chr9:9
chr10:10
chr11:11
chr12:12
chr13:13
chr14:14
chr15:15
chr16:16
chr17:17
chr18:18
chr19:19
chr20:20
chr21:21
chr22:22
chrX:chrX
chrY:chrY
chrM:chrM
all:all
EOF

printf "sample\tchrom\tchr\tchrom_length\tnum_ivls\ttotal_ivl_bp\tchrom_frac_genome\tfrac_all_ivls\tfrac_all_bp\tmin\tmax\tmean\n"
for CHROM_PAIR in ${CHROM_LIST[*]}; do
	for FILE in $(ls ${SUMMARYDATA_DIR}/*.tsv | sort); do
		SAMPLENAME=$(basename ${FILE} | cut -d'_' -f2)
		printf "${SAMPLENAME}\t"
		IFS=":" read -ra CHROM <<< ${CHROM_PAIR}
		LINE=$(grep -w ^${CHROM[0]} ${FILE} | sed "s/^\([^\t]*\t*\)/\1\t${CHROM[1]}\t/" )
		printf "${LINE}\n"
	done
done

exit 0
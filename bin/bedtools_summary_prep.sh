#!/usr/bin/env bash
# name:		bedtools_summary_prep.sh
# author: 	Reece Chae
# description: Basic tool to compress and index bed files.
# 		Can also prepare bed files for bedtools summary
# 		Script requires bgzip and tabix and can be used with docker image (staphb/htslib). 
#

COMPRESSANDINDEX=false

usage() {
	printf "usage:     	$0 -i <input bed file> \n"
	printf "		-i <input bed file> (required) \n"
	printf "		-g <genome reference file>.  If specified, will create a filtered bed file from input bed file, composed of only chromosomes defined in genome reference file. (optional)\n"
	printf "		-c compress and index output (optional, default = false) \n\n"
	printf "1. Compress and index bed file\n"
	printf " $ $0 -i input.bed -c  \n\n"
	printf "2. Create filtered bed file from bed file using genome reference file\n"
	printf " $ $0 -i input.bed -g genome.tsv  \n"
	printf "\n\n\n"
	exit 1
}

check_prereq() {
	if [ ! -e "${INPUTBED}" ]; then  
		printf "erro: The input file ${INPUTBED} does not exist\n\n"
		usage
	elif [ -n "${GENOMEFILE}" ] && [ ! -e "${GENOMEFILE}" ]; then
		printf "erro: The genome reference file ${GENOMEFILE} does not exist\n\n"
		usage
	fi
}

compressandindex() {
	BEDFILE=$1
	printf "info: compressing ${BEDFILE}\n"
	bgzip ${BEDFILE}
	printf "info: creating index for ${BEDFILE} with tabix\n"
	tabix -p bed ${BEDFILE}.gz
}

# main
while getopts "i:g:ch" opt; do
	case ${opt} in
		i)
		INPUTBED=${OPTARG}
		OUTPUTBED=${INPUTBED}
		;;
		g) 
		GENOMEFILE=${OPTARG}
		BEDBASENAME=$(basename ${INPUTBED})
		BEDDIRNAME=$(dirname ${INPUTBED})
		FILTEREDBED=$(echo ${BEDDIRNAME}/filtered_${BEDBASENAME} )
		;;
		c)
		COMPRESSANDINDEX=true
		;;
		h)
		usage
		;;
		\?)
		echo "Invalid option: -${OPTARG}" >&2
		usage
		;;
		:)
		echo "Option -${OPTARG} require argument." >&2
		usage
		;;
	esac
done
shift $((OPTIND -1))

check_prereq
if [ -n "${FILTEREDBED}" ]; then
	VALID_CHR=$(awk '{print $1}' ${GENOMEFILE} )
	printf "info: creating filtered ${INPUTBED} using ${GENOMEFILE}\n"
	grep -wFf <(echo "${VALID_CHR}" ) ${INPUTBED} > ${FILTEREDBED}
	OUTPUTBED=${FILTEREDBED}
fi
if [ "${COMPRESSANDINDEX}" = true ]; then
	compressandindex ${OUTPUTBED}
fi

exit 0
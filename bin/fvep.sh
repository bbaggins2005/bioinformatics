#!/usr/bin/env bash
# name:		fvep.sh
# author: 	Reece Chae
# description:	Basic wrapper script for filter_vep
#

FILTERCMD=${HOME}/Projects/ensembl-vep/filter_vep 
COMPRESSANDINDEX=false
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

usage() {
	printf "usage:     	$0 -i <input vcf> -f <filter expression> [ -c (optional) ]  \n"
	printf "description:	Basic wrapper script for filter_vep \n\n"
	printf "		-i <compressed or uncompressed input vcf> \n"
	printf "		-f <filter_vep filter expression> \n"
	printf "		-c compress and index output (optional, default = false) \n\n\n\n"
	exit 1
}

check_prereq() {
	if [ -z "${INPUTVCF}" ] || [ -z "${FILTER}" ]; then
		printf "Error: must specify the -i and -f switches\n\n"
		usage
	elif [ ! -e "${INPUTVCF}" ]; then  
		printf "Error: The input file ${INPUTVCF} does not exist\n\n"
		usage
	elif [ "${#FILTER}" -eq 0 ]; then
		printf "Error: Filter is null.  Please specify filter\n\n"
		usage
	fi
}

compressandindex() {
	CI_VCFFILE=$1
	bgzip ${CI_VCFFILE}
	tabix -p vcf ${CI_VCFFILE}.gz
}

# main
while getopts "i:f:ch" opt; do
	case ${opt} in
		i)
		INPUTVCF=${OPTARG}
		OUTPUTVCF=$(echo ${INPUTVCF} | tr '[:upper:]' '[:lower:]' | sed -E "s/(\.vcf|\.vcf\.gz)$/_output_${TIMESTAMP}&/")
		;;
		f) 
		FILTER=${OPTARG}
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
${FILTERCMD} --format vcf -i ${INPUTVCF} -o ${OUTPUTVCF} --filter "${FILTER}" --force_overwrite
if [ "${COMPRESSANDINDEX}" = true ]; then
	compressandindex ${OUTPUTVCF}
fi

exit 0
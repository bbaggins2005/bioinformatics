#!/usr/bin/env bash
# name:		coverage_depth.sh
# author: 	Reece Chae
# description:	Basic wrapper script for coverage and depth analysis
# https://medium.com/ngs-sh/coverage-analysis-from-the-command-line-542ef3545e2c
# Requires image: staphb/bedtools

INPUT=$1
MODE=$2
OUTPUTFILEPREFIX=$(basename ${INPUT})
OUTPUTDIR="data"
LOGDIR="log"

[ -d "${OUTPUTDIR}" ] || mkdir -p ${OUTPUTDIR}
[ -d "${LOGDIR}" ] || mkdir -p ${LOGDIR}
OUTPUTFILE="${OUTPUTDIR}/${OUTPUTFILEPREFIX}"
LOGFILE="${LOGDIR}/coverage_depth_${OUTPUTFILEPREFIX}.log"
echo "info: Starting bedtools for ${INPUT}" | tee -a ${LOGFILE}
if [ "${MODE,,}" = "zero" ]; then
    echo "info: generating bed file for zero coverage"
    bedtools genomecov -ibam ${INPUT} -bga | grep -w "0$" > ${OUTPUTFILE}_zero.bed
elif [ "${MODE,,}" = "all" ]; then
    echo "info: generating bed file for all coverage"
    bedtools genomecov -ibam ${INPUT} -bga > ${OUTPUTFILE}_all.bed
else
    echo "info: generating bed file for standard coverage"
    bedtools genomecov -ibam ${INPUT} -bg > ${OUTPUTFILE}.bed
fi
echo "info: Completed. See ${OUTPUTFILE} bed file" | tee -a ${LOGFILE}
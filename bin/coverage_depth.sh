#!/usr/bin/env bash
# name:		coverage_depth.sh
# author: 	Reece Chae
# description:	Basic wrapper script for coverage and depth analysis
# https://medium.com/ngs-sh/coverage-analysis-from-the-command-line-542ef3545e2c
# Requires image: staphb/bedtools

INPUT=$1
OUTPUTFILEPREFIX=$(basename ${INPUT})
OUTPUTDIR="data"
LOGDIR="log"

[ -d "${OUTPUTDIR}" ] || mkdir -p ${OUTPUTDIR}
[ -d "${LOGDIR}" ] || mkdir -p ${LOGDIR}
OUTPUTFILE="${OUTPUTDIR}/${OUTPUTFILEPREFIX}.bed"
LOGFILE="${LOGDIR}/coverage_depth_${OUTPUTFILEPREFIX}.log"
echo "info: Starting bedtools for ${INPUT}" | tee -a ${LOGFILE}
bedtools genomecov -ibam ${INPUT} -bga | grep -w "0$" > ${OUTPUTFILE}
echo "info: Completed. See ${OUTPUTFILE}" | tee -a ${LOGFILE}
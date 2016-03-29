#!/bin/bash
# 
# Usage ./change_encoding ./ (converts videos from the current directory that are an mkv container)
#       ./change_encoding DIRECTORY (looks in that directory for videos to encode)

basepath=$(basename "${1}")
dirpath=$(dirname "${1}")
encodepath="${dirpath}/${basepath}/"

for file in "${encodepath}"*.mkv; do
  inputfile="${file}"
  outputfile="${file%.mkv}_hevc.mkv"
  errorfile="${outputfile}.hevc_error.log"
  durregex='(?<=Duration\s{33}:\s)(\d{1,2}h)?\s*(\d{1,2}mn)?\s*(\d{1,2}s)?'
  errorfree=0
  sametime=0

  while [[ $errorfree != 1 || $sametime != 1 ]]; do
    if [[ -e "${outputfile}" ]]; then
      rm "${outputfile}"
    fi    

    ffmpeg \
    -i "${inputfile}" \
    -c:v libx265 -preset ultrafast -x265-params \
    crf=23:qcomp=0.75:aq-mode=1:aq_strength=1.0:qg-size=16:psy-rd=0.7:psy-rdoq=5.0:rdoq-level=1:merange=44 \
    -c:a copy \
    -c:s copy \
    "${outputfile}";

    ffmpeg -v error -i "${outputfile}" -f null - 2>"${errorfile}"

    if [[ -s "${errorfile}" ]]; then
      errorfree=0
    else
      errorfree=1
    fi

    orgtime=$(mediainfo ${inputfile} |  grep -m 1 -oP "${durregex}")
    newtime=$(mediainfo ${outputfile} |  grep -m 1 -oP "${durregex}")

    if [[ "${orgtime}" = "${newtime}" ]]; then
      sametime=1
    fi
  done
 
  rm "${inputfile}" "${errorfile}"

  sleep 2

  mv "${outputfile}" "${inputfile}"

  sleep 240
done

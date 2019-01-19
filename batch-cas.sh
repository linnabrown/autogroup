#!/bin/bash


for dir in /ssd/huangle/archaea_gff_faa_fna/*
do
{
  if [ -d "$dir" ]
    then
       for file_name in $dir/*
       do
           {
               ${file_name#*.}
               if [ "${file_name#*.}"x = "faa"x ]; then
                   faa="$file_name"
               elif [ "${file_name#*.}"x = "fna"x ]; then
                   fna="$file_name"
               elif ["${file_name#*.}"x = "gff"x]; then
                   gff="$file_name"
               fi

           }
       done
       echo acr_aca_cri_runner.py -n $fna -f $gff -a $faa -o /ssd/huangle/archaea_gff_faa_fna_output/${dir##*/}
  fi
}
done

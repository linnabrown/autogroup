#!/bin/bash


for dir in /ssd/huangle/archaea_gff_faa_fna/*
do
{
  if [ -d "$dir" ]
    then
       for file_name in $dir/*
       do
           {
               suffix=${file_name#*.}
               if [ "$suffix" == "faa" ]; then
                   faa="$file_name"
               elif [ "$suffix" == "fna" ]; then
                   fna="$file_name"
               else
                   gff="$file_name"
               fi

           }
       done
       python acr_aca_cri_runner.py -n $fna -f $gff -a $faa -o /ssd/huangle/archaea_gff_faa_fna_output/${dir##*/}
}&done

#!/bin/bash

#
for dir in /ssd/huangle/archaea_gff_faa_fna/*;
do
{
  if [ -d "$dir" ]; then

       echo acr_aca_cri_runner.py -n "$dir"_genomic.fna -f "$dir"_genomic.gff -a "$dir"_protein.faa -o /ssd/huangle/archaea_gff_faa_fna_output/${dir##*/}
  fi
}
done

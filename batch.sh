fn="/ibgpu01/huangle/acr_aca_finder_result/complete_genome_bac_batch"
for (( i=0; i<23; i++ ))
     do  
         {   
             for element in `ls $fn/$i`
             do 
                gcf=$fn/$i/$element
                if [ -d $gcf ]
                then
                   docker run --rm -v $gcf/:/app/acr_aca_finder/${gcf##*/}\
                    -i haidyi/acr_aca_finder:latest\
                    python3 acr_aca_cri_runner.py\
                    -n ${gcf##*/}/${gcf##*/}_genomic.fna\
                    -f ${gcf##*/}/${gcf##*/}_genomic.gff\
                    -a ${gcf##*/}/${gcf##*/}_protein.faa\
                    -o ${gcf##*/}/output\
                    -c 0 -z B
                fi
             done
         } &  #将上述程序块放到后台执行 
     done
     wait

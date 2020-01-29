import sys
import os

sys.path.append(os.path.abspath("/home/qxu/projects/regulatoryNetwork/cell_trans/data"))

from runenhancer import *

RUN_INDEX={"KRT_p300":"SE"}
# configfile: "config.yaml"
atac=[]
h3k27ac=[]
enhancerbed="../KRT_enhancer.bed"
p300=["KRT_p300"]

STARREFDIR =    "~/.local/share/genomes/hg38/star"
##### TOOLS #####
TOOLDIR=        "~/bin/"
STAR =          "~/bin/STAR-2.5.3a/bin/Linux_x86_64/STAR"
PICARD=         TOOLDIR+"picard.jar"



def main(p300,atac,h3k27ac,enhancerbed):
    # if len(RUN_INDEX)==1:
    #     i=RUN_INDEX[0]
    #     star_map(i,RUN_INDEX[i])
    #     rm_dup(i)
    #     call_peak(i, INPUT=None)
    # else:
    for i in RUN_INDEX:
        star_map(i,RUN_INDEX[i])
        rm_dup(i)
        call_peak(i, INPUT=None)

    if len(p300)==0:
        runATACsample(atac,h3k27ac,enhancerbed)
    else:
        runP300sample(p300,enhancerbed)

main(p300,atac,h3k27ac,enhancerbed)



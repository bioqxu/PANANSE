import os

def readtools(toolstable):
    with open toolstable as ttable:
        for line in ttable:
            if not line.startswith("#"):
                exec("self." + line.split()[0] + "=" + line.split()[1])

class Runenhancer(object):
    def __init__(self, toolstable, samplestable):
        readtools(toolstable)
        print(self.CPU)
        

    def star_map(self, sample, rtype="PE"):
        if not os.path.exists("bam"):
            os.makedirs("bam")
        outputf = "bam/"+sample+"_sort.bam"
        logf = "bam/"+sample+"_sort.log"
        
        if rtype=="PE":
            inputf1 = "../fastq/"+sample+"_R1.fastq.gz"
            inputf2 = "../fastq/"+sample+"_R2.fastq.gz"
            shell1 = """%s --runThreadN %s --outFilterType BySJout \
                    --outSAMtype BAM SortedByCoordinate --outWigType wiggle \
                    --outWigStrand Unstranded \
                    --genomeDir %s \
                    --readFilesCommand zcat \
                    --readFilesIn %s %s \
                    --outFileNamePrefix %s \
                    > %s 2>&1""" % (STAR, CPU, STARREFDIR, inputf1, inputf2, sample, logf)
        else:
            inputf = "../fastq/"+sample+".fastq.gz"
            shell1 = """%s --runThreadN %s --outFilterType BySJout \
                    --outSAMtype BAM SortedByCoordinate --outWigType wiggle \
                    --outWigStrand Unstranded \
                    --genomeDir %s \
                    --readFilesCommand zcat \
                    --readFilesIn %s \
                    --outFileNamePrefix %s \
                    > %s 2>&1""" % (STAR, CPU, STARREFDIR, inputf, sample, logf)
        shell2 = "mv %sAligned.sortedByCoord.out.bam %s" % (sample, outputf)
        shell3 = "mv %sLog.final.out %s" % (sample, logf)
        shell4 = "rm -rf %s*" % (sample)
        # shell5 = "mv *sra bam/"

        runShell1=os.popen(shell1)
        runShell1.readlines()
        runShell2=os.popen(shell2)
        runShell2.readlines()
        runShell3=os.popen(shell3)
        runShell3.readlines()
        runShell4=os.popen(shell4)
        runShell4.readlines()
        # runShell5=os.popen(shell5)
        # runShell5.readlines()

    def rm_dup(self, sample):
        inputf="../bam/"+sample+"_sort.bam"
        outputf1="../bam/"+sample+"_sort_rmdup.bam"
        outputf2="../bam/"+sample+"_sort_rmdup.matrix"
        logf="../bam/"+sample+"_sort_rmdup.log"

        shell= """
                java -Xms5g -Xmx20g -XX:ParallelGCThreads=%s \
                -jar %s MarkDuplicates \
                    INPUT=%s \
                    OUTPUT=%s \
                    METRICS_FILE=%s \
                    ASO=coordinate \
                    CREATE_INDEX=true \
                    REMOVE_DUPLICATEs= true  > %s 2>&1
                """ % (CPU, PICARD, inputf, outputf1, outputf2, logf)
        runShell=os.popen(shell)
        runShell.readlines()

    def call_peak(self, sample, INPUT=None):
        if not os.path.exists("macs2_result"):
            os.makedirs("macs2_result")
        inputf="bam/"+sample+"_sort_rmdup.bam"
        outputf= "macs2_result/"+sample+"_peaks.narrowPeak"
        params= ["ATAC_seq_"+sample, "../macs2_result"]
        logf= "macs2_result/"+sample+"_macs2.log"
        if INPUT==None:
            shell1 = """
                    %s callpeak -t %s -f BAM -B -g hs -nomodel --shift -100 --extsize 200 -n %s > %s 2>&1 
                    """ % (macs2, inputf, sample, logf)
        else:
            shell1 = """
                    %s callpeak -c %s -t %s -f BAM -B -g hs -nomodel --shift -100 --extsize 200 -n %s > %s 2>&1 
                    """ % (macs2, "bam/"+INPUT+"_sort_rmdup.bam", inputf, sample, logf)
        shell2 = "mv %s_treat_pileup.bdg %s.bdg" % (sample, params[1]+"/"+sample)
        shell3 = "mv %s %s" % (sample+"_peaks.narrowPeak", outputf)
        shell4 = "rm -rf %s*" % (sample)

        runShell1=os.popen(shell1)
        runShell1.readlines()
        runShell2=os.popen(shell2)
        runShell2.readlines()
        runShell3=os.popen(shell3)
        runShell3.readlines()
        runShell4=os.popen(shell4)
        runShell4.readlines()

    def read_chrsize(self, sfile=Chrom_sizes):
        sdic={}
        with open (sfile) as sizes:
            for i in sizes:
                sdic[i.split()[0]]=int(i.split()[1])
        return(sdic)

    def runATACsample(self, atac, h3k27ac, enhancerbed):
        if len(atac)==1:
            fl2=open(enhancerbed[:-4]+"_idrpeaks.bed","w")
            with open("macs2_result/"+atac[0]+"_peaks.narrowPeak") as idrpeak:
                for line in idrpeak:
                    a=line.split()
                    p=int(a[9])+int(a[1])
                    fl2.write(a[0]+"\t"+str(p-100)+"\t"+str(p+100)+"\n")
        else:
            idrCommd = idr + " --samples "
            for i in atac:
                mi="macs2_result/"+i+"_peaks.narrowPeak "
                idrCommd+=mi
            runIdr=os.popen(idrCommd)
            runIdr.readlines()
            # print(idrCommd)
            fl2=open(enhancerbed[:-4]+"_idrpeaks.bed","w")
            with open("idrValues.txt") as idrpeak:
                for line in idrpeak:
                    a=line.split()
                    p=int(a[9])+int(a[1])
                    fl2.write(a[0]+"\t"+str(p-100)+"\t"+str(p+100)+"\n")
            os.system("rm idrValues.txt")


        runSortBdg=os.popen("sort -k1,1 -k2,2n macs2_result/"+ h3k27ac[0] +".bdg > macs2_result/"+ h3k27ac[0] +"_sort.bdg")
        runSortBdg.readlines()

        run2wig=os.popen(ucsctools + "bedGraphToBigWig macs2_result/"+ h3k27ac[0] +"_sort.bdg "+Chrom_sizes+" macs2_result/"+ h3k27ac[0] +"_sort.wig")
        run2wig.readlines()

        fl2=open(enhancerbed,"w")
        chrsizedic=read_chrsize()
        with open(enhancerbed[:-4]+"_idrpeaks.bed") as bdgf:
            for line in bdgf:
                a=line.split()
                if int(a[1])>0 and chrsizedic[a[0]]>int(a[2]):
                    commd1=os.popen(ucsctools + "bigWigSummary -type=max macs2_result/"+ h3k27ac[0] +"_sort.wig "+a[0]+" "+a[1]+" "+a[2]+" 1")
                    r=commd1.read()
                    if r != "":
                        fl2.write(a[0]+"\t"+a[1]+"\t"+a[2]+"\t"+str(r))

    def runP300sample(self, p300,enhancerbed):
        if len(p300)==1:
            fl2=open(enhancerbed[:-4]+"_idrpeaks.bed","w")
            with open("macs2_result/"+p300[0]+"_peaks.narrowPeak") as idrpeak:
                for line in idrpeak:
                    a=line.split()
                    p=int(a[9])+int(a[1])
                    fl2.write(a[0]+"\t"+str(p-100)+"\t"+str(p+100)+"\n")
        else:
            idrCommd="idr --samples "
            for i in p300:
                mi="macs2_result/"+i+"_peaks.narrowPeak "
                idrCommd+=mi
            runIdr=os.popen(idrCommd)
            runIdr.readlines()

            fl2=open(enhancerbed[:-4]+"_idrpeaks.bed","w")
            with open("idrValues.txt") as idrpeak:
                for line in idrpeak:
                    a=line.split()
                    p=int(a[9])+int(a[1])
                    fl2.write(a[0]+"\t"+str(p-100)+"\t"+str(p+100)+"\n")
            os.system("rm idrValues.txt")


        runSortBdg=os.popen("sort -k1,1 -k2,2n macs2_result/"+ p300[0] +".bdg > macs2_result/"+ p300[0] +"_sort.bdg")
        runSortBdg.readlines()

        run2wig=os.popen(ucsctools + "bedGraphToBigWig ../macs2_result/"+ p300[0] +"_sort.bdg "+Chrom_sizes+" macs2_result/"+ p300[0] +"_sort.wig")
        run2wig.readlines()


        fl2=open(enhancerbed,"w")
        chrsizedic=read_chrsize()
        with open(enhancerbed[:-4]+"_idrpeaks.bed") as bdgf:
            for line in bdgf:
                a=line.split()
                if int(a[1])>0 and chrsizedic[a[0]]>int(a[2]):
                    commd1=os.popen(ucsctools + "bigWigSummary -type=max ../macs2_result/"+ p300[0] +"_sort.wig "+a[0]+" "+a[1]+" "+a[2]+" 1")
                    r=commd1.read()
                    if r != "":
                        fl2.write(a[0]+"\t"+a[1]+"\t"+a[2]+"\t"+str(r))



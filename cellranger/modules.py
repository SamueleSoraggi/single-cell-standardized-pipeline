########fastq dump script
def fastqdump(SRAname):
    inputs = [SRAname]
    outputs = [SRAname+'_1.fastq',SRAname+'_2.fastq']
    options = {
        'cores': 1,
        'memory': '8g',
        'walltime': '00:10:00'
    }

    spec = '''
    SRAname={SRAname}
    source activate fastq
    echo "---- converting SRA file " $SRAname " to fastq format"
    fastq-dump --split-3 $SRAname
    '''.format(SRAname=SRAname)

    return inputs, outputs, options, spec

########fastqc script
def fastqc(FASTQname):
    inputs = [FASTQname]
    outputs = []
    options = {
        'cores': 1,
        'memory': '8g',
        'walltime': '00:10:00'
    }

    spec = '''
    FASTQname={FASTQname}
    source activate fastq
    echo "---- fastqc on " $FASTQname
    fastqc -o ./fastqc $FASTQname
    '''.format(FASTQname=FASTQname)

    return inputs, outputs, options, spec

#print pairs in shell
#    firstEnd=(`ls *_1.fastq`)
#    secondEnd=(`ls *_2.fastq`)
#    lth=(`echo ${firstEnd[@]} | wc -w`)
#    pairedEnds=()
#    for i in `seq 0 $(($lth-1))`
#    do
#    pairedEnds=(${pairedEnds[@]} ${firstEnd[$i]} ${secondEnd[$i]})
#    done    

###use cellranger mkref to generate the reference folder
###$ cellranger mkref --genome=outFolder --fasta=genome.fa --genes=genes.gtf
######## NEEDS TO BE CHANGED TO CONNECT THE RIGHT OUTPUT TO THE NEXT CELLRANGER STEP
def makeRef(fasta, gtf, outName, transcriptome, walltime='12:00:00', cores=8, memory='50g', account='Carl'):
    inputs = []
    outputs = [transcriptome+'/log.txt']
    options = {
        'cores': cores,
        'memory': memory,
        'walltime': walltime,
        'account':account
    }
 
    spec = '''
    source activate fastq
    echo "STARTED make reference"
    cellranger mkref --genome={outName} --fasta={fasta} --genes={gtf} --nthreads {cores}
    echo "DONE make reference"
    cp {outName}/* {transcriptome}/
    echo 'hello' > {transcriptome}/log.txt 
    '''.format(fasta=fasta, transcriptome=transcriptome, gtf=gtf, outName=outName, cores=cores)

    return inputs, outputs, options, spec

def cellRanger(sampleFolder, transcriptome, outName, sample, walltime='8:00:00', cores=8, memory='200g', account='Carl'):
    fastqs=sampleFolder #adjust on your dataset
    inputs = []
    outputs = [outName+'/outs/possorted_genome_bam.bam',outName+'/log.txt']
    options = {
        'cores': cores,
        'memory': memory,
        'walltime': walltime,
        'account':account
    }
 
    spec = '''
    source activate fastq
    echo "STARTED cellranger count on {outName}"
    cellranger count --localcores={cores} --id={outName} --transcriptome={transcriptome} --fastqs={fastqs} --sample={sample}
    echo "DONE cellranger count on  {outName}"
    echo 'hello' > {outName}/log.txt 
    '''.format(transcriptome=transcriptome, fastqs=fastqs, sampleFolder=sampleFolder, outName=outName, sample=sample, cores=cores)

    return inputs, outputs, options, spec

def velocyto(sampleFolder, gtfFile, sample, walltime='12:00:00', cores=12, memory='300g', account='Carl'):
    inputs = [sampleFolder + '/outs/possorted_genome_bam.bam', sampleFolder + '/log.txt']
    outputs = ['./velocyto_' + sample + '/logvelo.txt']
    options = {
        'cores': cores,
        'memory': memory,
        'walltime': walltime,
        'account':account
    }

    samtoolsMemory = ( int(memory.rstrip('g')) - int( int(memory.rstrip('g'))/8)  )
    
    spec = '''
    echo "STARTED velocyto"
    mkdir -p ./velocyto_{sample}
    source activate SCvelocyto
    source /com/extra/samtools/1.6.0/load.sh
    #samtools sort -@ {cores} -t CB -O BAM -o {sampleFolder}/outs/cellsorted_possorted_genome_bam.bam {sampleFolder}/outs/possorted_genome_bam.bam
    #velocyto run --outputfolder ./velocyto_{sample}  --samtools-threads {cores} --samtools-memory {samtoolsMemory} {sampleFolder}/outs/possorted_genome_bam.bam {gtfFile}
    velocyto run --outputfolder ./velocyto_{sample} {sampleFolder}/outs/possorted_genome_bam.bam {gtfFile}
    echo "DONE velocyto"
    echo "done :)" > ./velocyto_{sample}/logvelo.txt
    '''.format(sampleFolder=sampleFolder, gtfFile=gtfFile, sample=sample, cores=cores, samtoolsMemory=samtoolsMemory)

    return inputs, outputs, options, spec



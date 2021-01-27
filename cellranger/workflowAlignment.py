import numpy as np
from gwf import Workflow
import os, sys
from modules import *

gwf = Workflow()

###run fastqdump
#select files
#SRRfiles = [f for f in os.listdir('.') if f.startswith('SRR') and not f.endswith('.out') and not f.endswith('.fastq') and not f.endswith('.py') and not f.endswith('.txt') and not f.endswith('.csv')]

#for f in SRRfiles:
#    gwf.target_from_template('fastqdump_' + f, fastqdump(SRAname=f) )

###run fastqc
#select files
#FASTQfiles = [f for f in os.listdir('.') if f.endswith('.fastq')]

#for f in FASTQfiles:
#    gwf.target_from_template('fastqc_' + f, fastqc(FASTQname=f) )



###Run Cellranger on whole cell data

#for fld in fldNames:
    #gwf.target_from_template( 'ranger_ext_all', cellRanger(sampleFolder=fld, sample=samples[0]+','+samples[1]+','+samples[2]+','+samples[3], outName='exonAll', transcriptome=fldRef, walltime='24:00:00', memory='250g', cores=10) )
    #gwf.target_from_template( 'velocyto_ext_'+sample.split('-')[2], velocyto(sampleFolder=fld, sample=sample, outName='extended', gtfFile=gtfFile) )


###Run Cellranger on single cell and nuclei data
fldNames = ['/faststorage/project/Carl/Dataset/wholecell/H201SC19100215/raw_data/FKDL192551579-1a.191230_ST-E00205_0920_AH3Y7NCCX2']
samples=[ ['DMAC-monkey-AK2831', 'DMAC-monkey-AK2832', 'DMAC-monkey-AK2833', 'DMAC-monkey-AK2834'] ]

outName = ['whole_cell']
fldRef='/faststorage/project/Carl/ref_annotation/Clint_PTRv2_whole_cells'
gtfFile='/faststorage/project/Carl/ref_annotation/Clint_PTRv2_whole_cells/genes/genes.gtf'

for fld,smp,name in zip(fldNames,samples,outName):
    #name = fld.split('/')[-1].split('-')[0] 
    gwf.target_from_template( 'ranger_'+str(name), cellRanger(sampleFolder=fld,
                                                              sample=smp[0]+','+smp[1]+','+smp[2]+','+smp[3],
                                                              outName='cellranger_'+str(name),
                                                              transcriptome=fldRef,
                                                              walltime='24:00:00',
                                                              memory='250g',
                                                              cores=10) )
    gwf.target_from_template( 'velocyto_'+str(name), velocyto(sampleFolder='cellranger_'+str(name),
                                                              sample=str(name),
                                                              gtfFile=gtfFile,
                                                              memory='200g') )


    
fldNames = [ '/faststorage/project/Carl/Dataset/wholenuclei/H201SC19100215/raw_data/FKDL202561775-1a.200301_ST-E00192_1032_AH7MC5CCX2',
             '/faststorage/project/Carl/Dataset/wholenuclei/H201SC19100215/raw_data/FKDL202561774-1a.200301_ST-E00192_1032_AH7MC5CCX2']
samples=[ ['Hepes-AK654', 'Hepes-AK655', 'Hepes-AK656', 'Hepes-AK657'],
          ['NST-AK646', 'NST-AK647', 'NST-AK687', 'NST-AK649' ] ]

outName = ['nuclei_HEPES','nuclei_NST']
fldRef='/faststorage/project/Carl/ref_annotation/Clint_PTRv2_nuclei'
gtfFile='/faststorage/project/Carl/ref_annotation/Clint_PTRv2_whole_cells/genes/genes.gtf'

for fld,smp,name in zip(fldNames,samples,outName):
    #name = fld.split('/')[-1].split('-')[0] 
    gwf.target_from_template( 'ranger_'+str(name), cellRanger(sampleFolder=fld,
                                                              sample=smp[0]+','+smp[1]+','+smp[2]+','+smp[3],
                                                              outName='cellranger_'+str(name),
                                                              transcriptome=fldRef,
                                                              walltime='24:00:00',
                                                              memory='250g',
                                                              cores=10) )
    gwf.target_from_template( 'velocyto_'+str(name), velocyto(sampleFolder='cellranger_'+str(name),
                                                              sample=str(name),
                                                              gtfFile=gtfFile,
                                                              memory='200g') )

outName = ['piRNA_nuclei_HEPES','piRNA_nuclei_NST','piRNA_whole_cell']
fldRef='/faststorage/project/Carl/ref_annotation/Clint_PTRv2_extraa_feat'
gtfFile='/faststorage/project/Carl/ref_annotation/Clint_PTRv2_extraa_feat/genes/genes.gtf'
#for fld,smp,name in zip(fldNames,samples,outName):
    #name = fld.split('/')[-1].split('-')[0] 
#    gwf.target_from_template( 'ranger_'+str(name), cellRanger(sampleFolder=fld,
#                                                              sample=smp[0]+','+smp[1]+','+smp[2]+','+smp[3],
#                                                              outName='cellranger_'+str(name),
#                                                              transcriptome=fldRef,
#                                                              walltime='18:00:00',
#                                                              memory='100g',
#                                                              cores=8) )
#    gwf.target_from_template( 'velocyto_'+str(name), velocyto(sampleFolder='cellranger_'+str(name),
#                                                              sample=str(name),
#                                                              gtfFile=gtfFile,
#                                                              walltime='18:00:00',
#                                                              memory='200g',
#                                                              cores=8))
























#fastaFile='/project/primatescrna/faststorage/Data/CHIMP/genome/genome.fa'
#gtfFile='/project/primatescrna/faststorage/Data/CHIMP/genome/Chimpanzee_Testis_v2.gtf'
#fldRef='/faststorage/project/Carl/ref_annotation/Heidelberg'

#gwf.target_from_template( 'mkref_Heid_',  makeRef(fasta=fastaFile,
#                                                  gtf=gtfFile,
#                                                  outName='Heidelberg',
#                                                  transcriptome=fldRef,
#                                                  walltime='18:00:00',
#                                                  cores=8,
#                                                  memory='50g',
#                                                  account='Carl'))
    
#for fld,smp in zip(fldNames,samples):
#    name = fld.split('/')[-1].split('-')[0]
#    gwf.target_from_template( 'ranger_Heid_'+str(name), cellRanger(sampleFolder=fld,
#                                                              sample=smp[0]+','+smp[1]+','+smp[2]+','+smp[3],
#                                                              outName='nuclei_Heid_'+str(name),
#                                                              transcriptome=fldRef,
#                                                              walltime='24:00:00',
#                                                              memory='300g',
#                                                              cores=10) )

#    gwf.target_from_template( 'velocyto_Heid_'+str(name), velocyto(sampleFolder='nuclei_Heid_'+str(name),
#                                                              sample=str(name),
#                                                              gtfFile=gtfFile) )

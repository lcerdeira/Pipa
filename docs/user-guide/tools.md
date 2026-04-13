# Supported Tools

PIPA includes **48 bioinformatics tools** organized into 7 categories.

## Trimming Tools

| Tool | Purpose | Reference |
|------|---------|-----------|
| [Trim Galore](https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/) | Quality/adapter trimming for Illumina | Krueger F (2012) |
| [Porechop_ABI](https://github.com/bonsai-team/Porechop_ABI) | Adapter removal for Nanopore | Bonenfant Q et al. (2023) |

## Assembly Tools

| Tool | Purpose | Reference |
|------|---------|-----------|
| [SPAdes](https://github.com/ablab/spades) | Short-read assembly | Bankevich A et al. (2012) |
| [Flye](https://github.com/fenderglass/Flye) | Long-read assembly | Kolmogorov M et al. (2019) |
| [Unicycler](https://github.com/rrwick/Unicycler) | Hybrid assembly | Wick RR et al. (2017) |
| [Canu](https://github.com/marbl/canu) | Long-read assembly | Koren S et al. (2017) |

## General Annotation

| Tool | Purpose | Reference |
|------|---------|-----------|
| [Prokka](https://github.com/tseemann/prokka) | Gene annotation (CDS, rRNA, tRNA) | Seemann T (2014) |
| [Bakta](https://github.com/oschwengers/bakta) | Rapid bacterial genome annotation | Schwengers O et al. (2021) |
| [MLST](https://github.com/tseemann/mlst) | Multi-locus sequence typing | Seemann T |
| [Barrnap](https://github.com/tseemann/barrnap) | Ribosomal RNA prediction | Seemann T |
| [tRNAscan-SE](http://lowelab.ucsc.edu/tRNAscan-SE/) | tRNA prediction | Chan PP & Lowe TM (2019) |
| [EggNOG-mapper](https://github.com/eggnogdb/eggnog-mapper) | Functional annotation (orthologous groups) | Cantalapiedra CP et al. (2021) |
| [KOFAM](https://www.genome.jp/tools/kofamkoala/) | KEGG functional annotation | Aramaki T et al. (2020) |

## Assembly Quality

| Tool | Purpose | Reference |
|------|---------|-----------|
| [BUSCO](https://busco.ezlab.org/) | Assembly completeness assessment | Manni M et al. (2021) |
| [CheckM](https://github.com/Ecogenomics/CheckM) | Assembly quality assessment | Parks DH et al. (2015) |
| [QUAST](https://github.com/ablab/quast) | Contig quality assessment | Gurevich A et al. (2013) |

## Resistance & Virulence

| Tool | Purpose | Reference |
|------|---------|-----------|
| [Abricate](https://github.com/tseemann/abricate) | Resistance gene screening (NCBI) | Seemann T |
| [Abricate VFDB](https://github.com/tseemann/abricate) | Virulence factor detection (VFDB) | Seemann T |
| [AMRFinderPlus](https://github.com/ncbi/amr) | NCBI AMR detection | Feldgarden M et al. (2021) |
| [mcroni](https://github.com/liampshaw/mcroni) | Colistin resistance (mcr-1 variation) | Shaw LP et al. |

## Mobile Elements & Defense

| Tool | Purpose | Reference |
|------|---------|-----------|
| [PlasmidFinder](https://bitbucket.org/genomicepidemiology/plasmidfinder) | Plasmid replicon identification | Carattoli A et al. (2014) |
| [MOB-suite](https://github.com/phac-nml/mob-suite) | Plasmid classification and typing | Robertson J et al. (2018) |
| [Phigaro](https://github.com/bobeobibo/phigaro) | Prophage region detection | Starikova EV et al. (2020) |
| [PhiSpy](https://github.com/linsalrob/PhiSpy) | Prophage prediction | Akhter S et al. (2012) |
| [CRISPRCasFinder](https://crisprcas.i2bc.paris-saclay.fr/) | CRISPR array and Cas gene detection | Couvin D et al. (2018) |
| [DefenseFinder](https://github.com/mdmparis/defense-finder) | Anti-phage system detection | Tesson F et al. (2022) |
| [ISMapper](https://github.com/jhawkey/IS_mapper) | Insertion site identification | Hawkey J et al. (2015) |

## Organism-Specific Typing

| Tool | Organism | Purpose | Reference |
|------|----------|---------|-----------|
| [Kleborate](https://github.com/klebgenomics/Kleborate) | *Klebsiella* | Virulence and resistance typing | Lam MMC et al. (2021) |
| [staphtyper](https://github.com/rpetit3/staphtyper) | *Staphylococcus aureus* | agr, spa, SCCmec typing | Petit RA |
| [TBProfiler](https://github.com/jodyphelan/TBProfiler) | *Mycobacterium tuberculosis* | Resistance and lineage detection | Phelan JE et al. (2019) |
| [ClermonTyping](https://github.com/A-BN/ClermonTyping) | *Escherichia* | Phylotyping | Beghain J et al. (2018) |
| [ECTyper](https://github.com/phac-nml/ecoli_serotyping) | *Escherichia coli* | Serotype prediction | Laing C et al. (2014) |
| [emmtyper](https://github.com/MDU-PHL/emmtyper) | *Streptococcus pyogenes* | emm-typing | MDU-PHL |
| [GenoTyphi](https://github.com/katholt/genotyphi) | *Salmonella* Typhi | Genotyping | Wong VK et al. (2016) |
| [hicap](https://github.com/scwatts/hicap) | *Haemophilus influenzae* | Cap locus serotype | Watts SC & Holt KE (2019) |
| [HpSuisSero](https://github.com/jimmyliu1326/HpSuisSero) | *Haemophilus parasuis* | Serotype prediction | Liu J |
| [legsta](https://github.com/tseemann/legsta) | *Legionella pneumophila* | Typing | Seemann T |
| [LisSero](https://github.com/MDU-PHL/LisSero) | *Listeria monocytogenes* | Serogroup prediction | MDU-PHL |
| [meningotype](https://github.com/MDU-PHL/meningotype) | *Neisseria meningitidis* | Serotyping | MDU-PHL |
| [ngmaster](https://github.com/MDU-PHL/ngmaster) | *Neisseria gonorrhoeae* | Multi-antigen ST | MDU-PHL |
| [pasty](https://github.com/rpetit3/pasty) | *Pseudomonas aeruginosa* | Serogrouping | Petit RA |
| [pbptyper](https://github.com/rpetit3/pbptyper) | *Streptococcus pneumoniae* | PBP typing | Petit RA |
| [PneumoCaT](https://github.com/phe-bioinformatics/PneumoCaT) | *Streptococcus pneumoniae* | Capsular typing | Kapatai G et al. (2016) |
| [sccmec](https://github.com/rpetit3/sccmec) | *Staphylococcus aureus* | SCCmec typing | Petit RA |
| [SeqSero2](https://github.com/denglab/SeqSero2) | *Salmonella* | Serotype prediction | Zhang S et al. (2019) |
| [SeroBA](https://github.com/sanger-pathogens/seroba) | *Streptococcus pneumoniae* | Serotyping from reads | Epping L et al. (2018) |
| [ShigaPass](https://github.com/imanyass/ShigaPass) | *Shigella* | Serotype prediction | Yassine I et al. |
| [ShigaTyper](https://github.com/CFSAN-Biostatistics/shigatyper) | *Shigella* | Serotype from reads | Wu Y et al. (2019) |
| [ShigEiFinder](https://github.com/LanLab/ShigEiFinder) | *Shigella*/EIEC | Serotyping | Lan R et al. |
| [SISTR](https://github.com/phac-nml/sistr_cmd) | *Salmonella* | Serovar prediction | Yoshida CE et al. (2016) |
| [spaTyper](https://github.com/HCGB-IGTP/spaTyper) | *Staphylococcus aureus* | spa typing | Sanchez-Herrero JF |
| [SsuisSero](https://github.com/jimmyliu1326/SsuisSero) | *Streptococcus suis* | Serotype prediction | Liu J |
| [staphopia-sccmec](https://github.com/staphopia/staphopia-sccmec) | *Staphylococcus aureus* | SCCmec typing | Petit RA & Read TD (2018) |
| [STECFinder](https://github.com/LanLab/STECFinder) | *Escherichia coli* (STEC) | Serotyping | Lan R et al. |

import subprocess
import os

def TrimageRun():
    if len(os.listdir("pipa/data/input/illumina")) != 0:
        path = "pipa/data/input/illumina"
        files = os.listdir(path)

        if "R1" in files[0]:
            for i in range(1, len(files), 2):
                fastq_r1 = path + "/" + files[i-1]
                fastq_r2 = path + "/" + files[i]
                #Verificar se o comando abaixo está correto
                command = ["trim_galore", "--paired", "--no_report_file", "-o", "pipa/data/trimmed/illumina", fastq_r1, fastq_r2]
                subprocess.run(command)
        
        else:
        
            for file in files:
                fastq = path + "/" + file
                # Verificar se o comando abaixo está correto
                command = ["trim_galore", "--no_report_file", "-o", "pipa/data/trimmed/illumina", fastq]
                subprocess.run(command)
    
    if len(os.listdir("pipa/data/input/nanopore")) != 0:
        path = "pipa/data/input/nanopore"
        # Verificar se o comando abaixo está correto
        command = ["porechop", "-i", path, "-o", "pipa/data/trimmed/nanopore/output_reads.fastq.gz"]
        subprocess.run(command)

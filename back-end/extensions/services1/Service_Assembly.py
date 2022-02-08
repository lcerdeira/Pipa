
import subprocess
import os
def AssemblyRun():
    if len(os.listdir("pipa/data/trimmed/illumina")) != 0:
        path = "pipa/data/trimmed/illumina"
        files = os.listdir(path)
        
        if "R1" in files[0]:
            for i in range(1, len(files), 2):
                fastq_r1 = path + "/" + files[i-1]
                fastq_r2 = path + "/" + files[i]
                # Verificar se o comando abaixo está correto
                # "--careful", "--cov-cutoff", "auto"
                command = ["spades.py", "-1", fastq_r1, "-2", fastq_r2, "--careful", "--cov-cutoff", "auto", "-o", "pipa/data/assembly/spades"]
                subprocess.run(command)
        
        else:
            for f in files:
                file = path + "/" + f
                # Verificar se o comando abaixo está correto
                command = ["spades.py", "-s", file, "-o", "pipa/data/assembly/spades"]
                subprocess.run(command)
    
    if len(os.listdir("pipa/data/trimmed/nanopore")) != 0:
        path = "pipa/data/trimmed/nanopore"
        files = os.listdir(path)
        
        for f in files:
            file = path + "/" + f
            print("\n__CANU RUN__\n")
            command = ["canu", "-p", "ecoli", "-d", "ecoli-oxford", "genomeSize=4.8m", "-nanopore", file]
            subprocess.run(command)
            print("\n__FLYE RUN__\n")
            # Verificar se o comando abaixo está correto
            command = ["flye", "--nano-raw", file, "-o", "pipa/data/assembly/flye"]
            subprocess.run(command)
            print("\n__UNICYCLER RUN__\n")
            # Verificar se o comando abaixo está correto
            command = ["unicycler", "-l", file, "-o", "pipa/data/assembly/unicycler"]
            subprocess.run(command)

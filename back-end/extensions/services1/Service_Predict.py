import subprocess
import os

def PredictRun():
    
    folders = os.listdir("pipa/data/assembly")
    
    for folder in folders:
        actual_folder = "pipa/data/assembly/" + folder
        files = os.listdir(actual_folder)
        
        file = [x for x in files if ".fasta" in x]
        
        if len(file) > 0:
            file = file[0]
        else:
            continue
        
        fasta_file = "pipa/data/assembly/" + folder + "/" + file
        print("\n__PROKKA RUN__\n")
        # Verificar se o comando abaixo está correto
        
        prokka_command = ["prokka",
                            "--outdir", "pipa/data/predicted/prokka",
                            "--proteins", "NTUH_proteins.aa",
                            "--genus", "Klebsiella",
                            "--species", "pneumoniae",
                            "--force", "--centre",
                            "X", "--rfam",
                            fasta_file]
        
        subprocess.run(prokka_command)
        print("\n__MLST RUN__\n")
        # Verificar se o comando abaixo está correto
        mlst_command = ["mlst", fasta_file]
        subprocess.run(mlst_command)
        print("\n__BARRNAP RUN__\n")
        # Verificar se o comando abaixo está correto
        barrnap_command = ["barrnap", fasta_file]
        subprocess.run(barrnap_command)
        print("\n__ABRICATE RUN__\n")
        # Verificar se o comando abaixo está correto
        abricate_command = ["abricate",
                            fasta_file,
                            ]
        subprocess.run(abricate_command)
        print("\n__KLEBORATE RUN__\n")
        # Verificar se o comando abaixo está correto
        kleborate_command = ["kleborate",
                                "-o", "pipa/data/predicted/kleborate/kleborate.txt",
                                "-a", fasta_file,
                                ]
        subprocess.run(kleborate_command)
        print("\n__PHIGARO RUN__\n")
        # Verificar se o comando abaixo está correto
        phigaro_command = ["phigaro",
                            "-f", fasta_file,
                            "-o", "pipa/data/predicted/phigaro",
                            ]
        subprocess.run(phigaro_command)
        print("\n__KOFAM RUN__\n")
        # Verificar se o comando abaixo está correto
        kofam_command = ["exec_annotation",
                            "-o", "pipa/data/predicted/kofam",
                            fasta_file
                            ]
        subprocess.run(kofam_command)

import subprocess
import os
from .services1 import Service_Trimage
from .services1 import Service_Assembly
from .services1 import Service_Predict
from .services1 import Service_Report
from .services1 import Service_FolderVerification

class Pipa():

    def init_app(self, app):
        app.pipa = self
        
        """ 
        trimage = Service_Trimage()
        assembly = Service_Assembly()
        predict = Service_Predict()
        report = Service_Report()
        folderVerification = Service_FolderVerification()
        trimage.TrimageRun()
        assembly.AssemblyRun()
        predict.PredictRun()
        report.ReportRun()
        folderVerification.FolderVerificationRun() 
        Service_Trimage.TrimageRun()
        Service_Assembly.AssemblyRun()
        Service_Predict.PredictRun()
        Service_Report.ReportRun()
        Service_FolderVerification.FolderVerificationRun() 
         """
        
    def TrimageRun(self):
        if len(os.listdir("./data/input/illumina")) != 0:
            path = "./data/input/illumina"
            files = os.listdir(path)

            if "R1" in files[0]:
                for i in range(1, len(files), 2):
                    fastq_r1 = path + "/" + files[i-1]
                    fastq_r2 = path + "/" + files[i]
                    #Verificar se o comando abaixo está correto
                    command = ["trim_galore", "--paired", "--no_report_file", "-o", "./data/trimmed/illumina", fastq_r1, fastq_r2]
                    subprocess.run(command)
            
            else:
            
                for file in files:
                    fastq = path + "/" + file
                    # Verificar se o comando abaixo está correto
                    command = ["trim_galore", "--no_report_file", "-o", "./data/trimmed/illumina", fastq]
                    subprocess.run(command)
        
        if len(os.listdir("./data/input/nanopore")) != 0:
            path = "./data/input/nanopore"
            # Verificar se o comando abaixo está correto
            command = ["porechop", "-i", path, "-o", "./data/trimmed/nanopore/output_reads.fastq.gz"]
            subprocess.run(command) 

        
    def AssemblyRun(self):
        if len(os.listdir("./data/trimmed/illumina")) != 0:
            path = "./data/trimmed/illumina"
            files = os.listdir(path)
            
            if "R1" in files[0]:
                for i in range(1, len(files), 2):
                    fastq_r1 = path + "/" + files[i-1]
                    fastq_r2 = path + "/" + files[i]
                    # Verificar se o comando abaixo está correto
                    # "--careful", "--cov-cutoff", "auto"
                    command = ["spades.py", "-1", fastq_r1, "-2", fastq_r2, "--careful", "--cov-cutoff", "auto", "-o", "./data/assembly/spades"]
                    subprocess.run(command)
            
            else:
                for f in files:
                    file = path + "/" + f
                    # Verificar se o comando abaixo está correto
                    command = ["spades.py", "-s", file, "-o", "./data/assembly/spades"]
                    subprocess.run(command)
        
        if len(os.listdir("./data/trimmed/nanopore")) != 0:
            path = "./data/trimmed/nanopore"
            files = os.listdir(path)
            
            for f in files:
                file = path + "/" + f
                print("\n__CANU RUN__\n")
                command = ["canu", "-p", "ecoli", "-d", "ecoli-oxford", "genomeSize=4.8m", "-nanopore", file]
                subprocess.run(command)
                print("\n__FLYE RUN__\n")
                # Verificar se o comando abaixo está correto
                command = ["flye", "--nano-raw", file, "-o", "./data/assembly/flye"]
                subprocess.run(command)
                print("\n__UNICYCLER RUN__\n")
                # Verificar se o comando abaixo está correto
                command = ["unicycler", "-l", file, "-o", "./data/assembly/unicycler"]
                subprocess.run(command) 


    def PredictRun(self):
        folders = os.listdir("./data/assembly")
        
        for folder in folders:
            actual_folder = "./data/assembly/" + folder
            files = os.listdir(actual_folder)
            
            file = [x for x in files if ".fasta" in x]
            
            if len(file) > 0:
                file = file[0]
            else:
                continue
            
            fasta_file = "./data/assembly/" + folder + "/" + file
            print("\n__PROKKA RUN__\n")
            # Verificar se o comando abaixo está correto
            
            prokka_command = ["prokka",
                                "--outdir", "./data/predicted/prokka",
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
                                    "-o", "./data/predicted/kleborate/kleborate.txt",
                                    "-a", fasta_file,
                                    ]
            subprocess.run(kleborate_command)
            print("\n__PHIGARO RUN__\n")
            # Verificar se o comando abaixo está correto
            phigaro_command = ["phigaro",
                                "-f", fasta_file,
                                "-o", "./data/predicted/phigaro",
                                ]
            subprocess.run(phigaro_command)
            print("\n__KOFAM RUN__\n")
            #Verificar se o comando abaixo está correto
            #kofam_command = ["exec_annotation",
            #                    "-o", "./data/predicted/kofam",
            #                    fasta_file
            #                    ]
            #subprocess.run(kofam_command) 


    def ReportRun(self):
        actual_folder = "./data/predicted/prokka/"
        files = os.listdir(actual_folder)
        file = [x for x in files if ".txt" in x]
        if len(file) > 0:
            file = file[0]
            name_file = file.split(".")[0]
        else:
            name_file = "none"
            file = ""
        text_file = "./data/predicted/prokka/" + file
        print("\n__Generate report__\n")
        report_tsv = "./static/report/" + name_file + ".tsv"
        report_svg = "static/report/" + name_file + ".svg"
        # Verificar se o comando abaixo está correto
        #command = ["KEGG-decoder",
        #            "--input", text_file,
        #            "--output", report_tsv,
        #            "--vizoption", "static"]
        #subprocess.run(command)
        return report_svg 



    def FolderVerificationRun(self):
        files = os.listdir("./")
        print(files)
        if "data" not in files:
            os.mkdir("./data")
        files = os.listdir("./static/")
        if "report" not in files:
            os.mkdir("./static/report")
        files = os.listdir("./data")
        folders_tools = ["assembly", "input", "predicted", "trimmed"]
        for f in folders_tools:
            if f not in files:
                path = "./data/"+f
                os.mkdir(path)
        folders_trimm = ["illumina", "nanopore", "pacbio"]
        files_input = os.listdir("./data/input")
        files_trimmed = os.listdir("./data/trimmed")
        for f in folders_trimm:
            if f not in files_input:
                path = "./data/input/"+f
                os.mkdir(path)
            if f not in files_trimmed:
                path = "./data/trimmed/"+f
                os.mkdir(path)
        files_predicted = os.listdir("./data/predicted")
        folders_predicted = ["abricate", "barrnap", "kleborate", "kofam", "mlst", "phigaro", "prokka"]
        for f in folders_predicted:
            if f not in files_predicted:
                path = "./data/predicted/"+f
                os.mkdir(path)
pipa = Pipa()


def init_app(app):
    pipa.init_app(app)

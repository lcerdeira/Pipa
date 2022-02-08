import subprocess
import os

def FolderVerificationRun():
   
    files = os.listdir("pipa/")
    if "data" not in files:
        os.mkdir("pipa/data")
    files = os.listdir("pipa/static/")
    if "report" not in files:
        os.mkdir("pipa/static/report")
    files = os.listdir("pipa/data")
    folders_tools = ["assembly", "input", "predicted", "trimmed"]
    for f in folders_tools:
        if f not in files:
            path = "pipa/data/"+f
            os.mkdir(path)
    folders_trimm = ["illumina", "nanopore", "pacbio"]
    files_input = os.listdir("pipa/data/input")
    files_trimmed = os.listdir("pipa/data/trimmed")
    for f in folders_trimm:
        if f not in files_input:
            path = "pipa/data/input/"+f
            os.mkdir(path)
        if f not in files_trimmed:
            path = "pipa/data/trimmed/"+f
            os.mkdir(path)
    files_predicted = os.listdir("pipa/data/predicted")
    folders_predicted = ["abricate", "barrnap",
                            "kleborate", "kofam", "mlst", "phigaro", "prokka"]
    for f in folders_predicted:
        if f not in files_predicted:
            path = "pipa/data/predicted/"+f
            os.mkdir(path)

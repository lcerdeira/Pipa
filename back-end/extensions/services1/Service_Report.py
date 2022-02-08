import subprocess
import os

def ReportRun():
    
    actual_folder = "pipa/data/predicted/prokka"
    files = os.walk(actual_folder)
    file = [x for x in files if ".txt" in x]
    if len(file) > 0:
        file = file[0]
        name_file = file.split(".")[0]
    else:
        name_file = "none"
        file = ""
    text_file = "pipa/data/predicted/prokka/" + file
    print("\n__Generate report__\n")
    report_tsv = "pipa/static/report/" + name_file + ".tsv"
    report_svg = "static/report/" + name_file + ".svg"
    # Verificar se o comando abaixo está correto
    command = ["KEGG-decoder",
                "--input", text_file,
                "--output", report_tsv,
                "--vizoption", "static"]
    subprocess.run(command)
    return report_svg

import os
import subprocess
from platform import system
from setuptools import setup


current_dir = os.getcwd()

os.system('python3 -m pip install --user --upgrade cutadapt')

porechop_setup = f'{current_dir}/modules/Porechop/setup.py'

os.system(f'python3 {porechop_setup} install')

os.system('pip3 install nanopack')

os.system('pip3 install pycoQC')

os.system('pip3 install cutadapt')

os.system('pip3 install biopython')

os.system('pip3 install numpy')

any2fasta_dir = f'{current_dir}/modules/any2fasta/'

os.system(f'chmod +x {any2fasta_dir}')

os.system('git clone https://github.com/gmod/jbrowse modules/jbrowse')

subprocess.call(['cd', f'{current_dir}/modules/jbrowse', 'git checkout 1.16.11-release', './setup.sh'])

os.system('git clone https://github.com/rrwick/Bandage.git modules/Bandage')

os.path.join(os.environ.get('QT_SELECT'), '=5')

subprocess.call(['cd', f'{current_dir}/modules/Bandage', 'qmake', 'make'])

os.system('git clone https://github.com/sanger-pathogens/Artemis.git modules/Artemis')

subprocess.call(['cd', f'{current_dir}/modules/Artemis', 'mvn validate', 'mvn clean package'])

os.system('git clone https://github.com/arq5x/bedtools2.git modules/bedtools2')

subprocess.call(['cd', f'{current_dir}/modules/bedtools2', 'make'])

os.system('git clone https://github.com/brinkmanlab/islandpath.git modules/islandpath')

os.system('git clone https://github.com/CRISPRlab/CRISPRviz.git modules/CRISPRviz')

os.system('git clone https://github.com/ablab/quast.git modules/quast')

os.system('git clone https://github.com/PacificBiosciences/barcoding.git modules/barcoding')

os.system('git clone https://github.com/marbl/canu.git modules/canu')

os.system('./modules/canu/src make')

flye_make = f'{current_dir}/modules/Flye/make'

os.system(flye_make)

unicycler_setup = f'{current_dir}/modules/Unicycler/setup.py'

os.system(f'python3 {unicycler_setup} install')

nanopolish_make = f'{current_dir}/modules/nanopolish/make'

os.system(nanopolish_make)

os.system('cpan Bio::Perl Data::Dumper Log:Log4perl Config::Simple Moose MooseX::Singleton')

prokka_setup = f'{current_dir}/modules/prokka/bin/prokka'

os.system(f'{prokka_setup} --setupdb')

os.system('python3 ./modules/Kleborate/setup.py')

os.system(f'{current_dir}/modules/abricate/bin/abricate --check')

os.system(f'{current_dir}/modules/abricate/bin/abricate --setupdb')

os.system(f'{current_dir}/modules/abricate/bin/abricate {current_dir}/modules/abricate/test/assembly.fa')

os.system(f'{current_dir}/modules/Prodigal/make install')

os.system(f'{current_dir}/modules/hmmer-3.3.2/./configure --prefix {current_dir}/modules/hmmer-3.3.2')

subprocess.call(['cd', f'{current_dir}/modules/hmmer-3.3.2', 'make'])

subprocess.call(['cd', f'{current_dir}/modules/hmmer-3.3.2', 'make check'])

subprocess.call(['cd', f'{current_dir}/modules/hmmer-3.3.2', 'make install'])

subprocess.call(['cd', f'{current_dir}/modules/phigaro', 'phigaro-setup --no-updatedb'])

os.path.join(os.environ.get('PATH'), ':{current_dir}/modules/barrnap/bin:{current_dir}/modules/CRISPRviz/bin:{current_dir}/modules/quast/quast.py')

os.system(f'java -jar {current_dir}/modules/pilon-1.24.jar --version')

os.system('which crisprviz.sh')

os.system(f'cd {current_dir}/modules/quast && ./setup.py install')

os.system(f'cd {current_dir}/modules/quast && ./setup.py test')

os.system(f'mkdir {current_dir}/dataDB')

os.system('python3 ./back-end/app.py flask run')

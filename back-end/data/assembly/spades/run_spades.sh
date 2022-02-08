set -e
true
true
/root/bio/Modules/SPAdes-3.15.2/bin/spades-hammer /root/bio/Pipa/pipa/data/assembly/spades/corrected/configs/config.info
/usr/bin/python /root/bio/Modules/SPAdes-3.15.2/src/spades_pipeline/scripts/compress_all.py --input_file /root/bio/Pipa/pipa/data/assembly/spades/corrected/corrected.yaml --ext_python_modules_home /root/bio/Modules/SPAdes-3.15.2/ext/src/python_libs --max_threads 16 --output_dir /root/bio/Pipa/pipa/data/assembly/spades/corrected --gzip_output
true
true
/root/bio/Modules/SPAdes-3.15.2/bin/spades-core /root/bio/Pipa/pipa/data/assembly/spades/K21/configs/config.info /root/bio/Pipa/pipa/data/assembly/spades/K21/configs/careful_mode.info
/root/bio/Modules/SPAdes-3.15.2/bin/spades-core /root/bio/Pipa/pipa/data/assembly/spades/K33/configs/config.info /root/bio/Pipa/pipa/data/assembly/spades/K33/configs/careful_mode.info
/root/bio/Modules/SPAdes-3.15.2/bin/spades-core /root/bio/Pipa/pipa/data/assembly/spades/K55/configs/config.info /root/bio/Pipa/pipa/data/assembly/spades/K55/configs/careful_mode.info
/usr/bin/python /root/bio/Modules/SPAdes-3.15.2/src/spades_pipeline/scripts/copy_files.py /root/bio/Pipa/pipa/data/assembly/spades/K55/before_rr.fasta /root/bio/Pipa/pipa/data/assembly/spades/before_rr.fasta /root/bio/Pipa/pipa/data/assembly/spades/K55/assembly_graph_after_simplification.gfa /root/bio/Pipa/pipa/data/assembly/spades/assembly_graph_after_simplification.gfa /root/bio/Pipa/pipa/data/assembly/spades/K55/final_contigs.fasta /root/bio/Pipa/pipa/data/assembly/spades/contigs.fasta /root/bio/Pipa/pipa/data/assembly/spades/K55/first_pe_contigs.fasta /root/bio/Pipa/pipa/data/assembly/spades/first_pe_contigs.fasta /root/bio/Pipa/pipa/data/assembly/spades/K55/strain_graph.gfa /root/bio/Pipa/pipa/data/assembly/spades/strain_graph.gfa /root/bio/Pipa/pipa/data/assembly/spades/K55/scaffolds.fasta /root/bio/Pipa/pipa/data/assembly/spades/scaffolds.fasta /root/bio/Pipa/pipa/data/assembly/spades/K55/scaffolds.paths /root/bio/Pipa/pipa/data/assembly/spades/scaffolds.paths /root/bio/Pipa/pipa/data/assembly/spades/K55/assembly_graph_with_scaffolds.gfa /root/bio/Pipa/pipa/data/assembly/spades/assembly_graph_with_scaffolds.gfa /root/bio/Pipa/pipa/data/assembly/spades/K55/assembly_graph.fastg /root/bio/Pipa/pipa/data/assembly/spades/assembly_graph.fastg /root/bio/Pipa/pipa/data/assembly/spades/K55/final_contigs.paths /root/bio/Pipa/pipa/data/assembly/spades/contigs.paths
true
true
/usr/bin/python /root/bio/Modules/SPAdes-3.15.2/src/spades_pipeline/scripts/correction_iteration_script.py --corrected /root/bio/Pipa/pipa/data/assembly/spades/contigs.fasta --assembled /root/bio/Pipa/pipa/data/assembly/spades/misc/assembled_contigs.fasta --assembly_type contigs --output_dir /root/bio/Pipa/pipa/data/assembly/spades --bin_home /root/bio/Modules/SPAdes-3.15.2/bin
/usr/bin/python /root/bio/Modules/SPAdes-3.15.2/src/spades_pipeline/scripts/correction_iteration_script.py --corrected /root/bio/Pipa/pipa/data/assembly/spades/scaffolds.fasta --assembled /root/bio/Pipa/pipa/data/assembly/spades/misc/assembled_scaffolds.fasta --assembly_type scaffolds --output_dir /root/bio/Pipa/pipa/data/assembly/spades --bin_home /root/bio/Modules/SPAdes-3.15.2/bin
true
/usr/bin/python /root/bio/Modules/SPAdes-3.15.2/src/spades_pipeline/scripts/breaking_scaffolds_script.py --result_scaffolds_filename /root/bio/Pipa/pipa/data/assembly/spades/scaffolds.fasta --misc_dir /root/bio/Pipa/pipa/data/assembly/spades/misc --threshold_for_breaking_scaffolds 3
true

"""
Copyright 2017 Ryan Wick (rrwick@gmail.com)
https://github.com/rrwick/Unicycler

This file is part of Unicycler. Unicycler is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Unicycler is distributed in
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Unicycler. If
not, see <http://www.gnu.org/licenses/>.
"""

import unittest
import os
import subprocess


def run_unicycler(help_option):
    """
    This function runs Unicycler with either --help or --help_all.
    """
    unicycler_runner = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                    'unicycler-runner.py')
    unicycler_cmd = [unicycler_runner]
    if help_option:
        unicycler_cmd.append(help_option)
    p = subprocess.Popen(unicycler_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout.decode(), stderr.decode(), p.returncode


class TestBasicHelpText(unittest.TestCase):
    def setUp(self):
        self.stdout, self.stderr, self.return_code = run_unicycler('--help')

    def test_return_code(self):
        self.assertEqual(self.return_code, 0)

    def test_output(self):
        self.assertTrue(len(self.stdout) > 0)
        self.assertEqual(len(self.stderr), 0)

    def test_title(self):
        self.assertTrue('Unicycler: an assembly pipeline for bacterial genomes'
                        in self.stdout)

    def test_basic_options(self):
        self.assertTrue('--help' in self.stdout)
        self.assertTrue('--help_all' in self.stdout)
        self.assertTrue('--version' in self.stdout)
        self.assertTrue('--short1' in self.stdout)
        self.assertTrue('--short2' in self.stdout)
        self.assertTrue('--unpaired' in self.stdout)
        self.assertTrue('--long' in self.stdout)
        self.assertTrue('--out' in self.stdout)
        self.assertTrue('--verbosity' in self.stdout)
        self.assertTrue('--min_fasta_length' in self.stdout)
        self.assertTrue('--keep' in self.stdout)
        self.assertTrue('--threads' in self.stdout)
        self.assertTrue('--mode' in self.stdout)
        self.assertTrue('--linear_seqs' in self.stdout)

    def test_extended_options(self):
        self.assertFalse('--spades_path' in self.stdout)
        self.assertFalse('--no_correct' in self.stdout)
        self.assertFalse('--min_kmer_frac' in self.stdout)
        self.assertFalse('--max_kmer_frac' in self.stdout)
        self.assertFalse('--kmer_count' in self.stdout)
        self.assertFalse('--no_rotate' in self.stdout)
        self.assertFalse('--start_genes' in self.stdout)
        self.assertFalse('--start_gene_id' in self.stdout)
        self.assertFalse('--start_gene_cov' in self.stdout)
        self.assertFalse('--makeblastdb_path' in self.stdout)
        self.assertFalse('--tblastn_path' in self.stdout)
        self.assertFalse('--no_pilon' in self.stdout)
        self.assertFalse('--bowtie2_path' in self.stdout)
        self.assertFalse('--bowtie2_build_path' in self.stdout)
        self.assertFalse('--samtools_path' in self.stdout)
        self.assertFalse('--pilon_path' in self.stdout)
        self.assertFalse('--java_path' in self.stdout)
        self.assertFalse('--min_polish_size' in self.stdout)
        self.assertFalse('--min_component_size' in self.stdout)
        self.assertFalse('--min_dead_end_size' in self.stdout)
        self.assertFalse('--contamination' in self.stdout)
        self.assertFalse('--scores' in self.stdout)
        self.assertFalse('--low_score' in self.stdout)


class TestExtendedHelpText(unittest.TestCase):
    def setUp(self):
        self.stdout, self.stderr, self.return_code = run_unicycler('--help_all')

    def test_return_code(self):
        self.assertEqual(self.return_code, 0)

    def test_output(self):
        self.assertTrue(len(self.stdout) > 0)
        self.assertEqual(len(self.stderr), 0)

    def test_title(self):
        self.assertTrue('Unicycler: an assembly pipeline for bacterial genomes'
                        in self.stdout)

    def test_basic_options(self):
        self.assertTrue('--help' in self.stdout)
        self.assertTrue('--help_all' in self.stdout)
        self.assertTrue('--version' in self.stdout)
        self.assertTrue('--short1' in self.stdout)
        self.assertTrue('--short2' in self.stdout)
        self.assertTrue('--unpaired' in self.stdout)
        self.assertTrue('--long' in self.stdout)
        self.assertTrue('--out' in self.stdout)
        self.assertTrue('--verbosity' in self.stdout)
        self.assertTrue('--min_fasta_length' in self.stdout)
        self.assertTrue('--keep' in self.stdout)
        self.assertTrue('--threads' in self.stdout)
        self.assertTrue('--mode' in self.stdout)
        self.assertTrue('--linear_seqs' in self.stdout)

    def test_extended_options(self):
        self.assertTrue('--spades_path' in self.stdout)
        self.assertTrue('--no_correct' in self.stdout)
        self.assertTrue('--min_kmer_frac' in self.stdout)
        self.assertTrue('--max_kmer_frac' in self.stdout)
        self.assertTrue('--kmer_count' in self.stdout)
        self.assertTrue('--no_rotate' in self.stdout)
        self.assertTrue('--start_genes' in self.stdout)
        self.assertTrue('--start_gene_id' in self.stdout)
        self.assertTrue('--start_gene_cov' in self.stdout)
        self.assertTrue('--makeblastdb_path' in self.stdout)
        self.assertTrue('--tblastn_path' in self.stdout)
        self.assertTrue('--no_pilon' in self.stdout)
        self.assertTrue('--bowtie2_path' in self.stdout)
        self.assertTrue('--bowtie2_build_path' in self.stdout)
        self.assertTrue('--samtools_path' in self.stdout)
        self.assertTrue('--pilon_path' in self.stdout)
        self.assertTrue('--java_path' in self.stdout)
        self.assertTrue('--min_polish_size' in self.stdout)
        self.assertTrue('--min_component_size' in self.stdout)
        self.assertTrue('--min_dead_end_size' in self.stdout)
        self.assertTrue('--contamination' in self.stdout)
        self.assertTrue('--scores' in self.stdout)
        self.assertTrue('--low_score' in self.stdout)


class TestEmptyCommand(unittest.TestCase):
    def setUp(self):
        self.stdout, self.stderr, self.return_code = run_unicycler('')

    def test_return_code(self):
        self.assertNotEqual(self.return_code, 0)

    def test_output(self):
        self.assertEqual(len(self.stdout), 0)
        self.assertTrue(len(self.stderr) > 0)

    def test_error_message(self):
        # When run without any arguments, Unicycler should print its basic help.
        self.assertTrue('Unicycler:' in self.stderr)
        self.assertTrue('Help' in self.stderr)
        self.assertTrue('Input' in self.stderr)
        self.assertTrue('Output' in self.stderr)

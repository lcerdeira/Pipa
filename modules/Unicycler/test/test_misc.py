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
import unicycler.misc


class TestMiscFunctions(unittest.TestCase):

    def test_float_to_str(self):
        self.assertEqual('14.3', unicycler.misc.float_to_str(14.312, 1))
        self.assertEqual('1,000,000.1', unicycler.misc.float_to_str(1000000.101, 1))
        self.assertEqual('14.31', unicycler.misc.float_to_str(14.312, 2))
        self.assertEqual('14.32', unicycler.misc.float_to_str(14.319, 2))
        self.assertEqual(' 14.32', unicycler.misc.float_to_str(14.319, 2, 100))
        self.assertEqual(' 14.32', unicycler.misc.float_to_str(14.319, 2, 100.99999999))
        self.assertEqual('   14.32', unicycler.misc.float_to_str(14.319, 2, 999.9999999))

    def test_int_to_str(self):
        self.assertEqual('14', unicycler.misc.int_to_str(14))
        self.assertEqual('140', unicycler.misc.int_to_str(140))
        self.assertEqual('1,400', unicycler.misc.int_to_str(1400))
        self.assertEqual('14,000', unicycler.misc.int_to_str(14000))
        self.assertEqual('       14,000', unicycler.misc.int_to_str(14000, 1000000000))

    def test_get_nice_header(self):
        self.assertEqual(unicycler.misc.get_nice_header('NODE_1_length_49055_cov_41.580185'),
                         'NODE_1')
        self.assertEqual(unicycler.misc.get_nice_header('NODE_69_length_12837_cov_39.210640'),
                         'NODE_69')
        self.assertEqual(unicycler.misc.get_nice_header('name stuff'),
                         'name')
        self.assertEqual(unicycler.misc.get_nice_header('name stuff stuff stuff'),
                         'name')

    def test_is_header_spades_format(self):
        self.assertTrue(unicycler.misc.is_header_spades_format('NODE_1_length_49055_'
                                                               'cov_41.580185'))
        self.assertTrue(unicycler.misc.is_header_spades_format('NODE_69_length_12837_'
                                                               'cov_39.210640'))
        self.assertFalse(unicycler.misc.is_header_spades_format('name stuff'))
        self.assertFalse(unicycler.misc.is_header_spades_format('name stuff stuff stuff'))

    def test_reverse_complement(self):
        self.assertEqual('GCAGGCCGCTTAATGAATAGATCATGGCTGCGCCGCCTACCGGTCCGAGACCTTCGCTGA',
                         unicycler.misc.reverse_complement('TCAGCGAAGGTCTCGGACCGGTAGGCGGCGCAGCCATG'
                                                           'ATCTATTCATTAAGCGGCCTGC'))
        self.assertEqual('', unicycler.misc.reverse_complement(''))
        self.assertEqual('TATTTNGTTANAT', unicycler.misc.reverse_complement('ATNTAACNAAATA'))
        self.assertEqual('ATNTAACNAAATA', unicycler.misc.reverse_complement('TATTTNGTTANAT'))
        self.assertEqual('TGACBWDARAYACHASKGVTMACNG',
                         unicycler.misc.reverse_complement('CNGTKABCMSTDGTRTYTHWVGTCA'))
        self.assertEqual('tgACBWDARAYACHASKGVTMACnG',
                         unicycler.misc.reverse_complement('CnGTKABCMSTDGTRTYTHWVGTca'))

    def test_get_random_base(self):
        a_count, c_count, g_count, t_count, other_count = 0, 0, 0, 0, 0
        for i in range(10000):
            base = unicycler.misc.get_random_base()
            if base == 'A':
                a_count += 1
            elif base == 'C':
                c_count += 1
            elif base == 'G':
                g_count += 1
            elif base == 'T':
                t_count += 1
            else:
                other_count += 1
        self.assertTrue(a_count > 0)
        self.assertTrue(c_count > 0)
        self.assertTrue(g_count > 0)
        self.assertTrue(t_count > 0)
        self.assertTrue(other_count == 0)

    def test_get_random_sequence(self):
        self.assertEqual(10, len(unicycler.misc.get_random_sequence(10)))
        self.assertEqual(100, len(unicycler.misc.get_random_sequence(100)))
        self.assertEqual(1000, len(unicycler.misc.get_random_sequence(1000)))

    def test_get_percentile(self):
        self.assertEqual(20, unicycler.misc.get_percentile([50, 20, 40, 35, 15], 30))
        self.assertEqual(20, unicycler.misc.get_percentile([20, 50, 40, 35, 15], 40))
        self.assertEqual(35, unicycler.misc.get_percentile([50, 20, 40, 35, 15], 50))
        self.assertEqual(50, unicycler.misc.get_percentile([50, 20, 15, 35, 40], 100))
        self.assertEqual(7, unicycler.misc.get_percentile([3, 16, 7, 8, 8, 13, 10, 15, 6, 20],
                                                          25))
        self.assertEqual(8, unicycler.misc.get_percentile([16, 7, 8, 8, 13, 10, 15, 6, 20, 3],
                                                          50))
        self.assertEqual(15, unicycler.misc.get_percentile([3, 16, 7, 15, 8, 13, 10, 8, 6, 20],
                                                           75))
        self.assertEqual(20, unicycler.misc.get_percentile([20, 16, 7, 8, 8, 13, 10, 15, 6, 3],
                                                           100))
        self.assertEqual(7, unicycler.misc.get_percentile([3, 6, 7, 8, 8, 9, 10, 13, 15, 16, 20],
                                                          25))
        self.assertEqual(9, unicycler.misc.get_percentile([7, 9, 10, 3, 8, 15, 16, 13, 8, 20, 6],
                                                          50))
        self.assertEqual(15, unicycler.misc.get_percentile([3, 15, 13, 7, 8, 20, 10, 8, 16, 6, 9],
                                                           75))
        self.assertEqual(20, unicycler.misc.get_percentile([6, 13, 10, 8, 15, 3, 9, 8, 16, 7, 20],
                                                           100))

    def test_weighted_average(self):
        self.assertAlmostEqual(1.0, unicycler.misc.weighted_average(1.0, 2.0, 1.0, 0.0))
        self.assertAlmostEqual(2.0, unicycler.misc.weighted_average(1.0, 2.0, 0.0, 1.0))
        self.assertAlmostEqual(1.5, unicycler.misc.weighted_average(1.0, 2.0, 0.5, 0.5))
        self.assertAlmostEqual(1.5, unicycler.misc.weighted_average(1.0, 2.0, 1.5, 1.5))
        self.assertAlmostEqual(1.5, unicycler.misc.weighted_average(1.0, 2.0, 1.5, 1.5))
        self.assertAlmostEqual(1.3333333333333, unicycler.misc.weighted_average(1.0, 2.0, 4, 2))
        self.assertAlmostEqual(1.6666666666666, unicycler.misc.weighted_average(1.0, 2.0, 3, 6))
        self.assertAlmostEqual(1.6666666666666, unicycler.misc.weighted_average(1.0, 2.0, 3, 6))

    def test_weighted_average_list(self):
        self.assertAlmostEqual(1.0, unicycler.misc.weighted_average_list([1.0, 2.0, 3.0],
                                                                         [2.0, 0.0, 0.0]))
        self.assertAlmostEqual(2.0, unicycler.misc.weighted_average_list([1.0, 2.0, 3.0],
                                                                         [2.0, 0.0, 2.0]))
        self.assertAlmostEqual(2.5, unicycler.misc.weighted_average_list([1.0, 2.0, 3.0],
                                                                         [0.0, 1.0, 1.0]))
        self.assertAlmostEqual(2.6666666666666,
                               unicycler.misc.weighted_average_list([1.0, 2.0, 3.0],
                                                                    [0.0, 1.0, 2.0]))

    def test_round_to_nearest_odd(self):
        self.assertEqual(1, unicycler.misc.round_to_nearest_odd(0.9))
        self.assertEqual(1, unicycler.misc.round_to_nearest_odd(0.1))
        self.assertEqual(1, unicycler.misc.round_to_nearest_odd(1.9))
        self.assertEqual(3, unicycler.misc.round_to_nearest_odd(2.1))
        self.assertEqual(3, unicycler.misc.round_to_nearest_odd(2.9))
        self.assertEqual(3, unicycler.misc.round_to_nearest_odd(3.9))
        self.assertEqual(5, unicycler.misc.round_to_nearest_odd(4.1))
        self.assertEqual(5, unicycler.misc.round_to_nearest_odd(5.0))

    def test_get_compression_type(self):
        sample_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_data')
        ref = os.path.join(sample_dir, 'reference.fasta')
        reads = os.path.join(sample_dir, 'short_reads_1.fastq.gz')
        self.assertEqual('plain', unicycler.misc.get_compression_type(ref))
        self.assertEqual('gz', unicycler.misc.get_compression_type(reads))

    def test_get_sequence_file_type(self):
        sample_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_data')
        ref = os.path.join(sample_dir, 'reference.fasta')
        reads = os.path.join(sample_dir, 'short_reads_1.fastq.gz')
        self.assertEqual('FASTA', unicycler.misc.get_sequence_file_type(ref))
        self.assertEqual('FASTQ', unicycler.misc.get_sequence_file_type(reads))

    def test_get_num_agreement(self):
        self.assertAlmostEqual(1.0, unicycler.misc.get_num_agreement(2.0, 2.0))
        self.assertAlmostEqual(1.0, unicycler.misc.get_num_agreement(200.0, 200.0))
        self.assertAlmostEqual(0.0, unicycler.misc.get_num_agreement(0.0, 2.0))
        self.assertAlmostEqual(0.0, unicycler.misc.get_num_agreement(0.0, 200.0))
        self.assertAlmostEqual(0.5, unicycler.misc.get_num_agreement(1.0, 2.0))
        self.assertAlmostEqual(0.5, unicycler.misc.get_num_agreement(100.0, 200.0))

    def test_flip_number_order(self):
        self.assertEqual(unicycler.misc.flip_number_order(5, 6), ((5, 6), False))
        self.assertEqual(unicycler.misc.flip_number_order(6, 5), ((6, 5), False))
        self.assertEqual(unicycler.misc.flip_number_order(-5, -6), ((6, 5), True))
        self.assertEqual(unicycler.misc.flip_number_order(-6, -5), ((5, 6), True))

    def test_load_fasta(self):
        sample_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_data')
        ref = os.path.join(sample_dir, 'reference.fasta')
        fasta = unicycler.misc.load_fasta(ref)
        self.assertEqual(len(fasta), 3)
        self.assertEqual(fasta[0][0], 'NC_016833.1')
        self.assertEqual(fasta[2][0], 'NC_016834.1')
        self.assertTrue(fasta[0][1].startswith('ATGCTGATGAAAATACCTAAATAATCAGCCAGCACTCTATCTTTCCAAAT'
                                               'CCACAGCATAGCAAAGAGAGCAAAAGAGCCTGTAAATTCAGAAATT'))
        self.assertTrue(fasta[2][1].endswith('AGTTGATTTAAATCGCTACACCATTATGATTCATGTAGCGATTTAAATTACT'
                                             'ACATAATGGTGATTAGC'))

    def test_load_fasta_with_full_header(self):
        sample_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_data')
        ref = os.path.join(sample_dir, 'reference.fasta')
        fasta = unicycler.misc.load_fasta_with_full_header(ref)
        self.assertEqual(len(fasta), 3)
        self.assertEqual(fasta[0][0], 'NC_016833.1')
        self.assertEqual(fasta[2][0], 'NC_016834.1')
        self.assertEqual(fasta[0][1], 'NC_016833.1 Shigella sonnei 53G plasmid A, complete genome '
                                      'length=215774 circular=true')
        self.assertEqual(fasta[2][1], 'NC_016834.1 Shigella sonnei 53G plasmid E, complete genome '
                                      'length=8953 circular=true')
        self.assertTrue(fasta[0][2].startswith('ATGCTGATGAAAATACCTAAATAATCAGCCAGCACTCTATCTTTCCAAAT'
                                               'CCACAGCATAGCAAAGAGAGCAAAAGAGCCTGTAAATTCAGAAATT'))
        self.assertTrue(fasta[2][2].endswith('AGTTGATTTAAATCGCTACACCATTATGATTCATGTAGCGATTTAAATTACT'
                                             'ACATAATGGTGATTAGC'))

    def test_score_function(self):
        self.assertAlmostEqual(unicycler.misc.score_function(0.0, 1.0), 0.0)
        self.assertAlmostEqual(unicycler.misc.score_function(0.0, 2.0), 0.0)
        self.assertAlmostEqual(unicycler.misc.score_function(0.0, 100.0), 0.0)
        self.assertAlmostEqual(unicycler.misc.score_function(2.0, 2.0), 0.5)
        self.assertAlmostEqual(unicycler.misc.score_function(12.0, 12.0), 0.5)
        self.assertAlmostEqual(unicycler.misc.score_function(24.0, 12.0), 0.666666666666666666666)
        self.assertAlmostEqual(unicycler.misc.score_function(6.0, 12.0), 0.3333333333333333333333)
        self.assertAlmostEqual(unicycler.misc.score_function(100000000000000.0, 1.0), 1.0)
        self.assertAlmostEqual(unicycler.misc.score_function(100000000000000.0, 10.0), 1.0)

    def test_strip_read_extensions_fasta(self):
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fasta'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fasta.gz'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fasta'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fasta.gz'), 'file')

    def test_strip_read_extensions_fna(self):
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fna'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fna.gz'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fna'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fna.gz'), 'file')

    def test_strip_read_extensions_fa(self):
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fa'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fa.gz'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fa'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fa.gz'), 'file')

    def test_strip_read_extensions_other_fasta(self):
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fas'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fsa.gz'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fas'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fsa.gz'), 'file')

    def test_strip_read_extensions_fastq(self):
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fastq'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fastq.gz'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fastq'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fastq.gz'), 'file')

    def test_strip_read_extensions_fq(self):
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fq'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fq.gz'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fq'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.fq.gz'), 'file')

    def test_strip_read_extensions_capitals(self):
        self.assertEqual(unicycler.misc.strip_read_extensions('FILE.FASTA'), 'FILE')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.FNA.GZ'), 'file')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/FILE.fa.gz'), 'FILE')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/FiLe.FaStQ'), 'FiLe')

    def test_strip_read_extensions_fastq_extra_dots(self):
        self.assertEqual(unicycler.misc.strip_read_extensions('file.R1.fastq'), 'file.R1')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.R2.fastq'), 'file.R2')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.R1.fasta.gz'), 'file.R1')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.R2.fasta.gz'), 'file.R2')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.R1.fasta'), 'file.R1')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.R2.fasta'), 'file.R2')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.R1.fasta.gz'),
                         'file.R1')
        self.assertEqual(unicycler.misc.strip_read_extensions('path/to/file.R2.fasta.gz'),
                         'file.R2')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fastq.R1'), 'file.fastq.R1')
        self.assertEqual(unicycler.misc.strip_read_extensions('file.fastq.R2'), 'file.fastq.R2')

    def test_add_line_breaks_to_sequence(self):
        self.assertEqual(unicycler.misc.add_line_breaks_to_sequence('ATGCTGATGAAAATACC', 4),
                         'ATGC\nTGAT\nGAAA\nATAC\nC\n')
        self.assertEqual(unicycler.misc.add_line_breaks_to_sequence('ATGCTGATGAAAATACC', 8),
                         'ATGCTGAT\nGAAAATAC\nC\n')
        self.assertEqual(unicycler.misc.add_line_breaks_to_sequence('ATGCTGATGAAAATACC', 80),
                         'ATGCTGATGAAAATACC\n')

    def test_colour(self):
        t = 'test string'
        self.assertEqual(t, unicycler.misc.colour(t, 'normal'))
        self.assertEqual(t, unicycler.misc.colour(t, ''))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'green'))
        self.assertEqual(unicycler.misc.green(t), unicycler.misc.colour(t, 'green'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'bold_green'))
        self.assertEqual(unicycler.misc.bold_green(t), unicycler.misc.colour(t, 'bold_green'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'red'))
        self.assertEqual(unicycler.misc.red(t), unicycler.misc.colour(t, 'red'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'bold_red'))
        self.assertEqual(unicycler.misc.bold_red(t), unicycler.misc.colour(t, 'bold_red'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'bold'))
        self.assertEqual(unicycler.misc.bold(t), unicycler.misc.colour(t, 'bold'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'bold_underline'))
        self.assertEqual(unicycler.misc.bold_underline(t),
                         unicycler.misc.colour(t, 'bold_underline'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'underline'))
        self.assertEqual(unicycler.misc.underline(t), unicycler.misc.colour(t, 'underline'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'dim'))
        self.assertEqual(unicycler.misc.dim(t), unicycler.misc.colour(t, 'dim'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'dim_underline'))
        self.assertEqual(unicycler.misc.dim_underline(t),
                         unicycler.misc.colour(t, 'dim_underline'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'bold_yellow'))
        self.assertEqual(unicycler.misc.bold_yellow(t), unicycler.misc.colour(t, 'bold_yellow'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'bold_yellow_underline'))
        self.assertEqual(unicycler.misc.bold_yellow_underline(t),
                         unicycler.misc.colour(t, 'bold_yellow_underline'))
        self.assertNotEqual(t, unicycler.misc.colour(t, 'bold_red_underline'))
        self.assertEqual(unicycler.misc.bold_red_underline(t),
                         unicycler.misc.colour(t, 'bold_red_underline'))

    def test_len_without_format(self):
        t = 'test string'
        self.assertEqual(len(t), unicycler.misc.len_without_format(unicycler.misc.green(t)))
        self.assertEqual(len(t), unicycler.misc.len_without_format(unicycler.misc.bold_red(t)))
        self.assertEqual(len(t),
                         unicycler.misc.len_without_format(unicycler.misc.bold_yellow_underline(t)))

    def test_remove_formatting(self):
        t = 'test string'
        self.assertEqual(t, unicycler.misc.remove_formatting(unicycler.misc.green(t)))
        self.assertEqual(t, unicycler.misc.remove_formatting(unicycler.misc.bold_red(t)))
        self.assertEqual(t,
                         unicycler.misc.remove_formatting(unicycler.misc.bold_yellow_underline(t)))

    def test_get_all_files_in_current_dir(self):
        starting_cwd = os.getcwd()
        test_dir = os.path.dirname(__file__)
        os.chdir(test_dir)
        self.assertTrue(os.path.basename(__file__) in unicycler.misc.get_all_files_in_current_dir())
        os.chdir(starting_cwd)

    def test_convert_fastq_to_fasta(self):
        test_fastq = os.path.join(os.path.dirname(__file__), 'test_misc.fastq')
        test_fasta = os.path.join(os.path.dirname(__file__), 'temp_test.fasta')
        unicycler.misc.convert_fastq_to_fasta(test_fastq, test_fasta)
        fasta = unicycler.misc.load_fasta(test_fasta)
        self.assertEqual(len(fasta), 3)
        self.assertEqual(fasta[1][0], 'read_2')
        self.assertEqual(fasta[1][1], 'CACATACAGGCAGAGTGGCCGTGAAAGAAAGCAATCAGCGATGGTGCTCTGACGGGTTC'
                                      'GAGTTCTGCTGTGATAACGGAGAGAGACTGCGTGTCACGTTCGCGCTGGACTGCTGTGA'
                                      'TCGTGAG')
        os.remove(test_fasta)

    def test_java_version_parsing_1(self):
        java_version_output = 'java version "1.8.0_77"\n' \
                              'Java(TM) SE Runtime Environment (build 1.8.0_77-b03)\n' \
                              'Java HotSpot(TM) 64-Bit Server VM (build 25.77-b03, mixed mode)'
        version = unicycler.misc.java_version_from_java_output(java_version_output)
        self.assertEqual(version, '1.8.0_77')

    def test_java_version_parsing_2(self):
        java_version_output = 'java version "1.7.0_80"\n' \
                              'Java(TM) SE Runtime Environment (build 1.7.0_80-b15)\n' \
                              'Java HotSpot(TM) 64-Bit Server VM (build 24.80-b11, mixed mode)'
        version = unicycler.misc.java_version_from_java_output(java_version_output)
        self.assertEqual(version, '1.7.0_80')

    def test_java_version_parsing_3(self):
        java_version_output = 'java version "9.0.1"\n' \
                              'Java(TM) SE Runtime Environment (build 9.0.1+11)\n' \
                              'Java HotSpot(TM) 64-Bit Server VM (build 9.0.1+11, mixed mode)'
        version = unicycler.misc.java_version_from_java_output(java_version_output)
        self.assertEqual(version, '9.0.1')

    def test_java_version_parsing_4(self):
        java_version_output = 'openjdk version "1.8.0_131"\n' \
                              'OpenJDK Runtime Environment (build 1.8.0_131-8u131-b11-2-b11)\n' \
                              'OpenJDK 64-Bit Server VM (build 25.131-b11, mixed mode)'
        version = unicycler.misc.java_version_from_java_output(java_version_output)
        self.assertEqual(version, '1.8.0_131')

    def test_java_version_parsing_5(self):
        java_version_output = 'this is rubbish output'
        version = unicycler.misc.java_version_from_java_output(java_version_output)
        self.assertEqual(version, '')

    def test_java_version_parsing_6(self):
        java_version_output = 'openjdk version "9-Ubuntu"\n' \
                              'OpenJDK Runtime Environment (build 9-Ubuntu+0-9b181-4)\n' \
                              'OpenJDK 64-Bit Server VM (build 9-Ubuntu+0-9b181-4, mixed mode)'
        version = unicycler.misc.java_version_from_java_output(java_version_output)
        self.assertEqual(version, '9-Ubuntu')

    def test_spades_version_parsing_1(self):
        spades_version_output = 'SPAdes v3.10.1'
        version = unicycler.misc.spades_version_from_spades_output(spades_version_output)
        self.assertEqual(version, '3.10.1')

    def test_spades_version_parsing_2(self):
        spades_version_output = 'SPAdes v3.8.2'
        version = unicycler.misc.spades_version_from_spades_output(spades_version_output)
        self.assertEqual(version, '3.8.2')

    def test_spades_version_parsing_3(self):
        spades_version_output = 'option -v not recognized\nSPAdes genome assembler v.3.5.0\n\n' \
                                'Usage: SPAdes-3.5.0-Darwin/bin/spades.py [options] ' \
                                '-o <output_dir>\n\nBasic options:'
        version = unicycler.misc.spades_version_from_spades_output(spades_version_output)
        self.assertEqual(version, '3.5.0')

    def test_spades_version_parsing_4(self):
        spades_version_output = 'option -v not recognized\nSPAdes genome assembler v.2.4.0\n\n' \
                                'Usage: SPAdes-2.4.0-Darwin/bin/spades.py [options] ' \
                                '-o <output_dir>\n\nBasic options:'
        version = unicycler.misc.spades_version_from_spades_output(spades_version_output)
        self.assertEqual(version, '2.4.0')

    def test_spades_version_status_1(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('2.4.0'), 'too old')

    def test_spades_version_status_2(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.4.0'), 'too old')

    def test_spades_version_status_3(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.6.0'), 'too old')

    def test_spades_version_status_4(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.6.1'), 'too old')

    def test_spades_version_status_5(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.6.2'), 'good')

    def test_spades_version_status_6(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.7.0'), 'good')

    def test_spades_version_status_7(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.9.9'), 'good')

    def test_spades_version_status_8(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.13.0'), 'good')

    def test_spades_version_status_9(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.13.1'), 'too new')

    def test_spades_version_status_10(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('3.14.1'), 'too new')

    def test_spades_version_status_11(self):
        self.assertEqual(unicycler.misc.spades_status_from_version('4.0.0'), 'too new')

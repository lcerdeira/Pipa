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
import unicycler.read_ref
import unicycler.alignment
import unicycler.unicycler_align
import unicycler.log


class TestPerfectMatchAlignments(unittest.TestCase):

    def setUp(self):
        ref_fasta = os.path.join(os.path.dirname(__file__), 'test_semi_global_alignment.fasta')
        read_fastq = os.path.join(os.path.dirname(__file__), 'test_semi_global_alignment.fastq')
        refs = unicycler.read_ref.load_references(ref_fasta)
        read_dict, read_names, _ = unicycler.read_ref.load_long_reads(read_fastq)
        scoring_scheme = unicycler.alignment.AlignmentScoringScheme('3,-6,-5,-2')
        sensitivity_level = 0
        contamination_fasta = None
        threads = 1
        min_align_length = 10
        allowed_overlap = 0
        verbosity = 0
        self.aligned_reads = unicycler.unicycler_align.\
                semi_global_align_long_reads(refs, ref_fasta, read_dict, read_names, read_fastq,
                                             threads, scoring_scheme, [None], False,
                                             min_align_length, None, None, allowed_overlap,
                                             sensitivity_level, contamination_fasta, verbosity)
        unicycler.log.logger = unicycler.log.Log(log_filename=None, stdout_verbosity_level=0)

    def test_read_contained_1(self):
        read = self.aligned_reads['0']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '0')
        self.assertEqual(alignment.raw_score, 300)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 100)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 0)
        self.assertEqual(alignment.read_end_pos, 100)
        self.assertEqual(alignment.read_end_gap, 0)
        self.assertEqual(alignment.ref_start_pos, 60)
        self.assertEqual(alignment.ref_end_pos, 160)
        self.assertEqual(len(alignment.cigar_parts), 1)
        self.assertEqual(alignment.cigar_parts[0], '100M')

    def test_read_contained_2(self):
        read = self.aligned_reads['1']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '1')
        self.assertEqual(alignment.raw_score, 600)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 200)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 0)
        self.assertEqual(alignment.read_end_pos, 200)
        self.assertEqual(alignment.read_end_gap, 0)
        self.assertEqual(alignment.ref_start_pos, 100)
        self.assertEqual(alignment.ref_end_pos, 300)
        self.assertEqual(len(alignment.cigar_parts), 1)
        self.assertEqual(alignment.cigar_parts[0], '200M')

    def test_read_contained_3(self):
        read = self.aligned_reads['2']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '2')
        self.assertEqual(alignment.raw_score, 450)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 150)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 0)
        self.assertEqual(alignment.read_end_pos, 150)
        self.assertEqual(alignment.read_end_gap, 0)
        self.assertEqual(alignment.ref_start_pos, 0)
        self.assertEqual(alignment.ref_end_pos, 150)
        self.assertEqual(len(alignment.cigar_parts), 1)
        self.assertEqual(alignment.cigar_parts[0], '150M')

    def test_ref_contained_1(self):
        read = self.aligned_reads['3']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '3')
        self.assertEqual(alignment.raw_score, 300)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 100)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 62)
        self.assertEqual(alignment.read_end_pos, 162)
        self.assertEqual(alignment.read_end_gap, 138)
        self.assertEqual(alignment.ref_start_pos, 0)
        self.assertEqual(alignment.ref_end_pos, 100)
        self.assertEqual(len(alignment.cigar_parts), 3)
        self.assertEqual(alignment.cigar_parts[0], '62S')
        self.assertEqual(alignment.cigar_parts[1], '100M')
        self.assertEqual(alignment.cigar_parts[2], '138S')

    def test_ref_contained_2(self):
        read = self.aligned_reads['4']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '4')
        self.assertEqual(alignment.raw_score, 360)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 120)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 0)
        self.assertEqual(alignment.read_end_pos, 120)
        self.assertEqual(alignment.read_end_gap, 180)
        self.assertEqual(alignment.ref_start_pos, 0)
        self.assertEqual(alignment.ref_end_pos, 120)
        self.assertEqual(len(alignment.cigar_parts), 2)
        self.assertEqual(alignment.cigar_parts[0], '120M')
        self.assertEqual(alignment.cigar_parts[1], '180S')

    def test_ref_contained_3(self):
        read = self.aligned_reads['5']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '5')
        self.assertEqual(alignment.raw_score, 540)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 180)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 120)
        self.assertEqual(alignment.read_end_pos, 300)
        self.assertEqual(alignment.read_end_gap, 0)
        self.assertEqual(alignment.ref_start_pos, 0)
        self.assertEqual(alignment.ref_end_pos, 180)
        self.assertEqual(len(alignment.cigar_parts), 2)
        self.assertEqual(alignment.cigar_parts[0], '120S')
        self.assertEqual(alignment.cigar_parts[1], '180M')

    def test_read_start_overlap(self):
        read = self.aligned_reads['6']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '6')
        self.assertEqual(alignment.raw_score, 330)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 110)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 190)
        self.assertEqual(alignment.read_end_pos, 300)
        self.assertEqual(alignment.read_end_gap, 0)
        self.assertEqual(alignment.ref_start_pos, 0)
        self.assertEqual(alignment.ref_end_pos, 110)
        self.assertEqual(len(alignment.cigar_parts), 2)
        self.assertEqual(alignment.cigar_parts[0], '190S')
        self.assertEqual(alignment.cigar_parts[1], '110M')

    def test_read_end_overlap(self):
        read = self.aligned_reads['7']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '7')
        self.assertEqual(alignment.raw_score, 390)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 130)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 0)
        self.assertEqual(alignment.read_end_pos, 130)
        self.assertEqual(alignment.read_end_gap, 170)
        self.assertEqual(alignment.ref_start_pos, 170)
        self.assertEqual(alignment.ref_end_pos, 300)
        self.assertEqual(len(alignment.cigar_parts), 2)
        self.assertEqual(alignment.cigar_parts[0], '130M')
        self.assertEqual(alignment.cigar_parts[1], '170S')

    def test_end_to_end(self):
        read = self.aligned_reads['8']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '8')
        self.assertEqual(alignment.raw_score, 900)
        self.assertEqual(alignment.scaled_score, 100.0)
        self.assertEqual(alignment.percent_identity, 100.0)
        self.assertEqual(alignment.match_count, 300)
        self.assertEqual(alignment.mismatch_count, 0)
        self.assertEqual(alignment.insertion_count, 0)
        self.assertEqual(alignment.deletion_count, 0)
        self.assertEqual(alignment.read_start_pos, 0)
        self.assertEqual(alignment.read_end_pos, 300)
        self.assertEqual(alignment.read_end_gap, 0)
        self.assertEqual(alignment.ref_start_pos, 0)
        self.assertEqual(alignment.ref_end_pos, 300)
        self.assertEqual(len(alignment.cigar_parts), 1)
        self.assertEqual(alignment.cigar_parts[0], '300M')


class TestContainedReadAlignments(unittest.TestCase):
    """
    These test cases use real reads/contigs and cover cases where the read aligns to the middle of
    the contig
    """
    def setUp(self):
        unicycler.log.logger = unicycler.log.Log(log_filename=None, stdout_verbosity_level=0)
        temp_name = 'TEMP_' + str(os.getpid())
        self.temp_fasta = temp_name + '.fasta'
        self.temp_fastq = temp_name + '.fastq'
        all_ref_fasta = os.path.join(os.path.dirname(__file__),
                                     'test_semi_global_alignment_contained_reads.fasta')
        self.all_refs = unicycler.read_ref.load_references(all_ref_fasta)
        all_read_fastq = os.path.join(os.path.dirname(__file__),
                                           'test_semi_global_alignment_contained_reads.fastq')
        self.all_reads, _, _ = unicycler.read_ref.load_long_reads(all_read_fastq)

        # Alignments are tests with approximate boundaries to allow for a big of wiggle room if the
        # implementation changes.
        self.pos_margin_of_error = 10

    def do_alignment(self, read_ref_name, sensitivity_level):
        # Save just the read/ref of interest (which will have the same name) into temporary
        # separate files, so th alignment can be done for just them.
        ref = [x for x in self.all_refs if x.name == read_ref_name][0]
        read = [x for x in self.all_reads.values() if x.name == read_ref_name][0]
        with open(self.temp_fasta, 'wt') as ref_fasta:
            ref_fasta.write('>' + ref.name + '\n')
            ref_fasta.write(ref.sequence + '\n')
        with open(self.temp_fastq, 'wt') as read_fastq:
            read_fastq.write('@' + read.name + '\n')
            read_fastq.write(read.sequence + '\n')
            read_fastq.write('+\n')
            read_fastq.write(read.qualities + '\n')

        refs = unicycler.read_ref.load_references(self.temp_fasta)
        read_dict, read_names, _ = unicycler.read_ref.load_long_reads(self.temp_fastq)
        scoring_scheme = unicycler.alignment.AlignmentScoringScheme('3,-6,-5,-2')
        contamination_fasta = None
        threads = 1
        min_align_length = 10
        allowed_overlap = 0
        verbosity = 0
        self.aligned_reads = unicycler.unicycler_align.\
                semi_global_align_long_reads(refs, self.temp_fasta, read_dict, read_names,
                                             self.temp_fastq, threads, scoring_scheme, [None],
                                             False, min_align_length, None, None, allowed_overlap,
                                             sensitivity_level, contamination_fasta, verbosity)

    def tearDown(self):
        if os.path.isfile(self.temp_fasta):
            os.remove(self.temp_fasta)
        if os.path.isfile(self.temp_fastq):
            os.remove(self.temp_fastq)

    def test_short_contained_read(self):
        self.do_alignment('0', 0)
        read = self.aligned_reads['0']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '0')
        self.assertTrue(alignment.raw_score >= 1418)
        self.assertTrue(alignment.scaled_score > 90.78)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)  # end of read
        self.assertEqual(read_end, 608)  # end of read
        self.assertTrue(abs(alignment.ref_start_pos - 31040) < self.pos_margin_of_error)
        self.assertTrue(abs(alignment.ref_end_pos - 31679) < self.pos_margin_of_error)

    def test_medium_contained_read(self):
        self.do_alignment('1', 0)
        read = self.aligned_reads['1']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '1')
        self.assertTrue(alignment.raw_score >= 16608)
        self.assertTrue(alignment.scaled_score > 90.12)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)  # end of read
        self.assertEqual(read_end, 7360)  # end of read
        self.assertTrue(abs(alignment.ref_start_pos - 68597) < self.pos_margin_of_error)
        self.assertTrue(abs(alignment.ref_end_pos - 76202) < self.pos_margin_of_error)

    def test_long_contained_read(self):
        self.do_alignment('2', 0)
        read = self.aligned_reads['2']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '2')
        self.assertTrue(alignment.raw_score >= 122681)
        self.assertTrue(alignment.scaled_score > 91.19)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)  # end of read
        self.assertEqual(read_end, 52096)  # end of read
        self.assertTrue(abs(alignment.ref_start_pos - 2986) < self.pos_margin_of_error)
        self.assertTrue(abs(alignment.ref_end_pos - 57064) < self.pos_margin_of_error)


class TestToughAlignments(unittest.TestCase):
    """
    These test cases are made from real alignments which proved to be difficult.
    """
    def setUp(self):
        unicycler.log.logger = unicycler.log.Log(log_filename=None, stdout_verbosity_level=0)
        temp_name = 'TEMP_' + str(os.getpid())
        self.temp_fasta = temp_name + '.fasta'
        self.temp_fastq = temp_name + '.fastq'
        all_ref_fasta = os.path.join(os.path.dirname(__file__),
                                     'test_semi_global_alignment_tough.fasta')
        self.all_refs = unicycler.read_ref.load_references(all_ref_fasta)
        all_read_fastq = os.path.join(os.path.dirname(__file__),
                                           'test_semi_global_alignment_tough.fastq')
        self.all_reads, _, _ = unicycler.read_ref.load_long_reads(all_read_fastq)

        # Alignments are tests with approximate boundaries to allow for a big of wiggle room if the
        # implementation changes.
        self.pos_margin_of_error = 10

    def do_alignment(self, read_ref_name, sensitivity_level):
        # Save just the read/ref of interest (which will have the same name) into temporary
        # separate files, so th alignment can be done for just them.
        ref = [x for x in self.all_refs if x.name == read_ref_name][0]
        read = [x for x in self.all_reads.values() if x.name == read_ref_name][0]
        with open(self.temp_fasta, 'wt') as ref_fasta:
            ref_fasta.write('>' + ref.name + '\n')
            ref_fasta.write(ref.sequence + '\n')
        with open(self.temp_fastq, 'wt') as read_fastq:
            read_fastq.write('@' + read.name + '\n')
            read_fastq.write(read.sequence + '\n')
            read_fastq.write('+\n')
            read_fastq.write(read.qualities + '\n')

        refs = unicycler.read_ref.load_references(self.temp_fasta)
        read_dict, read_names, _ = unicycler.read_ref.load_long_reads(self.temp_fastq)
        scoring_scheme = unicycler.alignment.AlignmentScoringScheme('3,-6,-5,-2')
        contamination_fasta = None
        threads = 1
        min_align_length = 10
        allowed_overlap = 0
        verbosity = 0
        self.aligned_reads = unicycler.unicycler_align.\
                semi_global_align_long_reads(refs, self.temp_fasta, read_dict, read_names,
                                             self.temp_fastq, threads, scoring_scheme, [None],
                                             False, min_align_length, None, None, allowed_overlap,
                                             sensitivity_level, contamination_fasta, verbosity)

    def tearDown(self):
        if os.path.isfile(self.temp_fasta):
            os.remove(self.temp_fasta)
        if os.path.isfile(self.temp_fastq):
            os.remove(self.temp_fastq)

    def test_tough_alignment_0(self):
        """
        The beginning of the reference in this case is repetitive, which was able to throw off
        Seqan's global chaining algorithm, resulting in an awkward alignment. I think I fixed this
        by limiting Seqan to the seeds which are near the diagonals of line tracing points.
        """
        self.do_alignment('0', 0)
        read = self.aligned_reads['0']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '0')
        self.assertTrue(alignment.raw_score >= 126074)
        self.assertTrue(alignment.scaled_score > 91.07)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertTrue(abs(read_start - 18662) < self.pos_margin_of_error)
        self.assertEqual(read_end, 72402)  # end of read
        self.assertEqual(alignment.ref_start_pos, 0)     # start of ref
        self.assertTrue(abs(alignment.ref_end_pos - 55814) < self.pos_margin_of_error)

    def test_tough_alignment_1(self):
        """
        This read goes through a repetitive area, which means that the densest area of common
        k-mers is not on the correct alignment line. This means more than one line tracing is
        required to get it right.
        """
        self.do_alignment('1', 0)
        read = self.aligned_reads['1']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '1')
        self.assertTrue(alignment.raw_score >= 20740)
        self.assertTrue(alignment.scaled_score > 91.02)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertTrue(abs(read_start - 10785) < self.pos_margin_of_error)
        self.assertTrue(abs(read_end - 19629) < self.pos_margin_of_error)
        self.assertEqual(alignment.ref_start_pos, 0)   # start of ref
        self.assertEqual(alignment.ref_end_pos, 9241)  # end of ref

    def test_tough_alignment_2(self):
        """
        This read goes through a repetitive area, which means that the densest area of common
        k-mers is not on the correct alignment line. This means more than one line tracing is
        required to get it right.
        """
        self.do_alignment('2', 0)
        read = self.aligned_reads['2']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '2')
        self.assertTrue(alignment.raw_score >= 34439)
        self.assertTrue(alignment.scaled_score > 90.35)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertTrue(abs(read_start - 22493) < self.pos_margin_of_error)
        self.assertEqual(read_end, 37581)  # end of read
        self.assertEqual(alignment.ref_start_pos, 0)     # start of ref
        self.assertTrue(abs(alignment.ref_end_pos - 15673) < self.pos_margin_of_error)

    def test_tough_alignment_3(self):
        """
        The first line tracing of this alignment is bad but uses all the points. This previously
        caused a crash when the program tried to do a second line trace but there were no points
        left to find a starting position.
        """
        self.do_alignment('3', 0)
        read = self.aligned_reads['3']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '3')
        self.assertTrue(alignment.raw_score >= 786)
        self.assertTrue(alignment.scaled_score > 75.19)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)  # start of read
        self.assertEqual(read_end, 872)  # end of read
        self.assertTrue(abs(alignment.ref_start_pos - 41783) < self.pos_margin_of_error)
        self.assertTrue(abs(alignment.ref_end_pos - 42680) < self.pos_margin_of_error)

    def test_tough_alignment_4(self):
        """
        Like so many of these tough ones, this case has a read which enters a repetitive region
        after overlapping with the end of the contig. Before I fixed some aspects of the alignment,
        the line tracing was getting caught on some of these spurious repeats instead of sticking
        to the main line.
        """
        self.do_alignment('4', 0)
        read = self.aligned_reads['4']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '4')
        self.assertTrue(alignment.raw_score >= 58531)
        self.assertTrue(alignment.scaled_score > 86.47)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertTrue(abs(read_start - 9582) < self.pos_margin_of_error)
        self.assertEqual(read_end, 39544)  # end of read
        self.assertEqual(alignment.ref_start_pos, 0)     # start of ref
        self.assertTrue(abs(alignment.ref_end_pos - 31277) < self.pos_margin_of_error)

    def test_tough_alignment_5(self):
        self.do_alignment('5', 0)
        read = self.aligned_reads['5']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '5')
        self.assertTrue(alignment.raw_score >= 2792)
        self.assertTrue(alignment.scaled_score > 89.37)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertTrue(abs(read_start - 5121) < self.pos_margin_of_error)
        self.assertEqual(read_end, 6396)  # end of read
        self.assertEqual(alignment.ref_start_pos, 0)     # start of ref
        self.assertTrue(abs(alignment.ref_end_pos - 1323) < self.pos_margin_of_error)

    def test_tough_alignment_6(self):
        """
        This one misses the right alignment on lower sensitivities because the line tracing never
        gets 'lost' but is still the wrong one. Higher sensitivities find the correct alignment by
        trying other starting points.
        """
        self.do_alignment('6', 0)
        read = self.aligned_reads['6']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '6')
        self.assertTrue(alignment.raw_score >= 10883)
        self.assertTrue(alignment.scaled_score > 88.50)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)  # start of read
        self.assertTrue(abs(read_end - 5077) < self.pos_margin_of_error)
        self.assertTrue(abs(alignment.ref_start_pos - 253445) < self.pos_margin_of_error)
        self.assertEqual(alignment.ref_end_pos, 258801)  # end of ref

    def test_tough_alignment_7(self):
        """
        This one misses the right alignment on lower sensitivities because the line tracing never
        gets 'lost' but is still the wrong one. Higher sensitivities find the correct alignment by
        trying other starting points.
        """
        self.do_alignment('7', 0)
        read = self.aligned_reads['7']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '7')
        self.assertTrue(alignment.raw_score >= 125555)
        self.assertTrue(alignment.scaled_score > 88.92)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)  # start of read
        self.assertTrue(abs(read_end - 57721) < self.pos_margin_of_error)
        self.assertTrue(abs(alignment.ref_start_pos - 35024) < self.pos_margin_of_error)
        self.assertEqual(alignment.ref_end_pos, 95758)  # end of ref

    def test_tough_alignment_8(self):
        """
        This has a weird change in slope - the read has a good part and a bad part. Ideally the
        alignment should get the whole thing!
        """
        self.do_alignment('8', 0)
        read = self.aligned_reads['8']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '8')
        self.assertTrue(alignment.raw_score >= 2812)
        self.assertTrue(alignment.scaled_score > 76.36)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertTrue(abs(read_start - 681) < self.pos_margin_of_error)
        self.assertEqual(read_end, 3808)  # end of read
        self.assertTrue(abs(alignment.ref_start_pos - 19594) < self.pos_margin_of_error)
        self.assertEqual(alignment.ref_end_pos, 21983)  # end of ref

    def test_tough_alignment_9(self):
        """
        This is a very low quality read.
        """
        self.do_alignment('9', 0)
        read = self.aligned_reads['9']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '9')

        # TO DO: refine the alignment algorithm to align this read correctly!
        # TO DO: refine the alignment algorithm to align this read correctly!
        # TO DO: refine the alignment algorithm to align this read correctly!
        # TO DO: refine the alignment algorithm to align this read correctly!
        # TO DO: refine the alignment algorithm to align this read correctly!
        # TO DO: refine the alignment algorithm to align this read correctly!

    def test_tough_alignment_10(self):
        """
        This is a very low quality read.
        """
        self.do_alignment('10', 0)
        read = self.aligned_reads['10']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '10')
        self.assertTrue(alignment.raw_score >= 4978)
        self.assertTrue(alignment.scaled_score > 71.07)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)  # start of read
        self.assertEqual(read_end, 10923)  # end of read
        self.assertTrue(abs(alignment.ref_start_pos - 2001) < self.pos_margin_of_error)
        self.assertTrue(abs(alignment.ref_end_pos - 12186) < self.pos_margin_of_error)

    def test_tough_alignment_11(self):
        """
        Repeats at one end of the read.
        """
        self.do_alignment('11', 0)
        read = self.aligned_reads['11']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '11')
        self.assertTrue(alignment.raw_score >= 6996)
        self.assertTrue(alignment.scaled_score > 92.95)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)  # start of read
        self.assertTrue(abs(read_end - 2863) < self.pos_margin_of_error)
        self.assertEqual(alignment.ref_start_pos, 0)  # start of ref
        self.assertTrue(abs(alignment.ref_end_pos - 2818) < self.pos_margin_of_error)

    def test_tough_alignment_12(self):
        """
        Repeats at one end of the read.
        """
        self.do_alignment('12', 0)
        read = self.aligned_reads['12']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '12')
        self.assertTrue(alignment.raw_score >= 3805)
        self.assertTrue(alignment.scaled_score > 92.83)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertTrue(abs(read_start - 3037) < self.pos_margin_of_error)
        self.assertEqual(read_end, 4611)  # end of read
        self.assertEqual(alignment.ref_start_pos, 0)  # start of ref
        self.assertTrue(abs(alignment.ref_end_pos - 1538) < self.pos_margin_of_error)

    def test_tough_alignment_13(self):
        """
        This read caused a crash before I added the getMaxSeedChainGapArea function in
        semi_global_align.cpp. It left a very large gap in the global seed chain which caused some
        problem with Seqan.
        """
        self.do_alignment('13', 1)
        read = self.aligned_reads['13']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '13')
        self.assertTrue(alignment.raw_score >= 101608)
        self.assertTrue(alignment.scaled_score > 88.49)
        read_start, read_end = alignment.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)    # start of read
        self.assertEqual(read_end, 46710)  # end of read
        self.assertTrue(abs(alignment.ref_start_pos - 109308) < self.pos_margin_of_error)
        self.assertTrue(abs(alignment.ref_end_pos - 159675) < self.pos_margin_of_error)

    def test_tough_alignment_14(self):
        """
        This read caused a crash before I added made a few fixes to the line tracing code. It won't
        produce an alignment, but this test will confirm that it doesn't crash.
        """
        self.do_alignment('14', 1)
        read = self.aligned_reads['14']
        self.assertEqual(len(read.alignments), 1)
        alignment = read.alignments[0]
        self.assertEqual(alignment.read.name, '14')
        self.assertTrue(alignment.raw_score >= 204)
        self.assertTrue(alignment.scaled_score > 93.0)

    def test_tough_alignment_15(self):
        """
        This read should hit the same reference twice, even at low sensitivities.
        """
        self.do_alignment('15', 0)
        read = self.aligned_reads['15']
        self.assertEqual(len(read.alignments), 2)
        alignment_1 = read.alignments[0]
        alignment_2 = read.alignments[1]
        self.assertEqual(alignment_1.read.name, '15')
        self.assertEqual(alignment_2.read.name, '15')
        self.assertTrue(alignment_1.raw_score >= 1846)
        self.assertTrue(alignment_2.raw_score >= 3137)
        read_start, _ = alignment_1.read_start_end_positive_strand()
        _, read_end = alignment_2.read_start_end_positive_strand()
        self.assertEqual(read_start, 0)    # start of read
        self.assertEqual(read_end, 4144)  # end of read

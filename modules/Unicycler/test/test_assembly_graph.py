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
import unicycler.assembly_graph
import unicycler.misc
import unicycler.log


class TestAssemblyGraphFunctionsFastg(unittest.TestCase):
    """
    Tests various AssemblyGraph functions on a graph loaded from a SPAdes FASTG file.
    """

    def setUp(self):
        test_fastg = os.path.join(os.path.dirname(__file__), 'test_assembly_graph.fastg')
        self.graph = unicycler.assembly_graph.AssemblyGraph(test_fastg, 25, paths_file=None,
                                                            insert_size_mean=401,
                                                            insert_size_deviation=60)
        unicycler.log.logger = unicycler.log.Log(log_filename=None, stdout_verbosity_level=0)

    def test_attributes(self):
        self.assertEqual(self.graph.overlap, 25)
        self.assertEqual(self.graph.insert_size_mean, 401)
        self.assertEqual(self.graph.insert_size_deviation, 60)

    def test_segments(self):
        self.assertEqual(len(self.graph.segments), 336)

    def test_sequence(self):
        self.assertEqual(self.graph.segments[273].forward_sequence, 'CGGCTGTTGCGGCTGTTGCGGCTGTT')
        self.assertEqual(self.graph.segments[273].reverse_sequence, 'AACAGCCGCAACAGCCGCAACAGCCG')
        self.assertEqual(self.graph.segments[170].forward_sequence,
                         'TTGTTTTACGTGCCAGCCGCTTGATCGATAGGAATTAAAACCCCAAAA')
        self.assertEqual(self.graph.segments[170].reverse_sequence,
                         'TTTTGGGGTTTTAATTCCTATCGATCAAGCGGCTGGCACGTAAAACAA')

    def test_forward_links(self):
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 904)

    def test_reverse_links(self):
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 904)

    def test_links_match(self):
        """
        Tests that each segment's forward links match up with its reverse complement's reverse
        links.
        """
        for segment, forward_link_list in self.graph.forward_links.items():
            reverse_link_list = self.graph.reverse_links[-segment]
            flipped_reverse_link_list = [-x for x in reverse_link_list]
            self.assertEqual(sorted(forward_link_list), sorted(flipped_reverse_link_list))

    def test_load_spades_paths(self):
        self.assertEqual(len(self.graph.paths), 0)
        paths_file = os.path.join(os.path.dirname(__file__), 'test_assembly_graph.fastg.paths')
        self.graph.load_spades_paths(paths_file)
        self.assertEqual(len(self.graph.paths), 53)

    def test_get_median_read_depth(self):
        diff = abs(self.graph.get_median_read_depth() - 40.2)
        self.assertTrue(diff < 0.1)

    def test_normalise_read_depths(self):
        self.graph.normalise_read_depths()
        self.assertAlmostEqual(self.graph.get_median_read_depth(), 1.0)

    def test_get_total_length(self):
        self.assertEqual(self.graph.get_total_length(), 187896)

    def test_get_total_length_no_overlaps(self):
        self.assertEqual(self.graph.get_total_length_no_overlaps(), 179496)

    def test_total_dead_end_count(self):
        self.assertEqual(self.graph.total_dead_end_count(), 0)

    def test_dead_end_count(self):
        for seg_num in self.graph.segments:
            self.assertEqual(self.graph.dead_end_count(seg_num), 0)

    def test_save_to_fasta(self):
        temp_fasta = os.path.join(os.path.dirname(__file__), 'temp.fasta')
        self.graph.save_to_fasta(temp_fasta)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 336)
        self.assertEqual(fasta[0][0], '1')
        self.assertEqual(fasta[335][0], '336')
        self.assertEqual(fasta[0][1], '1 length=449 depth=82.60x')
        self.assertEqual(fasta[335][1], '336 length=185 depth=124.44x')
        self.assertTrue(fasta[0][2].startswith('ACCAGCCGCTGCGGGCCACCCGGAGCACGCGGCACATTGCCTTGATGCTG'
                                               'AACT'))
        self.assertTrue(fasta[335][2].endswith('TGTCGTGAAGCTTCACGAAGATGATTTTTTTGACGAAGAAGA'))
        os.remove(temp_fasta)

    def test_save_to_fasta_length(self):
        temp_fasta = os.path.join(os.path.dirname(__file__), 'temp.fasta')

        self.graph.save_to_fasta(temp_fasta, min_length=0)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 336)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=1)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 336)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=10)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 336)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=20)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 336)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=26)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 336)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=27)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 318)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=30)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 306)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=40)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 285)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=50)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 239)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=100)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 151)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=200)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 103)
        os.remove(temp_fasta)

        self.graph.save_to_fasta(temp_fasta, min_length=1000)
        fasta = unicycler.misc.load_fasta_with_full_header(temp_fasta)
        self.assertEqual(len(fasta), 40)
        os.remove(temp_fasta)

    def test_save_specific_segments_to_fasta(self):
        temp_fasta = os.path.join(os.path.dirname(__file__), 'temp.fasta')
        seg_nums = [1, 3, 5, 7, 9]
        segments = [self.graph.segments[x] for x in seg_nums]
        self.graph.save_specific_segments_to_fasta(temp_fasta, segments)
        fasta = unicycler.misc.load_fasta(temp_fasta)
        self.assertEqual(len(fasta), 5)
        self.assertEqual(fasta[0][0], '1')
        self.assertEqual(fasta[2][0], '5')
        self.assertTrue(fasta[0][1].startswith('ACCAGCCGCTGCGGGCCACCCGGAGCACGCGGCACATTGCCTTGATGCT'
                                               'GAACT'))
        self.assertTrue(fasta[2][1].endswith('TGCATGACAAAGTCATCGGGCATTATCTGAACATAAAACACTATCAATAAG'
                                             'TT'))
        os.remove(temp_fasta)

    def test_save_to_gfa(self):
        """
        This test saves the graph to GFA, loads the GFA graph and then compares the two graphs to
        make sure they are the same.
        """
        temp_gfa = os.path.join(os.path.dirname(__file__), 'temp.gfa')
        self.graph.save_to_gfa(temp_gfa, include_insert_size=True)
        graph2 = unicycler.assembly_graph.AssemblyGraph(temp_gfa, 25)
        self.assertEqual(self.graph.overlap, graph2.overlap)
        self.assertEqual(self.graph.insert_size_mean, graph2.insert_size_mean)
        self.assertEqual(self.graph.insert_size_deviation, graph2.insert_size_deviation)
        self.assertEqual(len(self.graph.segments), len(graph2.segments))
        link_count_1, link_count_2 = 0, 0
        for link_list in self.graph.forward_links.values():
            link_count_1 += len(link_list)
        for link_list in graph2.forward_links.values():
            link_count_2 += len(link_list)
        self.assertEqual(link_count_1, link_count_2)
        os.remove(temp_gfa)

    def test_get_all_gfa_link_lines(self):
        gfa_link_lines = self.graph.get_all_gfa_link_lines()
        self.assertEqual(gfa_link_lines.count('\n'), 452)
        self.assertEqual(gfa_link_lines.count('25M'), 452)

    def test_filter_by_read_depth(self):
        # A loop segment can be removed only when its depth drops below the threshold.
        self.assertEqual(len(self.graph.segments), 336)
        self.graph.filter_by_read_depth(0.5)
        self.assertEqual(len(self.graph.segments), 336)
        self.graph.segments[68].depth = 21.0
        self.graph.filter_by_read_depth(0.5)
        self.assertEqual(len(self.graph.segments), 336)
        self.graph.segments[68].depth = 20.0
        self.graph.filter_by_read_depth(0.5)
        self.assertEqual(len(self.graph.segments), 335)

        # A low-depth segment is only removed if its a dead end.
        self.graph.segments[306].depth = 0.1
        self.graph.filter_by_read_depth(0.5)
        self.assertEqual(len(self.graph.segments), 335)
        self.graph.remove_segments([273])
        self.assertEqual(len(self.graph.segments), 334)
        self.graph.filter_by_read_depth(0.5)
        self.assertEqual(len(self.graph.segments), 333)

    def test_remove_segments(self):
        self.assertEqual(len(self.graph.segments), 336)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 904)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 904)

        self.graph.remove_segments([276])
        self.assertEqual(len(self.graph.segments), 335)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 902)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 902)

        self.graph.remove_segments([273])
        self.assertEqual(len(self.graph.segments), 334)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 894)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 894)

        self.graph.remove_segments([67, 108, 222, 297])
        self.assertEqual(len(self.graph.segments), 330)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 870)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 870)

    def test_remove_small_components(self):
        self.assertEqual(len(self.graph.segments), 336)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 904)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 904)

        self.graph.remove_small_components(5000)
        self.assertEqual(len(self.graph.segments), 336)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 904)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 904)

        self.graph.remove_small_components(6000)
        self.assertEqual(len(self.graph.segments), 335)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 902)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 902)

        self.graph.remove_small_components(180000)
        self.assertEqual(len(self.graph.segments), 335)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 902)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 902)

        self.graph.remove_small_components(190000)
        self.assertEqual(len(self.graph.segments), 0)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 0)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 0)

    def test_get_estimated_sequence_len(self):
        estimated_sequence_len = self.graph.get_estimated_sequence_len()
        self.assertTrue(estimated_sequence_len > 248000)
        self.assertTrue(estimated_sequence_len < 255000)

    def test_remove_all_overlaps(self):
        self.assertEqual(self.graph.overlap, 25)
        path_1_before_overlap_removal = self.graph.get_path_sequence([152, 297, 56, -222, -72])
        seg_lengths = {s.number: s.get_length() for s in self.graph.segments.values()}
        self.graph.remove_all_overlaps()
        self.assertEqual(self.graph.overlap, 0)
        path_1_after_overlap_removal = self.graph.get_path_sequence([152, 297, 56, -222, -72])
        self.assertTrue(path_1_after_overlap_removal in path_1_before_overlap_removal)
        for seg_num in seg_lengths:
            self.assertTrue(self.graph.segments[seg_num].get_length() <= seg_lengths[seg_num])

    def test_get_n_segment_length(self):
        self.assertEqual(self.graph.get_n_segment_length(50), 3217)


class TestAssemblyGraphFunctionsGfa(unittest.TestCase):
    """
    Tests various AssemblyGraph functions on a graph loaded from a GFA file.
    """

    def setUp(self):
        test_gfa = os.path.join(os.path.dirname(__file__), 'test_assembly_graph.gfa')
        self.graph = unicycler.assembly_graph.AssemblyGraph(test_gfa, 0)
        unicycler.log.logger = unicycler.log.Log(log_filename=None, stdout_verbosity_level=0)

    def test_attributes(self):
        self.assertEqual(self.graph.overlap, 0)
        self.assertAlmostEqual(self.graph.insert_size_mean, 543.21)
        self.assertAlmostEqual(self.graph.insert_size_deviation, 123.45)

    def test_segments(self):
        self.assertEqual(len(self.graph.segments), 19)

    def test_sequence(self):
        self.assertEqual(self.graph.segments[1].forward_sequence, 'TTCTATTTTG')
        self.assertEqual(self.graph.segments[1].reverse_sequence, 'CAAAATAGAA')
        self.assertEqual(self.graph.segments[19].forward_sequence, 'AAAAAAAAAAAAAAAAAAAAAAAAA')
        self.assertEqual(self.graph.segments[19].reverse_sequence, 'TTTTTTTTTTTTTTTTTTTTTTTTT')

    def test_forward_links(self):
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)

    def test_reverse_links(self):
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

    def test_links_match(self):
        """
        Tests that each segment's forward links match up with its reverse complement's reverse
        links.
        """
        for segment, forward_link_list in self.graph.forward_links.items():
            reverse_link_list = self.graph.reverse_links[-segment]
            flipped_reverse_link_list = [-x for x in reverse_link_list]
            self.assertEqual(sorted(forward_link_list), sorted(flipped_reverse_link_list))

    def test_get_median_read_depth(self):
        diff = abs(self.graph.get_median_read_depth() - 1.0)
        self.assertTrue(diff < 0.01)

    def test_normalise_read_depths(self):
        self.graph.normalise_read_depths()
        self.assertAlmostEqual(self.graph.get_median_read_depth(), 1.0)

    def test_get_total_length(self):
        self.assertEqual(self.graph.get_total_length(), 214)

    def test_get_total_length_no_overlaps(self):
        self.assertEqual(self.graph.get_total_length_no_overlaps(), 214)

    def test_total_dead_end_count(self):
        self.assertEqual(self.graph.total_dead_end_count(), 4)

    def test_dead_end_count(self):
        for seg_num in self.graph.segments:
            if seg_num == 16:
                expected_dead_ends = 2
            elif seg_num == 17 or seg_num == 18:
                expected_dead_ends = 1
            else:
                expected_dead_ends = 0
            self.assertEqual(self.graph.dead_end_count(seg_num), expected_dead_ends)

    def test_filter_homopolymer_loops(self):
        self.graph.filter_homopolymer_loops()
        self.assertEqual(len(self.graph.segments), 18)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 38)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 38)
        self.assertEqual(self.graph.get_total_length(), 189)
        self.assertEqual(self.graph.get_total_length_no_overlaps(), 189)

    def test_remove_small_components(self):
        self.graph.remove_small_components(19)
        self.assertEqual(len(self.graph.segments), 19)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

        self.graph.remove_small_components(20)
        self.assertEqual(len(self.graph.segments), 19)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

        self.graph.remove_small_components(21)
        self.assertEqual(len(self.graph.segments), 18)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

        self.graph.remove_small_components(25)
        self.assertEqual(len(self.graph.segments), 18)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

        self.graph.remove_small_components(26)
        self.assertEqual(len(self.graph.segments), 17)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 38)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 38)

    def test_remove_small_dead_ends(self):
        self.graph.remove_small_dead_ends(19)
        self.assertEqual(len(self.graph.segments), 19)
        self.assertEqual(self.graph.get_total_length(), 214)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

        self.graph.remove_small_dead_ends(20)
        self.assertEqual(len(self.graph.segments), 19)
        self.assertEqual(self.graph.get_total_length(), 214)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

        self.graph.remove_small_dead_ends(21)
        self.assertEqual(len(self.graph.segments), 17)
        self.assertEqual(self.graph.get_total_length(), 174)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 38)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 38)

        self.graph.remove_small_dead_ends(22)
        self.assertEqual(len(self.graph.segments), 16)
        self.assertEqual(self.graph.get_total_length(), 153)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 36)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 36)

        self.graph.remove_small_dead_ends(1000)
        self.assertEqual(len(self.graph.segments), 16)
        self.assertEqual(self.graph.get_total_length(), 153)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 36)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 36)

    def test_get_next_available_seg_number(self):
        self.assertEqual(self.graph.get_next_available_seg_number(), 20)
        self.graph.remove_segments([18])
        self.assertEqual(self.graph.get_next_available_seg_number(), 20)
        self.graph.remove_segments([19])
        self.assertEqual(self.graph.get_next_available_seg_number(), 18)

    def test_get_path_sequence(self):
        p = [17, 15, 14, 13, 12, 6, 11, 7, 9, 10, 15, 14, 13, 12, 1, 2, 3, 4, 5, 11, 8, 15, 18]
        self.assertEqual(self.graph.get_path_sequence(p),
                         'GCGTCGGATTATATCGATGCGGACCAGATCTACTTTATATAGTCTACTTACGACGCAAATAGGAGTCTCGG'
                         'GGATGATCAACTTTACAGGACCAGATCTACTTTATATAGTTCTATTTTGCAACTGAATTGGCTTATCTTGC'
                         'ACGACATGATGACCCGCGACGCAATTGACTCGTTGGACCTAGAACGTCAAGAGACCCTA')

        p = [-6, -12, -13, -14, -15, -8, -11, -6, -12, -13, -14, -15, -10]
        self.assertEqual(self.graph.get_path_sequence(p),
                         'CGTAAGTAGACTATATAAAGTAGATCTGGTCCAACGAGTCAATTGCGTCGTAAGTAGACTATATAAAGTAG'
                         'ATCTGGTCCTGTAAAGTTG')

        with self.assertRaises(unicycler.assembly_graph.BadPath):
            self.graph.get_path_sequence([14, 12])

    def test_bad_overlaps(self):
        self.graph.overlap = 4
        with self.assertRaises(unicycler.assembly_graph.BadOverlaps):
            self.graph.get_path_sequence([17, 15, 14, 13, 12, 6])

    def test_merge_simple_path_1(self):
        self.graph.merge_simple_path([1, 2, 3, 4, 5])
        self.assertEqual(len(self.graph.segments), 15)
        self.assertEqual(self.graph.segments[20].forward_sequence,
                         'TTCTATTTTGCAACTGAATTGGCTTATCTTGCACGACATGATGACCCGCG')
        self.assertEqual(self.graph.segments[20].reverse_sequence,
                         'CGCGGGTCATCATGTCGTGCAAGATAAGCCAATTCAGTTGCAAAATAGAA')
        self.assertEqual(self.graph.segments[20].depth, 1.0)
        self.assertEqual(self.graph.get_total_length(), 214)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 32)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 32)

        self.graph.merge_simple_path([-12, -13, -14])
        self.assertEqual(len(self.graph.segments), 13)
        self.assertEqual(self.graph.segments[21].forward_sequence, 'CTATATAAAGTAGATCTG')
        self.assertEqual(self.graph.segments[21].reverse_sequence, 'CAGATCTACTTTATATAG')
        self.assertEqual(self.graph.segments[21].depth, 2.0)
        self.assertEqual(self.graph.get_total_length(), 214)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 28)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 28)

    def test_merge_simple_path_2(self):
        with self.assertRaises(unicycler.assembly_graph.BadPath):
            self.graph.merge_simple_path([7, 10])

    def test_merge_simple_path_3(self):
        with self.assertRaises(unicycler.assembly_graph.BadPath):
            self.graph.merge_simple_path([12, 1])

    def test_merge_all_possible(self):
        self.graph.merge_all_possible(None, 2)
        self.assertEqual(len(self.graph.segments), 11)
        self.assertEqual(self.graph.get_total_length(), 214)
        self.assertEqual(self.graph.get_total_length_no_overlaps(), 214)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 24)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 24)
        self.assertEqual(self.graph.segments[1].forward_sequence,
                         'TTCTATTTTGCAACTGAATTGGCTTATCTTGCACGACATGATGACCCGCG')
        self.assertEqual(self.graph.segments[2].forward_sequence,
                         'ATAGGAGTCTCGGGGATGATCAACTTTACA')
        self.assertEqual(self.graph.segments[7].forward_sequence, 'CAGATCTACTTTATATAG')

    def test_get_simple_path(self):
        self.assertEqual(self.graph.get_simple_path(1, None, 2), [1, 2, 3, 4, 5])
        self.assertEqual(self.graph.get_simple_path(2, None, 2), [1, 2, 3, 4, 5])
        self.assertEqual(self.graph.get_simple_path(3, None, 2), [1, 2, 3, 4, 5])
        self.assertEqual(self.graph.get_simple_path(4, None, 2), [1, 2, 3, 4, 5])
        self.assertEqual(self.graph.get_simple_path(5, None, 2), [1, 2, 3, 4, 5])
        self.assertEqual(self.graph.get_simple_path(6, None, 2), [6])
        self.assertEqual(self.graph.get_simple_path(7, None, 2), [7, 9, 10])
        self.assertEqual(self.graph.get_simple_path(8, None, 2), [8])
        self.assertEqual(self.graph.get_simple_path(9, None, 2), [7, 9, 10])
        self.assertEqual(self.graph.get_simple_path(10, None, 2), [7, 9, 10])
        self.assertEqual(self.graph.get_simple_path(11, None, 2), [11])
        self.assertEqual(self.graph.get_simple_path(12, None, 2), [14, 13, 12])
        self.assertEqual(self.graph.get_simple_path(13, None, 2), [14, 13, 12])
        self.assertEqual(self.graph.get_simple_path(14, None, 2), [14, 13, 12])
        self.assertEqual(self.graph.get_simple_path(15, None, 2), [15])
        self.assertEqual(self.graph.get_simple_path(16, None, 2), [16])
        self.assertEqual(self.graph.get_simple_path(17, None, 2), [17])
        self.assertEqual(self.graph.get_simple_path(18, None, 2), [18])
        self.assertEqual(self.graph.get_simple_path(19, None, 2), [19])

    def test_get_mean_path_depth(self):
        self.assertAlmostEqual(self.graph.get_mean_path_depth([1])[0], 1.0)
        self.assertAlmostEqual(self.graph.get_mean_path_depth([1, 2, 3, 4, 5])[0], 1.0)
        self.assertAlmostEqual(self.graph.get_mean_path_depth([1, 2, 3, 4, 5, 11])[0],
                               1.10714285714286)
        self.assertAlmostEqual(self.graph.get_mean_path_depth([14, 13, 12])[0], 2.0)
        self.assertAlmostEqual(self.graph.get_mean_path_depth([14, 13, 12, 6])[0],
                               1.64285714285714)
        self.assertAlmostEqual(self.graph.get_mean_path_depth([19])[0], 10.0)
        self.assertAlmostEqual(self.graph.get_mean_path_depth([19, 19, 19])[0], 10.0)

    def test_add_link_1(self):
        self.assertEqual((len(self.graph.forward_links[18])
                          if 18 in self.graph.forward_links else 0), 0)
        self.assertEqual((len(self.graph.reverse_links[-18])
                          if -18 in self.graph.reverse_links else 0), 0)
        self.assertEqual((len(self.graph.forward_links[-17])
                          if -17 in self.graph.forward_links else 0), 0)
        self.assertEqual((len(self.graph.reverse_links[17])
                          if 17 in self.graph.reverse_links else 0), 0)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

        self.graph.add_link(18, 17)

        self.assertEqual((len(self.graph.forward_links[18])
                          if 18 in self.graph.forward_links else 0), 1)
        self.assertEqual((len(self.graph.reverse_links[-18])
                          if -18 in self.graph.reverse_links else 0), 1)
        self.assertEqual((len(self.graph.forward_links[-17])
                          if -17 in self.graph.forward_links else 0), 1)
        self.assertEqual((len(self.graph.reverse_links[17])
                          if 17 in self.graph.reverse_links else 0), 1)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 42)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 42)

    def test_add_link_2(self):
        self.assertEqual((len(self.graph.forward_links[18])
                          if 18 in self.graph.forward_links else 0), 0)
        self.assertEqual((len(self.graph.reverse_links[-18])
                          if -18 in self.graph.reverse_links else 0), 0)
        self.assertEqual((len(self.graph.forward_links[-17])
                          if -17 in self.graph.forward_links else 0), 0)
        self.assertEqual((len(self.graph.reverse_links[17])
                          if 17 in self.graph.reverse_links else 0), 0)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 40)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 40)

        self.graph.add_link(-17, -18)

        self.assertEqual((len(self.graph.forward_links[18])
                          if 18 in self.graph.forward_links else 0), 1)
        self.assertEqual((len(self.graph.reverse_links[-18])
                          if -18 in self.graph.reverse_links else 0), 1)
        self.assertEqual((len(self.graph.forward_links[-17])
                          if -17 in self.graph.forward_links else 0), 1)
        self.assertEqual((len(self.graph.reverse_links[17])
                          if 17 in self.graph.reverse_links else 0), 1)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 42)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 42)

        self.graph.add_link(18, 17)

        self.assertEqual((len(self.graph.forward_links[18])
                          if 18 in self.graph.forward_links else 0), 1)
        self.assertEqual((len(self.graph.reverse_links[-18])
                          if -18 in self.graph.reverse_links else 0), 1)
        self.assertEqual((len(self.graph.forward_links[-17])
                          if -17 in self.graph.forward_links else 0), 1)
        self.assertEqual((len(self.graph.reverse_links[17])
                          if 17 in self.graph.reverse_links else 0), 1)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 42)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 42)

    def test_get_connected_components_and_remove_link(self):
        components = self.graph.get_connected_components()
        self.assertEqual(len(components), 3)
        self.assertEqual(sorted([len(x) for x in components]), [1, 1, 17])

        self.graph.remove_link(17, 15)

        components = self.graph.get_connected_components()
        self.assertEqual(len(components), 4)
        self.assertEqual(sorted([len(x) for x in components]), [1, 1, 1, 16])

        self.graph.remove_link(-18, -15)

        components = self.graph.get_connected_components()
        self.assertEqual(len(components), 5)
        self.assertEqual(sorted([len(x) for x in components]), [1, 1, 1, 1, 15])

    def test_seq_from_signed_seg_num(self):
        self.assertEqual(self.graph.seq_from_signed_seg_num(1), 'TTCTATTTTG')
        self.assertEqual(self.graph.seq_from_signed_seg_num(-1), 'CAAAATAGAA')
        self.assertEqual(self.graph.seq_from_signed_seg_num(15), 'GGAC')
        self.assertEqual(self.graph.seq_from_signed_seg_num(-15), 'GTCC')

    def test_get_connected_segments(self):
        self.assertEqual(sorted(self.graph.get_connected_segments(1)), [2, 12])
        self.assertEqual(sorted(self.graph.get_connected_segments(15)), [8, 10, 14, 17, 18])
        self.assertEqual(sorted(self.graph.get_connected_segments(-19)), [19])
        self.assertEqual(sorted(self.graph.get_connected_segments(16)), [])

    def test_all_segments_below_depth(self):
        self.assertTrue(self.graph.all_segments_below_depth([1, 2, 3], 1.5))
        self.assertFalse(self.graph.all_segments_below_depth([1, 2, 3, 12], 1.5))
        self.assertTrue(self.graph.all_segments_below_depth([1, 2, 3, 12], 2.5))

    def test_get_exclusive_inputs(self):
        self.assertEqual(sorted(self.graph.get_exclusive_inputs(11)), sorted([5, 6]))
        self.assertEqual(sorted(self.graph.get_exclusive_inputs(-11)), sorted([7, 8]))
        self.assertEqual(sorted(self.graph.get_exclusive_inputs(15)), sorted([8, 10, 17]))
        self.assertEqual(self.graph.get_exclusive_inputs(13), [14])
        self.assertEqual(self.graph.get_exclusive_inputs(-13), [12])
        self.assertEqual(self.graph.get_exclusive_inputs(6), [])
        self.assertEqual(self.graph.get_exclusive_inputs(-6), [])
        self.assertEqual(self.graph.get_exclusive_inputs(8), [])
        self.assertEqual(self.graph.get_exclusive_inputs(-8), [])
        self.assertEqual(self.graph.get_exclusive_inputs(1), [])
        self.assertEqual(self.graph.get_exclusive_inputs(-1), [2])
        self.assertEqual(self.graph.get_exclusive_inputs(18), [])
        self.assertEqual(self.graph.get_exclusive_inputs(-18), [])

    def test_get_exclusive_outputs(self):
        self.assertEqual(sorted(self.graph.get_exclusive_outputs(-11)), sorted([5, 6]))
        self.assertEqual(sorted(self.graph.get_exclusive_outputs(11)), sorted([7, 8]))
        self.assertEqual(sorted(self.graph.get_exclusive_outputs(-15)), sorted([8, 10, 17]))
        self.assertEqual(self.graph.get_exclusive_outputs(-13), [14])
        self.assertEqual(self.graph.get_exclusive_outputs(13), [12])
        self.assertEqual(self.graph.get_exclusive_outputs(-6), [])
        self.assertEqual(self.graph.get_exclusive_outputs(6), [])
        self.assertEqual(self.graph.get_exclusive_outputs(-8), [])
        self.assertEqual(self.graph.get_exclusive_outputs(8), [])
        self.assertEqual(self.graph.get_exclusive_outputs(-1), [])
        self.assertEqual(self.graph.get_exclusive_outputs(1), [2])
        self.assertEqual(self.graph.get_exclusive_outputs(18), [])
        self.assertEqual(self.graph.get_exclusive_outputs(-18), [])

    def test_lead_exclusively_to(self):
        self.assertTrue(self.graph.lead_exclusively_to(2, 3))
        self.assertTrue(self.graph.lead_exclusively_to(-4, -3))
        self.assertTrue(self.graph.lead_exclusively_to(13, 12))
        self.assertTrue(self.graph.lead_exclusively_to(-13, -14))
        self.assertFalse(self.graph.lead_exclusively_to(14, 12))
        self.assertFalse(self.graph.lead_exclusively_to(11, 7))
        self.assertTrue(self.graph.lead_exclusively_to(6, 11))
        self.assertFalse(self.graph.lead_exclusively_to(-11, -6))
        self.assertTrue(self.graph.lead_exclusively_to(-14, -15))
        self.assertFalse(self.graph.lead_exclusively_to(15, 14))

    def test_lead_exclusively_from(self):
        self.assertTrue(self.graph.lead_exclusively_from(3, 2))
        self.assertTrue(self.graph.lead_exclusively_from(-3, -4))
        self.assertTrue(self.graph.lead_exclusively_from(12, 13))
        self.assertTrue(self.graph.lead_exclusively_from(-14, -13))
        self.assertFalse(self.graph.lead_exclusively_from(12, 14))
        self.assertTrue(self.graph.lead_exclusively_from(7, 11))
        self.assertFalse(self.graph.lead_exclusively_from(11, 6))
        self.assertTrue(self.graph.lead_exclusively_from(-6, -11))
        self.assertFalse(self.graph.lead_exclusively_from(-15, -14))
        self.assertTrue(self.graph.lead_exclusively_from(14, 15))

    def test_dead_end_change_if_deleted(self):
        self.assertEqual(self.graph.dead_end_change_if_deleted(1), 1)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-1), 1)
        self.assertEqual(self.graph.dead_end_change_if_deleted(3), 2)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-3), 2)
        self.assertEqual(self.graph.dead_end_change_if_deleted(6), 0)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-6), 0)
        self.assertEqual(self.graph.dead_end_change_if_deleted(8), 0)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-8), 0)
        self.assertEqual(self.graph.dead_end_change_if_deleted(11), 4)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-11), 4)
        self.assertEqual(self.graph.dead_end_change_if_deleted(12), 3)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-12), 3)
        self.assertEqual(self.graph.dead_end_change_if_deleted(15), 5)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-15), 5)
        self.assertEqual(self.graph.dead_end_change_if_deleted(16), -2)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-16), -2)
        self.assertEqual(self.graph.dead_end_change_if_deleted(17), -1)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-17), -1)
        self.assertEqual(self.graph.dead_end_change_if_deleted(18), -1)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-18), -1)
        self.assertEqual(self.graph.dead_end_change_if_deleted(19), 0)
        self.assertEqual(self.graph.dead_end_change_if_deleted(-19), 0)

    def test_dead_end_change_if_path_deleted(self):
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([1]), 1)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-1]), 1)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([3]), 2)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-3]), 2)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([6]), 0)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-6]), 0)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([8]), 0)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-8]), 0)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([11]), 4)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-11]), 4)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([12]), 3)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-12]), 3)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([15]), 5)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-15]), 5)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([16]), -2)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-16]), -2)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([17]), -1)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-17]), -1)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([18]), -1)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-18]), -1)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([19]), 0)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-19]), 0)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([3, 4]), 2)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-4, -3]), 2)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([3, 4, 5]), 1)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([1, 2, 3, 4, 5]), 0)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-5, -4, -3, -2, -1]), 0)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([12, 13, 14]), 2)
        self.assertEqual(self.graph.dead_end_change_if_path_deleted([-14, -13, -12]), 2)


class TestRepairMultiwayJunction(unittest.TestCase):
    """
    Tests the AssemblyGraph.repair_multi_way_junctions function
    """

    def setUp(self):
        test_gfa = os.path.join(os.path.dirname(__file__), 'test_multiway_junction_repair.gfa')
        self.graph = unicycler.assembly_graph.AssemblyGraph(test_gfa, 0)
        unicycler.log.logger = unicycler.log.Log(log_filename=None, stdout_verbosity_level=0)

    def test_graph(self):
        self.assertEqual(len(self.graph.segments), 38)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 84)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 84)

    def test_repair_multi_way_junctions_1(self):
        self.graph.repair_multi_way_junctions()
        downstream_1 = self.graph.get_downstream_seg_nums(1)
        downstream_2 = self.graph.get_downstream_seg_nums(2)
        upstream_3 = self.graph.get_upstream_seg_nums(-3)
        upstream_4 = self.graph.get_upstream_seg_nums(-4)
        new_seg_num = downstream_1[0]
        self.assertEqual(downstream_1, [new_seg_num])
        self.assertEqual(downstream_2, [new_seg_num])
        self.assertEqual(upstream_3, [new_seg_num])
        self.assertEqual(upstream_4, [new_seg_num])
        self.assertEqual(self.graph.segments[abs(new_seg_num)].get_length(), 0)
        self.assertEqual(sorted(self.graph.get_downstream_seg_nums(new_seg_num)), [-4, -3])
        self.assertEqual(sorted(self.graph.get_upstream_seg_nums(new_seg_num)), [1, 2])

    def test_repair_multi_way_junctions_2(self):
        self.graph.repair_multi_way_junctions()
        downstream_5 = self.graph.get_downstream_seg_nums(5)
        downstream_6 = self.graph.get_downstream_seg_nums(6)
        downstream_7 = self.graph.get_downstream_seg_nums(-7)
        upstream_8 = self.graph.get_upstream_seg_nums(-8)
        upstream_9 = self.graph.get_upstream_seg_nums(-9)
        new_seg_num = downstream_5[0]
        self.assertEqual(downstream_5, [new_seg_num])
        self.assertEqual(downstream_6, [new_seg_num])
        self.assertEqual(downstream_7, [new_seg_num])
        self.assertEqual(upstream_8, [new_seg_num])
        self.assertEqual(upstream_9, [new_seg_num])
        self.assertEqual(self.graph.segments[abs(new_seg_num)].get_length(), 0)
        self.assertEqual(sorted(self.graph.get_downstream_seg_nums(new_seg_num)), [-9, -8])
        self.assertEqual(sorted(self.graph.get_upstream_seg_nums(new_seg_num)), [-7, 5, 6])

    def test_repair_multi_way_junctions_3(self):
        self.graph.repair_multi_way_junctions()
        downstream_10 = self.graph.get_downstream_seg_nums(10)
        downstream_11 = self.graph.get_downstream_seg_nums(11)
        downstream_12 = self.graph.get_downstream_seg_nums(-12)
        upstream_13 = self.graph.get_upstream_seg_nums(-13)
        upstream_14 = self.graph.get_upstream_seg_nums(-14)
        upstream_15 = self.graph.get_upstream_seg_nums(15)
        new_seg_num = downstream_10[0]
        self.assertEqual(downstream_10, [new_seg_num])
        self.assertEqual(downstream_11, [new_seg_num])
        self.assertEqual(downstream_12, [new_seg_num])
        self.assertEqual(upstream_13, [new_seg_num])
        self.assertEqual(upstream_14, [new_seg_num])
        self.assertEqual(upstream_15, [new_seg_num])
        self.assertEqual(self.graph.segments[abs(new_seg_num)].get_length(), 0)
        self.assertEqual(sorted(self.graph.get_downstream_seg_nums(new_seg_num)), [-14, -13, 15])
        self.assertEqual(sorted(self.graph.get_upstream_seg_nums(new_seg_num)), [-12, 10, 11])

    def test_repair_multi_way_junctions_4(self):
        self.graph.repair_multi_way_junctions()
        downstream_16 = self.graph.get_downstream_seg_nums(16)
        downstream_17 = self.graph.get_downstream_seg_nums(16)
        downstream_18 = self.graph.get_downstream_seg_nums(-18)
        upstream_19 = self.graph.get_upstream_seg_nums(-19)
        upstream_20 = self.graph.get_upstream_seg_nums(-20)
        new_seg_num = downstream_16[0]
        self.assertEqual(downstream_16, [new_seg_num])
        self.assertEqual(downstream_17, [new_seg_num])
        self.assertEqual(downstream_18, [-20])
        self.assertEqual(upstream_19, [new_seg_num])
        self.assertEqual(sorted(upstream_20), sorted([-18, new_seg_num]))
        self.assertEqual(self.graph.segments[abs(new_seg_num)].get_length(), 0)
        self.assertEqual(sorted(self.graph.get_downstream_seg_nums(new_seg_num)), [-20, -19])
        self.assertEqual(sorted(self.graph.get_upstream_seg_nums(new_seg_num)), [16, 17])

    def test_repair_multi_way_junctions_5(self):
        self.graph.repair_multi_way_junctions()
        downstream_21 = self.graph.get_downstream_seg_nums(21)
        downstream_22 = self.graph.get_downstream_seg_nums(22)
        downstream_23 = self.graph.get_downstream_seg_nums(-23)
        upstream_24 = self.graph.get_upstream_seg_nums(-24)
        upstream_25 = self.graph.get_upstream_seg_nums(-25)
        upstream_26 = self.graph.get_upstream_seg_nums(26)
        new_seg_num = downstream_21[0]
        self.assertEqual(downstream_21, [new_seg_num])
        self.assertEqual(sorted(downstream_22), sorted([26, new_seg_num]))
        self.assertEqual(downstream_23, [-25])
        self.assertEqual(upstream_24, [new_seg_num])
        self.assertEqual(sorted(upstream_25), sorted([-23, new_seg_num]))
        self.assertEqual(upstream_26, [22])
        self.assertEqual(self.graph.segments[abs(new_seg_num)].get_length(), 0)
        self.assertEqual(sorted(self.graph.get_downstream_seg_nums(new_seg_num)), [-25, -24])
        self.assertEqual(sorted(self.graph.get_upstream_seg_nums(new_seg_num)), [21, 22])

    def test_repair_multi_way_junctions_6(self):
        self.graph.repair_multi_way_junctions()
        downstream_27 = self.graph.get_downstream_seg_nums(27)
        downstream_28 = self.graph.get_downstream_seg_nums(28)
        downstream_29 = self.graph.get_downstream_seg_nums(-29)
        upstream_30 = self.graph.get_upstream_seg_nums(-30)
        upstream_31 = self.graph.get_upstream_seg_nums(-31)
        upstream_32 = self.graph.get_upstream_seg_nums(32)
        new_seg_num_1 = downstream_27[0]
        new_seg_num_2 = downstream_29[0]
        self.assertEqual(downstream_27, [new_seg_num_1])
        self.assertEqual(sorted(downstream_28), sorted([new_seg_num_1, new_seg_num_2]))
        self.assertEqual(downstream_29, [new_seg_num_2])
        self.assertEqual(upstream_30, [new_seg_num_1])
        self.assertEqual(sorted(upstream_31), sorted([new_seg_num_1, new_seg_num_2]))
        self.assertEqual(upstream_32, [new_seg_num_2])
        self.assertEqual(self.graph.segments[abs(new_seg_num_1)].get_length(), 0)
        self.assertEqual(sorted(self.graph.get_downstream_seg_nums(new_seg_num_1)), [-31, -30])
        self.assertEqual(sorted(self.graph.get_upstream_seg_nums(new_seg_num_1)), [27, 28])
        self.assertEqual(self.graph.segments[abs(new_seg_num_2)].get_length(), 0)
        self.assertEqual(sorted(self.graph.get_downstream_seg_nums(new_seg_num_2)), [-31, 32])
        self.assertEqual(sorted(self.graph.get_upstream_seg_nums(new_seg_num_2)), [-29, 28])


class TestRemoveZeroLengthSegments(unittest.TestCase):
    """
    Tests the AssemblyGraph.remove_zero_length_segs function
    """

    def setUp(self):
        test_gfa = os.path.join(os.path.dirname(__file__), 'test_remove_zero_length_segs.gfa')
        self.graph = unicycler.assembly_graph.AssemblyGraph(test_gfa, 0)
        unicycler.log.logger = unicycler.log.Log(log_filename=None, stdout_verbosity_level=0)

    def link_exists(self, start, end):
        return (end in self.graph.forward_links[start] and
                start in self.graph.reverse_links[end] and
                -start in self.graph.forward_links[-end] and
                -end in self.graph.reverse_links[-start])

    def test_graph(self):
        self.assertEqual(len(self.graph.segments), 44)
        self.assertEqual(sum(len(x) for x in self.graph.forward_links.values()), 114)
        self.assertEqual(sum(len(x) for x in self.graph.reverse_links.values()), 114)

    def test_remove_zero_length_segs_1(self):
        """
        Tests that segment 9638 has been removed.
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(9638 not in self.graph.segments)
        self.assertTrue(9469 in self.graph.segments)
        self.assertTrue(self.link_exists(7719, 2695))

    def test_remove_zero_length_segs_2(self):
        """
        Tests that segment 5849 has been removed.
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(5849 not in self.graph.segments)
        self.assertTrue(self.link_exists(5381, -3894))

    def test_remove_zero_length_segs_3(self):
        """
        Tests that segment 6513 has not been removed (it's a junction point).
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(6513 in self.graph.segments)
        self.assertTrue(self.link_exists(8853, 6513))
        self.assertTrue(self.link_exists(2695, 6513))
        self.assertTrue(self.link_exists(6513, 8824))
        self.assertTrue(self.link_exists(6513, 9533))

    def test_remove_zero_length_segs_4(self):
        """
        Tests that both segments 8851 and 8852 have been removed.
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(8851 not in self.graph.segments)
        self.assertTrue(8852 not in self.graph.segments)
        self.assertTrue(1435 in self.graph.segments)
        self.assertTrue(4731 in self.graph.segments)
        self.assertTrue(self.link_exists(1435, -4731))

    def test_remove_zero_length_segs_5(self):
        """
        Tests that segment 4907 has not been removed (it's a junction point and a dead end).
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(4907 in self.graph.segments)
        self.assertTrue(self.link_exists(4907, 8189))
        self.assertTrue(self.link_exists(4907, -8223))

    def test_remove_zero_length_segs_6(self):
        """
        Tests that segment 10029 has been removed (it's a dead end but not a junction).
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(10029 not in self.graph.segments)
        self.assertTrue(9867 in self.graph.segments)
        self.assertTrue(self.link_exists(9867, 318))

    def test_remove_zero_length_segs_7(self):
        """
        Tests that segment 9822 has been removed (it's on a simple path).
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(9822 not in self.graph.segments)
        self.assertTrue(self.link_exists(-1435, 7719))

    def test_remove_zero_length_segs_8(self):
        """
        Tests that segment 1 has been removed (it's isolated and unconnected).
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(1 not in self.graph.segments)

    def test_remove_zero_length_segs_9(self):
        """
        Tests that segment 8232 has been removed.
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(8232 not in self.graph.segments)
        self.assertTrue(self.link_exists(7453, 1272))
        self.assertTrue(self.link_exists(-7450, 1272))

    def test_remove_zero_length_segs_10(self):
        """
        Tests that segments 9125 and 9126 have been removed (results in a 3-way split).
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(9125 not in self.graph.segments)
        self.assertTrue(9126 not in self.graph.segments)
        self.assertTrue(self.link_exists(1272, 5430))
        self.assertTrue(self.link_exists(1272, -3106))
        self.assertTrue(self.link_exists(1272, 5458))

    def test_remove_zero_length_segs_11(self):
        """
        Tests that segments 8854 and 8855 have been removed (in a simple path).
        """
        self.graph.remove_zero_length_segs()
        self.assertTrue(8854 not in self.graph.segments)
        self.assertTrue(8855 not in self.graph.segments)
        self.assertTrue(self.link_exists(2695, 6513))


class TestExpandRepeats(unittest.TestCase):

    def setUp(self):
        test_gfa = os.path.join(os.path.dirname(__file__), 'test_expand_repeats.gfa')
        self.graph = unicycler.assembly_graph.AssemblyGraph(test_gfa, 0)
        unicycler.log.logger = unicycler.log.Log(log_filename=None, stdout_verbosity_level=0)

    def test_expand_repeats_1(self):
        """
        Tests that the common sequence in segments 3 and 4 (just a C) is moved onto segment 2.
        """
        self.assertTrue(self.graph.segments[2].forward_sequence.endswith('AGCGACTGC'))
        self.assertTrue(self.graph.segments[3].forward_sequence.startswith, 'CAGCGACTAG')
        self.assertTrue(self.graph.segments[4].forward_sequence.startswith, 'CTGACGAGCA')
        self.graph.expand_repeats()
        self.assertTrue(self.graph.segments[2].forward_sequence.endswith('AGCGACTGCC'))
        self.assertTrue(self.graph.segments[3].forward_sequence.startswith, 'AGCGACTAG')
        self.assertTrue(self.graph.segments[4].forward_sequence.startswith, 'TGACGAGCA')

    def test_expand_repeats_2(self):
        """
        Tests that the common sequence in segments 7 and 8 (GATTAGCG) is moved onto segment 6.
        """
        self.assertTrue(self.graph.segments[6].forward_sequence.endswith('TACGATTAGC'))
        self.assertTrue(self.graph.segments[7].forward_sequence.startswith, 'GATTAGCGGC')
        self.assertTrue(self.graph.segments[8].forward_sequence.startswith, 'GATTAGCGCA')
        self.graph.expand_repeats()
        self.assertTrue(self.graph.segments[6].forward_sequence.endswith('GCGATTAGCG'))
        self.assertTrue(self.graph.segments[7].forward_sequence.startswith, 'GCTTATCTT')
        self.assertTrue(self.graph.segments[8].forward_sequence.startswith, 'CACGACATG')

    def test_expand_repeats_3(self):
        """
        Tests that the common sequence on both strands of segment 1 is moved onto segment 2.
        """
        self.assertEqual(self.graph.segments[1].forward_sequence, 'ATGGGGGGAT')
        self.assertTrue(self.graph.segments[2].forward_sequence.startswith('CGCTCAGGCG'))
        self.graph.expand_repeats()
        self.assertEqual(self.graph.segments[1].forward_sequence, 'GGGGGG')
        self.assertTrue(self.graph.segments[2].forward_sequence.startswith('ATCGCTCAGGCG'))

    def test_expand_repeats_4(self):
        """
        Tests that segment 5 isn't changed, because moving its common sequence (from each strand)
        onto segment 6 would involve more trimming than the segment could handle.
        """
        self.assertEqual(self.graph.segments[5].forward_sequence, 'ATATATATAT')
        self.assertTrue(self.graph.segments[6].forward_sequence.startswith('CGCTCAGGCG'))
        self.graph.expand_repeats()
        self.assertEqual(self.graph.segments[5].forward_sequence, 'ATATATATAT')
        self.assertTrue(self.graph.segments[6].forward_sequence.startswith('CGCTCAGGCG'))

    def test_expand_repeats_5(self):
        """
        Tests that paths through the graph are unchanged by the repeat expansion.
        """
        path_1_sequence_before = self.graph.get_path_sequence([-3, -2, 1, 2, 4])
        path_2_sequence_before = self.graph.get_path_sequence([-7, -6, -5, 6, 8])
        self.graph.expand_repeats()
        path_1_sequence_after = self.graph.get_path_sequence([-3, -2, 1, 2, 4])
        path_2_sequence_after = self.graph.get_path_sequence([-7, -6, -5, 6, 8])
        self.assertEqual(path_1_sequence_before, path_1_sequence_after)
        self.assertEqual(path_2_sequence_before, path_2_sequence_after)

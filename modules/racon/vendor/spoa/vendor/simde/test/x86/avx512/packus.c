/* SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 * Copyright:
 *   2020      Evan Nemerson <evan@nemerson.com>
 *   2020      Hidayat Khan <huk2209@gmail.com>
 */

#define SIMDE_TEST_X86_AVX512_INSN packus

#include <test/x86/avx512/test-avx512.h>
#include <simde/x86/avx512/packus.h>

static int
test_simde_mm512_packus_epi16 (SIMDE_MUNIT_TEST_ARGS) {
  static const struct {
    const int16_t a[32];
    const int16_t b[32];
    const uint8_t r[64];
  } test_vec[] = {
    { { -INT16_C( 11809),  INT16_C(  3301),  INT16_C(  4381), -INT16_C( 29201), -INT16_C( 11622), -INT16_C(  1564),  INT16_C(  3475), -INT16_C(  8537),
         INT16_C(  4169), -INT16_C( 23067),  INT16_C( 13975),  INT16_C( 16305), -INT16_C( 18418),  INT16_C( 12904), -INT16_C( 19774), -INT16_C( 24123),
        -INT16_C( 21629), -INT16_C( 24403), -INT16_C( 25412),  INT16_C( 22062),  INT16_C(  4719),  INT16_C(   591), -INT16_C(  2528),  INT16_C( 27104),
        -INT16_C( 15098), -INT16_C( 25330), -INT16_C( 16389),  INT16_C(  2780),  INT16_C( 17527),  INT16_C( 14652),  INT16_C(   758),  INT16_C( 31195) },
      {  INT16_C(   136),  INT16_C(   105),  INT16_C(    72),  INT16_C(   148),  INT16_C(    14),  INT16_C(   122),  INT16_C(   119),  INT16_C(    10),
         INT16_C(   241),  INT16_C(    56),  INT16_C(   132),  INT16_C(    39),  INT16_C(   126),  INT16_C(   191),  INT16_C(    60),  INT16_C(    45),
         INT16_C(    83),  INT16_C(   233),  INT16_C(    85),  INT16_C(   245),  INT16_C(    20),  INT16_C(   103),  INT16_C(    83),  INT16_C(   199),
         INT16_C(    26),  INT16_C(   245),  INT16_C(    65),  INT16_C(   103),  INT16_C(   126),  INT16_C(    64),  INT16_C(    96),  INT16_C(   126) },
      { UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),
        UINT8_C(136), UINT8_C(105), UINT8_C( 72), UINT8_C(148), UINT8_C( 14), UINT8_C(122), UINT8_C(119), UINT8_C( 10),
           UINT8_MAX, UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),    UINT8_MAX, UINT8_C(  0), UINT8_C(  0),
        UINT8_C(241), UINT8_C( 56), UINT8_C(132), UINT8_C( 39), UINT8_C(126), UINT8_C(191), UINT8_C( 60), UINT8_C( 45),
        UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,
        UINT8_C( 83), UINT8_C(233), UINT8_C( 85), UINT8_C(245), UINT8_C( 20), UINT8_C(103), UINT8_C( 83), UINT8_C(199),
        UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,
        UINT8_C( 26), UINT8_C(245), UINT8_C( 65), UINT8_C(103), UINT8_C(126), UINT8_C( 64), UINT8_C( 96), UINT8_C(126) } },
    { {  INT16_C(  1203),  INT16_C( 20072), -INT16_C(  6822), -INT16_C( 17085), -INT16_C( 19463), -INT16_C( 31707), -INT16_C( 26873),  INT16_C( 19532),
         INT16_C( 19377),  INT16_C( 20289),  INT16_C( 24205),  INT16_C( 19895), -INT16_C(  8484), -INT16_C( 26995), -INT16_C(  1218), -INT16_C(  3819),
         INT16_C( 32000),  INT16_C( 23103), -INT16_C( 32158),  INT16_C( 23575),  INT16_C( 15414),  INT16_C( 15840),  INT16_C( 11475), -INT16_C( 31607),
        -INT16_C( 13704),  INT16_C(  1492), -INT16_C( 29911),  INT16_C(  1362), -INT16_C(  8343), -INT16_C( 22628), -INT16_C( 20005), -INT16_C(  9320) },
      {  INT16_C(   215),  INT16_C(   144),  INT16_C(    76),  INT16_C(   143),  INT16_C(   205),  INT16_C(    92),  INT16_C(    85),  INT16_C(   113),
         INT16_C(   181),  INT16_C(    73),  INT16_C(   200),  INT16_C(   169),  INT16_C(   234),  INT16_C(   131),  INT16_C(   232),  INT16_C(   201),
         INT16_C(   147),  INT16_C(    24),  INT16_C(    70),  INT16_C(   104),  INT16_C(   116),  INT16_C(    13),  INT16_C(   166),  INT16_C(   234),
         INT16_C(   245),  INT16_C(   155),  INT16_C(   129),  INT16_C(   101),  INT16_C(   148),  INT16_C(     7),  INT16_C(    70),  INT16_C(    59) },
      {    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,
        UINT8_C(215), UINT8_C(144), UINT8_C( 76), UINT8_C(143), UINT8_C(205), UINT8_C( 92), UINT8_C( 85), UINT8_C(113),
           UINT8_MAX,    UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),
        UINT8_C(181), UINT8_C( 73), UINT8_C(200), UINT8_C(169), UINT8_C(234), UINT8_C(131), UINT8_C(232), UINT8_C(201),
           UINT8_MAX,    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),
        UINT8_C(147), UINT8_C( 24), UINT8_C( 70), UINT8_C(104), UINT8_C(116), UINT8_C( 13), UINT8_C(166), UINT8_C(234),
        UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),
        UINT8_C(245), UINT8_C(155), UINT8_C(129), UINT8_C(101), UINT8_C(148), UINT8_C(  7), UINT8_C( 70), UINT8_C( 59) } },
    { {  INT16_C( 11225), -INT16_C( 18093), -INT16_C(  1167), -INT16_C( 31455), -INT16_C(  6544),  INT16_C( 14994),  INT16_C(  4236), -INT16_C(  6364),
         INT16_C( 22277), -INT16_C( 15486), -INT16_C( 14632),  INT16_C( 17448),  INT16_C(  4442), -INT16_C( 10676),  INT16_C(  7511),  INT16_C( 12561),
         INT16_C( 25928), -INT16_C( 17942),  INT16_C(  2912), -INT16_C( 12226), -INT16_C( 12046),  INT16_C( 32266),  INT16_C( 12001), -INT16_C(  6554),
        -INT16_C(  6011),  INT16_C( 24233), -INT16_C( 11601),  INT16_C(  2466), -INT16_C(  4381),  INT16_C( 15072), -INT16_C(  3829),  INT16_C( 21355) },
      {  INT16_C(    85),  INT16_C(   183),  INT16_C(    75),  INT16_C(    83),  INT16_C(   146),  INT16_C(   253),  INT16_C(    55),  INT16_C(    70),
         INT16_C(   141),  INT16_C(   207),  INT16_C(    70),  INT16_C(    66),  INT16_C(   184),  INT16_C(    64),  INT16_C(   232),  INT16_C(     0),
         INT16_C(   161),  INT16_C(   158),  INT16_C(    63),  INT16_C(     8),  INT16_C(   195),  INT16_C(   145),  INT16_C(   233),  INT16_C(    26),
         INT16_C(   123),  INT16_C(   213),  INT16_C(   194),  INT16_C(   247),  INT16_C(   147),  INT16_C(    36),  INT16_C(   203),  INT16_C(   185) },
      {    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),
        UINT8_C( 85), UINT8_C(183), UINT8_C( 75), UINT8_C( 83), UINT8_C(146), UINT8_C(253), UINT8_C( 55), UINT8_C( 70),
           UINT8_MAX, UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,
        UINT8_C(141), UINT8_C(207), UINT8_C( 70), UINT8_C( 66), UINT8_C(184), UINT8_C( 64), UINT8_C(232), UINT8_C(  0),
           UINT8_MAX, UINT8_C(  0),    UINT8_MAX, UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),
        UINT8_C(161), UINT8_C(158), UINT8_C( 63), UINT8_C(  8), UINT8_C(195), UINT8_C(145), UINT8_C(233), UINT8_C( 26),
        UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,
        UINT8_C(123), UINT8_C(213), UINT8_C(194), UINT8_C(247), UINT8_C(147), UINT8_C( 36), UINT8_C(203), UINT8_C(185) } },
    { { -INT16_C(  9108),  INT16_C( 22871),  INT16_C( 18715), -INT16_C(  5023),  INT16_C( 26380),  INT16_C(  1662),  INT16_C( 21840), -INT16_C( 14815),
         INT16_C(  2769), -INT16_C( 27749), -INT16_C( 19764),  INT16_C( 18314), -INT16_C( 16059), -INT16_C( 16021), -INT16_C( 28531), -INT16_C(  1670),
        -INT16_C( 11923), -INT16_C( 30638), -INT16_C( 19430),  INT16_C(  9845), -INT16_C(  3301),  INT16_C( 27437),  INT16_C( 20040),  INT16_C(  6449),
        -INT16_C( 13224),  INT16_C(  9644),  INT16_C( 13950), -INT16_C( 15508), -INT16_C( 10248), -INT16_C( 31356), -INT16_C(   408), -INT16_C( 10882) },
      {  INT16_C(   209),  INT16_C(   234),  INT16_C(   210),  INT16_C(   160),  INT16_C(    62),  INT16_C(    14),  INT16_C(    60),  INT16_C(   228),
         INT16_C(   212),  INT16_C(   134),  INT16_C(   117),  INT16_C(     2),  INT16_C(   206),  INT16_C(   181),  INT16_C(     6),  INT16_C(   156),
         INT16_C(   231),  INT16_C(    92),  INT16_C(   152),  INT16_C(   127),  INT16_C(     7),  INT16_C(    98),  INT16_C(   181),  INT16_C(    75),
         INT16_C(    80),  INT16_C(   147),  INT16_C(    26),  INT16_C(    18),  INT16_C(    29),  INT16_C(   181),  INT16_C(    81),  INT16_C(   250) },
      { UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),
        UINT8_C(209), UINT8_C(234), UINT8_C(210), UINT8_C(160), UINT8_C( 62), UINT8_C( 14), UINT8_C( 60), UINT8_C(228),
           UINT8_MAX, UINT8_C(  0), UINT8_C(  0),    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),
        UINT8_C(212), UINT8_C(134), UINT8_C(117), UINT8_C(  2), UINT8_C(206), UINT8_C(181), UINT8_C(  6), UINT8_C(156),
        UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,
        UINT8_C(231), UINT8_C( 92), UINT8_C(152), UINT8_C(127), UINT8_C(  7), UINT8_C( 98), UINT8_C(181), UINT8_C( 75),
        UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),
        UINT8_C( 80), UINT8_C(147), UINT8_C( 26), UINT8_C( 18), UINT8_C( 29), UINT8_C(181), UINT8_C( 81), UINT8_C(250) } },
    { { -INT16_C( 10183), -INT16_C(  3242),  INT16_C( 21104),  INT16_C( 18034),  INT16_C(    89), -INT16_C( 25432), -INT16_C(  4171),  INT16_C( 16103),
        -INT16_C( 18369),  INT16_C(  1233),  INT16_C( 26579), -INT16_C( 17641), -INT16_C(  8571), -INT16_C( 22416), -INT16_C( 15824),  INT16_C( 27043),
        -INT16_C(  1638),  INT16_C(  2908), -INT16_C( 12724), -INT16_C( 23215), -INT16_C(  1330), -INT16_C( 31934),  INT16_C( 10729),  INT16_C( 10433),
        -INT16_C( 27678), -INT16_C( 19156),  INT16_C( 17402),  INT16_C( 32624), -INT16_C(  7902),  INT16_C( 21032), -INT16_C( 13405),  INT16_C( 15803) },
      {  INT16_C(    23),  INT16_C(    16),  INT16_C(   154),  INT16_C(   180),  INT16_C(   248),  INT16_C(   125),  INT16_C(   249),  INT16_C(     3),
         INT16_C(   209),  INT16_C(   134),  INT16_C(    41),  INT16_C(    55),  INT16_C(    46),  INT16_C(   173),  INT16_C(    68),  INT16_C(   189),
         INT16_C(    51),  INT16_C(    64),  INT16_C(   132),  INT16_C(    97),  INT16_C(    44),  INT16_C(   157),  INT16_C(   131),  INT16_C(   177),
         INT16_C(    89),  INT16_C(   105),  INT16_C(    61),  INT16_C(   140),  INT16_C(    41),  INT16_C(   100),  INT16_C(    36),  INT16_C(   200) },
      { UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C( 89), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,
        UINT8_C( 23), UINT8_C( 16), UINT8_C(154), UINT8_C(180), UINT8_C(248), UINT8_C(125), UINT8_C(249), UINT8_C(  3),
        UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,
        UINT8_C(209), UINT8_C(134), UINT8_C( 41), UINT8_C( 55), UINT8_C( 46), UINT8_C(173), UINT8_C( 68), UINT8_C(189),
        UINT8_C(  0),    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,
        UINT8_C( 51), UINT8_C( 64), UINT8_C(132), UINT8_C( 97), UINT8_C( 44), UINT8_C(157), UINT8_C(131), UINT8_C(177),
        UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,
        UINT8_C( 89), UINT8_C(105), UINT8_C( 61), UINT8_C(140), UINT8_C( 41), UINT8_C(100), UINT8_C( 36), UINT8_C(200) } },
    { { -INT16_C(  4009),  INT16_C(  9225), -INT16_C(   652), -INT16_C(  3963),  INT16_C( 25385),  INT16_C( 20109),  INT16_C( 12006),  INT16_C( 15103),
         INT16_C( 14216),  INT16_C(  2724),  INT16_C( 17524), -INT16_C(  8041), -INT16_C( 12178), -INT16_C(  9404),  INT16_C( 26356),  INT16_C( 19364),
        -INT16_C( 21162), -INT16_C( 13713), -INT16_C(  2902), -INT16_C( 11078),  INT16_C( 18519),  INT16_C( 15650),  INT16_C(  8822), -INT16_C(   392),
         INT16_C(  7257), -INT16_C( 13047), -INT16_C( 24480), -INT16_C( 12627), -INT16_C(  3472),  INT16_C( 26026),  INT16_C( 20056), -INT16_C( 20560) },
      {  INT16_C(    32),  INT16_C(   165),  INT16_C(    52),  INT16_C(   108),  INT16_C(   156),  INT16_C(   242),  INT16_C(    33),  INT16_C(    23),
         INT16_C(   250),  INT16_C(   158),  INT16_C(   146),  INT16_C(    10),  INT16_C(    22),  INT16_C(   220),  INT16_C(    32),  INT16_C(    95),
         INT16_C(     5),  INT16_C(    84),  INT16_C(   126),  INT16_C(   181),  INT16_C(   106),  INT16_C(   216),  INT16_C(   152),  INT16_C(   201),
         INT16_C(   212),  INT16_C(    44),  INT16_C(   211),  INT16_C(   234),  INT16_C(   166),  INT16_C(    78),  INT16_C(    82),  INT16_C(     6) },
      { UINT8_C(  0),    UINT8_MAX, UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,
        UINT8_C( 32), UINT8_C(165), UINT8_C( 52), UINT8_C(108), UINT8_C(156), UINT8_C(242), UINT8_C( 33), UINT8_C( 23),
           UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,
        UINT8_C(250), UINT8_C(158), UINT8_C(146), UINT8_C( 10), UINT8_C( 22), UINT8_C(220), UINT8_C( 32), UINT8_C( 95),
        UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),
        UINT8_C(  5), UINT8_C( 84), UINT8_C(126), UINT8_C(181), UINT8_C(106), UINT8_C(216), UINT8_C(152), UINT8_C(201),
           UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),
        UINT8_C(212), UINT8_C( 44), UINT8_C(211), UINT8_C(234), UINT8_C(166), UINT8_C( 78), UINT8_C( 82), UINT8_C(  6) } },
    { { -INT16_C( 19625), -INT16_C( 28581),  INT16_C(  6961),  INT16_C( 19525), -INT16_C(  4987),  INT16_C(  4388),  INT16_C(  5253),  INT16_C(  6106),
         INT16_C( 16872),  INT16_C( 20036),  INT16_C( 31508), -INT16_C(   456), -INT16_C(   479), -INT16_C(  6067), -INT16_C(  1200), -INT16_C( 22546),
         INT16_C( 18862), -INT16_C(  8393),  INT16_C( 31845), -INT16_C(  5589),  INT16_C( 20585), -INT16_C(  4357), -INT16_C( 10908),  INT16_C( 19461),
         INT16_C( 18710),  INT16_C( 11162), -INT16_C( 11580), -INT16_C(  6615),  INT16_C( 30416),  INT16_C(  8654), -INT16_C( 17295),  INT16_C(  8136) },
      {  INT16_C(     0),  INT16_C(   107),  INT16_C(    42),  INT16_C(   229),  INT16_C(    81),  INT16_C(   222),  INT16_C(   217),  INT16_C(    61),
         INT16_C(   196),  INT16_C(   231),  INT16_C(   145),  INT16_C(   103),  INT16_C(   155),  INT16_C(   121),  INT16_C(    80),  INT16_C(    93),
         INT16_C(   152),  INT16_C(   205),  INT16_C(    30),  INT16_C(    61),  INT16_C(   134),  INT16_C(   149),  INT16_C(    70),  INT16_C(   129),
         INT16_C(    58),  INT16_C(   161),  INT16_C(    53),  INT16_C(   212),  INT16_C(   144),  INT16_C(    40),  INT16_C(   230),  INT16_C(    49) },
      { UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,
        UINT8_C(  0), UINT8_C(107), UINT8_C( 42), UINT8_C(229), UINT8_C( 81), UINT8_C(222), UINT8_C(217), UINT8_C( 61),
           UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),
        UINT8_C(196), UINT8_C(231), UINT8_C(145), UINT8_C(103), UINT8_C(155), UINT8_C(121), UINT8_C( 80), UINT8_C( 93),
           UINT8_MAX, UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),    UINT8_MAX, UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,
        UINT8_C(152), UINT8_C(205), UINT8_C( 30), UINT8_C( 61), UINT8_C(134), UINT8_C(149), UINT8_C( 70), UINT8_C(129),
           UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),    UINT8_MAX,
        UINT8_C( 58), UINT8_C(161), UINT8_C( 53), UINT8_C(212), UINT8_C(144), UINT8_C( 40), UINT8_C(230), UINT8_C( 49) } },
    { {  INT16_C( 20094),  INT16_C( 16894), -INT16_C( 20372), -INT16_C(  9346), -INT16_C( 26314), -INT16_C( 27280),  INT16_C( 17375), -INT16_C(  5609),
         INT16_C( 32637),  INT16_C( 18827), -INT16_C( 27723), -INT16_C( 31459),  INT16_C( 27427),  INT16_C(   941),  INT16_C( 13137), -INT16_C( 12236),
         INT16_C( 12929), -INT16_C(  4847), -INT16_C( 28701),  INT16_C(  6600),  INT16_C( 14376),  INT16_C(  2223), -INT16_C( 14725), -INT16_C(  1550),
         INT16_C( 32069), -INT16_C(  1470),  INT16_C( 24592),  INT16_C( 13184),  INT16_C( 11723),  INT16_C(  7222),  INT16_C( 27488), -INT16_C(  7700) },
      {  INT16_C(   253),  INT16_C(   128),  INT16_C(   150),  INT16_C(   181),  INT16_C(    73),  INT16_C(    74),  INT16_C(   175),  INT16_C(    84),
         INT16_C(   134),  INT16_C(    60),  INT16_C(   207),  INT16_C(   177),  INT16_C(   165),  INT16_C(    93),  INT16_C(   186),  INT16_C(   174),
         INT16_C(    13),  INT16_C(    68),  INT16_C(   200),  INT16_C(   114),  INT16_C(   182),  INT16_C(    32),  INT16_C(     0),  INT16_C(   145),
         INT16_C(   196),  INT16_C(   108),  INT16_C(    60),  INT16_C(   143),  INT16_C(   235),  INT16_C(   242),  INT16_C(    43),  INT16_C(    92) },
      {    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0), UINT8_C(  0), UINT8_C(  0),    UINT8_MAX, UINT8_C(  0),
        UINT8_C(253), UINT8_C(128), UINT8_C(150), UINT8_C(181), UINT8_C( 73), UINT8_C( 74), UINT8_C(175), UINT8_C( 84),
           UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),
        UINT8_C(134), UINT8_C( 60), UINT8_C(207), UINT8_C(177), UINT8_C(165), UINT8_C( 93), UINT8_C(186), UINT8_C(174),
           UINT8_MAX, UINT8_C(  0), UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0), UINT8_C(  0),
        UINT8_C( 13), UINT8_C( 68), UINT8_C(200), UINT8_C(114), UINT8_C(182), UINT8_C( 32), UINT8_C(  0), UINT8_C(145),
           UINT8_MAX, UINT8_C(  0),    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,    UINT8_MAX,    UINT8_MAX, UINT8_C(  0),
        UINT8_C(196), UINT8_C(108), UINT8_C( 60), UINT8_C(143), UINT8_C(235), UINT8_C(242), UINT8_C( 43), UINT8_C( 92) } }
  };

  for (size_t i = 0 ; i < (sizeof(test_vec) / sizeof(test_vec[0])) ; i++) {
    simde__m512i a = simde_mm512_loadu_epi16(test_vec[i].a);
    simde__m512i b = simde_mm512_loadu_epi16(test_vec[i].b);
    simde__m512i r = simde_mm512_packus_epi16(a, b);
    simde_test_x86_assert_equal_u8x64(r, simde_mm512_loadu_epi16(test_vec[i].r));
  }

  return 0;
}

static int
test_simde_mm512_packus_epi32 (SIMDE_MUNIT_TEST_ARGS) {
  static const struct {
    const int32_t a[16];
    const int32_t b[16];
    const uint16_t r[32];
  } test_vec[] = {
    { {  INT32_C(       32838),  INT32_C(         707),  INT32_C(       18249),  INT32_C(       43411),  INT32_C(       33031),  INT32_C(       48266),  INT32_C(       46389),  INT32_C(       30506),
         INT32_C(       19447),  INT32_C(       16717),  INT32_C(        9608),  INT32_C(       32719),  INT32_C(       16128),  INT32_C(         507),  INT32_C(        9398),  INT32_C(       24219) },
      { -INT32_C(   374762927), -INT32_C(   768936372),  INT32_C(  1090040461), -INT32_C(   926955570),  INT32_C(  1560788893), -INT32_C(  1621228982), -INT32_C(  1144842958),  INT32_C(  1192845046),
         INT32_C(  1009828848),  INT32_C(  1175411385), -INT32_C(   611907827),  INT32_C(  1805862606),  INT32_C(  1355393542), -INT32_C(   554752084),  INT32_C(   848933692),  INT32_C(    41595665) },
      { UINT16_C(32838), UINT16_C(  707), UINT16_C(18249), UINT16_C(43411), UINT16_C(    0), UINT16_C(    0),      UINT16_MAX, UINT16_C(    0),
        UINT16_C(33031), UINT16_C(48266), UINT16_C(46389), UINT16_C(30506),      UINT16_MAX, UINT16_C(    0), UINT16_C(    0),      UINT16_MAX,
        UINT16_C(19447), UINT16_C(16717), UINT16_C( 9608), UINT16_C(32719),      UINT16_MAX,      UINT16_MAX, UINT16_C(    0),      UINT16_MAX,
        UINT16_C(16128), UINT16_C(  507), UINT16_C( 9398), UINT16_C(24219),      UINT16_MAX, UINT16_C(    0),      UINT16_MAX,      UINT16_MAX } },
    { {  INT32_C(       12094),  INT32_C(        4726),  INT32_C(        8941),  INT32_C(       18830),  INT32_C(       59545),  INT32_C(       48070),  INT32_C(       19949),  INT32_C(       35151),
         INT32_C(        6072),  INT32_C(       12329),  INT32_C(       28498),  INT32_C(       58296),  INT32_C(       46795),  INT32_C(        6001),  INT32_C(        1124),  INT32_C(       55437) },
      {  INT32_C(   502220354), -INT32_C(  1605560204), -INT32_C(   703619026), -INT32_C(  1195784320), -INT32_C(   194083815),  INT32_C(   118218517),  INT32_C(    51081277),  INT32_C(  1725667620),
         INT32_C(  1401146079),  INT32_C(   301191650), -INT32_C(   236518799), -INT32_C(   475422518),  INT32_C(   970463012),  INT32_C(   876667894),  INT32_C(  2000112723), -INT32_C(   992144411) },
      { UINT16_C(12094), UINT16_C( 4726), UINT16_C( 8941), UINT16_C(18830),      UINT16_MAX, UINT16_C(    0), UINT16_C(    0), UINT16_C(    0),
        UINT16_C(59545), UINT16_C(48070), UINT16_C(19949), UINT16_C(35151), UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,      UINT16_MAX,
        UINT16_C( 6072), UINT16_C(12329), UINT16_C(28498), UINT16_C(58296),      UINT16_MAX,      UINT16_MAX, UINT16_C(    0), UINT16_C(    0),
        UINT16_C(46795), UINT16_C( 6001), UINT16_C( 1124), UINT16_C(55437),      UINT16_MAX,      UINT16_MAX,      UINT16_MAX, UINT16_C(    0) } },
    { {  INT32_C(       49175),  INT32_C(       41937),  INT32_C(       55188),  INT32_C(       31931),  INT32_C(       19637),  INT32_C(       51840),  INT32_C(       10049),  INT32_C(       43243),
         INT32_C(       45672),  INT32_C(        6997),  INT32_C(       18930),  INT32_C(       32197),  INT32_C(       47049),  INT32_C(       45697),  INT32_C(       52185),  INT32_C(       24947) },
      { -INT32_C(   736896057),  INT32_C(    99575828),  INT32_C(  2035212882), -INT32_C(   789179505), -INT32_C(    24658035),  INT32_C(   162531336), -INT32_C(  1395356982),  INT32_C(   353191758),
         INT32_C(   921313570), -INT32_C(   616834679),  INT32_C(  1263897019),  INT32_C(   689654684),  INT32_C(   321364491),  INT32_C(  1948047530), -INT32_C(  1340018590),  INT32_C(  1506160183) },
      { UINT16_C(49175), UINT16_C(41937), UINT16_C(55188), UINT16_C(31931), UINT16_C(    0),      UINT16_MAX,      UINT16_MAX, UINT16_C(    0),
        UINT16_C(19637), UINT16_C(51840), UINT16_C(10049), UINT16_C(43243), UINT16_C(    0),      UINT16_MAX, UINT16_C(    0),      UINT16_MAX,
        UINT16_C(45672), UINT16_C( 6997), UINT16_C(18930), UINT16_C(32197),      UINT16_MAX, UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,
        UINT16_C(47049), UINT16_C(45697), UINT16_C(52185), UINT16_C(24947),      UINT16_MAX,      UINT16_MAX, UINT16_C(    0),      UINT16_MAX } },
    { {  INT32_C(       55439),  INT32_C(       17844),  INT32_C(       61328),  INT32_C(       24345),  INT32_C(       63347),  INT32_C(       31339),  INT32_C(       46891),  INT32_C(        2321),
         INT32_C(       10977),  INT32_C(       48751),  INT32_C(       62382),  INT32_C(       63314),  INT32_C(        8430),  INT32_C(       54682),  INT32_C(       41100),  INT32_C(       22441) },
      { -INT32_C(  1451062722), -INT32_C(  1100484320), -INT32_C(  1682893327), -INT32_C(   460127012),  INT32_C(   503611849), -INT32_C(  1040998693),  INT32_C(   442597476),  INT32_C(  1534200349),
        -INT32_C(  1257966443), -INT32_C(   697078555),  INT32_C(  1584539009), -INT32_C(   230554327),  INT32_C(  1645299334),  INT32_C(  1210254564), -INT32_C(  1570536060),  INT32_C(   620615055) },
      { UINT16_C(55439), UINT16_C(17844), UINT16_C(61328), UINT16_C(24345), UINT16_C(    0), UINT16_C(    0), UINT16_C(    0), UINT16_C(    0),
        UINT16_C(63347), UINT16_C(31339), UINT16_C(46891), UINT16_C( 2321),      UINT16_MAX, UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,
        UINT16_C(10977), UINT16_C(48751), UINT16_C(62382), UINT16_C(63314), UINT16_C(    0), UINT16_C(    0),      UINT16_MAX, UINT16_C(    0),
        UINT16_C( 8430), UINT16_C(54682), UINT16_C(41100), UINT16_C(22441),      UINT16_MAX,      UINT16_MAX, UINT16_C(    0),      UINT16_MAX } },
    { {  INT32_C(       44761),  INT32_C(       61317),  INT32_C(       39757),  INT32_C(       33421),  INT32_C(       47844),  INT32_C(        9986),  INT32_C(        7369),  INT32_C(         833),
         INT32_C(       14258),  INT32_C(       55590),  INT32_C(       10868),  INT32_C(       55724),  INT32_C(       17299),  INT32_C(        9835),  INT32_C(       13634),  INT32_C(       50233) },
      {  INT32_C(   100395934),  INT32_C(  1356800546), -INT32_C(  1720036458), -INT32_C(   160291243),  INT32_C(  1345914295), -INT32_C(  1770609509), -INT32_C(   724846119), -INT32_C(   627506116),
         INT32_C(   299930863),  INT32_C(  1281474486),  INT32_C(  1759959826), -INT32_C(  1184999422), -INT32_C(   116746402),  INT32_C(   361726012),  INT32_C(  1995004473),  INT32_C(  1313899103) },
      { UINT16_C(44761), UINT16_C(61317), UINT16_C(39757), UINT16_C(33421),      UINT16_MAX,      UINT16_MAX, UINT16_C(    0), UINT16_C(    0),
        UINT16_C(47844), UINT16_C( 9986), UINT16_C( 7369), UINT16_C(  833),      UINT16_MAX, UINT16_C(    0), UINT16_C(    0), UINT16_C(    0),
        UINT16_C(14258), UINT16_C(55590), UINT16_C(10868), UINT16_C(55724),      UINT16_MAX,      UINT16_MAX,      UINT16_MAX, UINT16_C(    0),
        UINT16_C(17299), UINT16_C( 9835), UINT16_C(13634), UINT16_C(50233), UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,      UINT16_MAX } },
    { {  INT32_C(       52576),  INT32_C(         538),  INT32_C(       40810),  INT32_C(       46680),  INT32_C(       39855),  INT32_C(        7344),  INT32_C(       63634),  INT32_C(       13126),
         INT32_C(         769),  INT32_C(        1285),  INT32_C(       29604),  INT32_C(       38442),  INT32_C(       16946),  INT32_C(       45406),  INT32_C(       39337),  INT32_C(       59340) },
      { -INT32_C(    18166378),  INT32_C(    50589672), -INT32_C(  1787320482),  INT32_C(    36479395), -INT32_C(  1841013126), -INT32_C(  1119640768),  INT32_C(  1750527124),  INT32_C(  1917788892),
        -INT32_C(   663733520), -INT32_C(  1998818519), -INT32_C(  1122151654),  INT32_C(  1858095604), -INT32_C(   402586457),  INT32_C(  1000686759),  INT32_C(   228850481),  INT32_C(   226489117) },
      { UINT16_C(52576), UINT16_C(  538), UINT16_C(40810), UINT16_C(46680), UINT16_C(    0),      UINT16_MAX, UINT16_C(    0),      UINT16_MAX,
        UINT16_C(39855), UINT16_C( 7344), UINT16_C(63634), UINT16_C(13126), UINT16_C(    0), UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,
        UINT16_C(  769), UINT16_C( 1285), UINT16_C(29604), UINT16_C(38442), UINT16_C(    0), UINT16_C(    0), UINT16_C(    0),      UINT16_MAX,
        UINT16_C(16946), UINT16_C(45406), UINT16_C(39337), UINT16_C(59340), UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,      UINT16_MAX } },
    { {  INT32_C(       22246),  INT32_C(       31966),  INT32_C(        2361),  INT32_C(       60791),  INT32_C(       42453),  INT32_C(       61153),  INT32_C(       37627),  INT32_C(       42144),
         INT32_C(       52219),  INT32_C(       23879),  INT32_C(        7014),  INT32_C(       30728),  INT32_C(        4893),  INT32_C(       52225),  INT32_C(       64094),  INT32_C(       57247) },
      { -INT32_C(   861234556),  INT32_C(  1227485555), -INT32_C(   345731215), -INT32_C(  1016894355), -INT32_C(  1596554935),  INT32_C(    40687487),  INT32_C(  1241369299),  INT32_C(  1294507209),
        -INT32_C(  1457860042),  INT32_C(   888292291),  INT32_C(  1075861203),  INT32_C(   184779714), -INT32_C(  2069112572), -INT32_C(  2088364112), -INT32_C(  1412660254),  INT32_C(  1442378783) },
      { UINT16_C(22246), UINT16_C(31966), UINT16_C( 2361), UINT16_C(60791), UINT16_C(    0),      UINT16_MAX, UINT16_C(    0), UINT16_C(    0),
        UINT16_C(42453), UINT16_C(61153), UINT16_C(37627), UINT16_C(42144), UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,      UINT16_MAX,
        UINT16_C(52219), UINT16_C(23879), UINT16_C( 7014), UINT16_C(30728), UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,      UINT16_MAX,
        UINT16_C( 4893), UINT16_C(52225), UINT16_C(64094), UINT16_C(57247), UINT16_C(    0), UINT16_C(    0), UINT16_C(    0),      UINT16_MAX } },
    { {  INT32_C(       35327),  INT32_C(       10685),  INT32_C(        2665),  INT32_C(       25878),  INT32_C(       62953),  INT32_C(       47992),  INT32_C(        4966),  INT32_C(       65128),
         INT32_C(       51079),  INT32_C(       41456),  INT32_C(       33707),  INT32_C(        2792),  INT32_C(       23807),  INT32_C(       13591),  INT32_C(       62280),  INT32_C(       19697) },
      {  INT32_C(  1897101336), -INT32_C(   569244740),  INT32_C(   560053852),  INT32_C(    36391551),  INT32_C(  1583229468),  INT32_C(  1553167777), -INT32_C(   833626894), -INT32_C(  1525006195),
         INT32_C(  1964453560), -INT32_C(  1907152591),  INT32_C(  1739568615),  INT32_C(   459922431), -INT32_C(  1485191163),  INT32_C(   805506109),  INT32_C(  1979601896),  INT32_C(  1276844179) },
      { UINT16_C(35327), UINT16_C(10685), UINT16_C( 2665), UINT16_C(25878),      UINT16_MAX, UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,
        UINT16_C(62953), UINT16_C(47992), UINT16_C( 4966), UINT16_C(65128),      UINT16_MAX,      UINT16_MAX, UINT16_C(    0), UINT16_C(    0),
        UINT16_C(51079), UINT16_C(41456), UINT16_C(33707), UINT16_C( 2792),      UINT16_MAX, UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,
        UINT16_C(23807), UINT16_C(13591), UINT16_C(62280), UINT16_C(19697), UINT16_C(    0),      UINT16_MAX,      UINT16_MAX,      UINT16_MAX } }
  };

  for (size_t i = 0 ; i < (sizeof(test_vec) / sizeof(test_vec[0])) ; i++) {
    simde__m512i a = simde_mm512_loadu_epi32(test_vec[i].a);
    simde__m512i b = simde_mm512_loadu_epi32(test_vec[i].b);
    simde__m512i r = simde_mm512_packus_epi32(a, b);
    simde_test_x86_assert_equal_u16x32(r, simde_mm512_loadu_epi32(test_vec[i].r));
  }

  return 0;
}

SIMDE_TEST_FUNC_LIST_BEGIN
  SIMDE_TEST_FUNC_LIST_ENTRY(mm512_packus_epi16)
  SIMDE_TEST_FUNC_LIST_ENTRY(mm512_packus_epi32)
SIMDE_TEST_FUNC_LIST_END

#include <test/x86/avx512/test-avx512-footer.h>

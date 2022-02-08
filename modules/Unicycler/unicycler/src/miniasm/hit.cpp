#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <assert.h>
#include <iostream>
#include <fstream>
#include <set>
#include <limits>

#pragma GCC diagnostic ignored "-Wpragmas"
#pragma GCC diagnostic ignored "-Wunknown-warning-option"
#pragma GCC diagnostic ignored "-Wvla"
#pragma GCC diagnostic ignored "-Wvla-extension"
#pragma GCC diagnostic ignored "-Wmaybe-uninitialized"

#include "miniasm/sdict.h"
#include "miniasm/paf.h"
#include "miniasm/kvec.h"
#include "miniasm/sys.h"
#include "miniasm/miniasm.h"
#include "miniasm/ksort.h"

#define ma_hit_key(a) ((a).qns)
KRADIX_SORT_INIT(hit, ma_hit_t, ma_hit_key, 8)

KSORT_INIT_GENERIC(uint32_t)

using namespace std;

typedef kvec_t(uint32_t) uint32_v;

void ma_hit_sort(size_t n, ma_hit_t *a)
{
    radix_sort_hit(a, a + n);
}

void ma_hit_mark_unused(sdict_t *read_dict, size_t n, const ma_hit_t *a)
{
    size_t i;
    for (i = 0; i < read_dict->n_seq; ++i)
        read_dict->seq[i].aux = 0;
    for (i = 0; i < n; ++i)
        read_dict->seq[a[i].qns>>32].aux = read_dict->seq[a[i].tn].aux = 1;
    for (i = 0; i < read_dict->n_seq; ++i) {
        sd_seq_t *s = &read_dict->seq[i];
        if (!s->aux) s->del = 1;
        else s->aux = 0;
    }
}

sdict_t *prefilter_contained_reads(const char *fn, int min_span, int min_match, int max_hang, float int_frac)
{
    paf_file_t *fp;
    paf_rec_t r;
    sdict_t *d;

    fp = paf_open(fn);
    d = init_seq_dict();
    while (paf_read(fp, &r) >= 0) {
        int l5, l3;
        if (r.qe - r.qs < min_span || r.te - r.ts < min_span || r.ml < min_match) continue;
        l5 = r.rev? r.tl - r.te : r.ts;
        l3 = r.rev? r.ts : r.tl - r.te;
        if (r.ql>>1 > r.tl) {
            if (l5 > max_hang>>2 || l3 > max_hang>>2 || r.te - r.ts < r.tl * int_frac) continue; // internal match
            if ((int)r.qs - l5 > max_hang<<1 && (int)(r.ql - r.qe) - l3 > max_hang<<1)
                sd_put(d, r.tn, r.tl);
        } else if (r.ql < r.tl>>1) {
            if (r.qs > max_hang>>2 || r.ql - r.qe > max_hang>>2 || r.qe - r.qs < r.ql * int_frac) continue; // internal
            if (l5 - (int)r.qs > max_hang<<1 && l3 - (int)(r.ql - r.qe) > max_hang<<1)
                sd_put(d, r.qn, r.ql);
        }
    }
    paf_close(fp);
    std::cerr << "[M::" << __func__ << "::" << sys_timestamp() << "] dropped " << d->n_seq << " contained reads\n";
    return d;
}

ma_hit_t *read_hits_file(const char *fn, int min_span, int min_match, sdict_t *read_dict, size_t *n, int bi_dir, const sdict_t *excl)
{
    paf_file_t *fp;
    paf_rec_t r;
    ma_hit_v h = {0,0,0};
    size_t i, tot = 0, tot_len = 0;

    fp = paf_open(fn);
    while (paf_read(fp, &r) >= 0) {
        ma_hit_t *p;
        ++tot;
        if (r.qe - r.qs < min_span || r.te - r.ts < min_span || r.ml < min_match) continue;
        if (excl && (sd_get(excl, r.qn) >= 0 || sd_get(excl, r.tn) >= 0)) continue;
        kv_pushp(ma_hit_t, h, &p);
        p->qns = (uint64_t)sd_put(read_dict, r.qn, r.ql)<<32 | r.qs;
        p->qe = r.qe;
        p->tn = sd_put(read_dict, r.tn, r.tl);
        p->ts = r.ts, p->te = r.te, p->rev = r.rev, p->ml = r.ml, p->bl = r.bl;
        if (bi_dir && p->qns>>32 != p->tn) {
            kv_pushp(ma_hit_t, h, &p);
            p->qns = (uint64_t)sd_put(read_dict, r.tn, r.tl)<<32 | r.ts;
            p->qe = r.te;
            p->tn = sd_put(read_dict, r.qn, r.ql);
            p->ts = r.qs, p->te = r.qe, p->rev = r.rev, p->ml = r.ml, p->bl = r.bl;
        }
    }
    paf_close(fp);
    for (i = 0; i < read_dict->n_seq; ++i)
        tot_len += read_dict->seq[i].len;
    std::cerr << "[M::" << __func__ << "::" << sys_timestamp() << "] read " << tot << " hits; stored " << h.n << " hits and " << read_dict->n_seq << " sequences (" << tot_len << " bp)\n";
    ma_hit_sort(h.n, h.a);
    *n = h.n;
    return h.a;
}


string get_read_name(const sdict_t *read_dict, int id) {
    return read_dict->seq[id].name;
}

bool is_read_illumina_contig(const sdict_t *read_dict, int id) {
    return get_read_name(read_dict, id).find("CONTIG_") == 0;
}

ma_sub_t *filter_reads_using_depth(int min_dp, float min_iden, int end_clip, size_t n, const ma_hit_t *a, const sdict_t *read_dict)
{
    size_t num_reads = read_dict->n_seq;

    size_t j, n_remained = 0;
    kvec_t(uint32_t) b = {0,0,0};
    ma_sub_t *subreads = 0;

    subreads = (ma_sub_t*)calloc(num_reads, sizeof(ma_sub_t));
    for (size_t i = 1, last = 0; i <= n; ++i) {

        // We've come to a new query sequence.
        if (i == n || a[i].qns>>32 != a[i-1].qns>>32) {
            size_t start, end;
            int query_i = int(a[i-1].qns>>32);

            ma_sub_t max, max2;
            kv_resize(uint32_t, b, i - last);
            b.n = 0;

            // Collect all starts and ends.
            for (j = last; j < i; ++j) {
                uint32_t qs, qe;
                int target_i = a[j].tn;

                // skip self match
                if (target_i == query_i || a[j].ml < a[j].bl * min_iden)
                    continue;

                qs = (uint32_t)a[j].qns + end_clip;
                qe = a[j].qe - end_clip;

                if (qe > qs) {
                    kv_push(uint32_t, b, qs<<1);
                    kv_push(uint32_t, b, qe<<1|1);

                    // If the query is a read and the target is an Illumina contig, then we add
                    // the start/end coordinates two more times. This is because Illumina contigs
                    // carry a lot of weight and should count more than alignments to other reads.
                    // E.g. one Illumina contig alignment is enough to get a read over a min depth
                    // of 3.
                    if (!is_read_illumina_contig(read_dict, query_i) && is_read_illumina_contig(read_dict, target_i)) {
                        kv_push(uint32_t, b, qs<<1);
                        kv_push(uint32_t, b, qe<<1|1);
                        kv_push(uint32_t, b, qs<<1);
                        kv_push(uint32_t, b, qe<<1|1);
                    }
                }
            }

            // If the read is an Illumina contig, then we may not have alignments to the middle of
            // the read. So we don't do the normal miniasm stuff but instead only clip off unaligned
            // parts from its ends.
            if (is_read_illumina_contig(read_dict, query_i)) {

                // If the Illumina contig has no alignments, then we just include the whole thing.
                if (b.n == 0) {
                    subreads[query_i].s = 0;
                    subreads[query_i].e = read_dict->seq[query_i].len;
                }
                // If the read has alignments, we use those to clip off unaligned parts.
                else {
                    uint32_t min_start = numeric_limits<uint32_t>::max();
                    uint32_t max_end = 0;
                    for (j = 0; j < b.n; ++j) {
                        if (b.a[j] & 1) {  // is an end position
                            uint32_t read_end = b.a[j] >> 1;
                            max_end = std::max(read_end, max_end);
                        } else {  // is a start position
                            uint32_t read_start = b.a[j] >> 1;
                            min_start = std::min(read_start, min_start);
                        }
                    }
                    subreads[query_i].s = min_start - end_clip;
                    subreads[query_i].e = max_end + end_clip;
                }
                subreads[query_i].del = 0;
                ++n_remained;
            }

            // If the read isn't a contig (i.e. it's a normal read) then we do the standard miniasm
            // behaviour: clip the read to the best depth region.
            else {
                ks_introsort_uint32_t(b.n, b.a);
                max.s = max.e = max.del = max2.s = max2.e = max2.del = 0;
                int dp;
                for (j = 0, dp = 0; j < b.n; ++j) {
                    int old_dp = dp;
                    if (b.a[j]&1)
                        --dp;
                    else
                        ++dp;

                    // If we've just exceeded the minimum depth, set the start.
                    if (old_dp < min_dp && dp >= min_dp) {
                        start = b.a[j]>>1;

                    // If we've just dropped below the minimum depth, set the end.
                    } else if (old_dp >= min_dp && dp < min_dp) {
                        end = b.a[j]>>1;
                        int len = int(end - start);

                        // Is this depth region a new best?
                        if (len > max.e - max.s) {
                            max2 = max;
                            max.s = u_int32_t(start);
                            max.e = u_int32_t(end);
                        }
                        // Is it a new second-best region? Not sure why we care...
                        else if (len > max2.e - max2.s) {
                            max2.s = u_int32_t(start);
                            max2.e = u_int32_t(end);
                        }
                    }
                }
                if (max.e - max.s > 0) {
                    assert(query_i < num_reads);
                    subreads[query_i].s = max.s - end_clip;
                    subreads[query_i].e = max.e + end_clip;
                    subreads[query_i].del = 0;
                    ++n_remained;
                }
                else
                    subreads[query_i].del = 1;
            }


            last = i;
        }
    }
    free(b.a);
    std::cerr << "[M::" << __func__ << "::" << sys_timestamp() << "] " << n_remained << " query sequences remain after sub\n";
    return subreads;
}

size_t filter_hits_using_span(const ma_sub_t *subreads, int min_span, size_t n, ma_hit_t *a)
{
    size_t i, m;
    for (i = m = 0; i < n; ++i) {
        ma_hit_t *p = &a[i];
        const ma_sub_t *rq = &subreads[p->qns>>32], *rt = &subreads[p->tn];
        int qs, qe, ts, te;
        if (rq->del || rt->del) continue;
        if (p->rev) {
            qs = p->te < rt->e? (uint32_t)p->qns : (uint32_t)p->qns + (p->te - rt->e);
            qe = p->ts > rt->s? p->qe : p->qe - (rt->s - p->ts);
            ts = p->qe < rq->e? p->ts : p->ts + (p->qe - rq->e);
            te = (uint32_t)p->qns > rq->s? p->te : p->te - (rq->s - (uint32_t)p->qns);
        } else {
            qs = p->ts > rt->s? (uint32_t)p->qns : (uint32_t)p->qns + (rt->s - p->ts);
            qe = p->te < rt->e? p->qe : p->qe - (p->te - rt->e);
            ts = (uint32_t)p->qns > rq->s? p->ts : p->ts + (rq->s - (uint32_t)p->qns);
            te = p->qe < rq->e? p->te : p->te - (p->qe - rq->e);
        }
        qs = (qs > rq->s? qs : rq->s) - rq->s;
        qe = (qe < rq->e? qe : rq->e) - rq->s;
        ts = (ts > rt->s? ts : rt->s) - rt->s;
        te = (te < rt->e? te : rt->e) - rt->s;
        if (qe - qs >= min_span && te - ts >= min_span) {
            double r = (double)((qe - qs) + (te - ts)) / ((p->qe - (uint32_t)p->qns) + (p->te - p->ts));
            p->bl = (int)(p->bl * r + .499);
            p->ml = (int)(p->ml * r + .499);
            p->qns = p->qns>>32<<32 | qs, p->qe = qe, p->ts = ts, p->te = te;
            a[m++] = *p;
        }
    }
    std::cerr << "[M::" << __func__ << "::" << sys_timestamp() << "] " << m << " hits remain after cut\n";
    return m;
}

size_t filter_hits_using_overhang(const ma_sub_t *subreads, int max_hang, int min_ovlp, size_t n, ma_hit_t *a, float *cov)
{
    size_t i, m;
    asg_arc_t t;
    uint64_t tot_dp = 0, tot_len = 0;
    for (i = m = 0; i < n; ++i) {
        ma_hit_t *h = &a[i];
        const ma_sub_t *sq = &subreads[h->qns>>32], *st = &subreads[h->tn];
        int r;
        if (sq->del || st->del) continue;
        r = ma_hit2arc(h, sq->e - sq->s, st->e - st->s, max_hang, .5, min_ovlp, &t);
        if (r >= 0 || r == MA_HT_QCONT || r == MA_HT_TCONT)
            a[m++] = *h, tot_dp += r >= 0? r : r == MA_HT_QCONT? sq->e - sq->s : st->e - st->s;
    }
    for (i = 1; i <= m; ++i)
        if (i == m || a[i].qns>>32 != a[i-1].qns>>32)
            tot_len += subreads[a[i-1].qns>>32].e - subreads[a[i-1].qns>>32].s;
    *cov = (double)tot_dp / tot_len;
    std::cerr << "[M::" << __func__ << "::" << sys_timestamp() << "] " << m << " hits remain after filtering; crude coverage after filtering: " << *cov << "\n";
    return m;
}

void merge_subreads(size_t n_sub, ma_sub_t *a, const ma_sub_t *b)
{
    size_t i;
    for (i = 0; i < n_sub; ++i)
        a[i].e = a[i].s + b[i].e, a[i].s += b[i].s;
}

void save_read_names(size_t n, const ma_hit_t *a, const sdict_t *read_dict, ma_sub_t *subreads, string all_read_list)
{
    set<string> all_read_names;
    size_t i, start = 0;
    for (i = 1; i <= n; ++i) {
        if (i == n || a[i].qns>>32 != a[start].qns>>32) {
            int id = int(a[start].qns >> 32);

            string read_name = get_read_name(read_dict, id);
            string full_read_name = read_name + ":";
            full_read_name += to_string(subreads[id].s + 1);
            full_read_name += '-';
            full_read_name += to_string(subreads[id].e);
            all_read_names.insert(full_read_name);

            start = i;
        }
    }

    ofstream all_list_file;
    all_list_file.open(all_read_list);
    for (set<string>::iterator it = all_read_names.begin(); it != all_read_names.end(); ++it)
        all_list_file << *it << "\n";
    all_list_file.close();
}

size_t remove_contained_reads(int max_hang, float int_frac, int min_ovlp, sdict_t *read_dict, ma_sub_t *subreads, size_t n, ma_hit_t *a, string contained_read_list)
{
    set<string> contained_read_names;

    int32_t *map, r;
    size_t i, m, old_n_seq = read_dict->n_seq;
    asg_arc_t t;
    for (i = m = 0; i < n; ++i) {
        ma_hit_t *h = &a[i];

        int query_i = int(h->qns>>32);
        int target_i = h->tn;
        ma_sub_t *query_subread = &subreads[query_i];
        ma_sub_t *target_subread = &subreads[target_i];

        r = ma_hit2arc(h, query_subread->e - query_subread->s, target_subread->e - target_subread->s, max_hang, int_frac, min_ovlp, &t);

        if (r == MA_HT_QCONT) {  // If the query is contained in the target
            query_subread->del = 1;
            contained_read_names.insert(get_read_name(read_dict, query_i));
        }
        else if (r == MA_HT_TCONT) {  // If the target is contained in the query
            target_subread->del = 1;
            contained_read_names.insert(get_read_name(read_dict, target_i));
        }
    }

    for (i = 0; i < read_dict->n_seq; ++i) {

        // Illumina contigs can't be deleted!
        if (is_read_illumina_contig(read_dict, i))
            subreads[i].del = 0;

        if (subreads[i].del)
            read_dict->seq[i].del = 1;
    }

    ma_hit_mark_unused(read_dict, n, a);
    map = sd_squeeze(read_dict);
    for (i = 0; i < old_n_seq; ++i) {
        if (map[i] >= 0)
            subreads[map[i]] = subreads[i];
    }
    for (i = m = 0; i < n; ++i) {
        ma_hit_t *h = &a[i];
        int32_t qn = map[h->qns>>32], tn = map[h->tn];
        if (qn >= 0 && tn >= 0) {
            a[i].qns = (uint64_t)qn<<32 | (uint32_t)a[i].qns;
            a[i].tn = tn;
            a[m++] = a[i];
        }
    }
    free(map);
    std::cerr << "[M::" << __func__ << "::" << sys_timestamp() << "] " << read_dict->n_seq << " sequences and " << m << " hits remain after containment removal\n";

    ofstream list_file;
    list_file.open(contained_read_list);
    for (set<string>::iterator it = contained_read_names.begin(); it != contained_read_names.end(); ++it)
        list_file << *it << "\n";
    list_file.close();

    return m;
}

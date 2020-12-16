# -*- coding: utf-8 -*-
# Copyright (c) 2018, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.


# these lines here used to see how many publications authors have
# I used this to determine which author would be a good test try for certain functions

# import collections
# from sne_the_mergers import ScholarlySearchEngine
# my_sse = ScholarlySearchEngine("metadata_sample.csv")
# authors = list()
# for my_dict in my_sse.data:
#     authors.extend(my_dict['authors'].split('; '))
# print(collections.Counter(authors))


from sne_the_mergers import ScholarlyNetworkEngine
import time

# these values are used to calculated computation times
cit_start=cit_end=co_start=co_end=aut_co_start=aut_co_end=aut_dis_start=aut_dis_end=rank_start=rank_end=0
cycles_start=cycles_end=cit_count_start=cit_count_end=h_index_start=h_index_end=START=END=0

# if you want to average the computation times increase the average number:)
avg = 100
for i in range(avg):

    START += time.perf_counter()
    my_sne = ScholarlyNetworkEngine("metadata_sample.csv", "citations_sample.csv")

    cit_start += time.perf_counter()
    citation = my_sne.citation_graph()
    cit_end += time.perf_counter()

    co_start += time.perf_counter()
    coupling = my_sne.coupling("10.7717/peerj-cs.112", "10.7717/peerj-cs.147")
    co_end += time.perf_counter()

    aut_co_start += time.perf_counter()
    aut_co = my_sne.aut_coupling('Arfon M., Smith', 'Albert, Krewinkel')
    aut_co_end += time.perf_counter()

    aut_dis_start += time.perf_counter()
    aut_dis = my_sne.aut_distance('Michel, Dumontier')
    aut_dis_end += time.perf_counter()

    cycles_start += time.perf_counter()
    cycles = my_sne.find_cycles()
    cycles_end += time.perf_counter()

    cit_count_start += time.perf_counter()
    cit_count = my_sne.cit_count_year('Michel, Dumontier', 2012)
    cit_count_end += time.perf_counter()

    h_index_start += time.perf_counter()
    h_index = my_sne.jou_h_index('PeerJ Computer Science')
    h_index_end += time.perf_counter()

    rank_start += time.perf_counter()
    rank = my_sne.category_rank(years=None)
    rank_end += time.perf_counter()
    END += time.perf_counter()

# printing results and computation times in [ms]

print('')
print('Citation graph', len(citation.nodes()), 'nodes:',citation.nodes(data=True))
print('Citation graph', len(citation.edges()),'edges:', citation.edges())
print('DOI coupling strength:', coupling)
print('Author coupling strength:', aut_co)
print('Author distance', len(aut_dis.nodes()), 'nodes:', aut_dis.nodes(data=True))
print('Author distance', len(aut_dis.edges()), 'edges:', aut_dis.edges(data=True))
print('Cycles:', cycles)
print('Citation count:', cit_count)
print('h index:', h_index)
print('Category rank:', rank)
print('')
print('Citation time:', round((cit_end-cit_start)*1000/avg,4), '[ms]')
print('Coupling time:', round((co_end-co_start)*1000/avg,4), '[ms]')
print('Author coupling time:', round((aut_co_end-aut_co_start)*1000/avg,4), '[ms]')
print('Author distance time:', round((aut_dis_end-aut_dis_start)*1000/avg,4), '[ms]')
print('Find cycles:', round((cycles_end-cycles_start)*1000/avg,4), '[ms]')
print('Cit Count:', round((cit_count_end-cit_count_start)*1000/avg,4), '[ms]')
print('h index:', round((h_index_end-h_index_start)*1000/avg,4), '[ms]')
print('Category ank:', round((rank_end-rank_start)*1000/avg,4), '[ms]')
print('Total time:', round((END-START)*1000/avg,4), '[ms]')











# my_sne.<method> ...
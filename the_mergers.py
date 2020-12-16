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
#
#
# This file is just a stub of the particular module that every group should
# implement for making its project work. In fact, all these functions returns None,
# which is not compliant at all with the specifications that have been provided at
# https://comp-think.github.io/2018-2019/slides/14%20-%20Project.html

from csv import DictReader
import networkx
import collections
import datetime
import itertools


def process_citation_data(citation_file_path):
    with open(citation_file_path, 'r', encoding='utf-8') as csvfile:
        reader = DictReader(csvfile)
        data = [dict(x) for x in reader]
        return data

# using a quick search instead of the sse.search that searches for a query in a col.
# since we only need a function that searched the doi in the doi column, this search is faster
# it returns the dict in sse.data when the doi's match
def quick_search(sse,doi):
    for my_dict in sse.data:
        if doi == my_dict['doi']:
            return my_dict

# returns a directed graph containing all the papers that take part in citation where the nodes are the papers
# and the edges are the citation direction between the nodes (citing node --> cited node)
def do_citation_graph(data, sse):
    citation_graph = networkx.DiGraph()                         # initiate directed graph
    for my_dict in data:                                        # iterating over dicts in data
        if len(my_dict['known refs']) > 0:                      # check if there are any refs in known refs
            for ref in my_dict['known refs'].split('; '):       # if so, iterate over the refs in known refs using split function
                for node in [ref, my_dict['doi']]:              # iterate over citing doi and cited doi's
                    if node not in citation_graph.nodes():      # check if doi is not yet a node in the citation graph
                        citation_graph.add_node(node, identifier=sse.pretty_print([quick_search(sse,node)]))                #if not, add it with as identifier the sse.pretty print
                citation_graph.add_edge(my_dict['doi'], ref)    # add directed edge from citing doi to cited doi
    return citation_graph


def do_coupling(data, sse, doi_1, doi_2):
    doi_1_refs = []                                                     # initiate two lists
    doi_2_refs = []
    for my_dict in data:                                                # iterate over dicts in data
        if doi_1 == my_dict['doi']:                                     # if doi1 matches with the doi in the dict
            doi_1_refs.extend(my_dict['known refs'].split('; '))        # doi1 refs list is extend with the known refs
        if doi_2 == my_dict['doi']:                                     # if doi1 matches with the doi in the dict
            doi_2_refs.extend(my_dict['known refs'].split('; '))        # doi1 refs list is extend with the known refs
    return len([item for item in doi_1_refs if item in doi_2_refs])     # return length of the list with items that are both in doi1 and doi2 refs


def do_aut_coupling(data, sse, aut_1, aut_2):
    ubow_aut_1 = []             # uniqye body of work author 1
    ubow_aut_2 = []             # unique body of work author 2
    publish1 = False            # initializing boolean1 and 2 for checking if author 1 and 2 published at least 1 paper
    publish2 = False
    aut_couple = 0              # start value of author coupling strength
    for my_dict in sse.data:                                    # iterating over dictionaries in sse.data
        authors = my_dict['authors'].split('; ')                # splitting the author value in separate authors
        if aut_1 in authors and aut_2 not in authors:           # if author 1 in, but author 2 not in authors
            publish1 = True                                     # author 1 has published at least 1 paper
            ubow_aut_1.append(my_dict['doi'])                   # add the paper to author 1's unique body of work
        if aut_2 in authors and aut_1 not in authors:           # if author 2 in, but author 1 not in authors
            publish2 = True                                     # author 2 has published at least 1 paper
            ubow_aut_2.append(my_dict['doi'])                   # add the paper to author 1's unique body of work
    if (publish1 and publish2) is False:                        # if either one of the authors has not published a paper
        return aut_couple                                       # returning author coupling will return 0
    for doi_1 in ubow_aut_1:                                    # otherwise iterate over author 1's unique body of work
        for doi_2 in ubow_aut_2:                                # iterate over author 1's unique body of work
            aut_couple += do_coupling(data, sse, doi_1, doi_2)  # add doi coupling strength to author coupling strength
    return aut_couple                                           # return author coupling strength


def do_aut_distance(data, sse, aut):
    aut_graph = networkx.Graph()                # initializing non-directional graph
    node_queue = collections.deque()            # initializing a node queue
    aut_graph.add_node(aut, distance=0)         # adding the author node to the graph with as attribute distance = 0
    node_queue.append(aut)                      # append author node to node queue
    checked_papers = set()                      # initialize an empty set that will keep track of the checked papers
    while len(node_queue) > 0:                  # run while there is still nodes in the node queue
        node_aut = node_queue.pop()             # the current node author is the first value in the queue
        for my_dict in sse.data:                            # iterating over dictionaries in sse.data
            authors = my_dict['authors'].split('; ')        # split authors value into separate authors
            if node_aut in authors and my_dict['doi'] not in checked_papers:    # checking if the current node author is in the section authors of the current dictionary
                checked_papers.add(my_dict['doi'])          # if so, add the doi to checked papers and,
                for co_aut in authors:                      # iterate over all the co-authors of the paper
                    if co_aut not in aut_graph.nodes():     # if the author does not have a node yet,
                        aut_graph.add_node(co_aut)          # add the note to the graph with the name of the current co-author,
                        node_queue.append(co_aut)                   # and the co-author node to the node queue
                pos_edges = itertools.combinations(authors, 2)      # the possible edges between the co-authors are the combinations (with length 2) of the authors list [note that (2,3) = (3,2) when using combinations and (2,2) is excluded]
                for pos_edge in pos_edges:                                      # iterating over possible edges
                    if (pos_edge[0],pos_edge[1]) not in aut_graph.edges():      # if the edge is not yet in the graph,
                        aut_graph.add_edge(pos_edge[0], pos_edge[1], weight=1)  # add it with weight = 1
                    else:                                                       # if the edge does exist,
                        aut_graph[pos_edge[0]][pos_edge[1]]['weight'] += 1      # add 1 to the weight
    for graph_node in aut_graph.nodes():                                        # iterating over graph nodes and,
        aut_graph.nodes[graph_node]['distance'] = networkx.shortest_path_length(aut_graph, aut, graph_node)     # adding the distance to the initial authors using the shortest_path_length function
    return aut_graph                                                            # return the graph


def do_find_cycles(data, sse):
    # the simple_cycle function returns a generator object where each cycle is a list of nodes with the first and last nodes being the same
    # the citation graph created in do_citation_graph is directional so we can use the simple_cycle function
    # iterating over the generator object and storing the items in tuples to obtain the demanded result
    return [tuple(item) for item in networkx.simple_cycles(do_citation_graph(data,sse))]


def do_cit_count_year(data, sse, aut, year):

    cit_count_dict = {}
    cur_year = datetime.datetime.today().year
    publish = False
    for my_dict in sse.data:
        authors = my_dict['authors'].split('; ')
        if aut in authors:
            publish = True
            doi = my_dict['doi']
            for my_cit_dict in data:
                if my_cit_dict['doi'] == doi:
                    this_year = my_dict['year']
                    if this_year not in cit_count_dict and ((year is not None and int(this_year) >= year) or year is None):
                        cit_count_dict[int(my_dict['year'])] = int(my_cit_dict['cited by'])
                    elif this_year in cit_count_dict:
                        cit_count_dict[int(my_dict['year'])] += int(my_cit_dict['cited by'])
    if year is not None:
        min_year = year
    elif publish is True:
        min_year = min(cit_count_dict)
    else:
        return cit_count_dict
    for zero_year in range(min_year, cur_year + 1):
        if zero_year not in cit_count_dict:
            cit_count_dict[zero_year] = 0
    return cit_count_dict


def do_jou_h_index(data, sse, jou):

   # It returns a non - negative integer that is the maximum value 'h' such that the given journal has published 'h'
   # papers that have each been cited at least 'h' times.
    cit_list = []
    for row in sse.data:
        if jou in row['journal'].split('; '):
            for d in data:
                if d['doi'] == row['doi']:
                    cit_list.append(int(d['cited by']))
    cit_list.sort(reverse=True)
    for index, value in enumerate(cit_list):
        if index + 1 > value:
            return index
    return None

def do_category_rank(data, sse, years):

    result = []
    category_list = []
    category_list_none = []
    for x in sse.data:

        category_list_none.extend(x['categories'].split('; '))
        if years is not None:
            for year in years:
                if year == int(x['year']):
                    category_list.extend(x['categories'].split('; '))

    top_10_tpl = collections.Counter(category_list).most_common(10)
    top_10_tpl_none = collections.Counter(category_list_none).most_common(10)

    if years is None or len(years) == 0:
        result.append(top_10_tpl_none)
    else:
        result.append(top_10_tpl)

    return result

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    VanillaHED.py

    Fischer, Andreas, et al. "Approximation of graph edit distance based on Hausdorff matching."
    Pattern recognition 48.2 (2015): 331-343.

    Basic implementation of edit cost operations.
"""

from HausdorffEditDistance import HausdorffEditDistance

import os
import glob
import itertools

from itertools import chain
from scipy.spatial.distance import cdist
import numpy as np
import networkx as nx

from Plotter import plot_assignment_hausdorff

__author__ = "Pau Riba, Anjan Dutta"
__email__ = "priba@cvc.uab.cat, adutta@cvc.uab.cat"


class VanillaHED(HausdorffEditDistance):
    """
        Vanilla Hausdorff Edit distance, implements basic costs for substitution insertion and deletion.
    """

    def __init__(self, del_node = 0.25, ins_node = 0.5, del_edge = 0.1, ins_edge = 0.1, metric = "euclidean"):
        self.del_node = del_node
        self.ins_node = ins_node
        self.del_edge = del_edge
        self.ins_edge = ins_edge
        self.metric = metric

    """
        Node edit operations
    """
    def node_substitution(self, g1, g2):
        """
            Node substitution costs
            :param g1, g2: Graphs whose nodes are being substituted
            :return: Matrix with the substitution costs
        """
        values1 = [v for k, v in g1.nodes(data=True)]
        v1 = [list(chain.from_iterable(l.values())) for l in values1]

        values2 = [v for k, v in g2.nodes(data=True)]
        v2 = [list(chain.from_iterable(l.values())) for l in values2]

        node_dist = cdist(np.array(v1), np.array(v2), metric=self.metric)

        return node_dist

    def node_insertion(self, g):
        """
            Node Insertion costs
            :param g: Graphs whose nodes are being inserted
            :return: List with the insertion costs
        """
        values = [v for k, v in g.nodes(data=True)]
        return [self.ins_node]*len(values) + self.edge_insertion(g.edge.values())

    def node_deletion(self, g):
        """
            Node Deletion costs
            :param g: Graphs whose nodes are being deleted
            :return: List with the deletion costs
        """
        values = [v for k, v in g.nodes(data=True)]
        return [self.del_node] * len(values) + self.edge_deletion(g.edge.values())

    """
        Edge edit operations
    """
    def edge_substitution(self, g1, g2):
        """
            Edge Substitution costs
            :param g: Adjacency list.
            :return: List of edge deletion costs
        """
        edge_dist = cdist(np.array([l.values() for l in g1]), np.array([l.values() for l in g2]), metric=self.metric)
        return edge_dist

    def edge_insertion(self, g):
        """
            Edge insertion costs
            :param g: Adjacency list.
            :return: List of edge insertion costs
        """
        insert_edges = [len(e) for e in g]
        return np.array([self.ins_edge] * len(insert_edges)) * insert_edges

    def edge_deletion(self, g):
        """
            Edge Deletion costs
            :param g: Adjacency list.
            :return: List of edge deletion costs
        """
        delete_edges = [len(e) for e in g]
        return np.array([self.del_edge] * len(delete_edges)) * delete_edges

if __name__ == '__main__':

    path_dataset = './data/'
    name_dataset = 'Letters'

    hed = VanillaHED()

    path_dataset = os.path.join(path_dataset, name_dataset)
    files = glob.glob(path_dataset + '/*.gml')
    for f1, f2 in itertools.combinations_with_replacement(files, 2):
        # Read graphs
        g1 = nx.read_gml(f1)
        g2 = nx.read_gml(f2)

        # Distance
        dist, assignment = hed.ged(g1, g2)

        fig = plot_assignment_hausdorff(g1, g2, assignment)
        fig.savefig('./data/Results/HED/'+g1.graph['class'] + '-' + g2.graph['class'] +'.png')

        print g1.graph['class'] + ' <-> ' + g2.graph['class'] + ' | Distance: ' + str(dist)

from graphviz import Graph, Digraph
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, Markdown
from mpl_toolkits.mplot3d import Axes3D
import inspect

BASE_SIZE = 5

def show(string, *args):
    try:
        display(Markdown(string.format(*args)))
    except:
        display(Markdown(string))


def get_latex_string_for_matrix(matrix, formatter='{:.2f}', left='(', right=')'):
    string = '\\begin{{equation}}\n\\left{}\\begin{{matrix}}\n'.format(left)
    for row in matrix[:-1]:
        string += ' & '.join([formatter.format(element)
                              for element in row]) + '\\\\\n'
    # Last row does not require a linebreak
    string += ' & '.join([formatter.format(element)
                          for element in matrix[-1]]) + '\n'

    return string + '\\end{{matrix}}\\right{}\n\\end{{equation}}'.format(right)


def get_latex_string_for_vector(vector, formatter='{:.2f}', left='(', right=')'):
    string = '$\\left{}\n'.format(left)
    string += ', '.join([formatter.format(v) for v in vector])
    return string + '\\right{}$'.format(right)


def getLabelForNode(node, labels):
    if inspect.isfunction(labels):
        return labels(node)
    if type(node) is int and type(labels) is list or type(labels) is tuple:
        return labels[node]
    if labels is None or node not in labels.keys():
        return str(node)
    else:
        return labels[node]


def getLabelForEdge(source, destination, labels):
    if inspect.isfunction(labels):
        return labels(source, destination)
    if type(source) is int and type(labels) is list or type(labels) is tuple:
        return labels[source]
    if labels is None or (source, destination) not in labels.keys():
        return ''
    else:
        return labels[(source, destination)]


def showGraph(graph, name, node_labels=None, edge_labels=None, comment='', directed=False):
    if directed:
        dg = Digraph(name, comment, format='png')
    else:
        dg = Graph(name, comment, format='png')

    for source, destinations in graph.items():
        # Add edges
        dg.node(str(source), getLabelForNode(source, node_labels))
        for destination in destinations:
            dg.node(str(destination), getLabelForNode(
                destination, node_labels))
            dg.edge(str(source), str(destination), label=getLabelForEdge(
                source, destination, edge_labels))
    display(dg)
    return dg


def invert_graph(g):
    g_inv = {}
    for destination, sources in g.items():
        for source in sources:
            if source not in g_inv.keys():
                g_inv[source] = []
            g_inv[source].append(destination)
    return g_inv


def code(method):
    show('''
```python
{}
```
    ''', inspect.getsource(method))


def show_module_methods(module):
    for name, member in inspect.getmembers(module):
        if inspect.isfunction(member):
            show('''#### {}'''.format(name))
            code(member)
            
def show_module_classes(module):
    for name, member in inspect.getmembers(module):
        if inspect.isclass(member):
            show('''#### {}'''.format(name))
            code(member)

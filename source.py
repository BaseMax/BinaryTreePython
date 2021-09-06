# https://github.com/BaseMax/BinaryTreePython
# https://github.com/BaseMax/BinaryTreeDiagram
# https://github.com/BaseMax/BinaryTreeDiagramDrawing

import itertools, graphviz as gvz
from math import log2, floor

matrix = {
    "xyz": (0, 1, 2, 3, 4, 5, 6, 7),
    "xzy": (0, 1, 4, 5, 2, 3, 6, 7),
    "yxz": (0, 1, 4, 5, 2, 3, 6, 7),
    "yzx": (0, 4, 1, 5, 2, 6, 3, 7),
    "zxy": (0, 2, 4, 6, 1, 3, 5, 7),
    "zyx": (0, 4, 2, 6, 1, 5, 3, 7),
}

value = input('Enter all of minterms in one line with space:')
# value = "0 1 2"
combf = list(map(lambda x: int(x),value.split()))
combf.sort()

def merge(lst):
    res = []
    for i in range(0, len(lst) - 1, 2):
        res.append((lst[i], lst[i + 1]))
    return res

def make_form(combf, fulltree):
    res = []
    for i in range(len(matrix[form])):
        if matrix[form][i] in combf:
            res.append(matrix[form][i])
        else:
            res.append(None)
    while (len(res) > 1):
        res = merge(res)
    return res[0]

def find_best_poly(combf, fulltree, w=0):
    new_combf = []
    for element in combf:
        if element in fulltree:
            new_combf.append(element)
            w += 1
    if len(new_combf) < 2:
        return w
    return find_best_poly(list(itertools.combinations(new_combf, 2)),merge(fulltree), w)

my_tree = []

def draw(tree, g, form, h=1):
    if (hasattr(tree, "__iter__")):
        
        l = draw(tree[0], g, form, 2 * h)
        r = draw(tree[1], g, form, 2 * h + 1)

        if l == r and r != (1, 1):

            g.node(f'{h}',f'{l[0]}',style="invis" if l==(0,0) else None)
            g.node(f'{2*h}',f'{l[0]}',style="invis")
            g.edge(f'{h}',f'{2*h}',style="invis")

            my_tree.append([
                str(h),
                str(2*h),
                str(l[0]),
                str(l[0]),
                "invis"
            ])

            g.node(f'{2*h+1}',f'{r[0]}',style="invis")
            g.edge(f'{h}',f'{2*h+1}',style = "invis")
            my_tree.append([
                str(h),
                str(2*h+1),
                str(l[0]),
                str(r[0]),
                "invis"
            ])
            
            return l
        
        g.node(f'{h}', f'{form[floor(log2(h))]}')
        g.node(f'{2*h}',f'{form[floor(log2(2*h))]}'  if l[1] else f'{l[0]}', style=None if l[0] else "invis")
        g.edge(f'{h}', f'{2*h}',style="dashed" if l[0] else "invis")

        my_tree.append([
            str(h),
            str(2*h),
            str(form[floor(log2(h))]),
            str(form[floor(log2(2*h))] if l[1] else l[0]),
            "dashed" if l[0] else "invis"
        ])
        
        g.node(f'{2*h+1}',f'{form[floor(log2(2*h+1))]}'  if r[1] else f'{r[0]}', style=None if r[0] else "invis")
        g.edge(f'{h}', f'{2*h+1}',style=None if r[0] else "invis")

        my_tree.append([
            str(h),
            str(h*h+1),
            str(form[floor(log2(h))]),
            str(form[floor(log2(2*h+1))] if r[1] else r[0]),
            # None if r[0] else "invis"
            "invis" if r[0] else "invis"
        ])
        
        return (1, 1)

    return (1, 0) if type(tree) == int else (0, 0)

def print_tree(tree):
    print("============== Show tree")
    index = 0
    for value in tree:
        print(index, value)
        index = index + 1
    print("==============")

def clean_tree(tree):
    print("tree:", tree, "\n")
    index = 0

    res_tree = [item for item in tree]
    print("length: ", len(tree))
    print_tree(res_tree)

    removed = 0

    for item in tree:
        # if item[4] == None:
        #     tree[index][4] = "invis"

        # if item[2] == 'y' and item[3] == '1':
        #     print("found", item)

        if item[2] == '0' or item[3] == '0':
            # print("remove ",index)
            del res_tree[index - removed]
            removed = removed + 1
        if item[2] == '1' and item[3] == '1':
            # print("remove ",index)
            del res_tree[index - removed]
            removed = removed + 1

        index = index+1

    return res_tree

if __name__ == "__main__":
    weight = {
        fulltree[0]: find_best_poly(list(itertools.combinations(combf, 2)),merge(fulltree[1]))
        for fulltree in matrix.items()
    }
    form = list(weight.keys())[list(weight.values()).index(max(weight.values()))]
    print(form)
    g = gvz.Graph(format="png",filename="btree.gv")
    tree = make_form(combf, matrix[form])
    draw(tree, g, form)

    print(g.source)

    my_tree = clean_tree(my_tree)
    node_added = 0

    print("my_tree:", my_tree, "\n")
    x = 0
    for value in my_tree:
        print(x, value)
        if value[3] == '1':
            print(value[2], "reached to 1")
            y = 0
            reached_to_x = []
            for value2 in my_tree:
                if value2[2] == value[2]:
                    print("\t", y, value2)
                    reached_to_x.append(value2)
                y = y + 1
            print("reached_to_x:", reached_to_x)
            print("len(reached_to_x):", len(reached_to_x))
            if len(reached_to_x) == 1:
                g.node('o'+str(100+node_added), '0') # style=None if r[0] else "invis")
                g.edge(value[0], 'o'+str(100+node_added))
                node_added = node_added + 1
        print("")
        x = x + 1

    g.view()


import re


class Bag:
    def __init__(self, color, parent=None, childs=None, edge_weights=None):
        self.color = color
        self.parents = [parent] if parent else []
        self.childs = childs if childs else []
        self.edge_weight = edge_weights if edge_weights else []

    def __repr__(self):
        return f'color: {self.color}\nparents: {[parent.color for parent in self.parents]}'


def traverse_back(bag):
    uniques = set()

    def backwards(bag):
        uniques.add(bag.color)
        for parent_bag in bag.parents:
            backwards(parent_bag)

    backwards(bag)
    return len(uniques) - 1


def traverse_forward(bag, this_weight):
    s = 0
    for weight, child_bag in zip(bag.edge_weight, bag.childs):
        s += this_weight * weight
        s += traverse_forward(child_bag, this_weight * weight)
    return s


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    bags = {}
    pat1 = re.compile(r"(\w+ \w+) bags contain")
    pat2 = re.compile(r"(\d+) (\w+ \w+) bag")

    for line in lines:
        parent_name = pat1.match(line)[1]
        if parent_name not in bags:
            bags[parent_name] = Bag(parent_name)

        for match in pat2.finditer(line):
            num, color = int(match[1]), match[2]
            if color not in bags:
                bags[color] = Bag(color, bags[parent_name])
            else:
                bags[color].parents.append(bags[parent_name])
            bags[parent_name].childs.append(bags[color])
            bags[parent_name].edge_weight.append(num)

    shinygold = bags['shiny gold']
    print(f'Part 1: {traverse_back(shinygold)}')
    print(f'Part 2: {traverse_forward(shinygold, 1)}')

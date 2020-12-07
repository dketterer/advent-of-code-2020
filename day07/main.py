class Bag:
    def __init__(self, color, parent, childs=None, edge_weights=None):
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

    lines = [line.strip().rstrip('.') for line in lines]

    bags = {}
    empty = 0
    for line in lines:
        parent_name = line.split('contain')[0].split('bags')[0].strip()
        childs = line.split('contain')[1].strip().split(',')
        if bags.get(parent_name, None) is None:
            bags[parent_name] = Bag(parent_name, None)

        for child in childs:
            child = child.strip()
            if 'other' in child:
                empty += 1
                continue
            num, adjective, color, _ = child.split(' ')
            color = f'{adjective} {color}'
            if bags.get(color, None) is None:
                bags[color] = Bag(color, bags[parent_name])
            else:
                bags[color].parents.append(bags[parent_name])
            bags[parent_name].childs.append(bags[color])
            bags[parent_name].edge_weight.append(int(num))

    shinygold = bags['shiny gold']
    print(f'Part 1: {traverse_back(shinygold)}')
    print(f'Part 2: {traverse_forward(shinygold, 1)}')

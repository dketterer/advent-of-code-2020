import re
from collections import defaultdict
from dataclasses import field, dataclass
from typing import List


@dataclass
class Food:
    ingredients: List[str] = field(default_factory=list)
    allergens: List[str] = field(default_factory=list)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    ingredient_pattern = re.compile(r"^([a-z\s]*)\(?.*")
    allergen_pattern = re.compile(r".*\(contains (.*)\)")

    foods = []
    all_ingredients = []

    for line in lines:
        food = Food()
        m_a = allergen_pattern.match(line)
        if m_a[1]:
            for allergen in map(str.strip, m_a[1].split(',')):
                food.allergens.append(allergen)
        m_i = ingredient_pattern.match(line)
        for ingredient in map(str.strip, m_i[1].strip().split(' ')):
            food.ingredients.append(ingredient)
            all_ingredients.append(ingredient)
        foods.append(food)

    allergen_candidates = defaultdict(lambda: set(all_ingredients))

    for food in foods:
        for allergen in food.allergens:
            allergen_candidates[allergen] = allergen_candidates[allergen].intersection(set(food.ingredients))

    ingredient_exlusion = set(all_ingredients).difference(
        *[allergen_candidates[allergen] for allergen in allergen_candidates.keys()])
    count_exclusion = 0
    for ingredient in ingredient_exlusion:
        count_exclusion += all_ingredients.count(ingredient)

    allergen_ingredient_match = []

    changed = True
    while changed:
        changed = False
        for allergen in allergen_candidates.keys():
            if len(allergen_candidates[allergen]) == 1:
                ingredient = allergen_candidates[allergen].pop()
                allergen_ingredient_match.append((allergen, ingredient))
                for allergen2 in allergen_candidates.keys():
                    if ingredient in allergen_candidates[allergen2]:
                        allergen_candidates[allergen2].remove(ingredient)
                        changed = True

    allergen_ingredient_match.sort(key=lambda tup: tup[0])
    canonical_dangerous_ingredient_list = ','.join([tup[1] for tup in allergen_ingredient_match])

    print(f'Part 1: {count_exclusion}')
    print(f'Part 2: {canonical_dangerous_ingredient_list}')

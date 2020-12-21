from sys import argv


def read_ingredient_lists(filename):
    with open(filename) as stream:
        return [
            IngredientList.from_string(s) for s in stream.read().strip().split("\n")
        ]


class IngredientList:
    def __init__(self, ingredients, allergens=None):
        self.ingredients = set(ingredients)
        self.allergens = set() if allergens is None else set(allergens)

    def __str__(self):
        return f"{' '.join(self.ingredients)} (contains {' ,'.join(self.allergens)})"

    def __repr__(self):
        return f"IngredientList({self.ingredients}, {self.allergens})"

    @classmethod
    def from_string(cls, string):
        if "(" in string:
            parts = string.partition(" (contains ")
            return cls(parts[0].split(" "), parts[-1][:-1].split(", "))
        return cls(string.split(" "))


def find_ingredients_containing_allergen(ingredient_lists):
    allergen_ingredients = {}
    for il in ingredient_lists:
        for allergen in il.allergens:
            if not allergen in allergen_ingredients:
                allergen_ingredients[allergen] = il.ingredients
            else:
                allergen_ingredients[allergen] = allergen_ingredients[
                    allergen
                ].intersection(il.ingredients)
    allergen_ingredients = make_unique(allergen_ingredients)
    return {v.pop(): k for k, v in allergen_ingredients.items()}


def make_unique(allergen_ingredients):
    while any(len(i) > 1 for i in allergen_ingredients.values()):
        for allergen, ingredients in allergen_ingredients.items():
            if len(ingredients) == 1:
                for a in allergen_ingredients.keys():
                    if not a == allergen:
                        allergen_ingredients[a] = allergen_ingredients[a].difference(
                            ingredients
                        )
    return allergen_ingredients


if __name__ == "__main__":
    ingredient_lists = read_ingredient_lists(argv[-1])
    allergen_ingredients = find_ingredients_containing_allergen(ingredient_lists)
    print(allergen_ingredients)
    print(
        sum(
            len(il.ingredients.difference(allergen_ingredients))
            for il in ingredient_lists
        )
    )
    print(
        ",".join(
            i
            for i in sorted(allergen_ingredients, key=lambda x: allergen_ingredients[x])
        )
    )

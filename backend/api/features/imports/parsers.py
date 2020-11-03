import pathlib
import re
import unicodedata

import bs4
import pint
import requests

from api.features.recipes.models import State
from api.features.recipes.schemas import (
    RecipeIngredient,
    InstructionCreate,
    RecipeCreate
)
from api.utils.db import get_db


def get_parser(url):
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.content, "html.parser")

    if "seriouseats.com" in url:
        return SeriousEatsParser(source=url, soup=soup)

    if "delish.com" in url:
        return DelishParser(source=url, soup=soup)

    parsers = {
        "tasty-recipes": TastyParser,
        "wprm-recipe-container": WPRMParser,
        "zip-recipe-parser": ZipRecipeParser,
    }

    for key, value in parsers.items():
        founder = soup.find(class_=key)

        if founder is not None:
            return value(source=url, soup=soup)

    raise ValueError("Unable to parse recipe.")


def int_or_float(value):
    try:
        int(value)
        return True
    except ValueError:
        try:
            float(value)
            return True
        except ValueError:
            if "/" in value or value.isnumeric():
                return True
            else:
                return False


def remove_numeric_in_string(string):
    numeric_less_string = string
    for character in string:
        if character.isnumeric() or character in ("/", ".", "(", ")", "-", "–", ","):
            numeric_less_string = replacer(numeric_less_string, character)

    return numeric_less_string.strip()


def standardize_units(unit):
    ureg = pint.UnitRegistry()

    try:
        if unit == '"':
            unit = "inch"
        units = ureg.parse_expression(unit)
        unit_string = str(units.units)

        if unit_string == "speed_of_light":
            standard_unit = "cup(s)"
        elif unit_string in ("H2O", "dimensionless"):
            standard_unit = "Unitless"
        else:
            standard_unit = unit_string.rstrip("s") + "(s)"
    except pint.errors.UndefinedUnitError:
        standard_unit = "Unitless"

    return standard_unit


def parenthetical_remover(string):
    string = re.sub(r"\([^()]*\)", "", string).rstrip()
    return string


def keep_alphanumeric(string):
    string = re.sub(r'[^a-z0-9/ ]', '', string)
    return string


def remove_wildcard(string):
    return re.sub(r"\*", "", string)


def replacer(string, replace):
    string = string.replace(f" {replace} ", " ")
    string = string.replace(f" {replace}", " ")
    string = string.replace(f"{replace} ", " ")
    string = string.replace(f"{replace}", " ")
    return string


class IngredientParser(object):
    def __init__(self, ingredient_line):

        self._ingredient_line = remove_wildcard(
            str(keep_alphanumeric(parenthetical_remover(ingredient_line)))
        ).lower()

        self._db = next(get_db())
        self._valid_states = None

        self._amount = 0
        self._unit = ""
        self._ingredient = ""
        self._state = ""

        self._copy = None

    @property
    def valid_states(self):
        if self._valid_states is None:
            valid_states: State = self._db.query(State).all()
            self._valid_states = [state.name for state in valid_states if state.name != '']

        return self._valid_states[:-1]

    def get_state(self):
        for state in self.valid_states:
            if state in self._ingredient_line:
                self._state = state
                self._ingredient_line = replacer(self._ingredient_line, state)

        return self._state

    def get_unit(self):
        copy_split = self._ingredient_line.split()

        split_list = []
        for split in copy_split:
            numeric_less = remove_numeric_in_string(split)

            if split != "+":
                unit = standardize_units(numeric_less)
            else:
                unit = "Unitless"

            if unit != "Unitless":
                if self._unit == "":
                    self._unit = unit
                else:
                    split_list.append(split)
                # split_list.append(replacer(split, numeric_less))
            else:
                split_list.append(split)

        self._copy = " ".join(split_list)

        return self._unit

    def get_amount(self):
        new_split = self._copy.split(maxsplit=2)
        for split in new_split:
            if int_or_float(split):
                self._amount = split
                break

        self._copy = replacer(self._copy, self._amount)

        return self._amount

    def get_ingredient(self):
        drop_words = ["to", "from"]
        last_split = self._copy.split()
        for last in last_split:
            for word in drop_words:
                if word == last:
                    self._copy = replacer(self._copy, word)
            if "or" == last:
                print(self._copy)
                index = self._copy.index("or")
                self._copy = replacer(self._copy, self._copy[: index - 1])

        rough_ingredient = parenthetical_remover(remove_numeric_in_string(self._copy))
        self._ingredient = rough_ingredient.strip().title()

        return self._ingredient

    @property
    def phrase(self):
        return self.amount, self._unit, self._ingredient, self._state

    @property
    def amount(self):
        amount = self._amount
        # catching 1/2 unicode
        try:
            amount = unicodedata.numeric(self._amount)
            return amount
        except TypeError:
            pass

        # converts 1/2 into 0.5
        try:
            amount = eval(self._amount)
            return amount
        except TypeError:
            pass

        return amount

    def parse(self):
        self.get_state()
        self.get_unit()
        self.get_amount()
        self.get_ingredient()
        return self.phrase


class RecipeParser(object):
    def __init__(self, source=None, soup=None):
        self._source = source

        self._soup = soup

    def get_title(self):
        raise Exception("Not implemented in subclass")

    def get_description(self):
        raise Exception("Not implemented in subclass")

    @staticmethod
    def _image_url_finder(url):
        path = pathlib.Path(url)

        return str(path.with_name("-".join(path.stem.split("-")[:-1]) + path.suffix))

    def get_image(self):
        raise Exception("Not implemented in subclass")

    def _default_author(self):
        return pathlib.Path(self._source).parent.stem.capitalize()

    def get_author(self):
        raise Exception("Not implemented in subclass")

    def get_source(self):
        return self._source

    def get_servings(self):
        raise Exception("Not implemented in subclass")

    def get_ingredients(self):
        raise Exception("Not implemented in subclass")

    def get_instructions(self):
        raise Exception("Not implemented in subclass")

    def build_recipe(self):
        return RecipeCreate(
            title=self.get_title(),
            description=self.get_description(),
            image=self.get_image(),
            author=self.get_author(),
            source=self.get_source(),
            servings=self.get_servings(),
            ingredients=self.get_ingredients(),
            instructions=self.get_instructions(),
        )


class DelishParser(RecipeParser):
    def get_title(self):
        return self._soup.find(class_="recipe-hed").get_text()

    def get_description(self):
        return None

    def get_image(self):
        try:
            return self._soup.find(class_='recipe-lede-image').find('img')['src']
        except AttributeError:
            return None

    def get_author(self):
        return self._soup.find(class_="byline-name").get_text()

    def _processing_servings(self):
        splits = self._soup.find(class_="yields-amount").get_text().split()

        numeric = []
        for thing in splits:
            try:
                x = int(thing)
                numeric.append(x)
            except ValueError:
                pass

        return int(sum(numeric) / len(numeric))

    def get_servings(self):
        return self._processing_servings()

    def get_ingredients(self):
        ingredient_list = [
            ingredient.get_text() for ingredient in
            self._soup.find(class_="ingredient-lists").find_all(class_="ingredient-item")
        ]

        ingredients = []
        for ingredient in ingredient_list:
            parser = IngredientParser(ingredient)
            amount, unit, ingredient, state = parser.parse()
            ingredients.append(
                RecipeIngredient(
                    ingredient=ingredient, amount=amount, unit=unit, state=state
                )
            )

        return ingredients

    def get_instructions(self):
        return [
            InstructionCreate(
                step=count + 1, instruction=instruction.get_text()
            ) for count, instruction in enumerate(self._soup.find(class_="direction-lists").find_all('li'))
        ]


class SeriousEatsParser(RecipeParser):
    def get_title(self):
        return self._soup.find(class_="recipe-title").get_text()

    def get_description(self):
        try:
            return self._soup.find(class_="headnote").get_text()
        except AttributeError:
            return self._soup.find(class_="recipe-introduction-body").get_text()

    def get_image(self):
        return None

    def get_author(self):
        return self._soup.find(class_="author-name").get_text()

    def get_servings(self):
        x = self._soup.find(class_="info yield").get_text()

        for split in x.split():
            if int_or_float(split):
                return split

    def get_ingredients(self):
        ingredient_list = [
            ingredient.get_text() for ingredient in self._soup.find(class_="recipe-ingredients").find_all('li')
        ]

        ingredients = []
        for ingredient in ingredient_list:
            parser = IngredientParser(ingredient)
            amount, unit, ingredient, state = parser.parse()
            ingredients.append(
                RecipeIngredient(
                    ingredient=ingredient, amount=amount, unit=unit, state=state
                )
            )

        return ingredients

    def get_instructions(self):
        return [
            InstructionCreate(
                step=count + 1, instruction=instruction.get_text()
            ) for count, instruction in enumerate(self._soup.find(class_="recipe-procedures-list").find_all('li'))
        ]


class TastyParser(RecipeParser):
    def get_title(self):
        return self._soup.find(class_="tasty-recipes").find("h2").get_text()

    def get_description(self):
        return self._soup.find(class_="tasty-recipes-description").get_text()

    def get_image(self):
        try:
            try:
                url = self._soup.find(class_="tasty-recipes-image").find("img")[
                    "data-lazy-src"
                ]
            except KeyError:
                url = self._soup.find(class_="tasty-recipes-image").find("img")["src"]

            return self._image_url_finder(url)

        except AttributeError:
            return None

    def get_author(self):
        author = self._soup.find(class_="tasty-recipes-author-name")

        if author is not None:
            return author.get_text()
        else:
            return None

    def get_servings(self):
        return self._soup.find(class_="tasty-recipes-yield").get_text().split()[0]

    def get_ingredients(self):
        ingredient_list = [
            ingredient.get_text()
            for ingredient in self._soup.find(
                class_="tasty-recipes-ingredients"
            ).find_all("li")
        ]

        ingredients = []
        for ingredient in ingredient_list:
            parser = IngredientParser(ingredient)
            amount, unit, ingredient, state = parser.parse()
            ingredients.append(
                RecipeIngredient(
                    ingredient=ingredient, amount=amount, unit=unit, state=state
                )
            )

        return ingredients

    def get_instructions(self):
        return [
            InstructionCreate(step=count + 1, instruction=instruction.get_text())
            for count, instruction in enumerate(
                self._soup.find(class_="tasty-recipes-instructions").find_all("li")
            )
        ]


class WPRMParser(RecipeParser):
    def get_title(self):
        return self._soup.find(class_="wprm-recipe-name").get_text()

    def get_description(self):
        description = self._soup.find(class_="wprm-recipe-summary")

        if description is not None:
            return description.get_text()
        else:
            return None

    def get_image(self):
        image = self._soup.find(class_="wprm-recipe-image").find("img")

        for attr in list(image.attrs.keys()):
            if "src" in attr and "set" not in attr:
                found = attr
                if "https" in image[found]:
                    return self._image_url_finder(image[found])

        return None

    def get_author(self):
        author = self._soup.find(class_="wprm-recipe-author")

        if author is not None:
            return author.get_text()

        return self._default_author()

    def get_servings(self):
        return self._soup.find(class_="wprm-recipe-servings").get_text()

    def get_ingredients(self):
        ingredient_list = [
            ingredient.get_text()
            for ingredient in self._soup.find(
                class_="wprm-recipe-ingredients"
            ).find_all("li")
        ]

        ingredients = []
        for ingredient in ingredient_list:
            parser = IngredientParser(ingredient)
            amount, unit, ingredient, state = parser.parse()
            ingredients.append(
                RecipeIngredient(
                    ingredient=ingredient, amount=amount, unit=unit, state=state
                )
            )

        return ingredients

    def get_instructions(self):
        return [
            InstructionCreate(
                step=count + 1, instruction=instruction.get_text().strip()
            )
            for count, instruction in enumerate(
                self._soup.find(class_="wprm-recipe-instructions").find_all("li")
            )
        ]


class ZipRecipeParser(RecipeParser):
    def get_title(self):
        return self._soup.find(id="zlrecipe-title").get_text()

    def get_description(self):
        return None

    def get_image(self):
        return self._soup.find(class_="img-desc-wrap").find("img")["src"]

    def get_author(self):
        author = self._soup.find(class_="ERSAuthor")

        if author is not None:
            return author.get_text()
        else:
            return self._default_author()

    def get_servings(self):
        return self._soup.find(itemprop="recipeYield").get_text().split()[0]

    def get_ingredients(self):
        ingredient_list = [
            ingredient.get_text()
            for ingredient in self._soup.find(id="zlrecipe-ingredients-list").find_all(
                "li"
            )
        ]

        ingredients = []
        for ingredient in ingredient_list:
            parser = IngredientParser(ingredient)
            amount, unit, ingredient, state = parser.parse()
            ingredients.append(
                RecipeIngredient(
                    ingredient=ingredient, amount=amount, unit=unit, state=state
                )
            )

        return ingredients

    def get_instructions(self):
        return [
            InstructionCreate(step=count + 1, instruction=instruction.get_text())
            for count, instruction in enumerate(
                self._soup.find(id="zlrecipe-instructions-list").find_all("li")
            )
        ]


if __name__ == '__main__':
    x = get_parser("https://www.ketoconnect.net/keto-salisbury-steak/")
    x.build_recipe()

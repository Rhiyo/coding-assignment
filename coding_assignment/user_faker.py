import json
import random
from typing import Callable


class UserFaker:
    """
    Handling fake data for users suited for CSV files.

    For a better experience the faker library would be better to use,
    but for this assignment I've implemented a simple anonymization class.
    """

    def set_user_values(self, json_path: str) -> None:
        """
        Reads json file with fake user values.

        Expects FistNames, LastNames, StreetNames, Suburbs list values.

        Must have more than 1 of each.
        """

        with open(json_path) as f:
            user_values = json.load(f)

        for val_name in ["FirstNames", "LastNames", "StreetNames", "Suburbs"]:
            if not val_name in user_values.keys():
                raise "Json in wrong format."

        for items in user_values.values():
            if len(items) < 2:
                raise "Need 2 more items for each value."

        self.user_values = user_values

    def gen_first_name(self) -> str:
        """
        Generates a random first name.
        """
        return random.choice(self.user_values["FirstNames"])

    def gen_last_name(self) -> str:
        """
        Generates a random last name.
        """
        return random.choice(self.user_values["LastNames"])

    def gen_address(self) -> str:
        """
        Generates a random address.
        """
        street_number = str(random.randint(1, 100))
        street_name = random.choice(self.user_values["StreetNames"])
        suburb = random.choice(self.user_values["Suburbs"])

        return " ".join([street_number, street_name, suburb])

    def gen_birthdate(self) -> str:
        """
        Generates a random birth date.
        """

        return "/".join(
            [
                str(random.randint(1, 28)),
                str(random.randint(1, 12)),
                str(random.randint(1950, 2021)),
            ]
        )

    def rep_first_name(self, first_name: str, seed: int = -1) -> str:
        """
        Replaces first name with different first name.
        """
        if seed > -1:
            random.seed(seed)
        return self.__until_not_same(first_name, self.gen_first_name)

    def rep_last_name(self, last_name: str, seed: int = -1) -> str:
        """
        Replaces last name with different last name.
        """
        if seed > -1:
            random.seed(seed)
        return self.__until_not_same(last_name, self.gen_last_name)

    def rep_address(self, address: str, seed: int = -1) -> str:
        """
        Replaces address with different address.
        """
        if seed > -1:
            random.seed(seed)
        return self.__until_not_same(address, self.gen_address)

    def rep_birthplace(self, birthplace: str, seed: int = -1) -> str:
        """
        Replaces address with different address.
        """
        if seed > -1:
            random.seed(seed)
        return self.__until_not_same(birthplace, self.gen_birthplace)

    def __until_not_same(self, ori_str: str, gen_func: Callable[[], str]) -> str:
        """
        Returns a value generated via gen_func that is not the same as ori_str.
        """
        new_str = gen_func()
        while ori_str == new_str:
            new_str = gen_func()

        return new_str

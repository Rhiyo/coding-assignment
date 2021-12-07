import pytest
import json
import random
from coding_assignment.user_faker import UserFaker

user_values_small = {
    "FirstNames": [
        "John",
        "Stephen",
    ],
    "LastNames": [
        "Smith",
        "Brown",
    ],
    "StreetNames": [
        "Meadow Rd",
        "Lane Wy",
    ],
    "Suburbs": [
        "Sydney",
        "Parramatta",
    ],
}


@pytest.fixture
def user_faker():
    user_faker = UserFaker()
    user_faker.user_values = user_values_small
    return user_faker


def test_set_user_values(user_faker, tmp_path):
    user_values_other = {
        "FirstNames": [
            "Johna",
            "Stephena",
        ],
        "LastNames": [
            "Smitha",
            "Browna",
        ],
        "StreetNames": [
            "Meadow Rda",
            "Lane Wya",
        ],
        "Suburbs": [
            "Sydneay",
            "Parramattaa",
        ],
    }

    p = tmp_path / "user_values.json"

    with open(p, "w") as f:
        json.dump(user_values_other, f)

    user_faker.set_user_values(p)

    assert user_faker.user_values == user_values_other


def test_set_user_values_format(user_faker, tmp_path):
    user_values_other = {
        "FirstNames": [
            "Johna",
            "Stephena",
        ],
        "LastNames": [
            "Smitha",
            "Browna",
        ],
        "StreetNames": [
            "Meadow Rda",
            "Lane Wya",
        ],
    }

    p = tmp_path / "user_values.json"

    with open(p, "w") as f:
        json.dump(user_values_other, f)

    with pytest.raises(Exception):
        user_faker.set_user_values(p)


def test_set_user_values_lengths(user_faker, tmp_path):
    user_values_other = {
        "FirstNames": [
            "Johna",
            "Stephena",
        ],
        "LastNames": [
            "Smitha",
            "Browna",
        ],
        "StreetNames": [
            "Meadow Rda",
            "Lane Wya",
        ],
        "Suburbs": ["Sydneay"],
    }

    p = tmp_path / "user_values.json"

    with open(p, "w") as f:
        json.dump(user_values_other, f)

    with pytest.raises(Exception):
        user_faker.set_user_values(p)


def test_gen_first_name(user_faker):
    random.seed(555)
    assert user_faker.gen_first_name() == "John"


def test_gen_last_name(user_faker):
    random.seed(555)
    assert user_faker.gen_last_name() == "Smith"


def test_gen_address(user_faker):
    random.seed(555)
    assert user_faker.gen_address() == "25 Lane Wy Sydney"


def test_gen_birthdate(user_faker):
    random.seed(555)
    assert user_faker.gen_birthdate() == "7/5/1970"


def test_rep_first_name(user_faker):
    random.seed(555)
    assert user_faker.rep_first_name("John") == "Stephen"


def test_rep_last_name(user_faker):
    random.seed(555)
    assert user_faker.rep_last_name("Smith") == "Brown"


def test_rep_address(user_faker):
    random.seed(555)
    assert user_faker.rep_address("25 Lane Wy Sydney") == "17 Meadow Rd Sydney"

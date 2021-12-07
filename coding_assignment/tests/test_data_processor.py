import pytest
import random
import coding_assignment.data_processor as dp

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
    ]
}

@pytest.fixture
def user_faker():
    user_faker = UserFaker()
    user_faker.user_values = user_values_small
    return user_faker

def test_generate_user_csv(user_faker, tmp_path):
    test_gen_users = "first_name,last_name,address,date_of_birth\n"
    test_gen_users += "John,Brown,21 Meadow Rd Sydney,5/5/2002\n"
    test_gen_users += "John,Brown,77 Lane Wy Sydney,27/3/1954\n"
    p = tmp_path / 'generated_users.csv'
    random.seed(555)
    dp.generate_user_csv(p, user_faker, 0.0001)
    with open(p, 'r') as f:
        gen_users = f.read()
    assert gen_users == test_gen_users

def test_anonymize_user_data_by_line(user_faker, tmp_path):
    test_anon_users = "first_name,last_name,address,date_of_birth\n"
    test_anon_users += "Stephen,Smith,14 Meadow Rd Sydney,5/5/2002\n"
    test_anon_users += "Stephen,Smith,92 Meadow Rd Sydney,27/3/1954\n"
    
    p_csv = tmp_path / 'generated_users.csv'
    p_to = tmp_path / 'anonymized_users.csv'

    random.seed(555)
    dp.generate_user_csv(p_csv, user_faker, 0.0001)

    dp.anonymize_user_data_by_line(p_csv, p_to, user_faker)

    with open(p_to, 'r') as f:
        anon_users = f.read()

    assert anon_users == test_anon_users

def test_anonymize_user_data_multiprocess(user_faker, tmp_path):
    test_anon_users = "first_name,last_name,address,date_of_birth\n"
    test_anon_users += "Stephen,Smith,17 Meadow Rd Sydney,5/5/2002\n"
    test_anon_users += "Stephen,Smith,71 Lane Wy Parramatta,27/3/1954\n"
    
    p_csv = tmp_path / 'generated_users.csv'
    p_to = tmp_path / 'anonymized_users.csv'

    random.seed(555)
    dp.generate_user_csv(p_csv, user_faker, 0.0001)
    dp.anonymize_user_data_multiprocess(p_csv, p_to, user_faker, seed=555)

    with open(p_to, 'r') as f:
        anon_users = f.read()

    assert anon_users == test_anon_users

def test_anonymize_user_row(user_faker):
    line = "Stephen,Smith,17 Meadow Rd Sydney,5/5/2002\n"
    returned_line = "John,Brown,21 Meadow Rd Sydney,5/5/2002\n"
    random.seed(555)
    assert dp.anonymize_user_row(line, user_faker) == returned_line

def test_get_chunks(user_faker, tmp_path):
    p = tmp_path / 'generated_users.csv'

    random.seed(555)
    dp.generate_user_csv(p, user_faker, 0.0001)
    
    expected_chunks = [(43, 1048576)]

    chunks = [chunk for chunk in dp.get_chunks(p)]
    assert chunks == expected_chunks

def test_process_chunk(user_faker, tmp_path):
    test_anon_users = "Stephen,Smith,17 Meadow Rd Sydney,5/5/2002\n"
    test_anon_users += "Stephen,Smith,71 Lane Wy Parramatta,27/3/1954\n"

    p = tmp_path / 'generated_users.csv'

    random.seed(555)
    dp.generate_user_csv(p, user_faker, 0.0001)
    
    chunks = [chunk for chunk in dp.get_chunks(p)]

    processed_chunk = dp.process_chunk(p, user_faker, chunks[0][0], chunks[0][1], seed=555)
    print(processed_chunk)
    assert test_anon_users == processed_chunk


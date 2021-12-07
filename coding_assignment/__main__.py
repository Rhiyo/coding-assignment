import coding_assignment.data_processor as dp
from coding_assignment.fwf_parser import FwfParser
from coding_assignment.user_faker import UserFaker


def main():
    fwf_parser = FwfParser()
    fwf_parser.set_spec("./spec.json")

    print("Generating Fixed Width File based on given spec to: random.txt")
    fwf_parser.generate_fwf("./random.txt", rows=100)

    print("Parsing Fixed With File to CSV: random.csv")
    fwf_parser.to_csv("./random.txt", "./random.csv")

    user_faker = UserFaker()
    user_faker.set_user_values("./user_values.json")
    print("User anonymize test size in mb:")
    print("(Can do 2gb (2000) as per assignment criteria but may take a while)")

    while True:
        try:
            size_mb = int(input("MB: "))
            break
        except ValueError:
            print("Int, please.")

    print(f"Generating {size_mb}MB sized user data file: user_data.csv")
    dp.generate_user_csv("./user_data.csv", user_faker, size_mb=size_mb)

    print("Anonymizing user file to: anon_user_data.csv")
    dp.anonymize_user_data_multiprocess(
        "./user_data.csv", "./anon_user_data.csv", user_faker
    )

    print("Finished with all objectives.")


if __name__ == "__main__":
    main()

# Super Exciting Coding Assignment!

Coding assignment including the ability to generate a fixed width file based on a spec, parse it to a csv, generate fake user data, anonyize that same user data.

The code contains a commented out example to start showing how transforming data could be distributed over a cluster using spark. However, for uncommented code all was done using the standard library. 

User Faker could be replaced with a library like faker, dask alongside pandas could be used as another way of distributed a data transform over a cluster.

# Fixed Width Files

A small example of working with fixed width files:

```
from coding_assignment.fwf_parser import FwfParser

# Create the parser object
fwf_parser = FwfParser()

# Feed in a spec (look at spec.json in parent dir for example)
fwf_parser.set_spec('./spec.json')

# Generate some random data as a fixed width file based on spec
fwf_parser.generate_fwf('./random.txt', rows=100)

# Parse random data fixed with file to a CSV
fwf_parser.to_csv('./random.txt', './random.csv')
```

## User data anonymization

Small code example again:

```
from coding_assignment.fwf_parser import FwfParser
from coding_assignment.user_faker import UserFaker

# Create a user_faker object and feed in fake values to use
user_faker = UserFaker()
user_faker.set_user_values('./user_values.json')

# Generate a CSV of user data
dp.generate_user_csv('./user_data.csv',user_faker, size_mb=size_mb)

# Anonymize a user CSV
dp.anonymize_user_data_multiprocess('./user_data.csv', './anon_user_data.csv', user_faker)

```

## Testing
The pytest library is required to run the tests within coding_assignment

## Running on docker

To build the ducker image run the below code, the build process will also run the tests and not build if tests fail.

```
docker build --tag coding-assignment .
```

To run the docker image with an interactive python script that goes through functions:

```
docker run -it coding-assignment
```
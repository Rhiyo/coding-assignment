import os
import multiprocessing
import random

from coding_assignment.user_faker import UserFaker
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import udf, col
# from pyspark.sql.types import StringType

def generate_user_csv(to_path : str, user_faker : UserFaker, size_mb : float = 50) -> None:
    '''
    Generates random user data based on user faker.
    '''

    with open(to_path, 'wb') as f:
        header_row = (','.join(['first_name','last_name','address','date_of_birth']) + "\n").encode("utf-8")
        
        byte_len = len(header_row)
        
        f.write(header_row)

        while True:
            first_name = user_faker.gen_first_name()
            last_name = user_faker.gen_last_name()
            address = user_faker.gen_address()
            birth_date = user_faker.gen_birthdate()
            
            row = (','.join([first_name,last_name,address,birth_date]) + '\n').encode("utf-8")

            byte_len += len(row)

            f.write(row)

            if byte_len > size_mb * 1000000:
                break

def anonymize_user_row(line : str, user_faker : UserFaker, seed : int = -1) -> str:
    '''
    Processes a line of user data for anonymization
    '''
    row = line.split(',')
            
    row[0] = user_faker.rep_first_name(row[0], seed)
    row[1] = user_faker.rep_last_name(row[1], seed)
    row[2] = user_faker.rep_address(row[2], seed)

    return ','.join(row)

def anonymize_user_data_by_line(csv_path : str, to_path : str, user_faker : UserFaker) -> None:
    '''
    Anonymize fields first_name, last_name and address of user csv file
    with fake values.
    
    Expects these fields to be in 1st, 2nd and 3rd column of csv.

    This is the slowest way, line by line.
    '''
    
    with open(csv_path, 'r') as read_file:
        
        with open(to_path, 'w') as write_file:
            
            write_file.write(read_file.readline())

            while read_file:
                line = read_file.readline()
                
                if(line == ""):
                    break

                write_file.write(anonymize_user_row(line, user_faker))

                

def anonymize_user_data_multiprocess(csv_path : str, to_path : str, user_faker : UserFaker, n_jobs : int = -1, seed : int = -1) -> None:
    '''
    Anonymize fields first_name, last_name and address of user csv file
    with fake values.
    
    Expects these fields to be in 1st, 2nd and 3rd column of csv.

    This is done with chunks and distirubed across processors,
    giving a speedup but taking more memory.
    '''

    if(n_jobs == -1):
        n_jobs = multiprocessing.cpu_count() - 1
    
    # Set up the pool for multiprocessing
    pool = multiprocessing.Pool(n_jobs)
    jobs = []

    # Create jobs to distribute amongt processes
    chunks = get_chunks(csv_path)
    for chunkStart,chunkSize in chunks:
        jobs.append( pool.apply_async(process_chunk,(csv_path, user_faker, chunkStart,chunkSize, seed)) )

    # Write results from job result queue to new file
    with open(to_path, 'w') as f:
        f.write("first_name,last_name,address,date_of_birth\n")
        for job in jobs:
            f.write(job.get())

    pool.close()

def process_chunk(csv_path : str, user_faker : UserFaker, chunkStart : int, chunkSize : int, seed : int = -1) -> str:
    '''
    Process chunks of user data.
    '''

    with open(csv_path) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        new_lines = ''
        if(seed > -1):
            random.seed(seed)
        for line in lines:
            new_lines += anonymize_user_row(line, user_faker) + '\n'
        
        return new_lines

def get_chunks(csv_path : str, size : int=1024*1024):
    '''
    Get chunck windows at bytes of the specified size for the file at
    csv_path. Chunk size will vary slightly as they are extended to 
    end at a line end.
    '''
    fileEnd = os.path.getsize(csv_path)
    with open(csv_path,'rb') as f:
        f.readline()
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

"""
def anonymize_user_data_spark(csv_path : str, to_path : str, user_faker : UserFaker):
    '''
    Anonymize fields first_name, last_name and address of user csv file
    with fake values.
    
    Expects these fields to be in 1st, 2nd and 3rd column of csv.

    Using the spark library for optimized distribution, and possibily to 
    extend with cluster.
    '''
    
    spark = SparkSession.builder.appName("Data Processor").getOrCreate()

    df = spark.read.csv(csv_path,header=True)
 
    first_name_udf = udf(user_faker.rep_first_name, StringType())
    last_name_udf = udf(user_faker.rep_last_name, StringType())
    address_udf = udf(user_faker.rep_address, StringType())
    df.withColumn('first_name',(first_name_udf(col('first_name')))).withColumn('last_name',(last_name_udf(col('last_name')))).withColumn('address',(address_udf(col('address')))).coalesce(1).write.csv(to_path)
"""
import boto3
import os
from os import listdir
from os.path import isfile, join
from hierarchy import Hierarchy

def print_s3_contents_boto3(connection, bucket):
    #for bucket in connection.buckets.all():
    for key in bucket.objects.all():
        print(key.key)

if __name__ == '__main__':
    boto3_connection = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket = boto3_connection.Bucket('econ-demog')
    bucket_name = 'econ-demog'

    quote_page = 'https://www2.census.gov/acs/downloads/Core_Tables/rural_statistics_area/2007/Wyoming/'

    quote_list = Hierarchy(quote_page)


    #key = boto.s3.key.Key(bucket,file_object)
    #filepath = '/home/david/PublicData/acs_files/'
    #
    for i in quote_list.files:
        file_name = i[i.rfind('/')+1:]
        folder = file_name[:-4]
        filepath = '/home/david/PublicData/acs_files/'+folder+'/'
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        quote_list.load_zip(i, filepath)
        acs_files = [f for f in listdir(filepath) if isfile(join(filepath,f))]

        #k = bucket.new_key(folder)

        for x in acs_files:
            data = open(filepath+x,'rb')
            #Create folder and upload files
            s3_client.put_object(Bucket=bucket_name, Key=folder+'/'+x, Body=data)

    print_s3_contents_boto3(boto3_connection, bucket)


####### create directory on s3 bucket
        # for subdir, dirs, files in os.walk(filepath):
        #     for file in files:
        #         full_path = os.path.join(subdir, file)
        #         with open(full_path, 'rb') as data:
        #             bucket.put_object(Key=full_path[len(filepath)+1:], Body=data)

####### upload single file on local machine to s3
    # file_name = 'DataSources.xslx'
    # file_path = '/home/david/PublicData/DataSources.xlsx'
    #
    # s3_client.upload_file(file_path, 'econ-demog', file_name)







    #boto3_connection.create_bucket(Bucket=bucket_name)
    # reviews_dir = '/home/davidhenslovitz/Galvanize/ZNAHealth/'
    # files = [f for f in listdir(reviews_dir) if isfile(join(reviews_dir,f))]
    # file_paths = [reviews_dir + f for f in listdir(reviews_dir) if isfile(join(reviews_dir,f))]
    # for i,path in enumerate(file_paths):
    #     print(path)
    #     s3_client.upload_file(path, bucket_name, files[i])
    #print_s3_contents_boto3(boto3_connection)

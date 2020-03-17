from minio import Minio

client = Minio('127.0.0.1:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)

# grab buckets
buckets = client.list_buckets()

# print
for bucket in buckets:
    print(bucket.name, bucket.creation_date)



# note: start docker like
# docker run -p 9000:9000 --name minio1 -v C:\Users\rldun\data:/data minio/minio server /data

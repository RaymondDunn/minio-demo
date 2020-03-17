"""
Save a recording as key-value frames

"""
import tifffile as tf
from minio import Minio
from minio.error import ResponseError
import io
import numpy as np
import time

# params
fname = 'C:/Users/rldun/Desktop/20200204-10-46-53_0-500.tiff'
bucketname = 'data'
fname_root = '20200204-10-46-53_short/'

# load tiff
d = tf.imread(fname)

# connect to minio
client = Minio('127.0.0.1:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)

# convert object to byte stream
individual_files = 0

if individual_files:
    tstart = time.time()
    try:
        for i in range(d.shape[0]):
            b = d[i, :, :].tobytes()
            bio = io.BytesIO(b)
            client.put_object(bucketname, fname_root + str(i), bio, len(b))
            if i % 100 == 0:
                print('At frame {}'.format(i))
    except ResponseError as err:
        print('Error during single file upload: {}'.format(err))
    tend = time.time()

else:
    tstart = time.time()
    try:
        b = d.tobytes()
        bio = io.BytesIO(b)
        client.put_object(bucketname, fname_root + 'data', bio, len(b))
    except ResponseError as err:
        print('Error during whole-file upload: {}'.format(err))

    tend = time.time()

print('That took {} seconds to transfer {} frames!'.format(tend - tstart, d.shape))


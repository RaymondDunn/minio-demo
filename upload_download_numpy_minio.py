"""
Save a recording as key-value frames

"""
import tifffile as tf
from minio import Minio
from minio.error import ResponseError
import io
import numpy as np


# params
fname = 'C:/Users/rldun/Desktop/20200204-10-46-53_0-500.tiff'
bucketname = 'data'
objname = 'f0'

# load tiff
d = tf.imread(fname)

# connect to minio
client = Minio('127.0.0.1:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)

# convert object to byte stream
f = d[0,:,:]
b = f.tobytes()
bio = io.BytesIO(b)

# upload object
try:
    client.put_object(bucketname, objname, bio, len(b))
except ResponseError as err:
    print('Error during upload: {}'.format(err))

# download object
try:
    downloaded_data = client.get_object(bucketname, objname)
except ResponseError as err:
    print('Error during download: {}'.format(err))

# compare
res = downloaded_data.read()
new_f = np.frombuffer(res, dtype=f.dtype).reshape(f.shape)
if np.array_equal(f, new_f):
    print('Arrays are equal!')



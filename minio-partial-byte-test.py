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
objname = fname_root + 'data'

# load tiff
d = tf.imread(fname)

# connect to minio
client = Minio('127.0.0.1:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)

# get number of bytes in single frame...
f_ndx_to_grab = 20
f = d[f_ndx_to_grab,:,:]
b = f.tobytes()
num_bytes_per_frame = len(b)

try:
    downloaded_data = client.get_partial_object(bucketname, objname, offset=f_ndx_to_grab*num_bytes_per_frame, length=num_bytes_per_frame)
except ResponseError as err:
    print('Error during download: {}'.format(err))

# compare downloaded chunk!
res = downloaded_data.read()
new_f = np.frombuffer(res, dtype=f.dtype).reshape(f.shape)
if np.array_equal(f, new_f):
    print('Arrays are equal!')

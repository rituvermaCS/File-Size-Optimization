# -*- coding: utf-8 -*-
"""Quantization_of_h5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TbpqDpYx8dobH2BEIwzZFvLwzRlghpYU
"""

import h5py

from google.colab import files

uploaded = files.upload()

f = h5py.File("model.h5", "r")


def traverse_datasets(hdf_file):
    def h5py_dataset_iterator(g, prefix=""):
        for key in g.keys():
            item = g[key]
            path = f"{prefix}/{key}"
            if isinstance(item, h5py.Dataset):  # test for dataset
                yield (path, item)
            elif isinstance(item, h5py.Group):  # test for group (go down)
                yield from h5py_dataset_iterator(item, path)

    for path, _ in h5py_dataset_iterator(hdf_file):
        yield path


for dset in traverse_datasets(f):
    print("Path:", dset)
    print("Shape:", f[dset].shape)
    print("Data type:", f[dset].dtype)

f2 = h5py.File("Quantized_model.h5", mode="a")
for dset in traverse_datasets(f):
    print("Path:", dset)
    f2[dset] = f[dset][...].astype("float16")
    print("Shape:", f[dset].shape)
    print("Data type:", f[dset].dtype)

for dset in traverse_datasets(f2):
    print("Path:", dset)
    print("Shape:", f2[dset].shape)
    print("Data type:", f2[dset].dtype)

f.close()
f2.close()

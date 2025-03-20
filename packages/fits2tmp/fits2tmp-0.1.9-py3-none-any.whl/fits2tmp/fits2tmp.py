import h5py
import zarr
import json
from astropy.io import fits
from astropy import wcs
import dask.array as da
from dask import delayed
from dask.distributed import Lock
import numpy as np
import os
import dask 
import tempfile

def arr_size_check(source_arr, desired_arr: tuple) -> bool:
    if len(source_arr.shape) < len(desired_arr):
        raise ValueError("You've asked for an array with more dimensions than the array stored")
    else:
        for i in range(min(len(source_arr.shape), len(desired_arr))):
            # using min here allows us to avoid an IndexError when we have more dimensions in the source array
            j = source_arr.shape[i] - desired_arr[i]
            if j < 0:
                raise IndexError("Desired array size is larger than the stored array in at least position %s: source array has dimensions %s, and you have requested $s", i, source_arr.shape, desired_arr)
        return True

#def fits_add_header(orig_header, sliced_data) -> fits.Header:
#    coords = wcs.WCS(orig_header)
#    new_header = orig_header
#    new_header.update(coords[data_sli].to_header())
#    return new_header

def header_dict(header) -> dict:
    d = {}
    for i in header.cards:
        d[i.keyword] = i.value
    return d

def dict2header(input_dict: dict) -> fits.Header:
    nh = fits.Header(cards=input_dict)
    return nh

def dict2file(input_dict: dict, filepath):
    with open(filepath, 'w') as f:
        f.write(json.dumps(input_dict))

def file2dict(input_file, filepath) -> dict:
    with open(filepath, 'r') as j:
        contents = json.loads(j.read())
    return contents
filepath = []

def fun(darr, destination, header, block_info=None):
    arr_loc = block_info[None]['array-location']
    print(arr_loc)
    ch_size = block_info[None]['chunk-shape']
    chunk_loc = block_info[None]['chunk-location']
    coords = []
    for i in range(len(arr_loc)):
        coords.append(slice(arr_loc[i][0],arr_loc[i][1]))
    block_id = str(chunk_loc).replace(',', '-').replace('(', '-').replace(')', '').replace(' ', '')
    n_header = dict2header(header_dict(header))
    wcs_obj = wcs.WCS(n_header)
    n_header.update(wcs_obj[coords].to_header())
    out = fits.PrimaryHDU(data=darr, header=n_header)
    outpath = destination.name  + '/' + block_id + ".fits"
    out.writeto(outpath)
    lock = Lock()
    with lock:
        filepath.append(outpath)
    return darr 

def fits2tmpfiles(inputpath, destination, chunks):
    f = fits.open(inputpath)
    destination = tempfile.TemporaryDirectory(dir=destination, delete=False)
    d = da.from_array(f[0].data, chunks=chunks)
    # TODO overlap
    de = da.overlap.overlap(d, depth=None, boundary=None)
    da.map_blocks(fun, d, destination, f[0].header, dtype=float).compute()
    print(filepath)

    return filepath

def disk2fakefits(filetype, inputpath, destination, arraysize, chunks=None):
    match filetype:
        case "fits":
            f = fits.open(inputpath)
            d = da.from_array(f[0].data, chunks=chunks)
            destination = tempfile.TemporaryDirectory(dir=destination, delete=False)
            n_header = dict2header(header_dict(f[0].header))
            wcs_obj = wcs.WCS(n_header)
        case "zarr":
            bar
        case "hdf5":
            baz
        case "xradio":
            weeble
        case _:
            raise ValueError("The specified file type is not supported by fits2tmp.")
    return d, destination, n_header, wcs_obj

def fakefits2tmpfiles(filetype, inputpath, destination, arraysize, chunks=None):
    darr, tempdest, n_header, wcs_obj = disk2fakefits(filetype, inputpath, destination, arraysize, chunks)
    print(darr.shape)
    dd = darr.to_delayed()
    fpaths = []
    for i in range(dd.shape[0]):
        x = i * chunks[0] 
        x_delt = x + chunks[0] - 1
        for j in range(dd.shape[1]):
            y = j * chunks[1]
            y_delt = y + chunks[1] - 1
            if len(dd.shape) == 2:
                dest = str(i) + str(j)
                data = dd[i][j]
                wcs_coords = wcs_obj.slice((slice(x,x_delt), slice(y,y_delt)))
            elif len(dd.shape) > 2:
                for k in range(dd.shape[2]):
                    data = dd[i][j][k]
                    z = k * chunks[2]
                    z_delt = z + chunks[2] - 1
                    dest = str(i) + str(j) + str(k)
                    t =wcs_obj[x:x_delt, y:y_delt, z:z_delt]
                    n_header.update(t.to_header())
                    hdu = fits.PrimaryHDU(data=data.compute(), header=n_header)
                    hdu.writeto(tempdest.name + dest + "fits")
                    fpaths.append(tempdest.name + dest + "fits")
    return fpaths
#def array2disk(array, metadata, outputtype, destination):

#def tmpfitsfile2disk(fitsfile, outputtype, destination):

#def tmpfitsfile2array(fitsfile, arraytype, arraysize, chunks=None):

#def makezarrmetadata(fitsheader):

#def makefitsmetadata(fitsheader, location):

#makehdf5metadata

#makexradiometadata

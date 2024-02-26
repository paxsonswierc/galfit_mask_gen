'''
Creates mask files to be used in Galfit.
'''
import os
import sys
import shutil
from astropy.io import fits
import numpy as np

def make_file(region_path):
    '''
    Makes temporary text file copy of regions file.

    Args:
        region_path (str): path to regions .reg file

    Returns: Path to temporary .txt file copy
    '''
    file_name, ext = os.path.splitext(region_path)
    file_path = file_name + '.txt'
    shutil.copyfile(region_path, file_path)

    return file_path

def read_regions(region_path):
    '''
    Reads regions file of circle regions into a list of 
    region coordinates.

    Args:
        region_path (str): path to regions .txt file

    Returns: list of coordinates for circular regions
    '''
    regions = []

    file = open(region_path)
    for line in file:
        if line[:6] == 'circle':
            coords = line[7:-2].split(',')
            coords = list(map(lambda a: round(float(a)), coords))
            regions.append(coords)

    return regions

def make_mask(regions, input_fits_path):
    '''
    Creates mask array the same size as an input fits image,
    with all values set to zero except for masked values.

    Args:
        regions (list[list[int]]): list of region coordinates
        input_fits_path (str): path to fits file to be masked

    Returns: numpy array of mask image
    '''
    hdul = fits.open(input_fits_path)

    image_length, image_height = np.shape(hdul[0].data)
    mask = np.zeros((image_length, image_height))

    for x in range(image_length):
        for y in range(image_height):
            for reg in regions:
                if ((x - reg[0] + 1)**2 + (y - reg[1] + 1)**2)**.5 < reg[2]:
                    mask[y][x] = 1

    return mask

def main():
    '''
    Creates mask files to be used in Galfit
    '''
    reg_file_path = sys.argv[1]
    input_fits_path = sys.argv[2]
    # Create temporary .txt regions file
    file_path = make_file(reg_file_path)
    # Get region coordinates
    regions = read_regions(file_path)
    # Create mask
    mask = make_mask(regions, input_fits_path)
    # Save mask to given path
    fits.writeto(sys.argv[3], mask, overwrite=True)
    # Delete temporary .txt regions file
    os.remove(file_path)

if __name__ == '__main__':
    main()

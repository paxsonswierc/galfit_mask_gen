import os
import sys
import shutil
from astropy.io import fits
import numpy as np

def make_file(region_path):
    file_name, ext = os.path.splitext(region_path)
    file_path = file_name + '.txt'
    shutil.copyfile(region_path, file_path)

    return file_path

def read_regions(region_path):
    regions = []

    file = open(region_path)
    for line in file:
        if line[:6] == 'circle':
            coords = line[7:-2].split(',')
            coords = list(map(lambda a: round(float(a)), coords))
            regions.append(coords)

    return regions

def make_mask(regions, input_fits_path):
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
    reg_file_path = sys.argv[1]
    input_fits_path = sys.argv[2]
    
    file_path = make_file(reg_file_path)

    regions = read_regions(file_path)
    
    mask = make_mask(regions, input_fits_path)

    fits.writeto(sys.argv[3], mask, overwrite=True)

    os.remove(file_path)
            

if __name__ == '__main__':
    main()

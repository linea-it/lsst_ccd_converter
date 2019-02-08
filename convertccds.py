from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime


def save_image_tiff(fits_ccd_filename, ouputdir, idx):
    print('Starting: ', fits_ccd_filename.split('/')[-1])
    start = datetime.datetime.now()
    hduccds = fits.open(fits_ccd_filename, memmap=True)  # open a FITS file
    imgccd = hduccds[1].data
    sizes = np.shape(imgccd)
    height = float(sizes[0])
    width = float(sizes[1])

    fig = plt.figure()
    fig.set_size_inches(width/height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(imgccd, vmin=1, vmax=200, cmap='gray')
    plt.savefig("{}/mid.png".format(ouputdir), dpi=height)
    plt.close()
    print('Converting', idx)

    os.system('vips im_vips2tiff {}/mid.png {}/{}.tif:deflate,tile:256x256,pyramid'.format(ouputdir, ouputdir, idx))
    end = datetime.datetime.now()
    print('DONE: ', str(end-start))


import glob
exps = glob.glob(
    '/home/felipe/repos/lsst/lsst_image/data_repo/calexp/00193824-g/R*/calexp*')
start = datetime.datetime.now()
for idx, exp in enumerate(exps):
    save_image_tiff(exp, '/home/felipe/repos/lsst/expviewer/images/exps', idx)
end = datetime.datetime.now()
print('DONE: ', str(end-start))

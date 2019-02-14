from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import concurrent.futures
import pyvips
import io

def save_image_tiff(fits_ccd_filename):
    outputdir='./exps'
    idx=fits_ccd_filename.split('/')[-1].split('det')[1].split('.fits')[0]
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
    buf = io.BytesIO()
    plt.savefig(buf, dpi = height)
    buf.seek(0)
    image = pyvips.Image.new_from_buffer(buf.read(), "")
    image.tiffsave("{}/{}.tif".format(outputdir, idx), tile=True, tile_width=256, tile_height=256, pyramid=True, bigtiff=True, compression='deflate')

    #plt.savefig("{}/{}.png".format(outputdir, idx), dpi=height)
    plt.close()
    #tile1 = pyvips.Image.new_from_file("{}/{}.png".format(outputdir, idx), access="sequential")
    #tile1.tiffsave("{}/{}.tif".format(outputdir, idx), tile=True, tile_width=256, tile_height=256, pyramid=True, bigtiff=True)

    #os.system('vips im_vips2tiff {}/{}.png {}/{}.tif:deflate,tile:256x256,pyramid'.format(outputdir, idx, outputdir, idx))
    end = datetime.datetime.now()
    #os.system('rm {}/{}.png'.format(outputdir, idx))
    return 'DONE: {}'.format(str(end-start))


import glob
exps = glob.glob(
    '/home/felipe/repos/lsst/lsst_image/data_repo/calexp/00193824-g/R*/calexp*')
start = datetime.datetime.now()
with concurrent.futures.ProcessPoolExecutor() as executor:
     for time in executor.map(save_image_tiff, exps):
         print(time)

#for idx, exp in enumerate(exps):
#    save_image_tiff(exp, './exps', idx)
end = datetime.datetime.now()
print('DONEALL: ', str(end-start))
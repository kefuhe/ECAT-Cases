# External libraries
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd

# CSI routines and ECAT routines
import csi.insar as insar
import csi.imagecovariance as imcov
from eqtools.csiExtend.sarUtils.readTiff2csisar import TiffsarReader, GammaTiffReader
import cmcrameri

if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    
    # set some flags
    input_check = True
    do_downsample = False
    output_check = False

    # CSI does most computations in a local Cartesian coordinate system. 
    # It presently supports only UTM projections, so we need to set the zone or centrial lon0 and lat0 to use.
    lon0, lat0 = -68.5, -23.0

    # Prepare InSAR data for Sentinel-1
    outName = 'S1_T128A'
    dirname = os.path.join('.', 'insar')
    unwphasename = 'Wushi_asc_los.tif'
    losname = 'Wushi_asc_los.tif'
    aziname = 'Wushi_asc_azi.tif'
    incname = 'Wushi_asc_inc.tif'
    # Way 1: read unwrapped phase and convert it to LOS displacement.
    # mysar = GammaTiffReader(name='Wushi', lon0=lon0, lat0=lat0, directory_name=dirname,
    #                         mode='unwrapped_phase')
    # mysar.extract_raw_grd(phsname=unwphasename, azifile=aziname, incfile=incname)

    # Way 2: read LOS displacement directly.
    mysar = GammaTiffReader(name='Wushi', lon0=lon0, lat0=lat0, directory_name=dirname,
                            mode='los_displacement')
    mysar.extract_raw_grd(phsname=losname, azifile=aziname, incfile=incname)

    mysar.read_observation(downsample=1, zero2nan=True)
    # Select pixels
    mysar.select_pixels(77.4, 79.6, 40, 42.5)

    # Remove Zero and NaN values and value where LOS equals 1
    mysar.checkZeros()
    mysar.checkNaNs()
    mysar.checkLosEqualsOne()

    mysar.print_input_summary()
    print(mysar.los[:6, :])

    # Plot Raw InSAR data
    mysar.plot_sar_values(rawdownsample4plot=1, save_fig=True, 
                          file_path='raw_insar.png', dpi=300,
                          colorbar_orientation='horizontal')
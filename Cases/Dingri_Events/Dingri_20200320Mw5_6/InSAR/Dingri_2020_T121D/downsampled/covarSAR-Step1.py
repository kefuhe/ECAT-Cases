# External libraries
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd

# CSI routines and ECAT routines
import csi.insar as insar
import csi.imagecovariance as imcov
from csi.csiutils import utm_zone_epsg
from eqtools.csiExtend.sarUtils.readGamma2csisar import GammasarReader

if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    
    # set some flags
    input_check = True
    do_downsample = False
    output_check = False

    # CSI does most computations in a local Cartesian coordinate system. It presently supports only UTM projections, so we need to set the zone to use.
    lon0, lat0 = 87.5, 28.5
    # UTM zone 47 for 2025 Mw 6.9 Dingri earthquake
    utmzone, epsg = utm_zone_epsg(lon0, lat0)
    print(f'UTM zone: {utmzone}, EPSG: {epsg}')

    # Prepare InSAR data for Sentinel-1
    outName = 'S1_T012D'
    prefix = r'geo_20200308_20200320'
    mysar = GammasarReader(name='Dingri', lon0=lon0, lat0=lat0, directory_name='..')
    mysar.extract_raw_grd(prefix=prefix)
    mysar.read_from_gamma(downsample=1, apply_wavelength_conversion=True, zero2nan=True)

    # Remove Zero and NaN values and value where LOS equals 1
    mysar.checkZeros()
    mysar.checkNaNs()
    mysar.checkLosEqualsOne()

    # Covariance first estimate on original data
    covar = imcov('Covariance estimator',mysar, verbose=True)

    # mask out high deformation above earthquake rupture
    maskOut = [87.2, 87.6, 28.5, 28.8]
    covar.maskOut([maskOut])

    # We use the computeCovariance method to sample the dataset with a random set on 0.002 of the pixels, 
    # estimate and remove a ramp, calculate the semivariogram at distances of every 2 km out to 100 km, 
    # convert the semivariogram to covariance, and estimate a fit of an exponential function vs. distance.
    covar.computeCovariance(function='exp', frac=0.002, every=2.0, distmax=100., rampEst=True)
    covar.plot(data='all')
    covar.write2file(savedir='./')

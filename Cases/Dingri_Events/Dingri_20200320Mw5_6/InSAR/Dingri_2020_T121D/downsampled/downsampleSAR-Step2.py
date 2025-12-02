# External libraries
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
matplotlib.rcParams['figure.figsize'] = (30,30) # make the plots bigger

# CSI routines and ECAT routines
import csi.insar as insar
import csi.geodeticplot as geoplt
import csi.imagedownsampling as imagedownsampling
import csi.imagecovariance as imcov
from csi import faultwithdip
from csi.csiutils import utm_zone_epsg
from eqtools.csiExtend.sarUtils.readGamma2csisar import GammasarReader
from eqtools.plottools import sci_plot_style


if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

    # set some flags
    input_check = False
    do_covar = False
    do_downsample = True
    output_check = True

    # UTM zone 45 for Dingri earthquake
    lon0, lat0 = 87.5, 28.5
    # UTM zone 45 for 2025 Mw 6.9 Dingri earthquake
    utmzone, epsg = utm_zone_epsg(lon0, lat0)
    print(f'UTM zone: {utmzone}, EPSG: {epsg}')

    # set the output name root
    outName = 'S1_T121D'
    prefix = r'geo_20200316_20200328'
    mysar = GammasarReader(name='Dingri', lon0=lon0, lat0=lat0, directory_name='..')
    mysar.extract_raw_grd(prefix=prefix)
    mysar.read_from_gamma(downsample=1, apply_wavelength_conversion=True, zero2nan=True)

    # Remove Zero and NaN values and value where LOS equals 1
    mysar.checkZeros()
    mysar.checkNaNs()
    mysar.checkLosEqualsOne()

    # Covariance object
    covar = imcov('Covariance estimator',mysar, verbose=True)

    # see covarSAR notebook for details
    if do_covar:
        # Covariance first estimate on original data
        covar = imcov('Covariance estimator',mysar, verbose=True)
        # mask out high deformation above earthquake rupture
        maskOut = [87.2, 87.6, 28.5, 28.8]
        covar.maskOut([maskOut])
        # run the semi-variogram covariance calculation
        covar.computeCovariance(function='exp', frac=0.02, every=2.0, distmax=100., rampEst=True)
        # plot results
        covar.plot(data='all')
        # write estimated function to file
        covar.write2file(savedir='./')

    else:  # read in previous calculation
        covar.read_from_covfile('Covariance estimator','Covariance_estimator.cov')
        print ('read previously calculated covariance estimates')

    # Box for Dingri area data cropping
    minlat, maxlat, minlon, maxlon =  np.min(mysar.lat), np.max(mysar.lat), np.min(mysar.lon), np.max(mysar.lon)
    # Box for plotting (same for now)
    plotMinLat = minlat
    plotMaxLat = maxlat
    plotMinLon = minlon
    plotMaxLon = maxlon
    # select relevant area from data for downsampling
    maskOut = [87.2, 87.6, 28.5, 28.8]
    # mysar.select_pixels(minlon, maxlon, minlat, maxlat)
    mysar.select_pixels(*maskOut)

    # check area of image after cropping
    print ('cropped image area longitude {} to {}'.format(mysar.lon.min(),mysar.lon.max()))

    jcrect = None
    if do_downsample:
        downsampler = imagedownsampling('Downsampler', mysar, faults=jcrect)
        downsampler.initialstate(10, 0.5, tolerance=0.05, plot=False, decimorig=10)

    downsampler.stdBased(0.005, plot=False, verboseLevel='minimum', decimorig=10, smooth=2, itmax=100)
    # Reject pixels based on fault trace and distance with unit in km
    # downsampler.reject_pixels_fault(1, jcrect)
    # downsampler.dataBased(threshold=0.003, plot=False, verboseLevel='minimum', decimorig=10, quantity='curvature', smooth=10, itmax=100)
    downsampler.writeDownsampled2File(prefix=outName+'_ifg', rsp=True)

    # read the decimated data back in
    sardecim = insar('Decimated DataSet', lon0=lon0, lat0=lat0)
    sardecim.read_from_varres(outName+'_ifg', factor=1.0, step=0.0)

    # Check for zeros and NaNs and LOS=1
    sardecim.checkLosEqualsOne()
    sardecim.checkLOS()  # plot direction of the LOS vectors

    # add covariance estimate
    sardecim.Cd = covar.buildCovarianceMatrix(sardecim, 'Covariance estimator',write2file=outName+'_ifg.cov')

    fault = jcrect
    if output_check:
        with sci_plot_style(figsize='double', pdf_fonttype=42):
            gp = geoplt(figure=1,latmin=plotMinLat,lonmin=plotMinLon,latmax=plotMaxLat,lonmax=plotMaxLon,
                        remove_direction_labels=True)
            gp.drawCoastlines(parallels=0.2, meridians=0.2, drawOnFault=True, resolution='50m')
            # gp.faulttrace(fault)
            gp.insar(mysar, decim=10, plotType='scatter', markersize=3)
            gp.titlemap('{} original'.format(outName))
            gp.savefig(prefix='raw_', ftype='pdf', dpi=600, saveFig=['map'])

        with sci_plot_style(figsize='double', pdf_fonttype=42):
            gp2 = geoplt(figure=3,latmin=plotMinLat,lonmin=plotMinLon,latmax=plotMaxLat,lonmax=plotMaxLon,
                         remove_direction_labels=True)
            gp2.drawCoastlines(parallels=0.2, meridians=0.2, drawOnFault=True, resolution='50m')
            # gp2.faulttrace(fault)
            gp2.insar(sardecim, data='data', plotType='decimate')
            gp2.titlemap('{} decimated'.format(outName))
            gp2.savefig(prefix='downsample_', ftype='pdf', dpi=600, saveFig=['map'])



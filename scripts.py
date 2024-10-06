""" This the scripting function which will hold the basic scripts used to locate the DFPS fibers on the sky."""
import pandas as pd
import os
from config import Configuration
from astroquery.mast import Catalogs
from utils import Utils
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import logging
logging.getLogger('matplotlib.font_manager').disabled = True


class Scripts:

    @staticmethod
    def tic_search(ra_deg, dec_deg, fov_deg, mag_cut):
        """ This function will query the TIC at the give position and return all stars in a given magnitude cut-off.

        :parameter ra_deg - The right ascension of the target in degrees.
        :parameter dec_deg - The declination of the target in degrees.
        :parameter fov_deg - The radius of the search area.
        :parameter mag_cut - The magnitude cutoff for the given star field.

        :return catalog_data_clip - The final dataframe of stars in the search area (ra, dec, magnitude)
        """

        if os.path.isfile(Configuration.DATA_DIRECTORY + Configuration.FIELD_NAME + '.csv') is False:
            Utils.log("No region file found for field " + Configuration.FIELD_NAME + ". We will query MAST.", "info")
            # make the search string
            search_string = str(ra_deg) + " " + str(dec_deg)

            # query the TIC for the given region
            catalog_data = Catalogs.query_region(search_string, radius=fov_deg, catalog='TIC').to_pandas()

            # now only select the stars in the given magnitude range based on the GAIA magnitudes
            catalog_data_clip = catalog_data[["ra", "dec", "GAIAmag"]][catalog_data.GAIAmag < mag_cut]

            # rename magnitude column to magnitude for convenience
            catalog_data_clip = catalog_data_clip.rename(columns={"GAIAmag": "mag"})

            # dump the file to the data directory so we don't have to requery every few minutes
            catalog_data_clip.to_csv(Configuration.DATA_DIRECTORY + Configuration.FIELD_NAME + '.csv')
        else:
            Utils.log("Legacy region file found for field " + Configuration.FIELD_NAME +
                      ". We will use the legacy file if this is not what you want, delete the file!", "info")
            # read in the legacy file
            catalog_data_clip = pd.read_csv(Configuration.DATA_DIRECTORY + Configuration.FIELD_NAME + '.csv',
                                            index_col=0)

        return catalog_data_clip

    @staticmethod
    def pick_n_plot(stars, offsets, pixel_size, plate_scale):
        """ This function will allow you to plot the searched stars on an x/y plot, place the guide cameras,
        automatically place the fibers, place desired locations, and then return an offset.

        :parameter stars - A pandas data frame with the ra, dec, and magnitude of the stars in the field.
        :parameter offsets - A numpy array with the offsets between the guide cameras and the sensors.
        :parameter pixel_size - The pixel size of the guide cameras.
        :parameter plate_scale - The plate scale of the telescope to convert between image and sky.

        :return movements - An np.array of movements is returned also a text file is also output for each readibility.
        """

        fig, ax = plt.subplots()

        # plot the stars in ra dec
        plt.scatter(stars.ra, stars.dec, marker='*', c='k', s=(20 - stars.mag) * 5)

        # add the field of view of the telescope on the frame
        for x in range(0, 2):
            xx = [Configuration.RA_DEG + Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2,
                  Configuration.RA_DEG - Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2]
            if x == 0:
                yy = [Configuration.DEC_DEG - Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2,
                      Configuration.DEC_DEG - Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2]
            else:
                yy = [Configuration.DEC_DEG + Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2,
                      Configuration.DEC_DEG + Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2]

            plt.plot(xx, yy, c='r')

        # add the field of view of the telescope on the frame
        for x in range(0, 2):
            yy = [Configuration.DEC_DEG + Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2,
                  Configuration.DEC_DEG - Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2]
            if x == 0:
                xx = [Configuration.RA_DEG - Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2,
                      Configuration.RA_DEG - Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2]
            else:
                xx = [Configuration.RA_DEG + Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2,
                      Configuration.RA_DEG + Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG / 2]
            plt.plot(xx, yy, c='r')

        def on_click(event):
            if event.button == 3:  # Right click
                plt.clf()  # Clear the figure
                plt.draw()  # Redraw
                plt.show()
            else:
                ra_cam = event.xdata
                dec_cam = event.ydata

                # add the field of view of the telescope on the frame
                for x in range(0, 2):
                    xx = [ra_cam + Configuration.DFPS_GUIDE_CAMERA_SIZE / 2,
                          ra_cam - Configuration.DFPS_GUIDE_CAMERA_SIZE / 2]
                    if x == 0:
                        yy = [dec_cam - Configuration.DFPS_GUIDE_CAMERA_SIZE / 2,
                              dec_cam - Configuration.DFPS_GUIDE_CAMERA_SIZE / 2]
                    else:
                        yy = [dec_cam + Configuration.DFPS_GUIDE_CAMERA_SIZE / 2,
                              dec_cam + Configuration.DFPS_GUIDE_CAMERA_SIZE / 2]

                    plt.plot(xx, yy, c='b')

                # add the field of view of the telescope on the frame
                for x in range(0, 2):
                    yy = [dec_cam + Configuration.DFPS_GUIDE_CAMERA_SIZE / 2,
                          dec_cam - Configuration.DFPS_GUIDE_CAMERA_SIZE / 2]
                    if x == 0:
                        xx = [ra_cam - Configuration.DFPS_GUIDE_CAMERA_SIZE / 2,
                              ra_cam - Configuration.DFPS_GUIDE_CAMERA_SIZE / 2]
                    else:
                        xx = [ra_cam + Configuration.DFPS_GUIDE_CAMERA_SIZE / 2,
                              ra_cam + Configuration.DFPS_GUIDE_CAMERA_SIZE / 2]
                    plt.plot(xx, yy, c='b')

        cid = fig.canvas.mpl_connect('button_press_event', on_click)

        plt.ylabel('Declination [deg]')
        plt.xlabel('Right Ascension [deg]')
        plt.show()


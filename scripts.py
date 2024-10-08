""" This the scripting function which will hold the basic scripts used to locate the DFPS fibers on the sky."""
import pandas as pd
import numpy as np
import os
from config import Configuration
from astroquery.mast import Catalogs
from utils import Utils
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import logging
logging.getLogger('matplotlib.font_manager').disabled = True
matplotlib.pyplot.set_loglevel (level = 'warning')
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)


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
    def plot_a_box(cen_x, cen_y, sz_x, sz_y):
        """ This function will return the coordinates of a box that can be plotted.

        :parameter cen_x - this is the x coordinate of the box
        :parameter cen_y - this is the y coordinate of the box
        :parameter sz - This is the length of on box side

        :return box_x, box_y - Two numpy arrays are returned which will allow you to plot a box.

        """

        # set up x vertices
        x1 = cen_x - sz_x / 2.
        x2 = cen_x + sz_x / 2.

        # set up y vertices
        y1 = cen_y - sz_y / 2.
        y2 = cen_y + sz_y / 2.

        # set up the np.arrays
        box_x = np.array([x1, x1, x2, x2, x1])
        box_y = np.array([y1, y2, y2, y1, y1])

        return box_x, box_y

    @staticmethod
    def plot_guide_cameras(cam_x, cam_y, cam_num):
        """ This function will return the positions to plot the guide cameras based on the camera provided.

        :parameter cam_x - The x center for the camera
        :parameter cam_y - The y center for the camera
        :parameter cam_num - The camera you selected on the image

        :return The required positions of all 4 cameras will be returned.
        """

        # convert the distance between cameras from x/y to ra/dec
        cam_off = (Configuration.DFPS_GUIDE_CAMERA_DIST * Configuration.OTTO_STRUVE_PLATE_SCALE) / 3600.
        if cam_num == '1':
            guide_cam_1_x, guide_cam_1_y = Scripts.plot_a_box(cam_x, cam_y, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_2_x, guide_cam_2_y = Scripts.plot_a_box(cam_x + cam_off, cam_y, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_3_x, guide_cam_3_y = Scripts.plot_a_box(cam_x, cam_y - cam_off, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_4_x, guide_cam_4_y = Scripts.plot_a_box(cam_x + cam_off, cam_y - cam_off, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
        elif cam_num == '2':
            guide_cam_1_x, guide_cam_1_y = Scripts.plot_a_box(cam_x - cam_off, cam_y, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_2_x, guide_cam_2_y = Scripts.plot_a_box(cam_x, cam_y, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_3_x, guide_cam_3_y = Scripts.plot_a_box(cam_x - cam_off, cam_y - cam_off, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_4_x, guide_cam_4_y = Scripts.plot_a_box(cam_x, cam_y - cam_off, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
        elif cam_num == '3':
            guide_cam_1_x, guide_cam_1_y = Scripts.plot_a_box(cam_x, cam_y + cam_off, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_2_x, guide_cam_2_y = Scripts.plot_a_box(cam_x + cam_off, cam_y + cam_off, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_3_x, guide_cam_3_y = Scripts.plot_a_box(cam_x, cam_y, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_4_x, guide_cam_4_y = Scripts.plot_a_box(cam_x + cam_off, cam_y, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
        else:
            guide_cam_1_x, guide_cam_1_y = Scripts.plot_a_box(cam_x - cam_off, cam_y + cam_off, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_2_x, guide_cam_2_y = Scripts.plot_a_box(cam_x, cam_y + cam_off, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_3_x, guide_cam_3_y = Scripts.plot_a_box(cam_x - cam_off, cam_y, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)
            guide_cam_4_x, guide_cam_4_y = Scripts.plot_a_box(cam_x, cam_y, Configuration.DFPS_GUIDE_CAMERA_FOV_X, Configuration.DFPS_GUIDE_CAMERA_FOV_Y)

        return guide_cam_1_x, guide_cam_1_y, guide_cam_2_x, guide_cam_2_y, guide_cam_3_x, guide_cam_3_y ,guide_cam_4_x, guide_cam_4_y

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

        fig, ax = plt.subplots(figsize=[8,6])

        # plot the stars in ra dec
        plt.scatter(stars.ra, stars.dec, marker='*', c='k', s=(20 - stars.mag) * 10)

        # add the field of view of the telescope on the image
        telescope_fov_x, telescope_fov_y = Scripts.plot_a_box(Configuration.RA_DEG,
                                                              Configuration.DEC_DEG,
                                                              Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG,
                                                              Configuration.OTTO_STRUVE_FIELD_OF_VIEW_DEG)
        plt.plot(telescope_fov_x, telescope_fov_y, c='g', label='Telescope')

        # now add the instrument cameras for reference on the image
        def on_click_cams(event):
            if event.button == 3:
                prompt = "Which camera canter are you trying to place?"
                cam = input(prompt)

                x = event.xdata
                y = event.ydata

                # get the positional information for the cameras
                gc_1x, gc_1y, gc_2x, gc_2y, gc_3x, gc_3y, gc_4x, gc_4y = Scripts.plot_guide_cameras(x, y, cam)

                plt.plot(gc_1x, gc_1y, c='r')
                plt.text(gc_1x[0], gc_1y[0], 'Guide-1')
                plt.plot(gc_2x, gc_2y, c='r')
                plt.text(gc_2x[0], gc_2y[0], 'Guide-2')
                plt.plot(gc_3x, gc_3y, c='r')
                plt.text(gc_3x[0], gc_3y[0], 'Guide-3')
                plt.plot(gc_4x, gc_4y, c='r')
                plt.text(gc_4x[0], gc_4y[0], 'Guide-4')
                plt.show()

                # now dump the positions to a text file for later
                f = open(Configuration.ANALYSIS_DIRECTORY + "guide_camera_positions.txt", "w")
                for idx in range(0, 5):
                    line = str(gc_1x[idx]) + ' ' + str(gc_1y[idx]) + ' ' + \
                           str(gc_2x[idx]) + ' ' + str(gc_2y[idx]) + ' ' + \
                           str(gc_3x[idx]) + ' ' + str(gc_3y[idx]) + ' ' + \
                           str(gc_4x[idx]) + ' ' + str(gc_4y[idx]) + "\n"
                    f.write(line)
                f.close()

        cid = fig.canvas.mpl_connect('button_press_event', on_click_cams)

        plt.ylabel('Declination [deg]')
        plt.xlabel('Right Ascension [deg]')
        plt.gca().invert_xaxis()
        plt.legend()
        plt.show()
        plt.close()

        fig, ax = plt.subplots(figsize=[8,6])

        # re-plot for the star pickers
        plt.scatter(stars.ra, stars.dec, marker='*', c='k', s=(20 - stars.mag) * 10)
        plt.plot(telescope_fov_x, telescope_fov_y, c='g', label='Telescope')

        # re-plot the camera positions
        gc = pd.read_csv(Configuration.ANALYSIS_DIRECTORY + 'guide_camera_positions.txt', sep=' ',
                         names=['gc_1x', 'gc_1y', 'gc_2x', 'gc_2y','gc_3x', 'gc_3y', 'gc_4x', 'gc_4y'])

        plt.plot(gc.gc_1x, gc.gc_1y, c='r', label='Guide Cameras')
        plt.text(gc.gc_1x[0], gc.gc_1y[0], 'Guide-1')
        plt.plot(gc.gc_2x, gc.gc_2y, c='r')
        plt.text(gc.gc_2x[0], gc.gc_2y[0], 'Guide-2')
        plt.plot(gc.gc_3x, gc.gc_3y, c='r')
        plt.text(gc.gc_3x[0], gc.gc_3y[0], 'Guide-3')
        plt.plot(gc.gc_4x, gc.gc_4y, c='r')
        plt.text(gc.gc_4x[0], gc.gc_4y[0], 'Guide-4')
        plt.legend()

        def on_click_fibers(event):
            if event.button == 3:  # Left click

                prompt = "Which camera is the star you are trying to place in?"
                cam = input(prompt)

                if cam == '1':
                    off_x = Configuration.OFFSET_X_1
                    off_y = Configuration.OFFSET_Y_1
                elif cam == '2':
                    off_x = Configuration.OFFSET_X_2
                    off_y = Configuration.OFFSET_Y_2
                elif cam == '3':
                    off_x = Configuration.OFFSET_X_3
                    off_y = Configuration.OFFSET_Y_3
                else:
                    off_x = Configuration.OFFSET_X_4
                    off_y = Configuration.OFFSET_Y_4

                # get the data from the figure
                global x, y
                x = event.xdata
                y = event.ydata

                # get the camera verticies
                plt.scatter(x, y, c='r', marker='.')

                # now plot the fiber on the frame

                offset_x = (Configuration.OTTO_STRUVE_PLATE_SCALE * off_x) / 3600
                offset_y = (Configuration.OTTO_STRUVE_PLATE_SCALE * off_y) / 3600

                plt.scatter(x + offset_x, y + offset_y, c='b')
                plt.show()

                # now dump the fiber position to a text file
                # now dump the positions to a text file for later
                f = open(Configuration.ANALYSIS_DIRECTORY + "camera_" + cam + "_fiber_position.txt", "w")
                f.write(str(x + offset_x) + " " + str(y + offset_y) + "\n")
                f.close()

        cid = fig.canvas.mpl_connect('button_press_event', on_click_fibers)

        plt.ylabel('Declination [deg]')
        plt.xlabel('Right Ascension [deg]')
        plt.gca().invert_xaxis()
        plt.show()
        plt.close()

        fig, ax = plt.subplots(figsize=[8,6])

        # re-plot for the star pickers
        plt.scatter(stars.ra, stars.dec, marker='*', c='k', s=(20 - stars.mag) * 10)
        plt.plot(telescope_fov_x, telescope_fov_y, c='g', label='Telescope')

        # re-plot the camera positions
        plt.plot(gc.gc_1x, gc.gc_1y, c='r', label='Guide Cameras')
        plt.text(gc.gc_1x[0], gc.gc_1y[0], 'Guide-1')
        plt.plot(gc.gc_2x, gc.gc_2y, c='r')
        plt.text(gc.gc_2x[0], gc.gc_2y[0], 'Guide-2')
        plt.plot(gc.gc_3x, gc.gc_3y, c='r')
        plt.text(gc.gc_3x[0], gc.gc_3y[0], 'Guide-3')
        plt.plot(gc.gc_4x, gc.gc_4y, c='r')
        plt.text(gc.gc_4x[0], gc.gc_4y[0], 'Guide-4')

        # re-plot the current fiber positions
        fiber1 = pd.read_csv(Configuration.ANALYSIS_DIRECTORY + 'camera_1_fiber_position.txt', sep=' ',
                         names=['fb_x', 'fb_y'])
        fiber2 = pd.read_csv(Configuration.ANALYSIS_DIRECTORY + 'camera_2_fiber_position.txt', sep=' ',
                         names=['fb_x', 'fb_y'])
        fiber3 = pd.read_csv(Configuration.ANALYSIS_DIRECTORY + 'camera_3_fiber_position.txt', sep=' ',
                         names=['fb_x', 'fb_y'])
        fiber4 = pd.read_csv(Configuration.ANALYSIS_DIRECTORY + 'camera_4_fiber_position.txt', sep=' ',
                         names=['fb_x', 'fb_y'])

        plt.scatter(fiber1.fb_x, fiber1.fb_y, c='b', label='Fibers')
        plt.text(fiber1.fb_x[0], fiber1.fb_y[0], 'Fiber-1')
        plt.scatter(fiber2.fb_x, fiber2.fb_y, c='b')
        plt.text(fiber2.fb_x[0], fiber2.fb_y[0], 'Fiber-2')
        plt.scatter(fiber3.fb_x, fiber3.fb_y, c='b')
        plt.text(fiber3.fb_x[0], fiber3.fb_y[0], 'Fiber-3')
        plt.scatter(fiber4.fb_x, fiber4.fb_y, c='b')
        plt.text(fiber4.fb_x[0], fiber4.fb_y[0], 'Fiber-4')

        # now we want to select the stars we want to move to
        def on_click_stars(event):
            if event.button == 3:  # Left click

                prompt = "Which fiber do you want to move to this star?"
                fiber = input(prompt)

                if fiber == '1':
                    fb_x = fiber1.fb_x[0]
                    fb_y = fiber1.fb_y[0]
                elif fiber == '2':
                    fb_x = fiber2.fb_x[0]
                    fb_y = fiber2.fb_y[0]
                elif fiber == '3':
                    fb_x = fiber3.fb_x[0]
                    fb_y = fiber3.fb_y[0]
                else:
                    fb_x = fiber4.fb_x[0]
                    fb_y = fiber4.fb_y[0]

                # get the data from the figure
                global x, y
                x = event.xdata
                y = event.ydata

                # get the camera verticies
                plt.scatter(x, y, s=80, facecolors='none', edgecolors='gold')

                # now get the offset in mm
                offset_x = ((x - fb_x) * 3600) / Configuration.OTTO_STRUVE_PLATE_SCALE
                offset_y = ((y - fb_y) * 3600) / Configuration.OTTO_STRUVE_PLATE_SCALE

                plt.text(x, y, 'Fiber ' + fiber + ' Offset X: ' + str(np.around(offset_x, decimals=3)) + "mm Y: " + str(np.around(offset_y, decimals=3)) + "mm")
                plt.show()

                f = open(Configuration.ANALYSIS_DIRECTORY + "fiber_" + fiber + "_change.txt", "w")
                f.write(str(x + offset_x) + " " + str(y + offset_y) + "\n")
                f.close()


        cid = fig.canvas.mpl_connect('button_press_event', on_click_stars)

        plt.legend(loc='upper right')
        plt.ylabel('Declination [deg]')
        plt.xlabel('Right Ascension [deg]')
        plt.gca().invert_xaxis()
        plt.show()
        plt.close()
        print('hold')

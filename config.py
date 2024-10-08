""" This serves as the configuration file for the DFPS Sky Positioner. """


class Configuration:

    # these are star field specific information
    FIELD_NAME = "WASP-52"
    RA_DEG = 348.4948229
    DEC_DEG = 8.7612697

    # update the offsets between the center of each guide camera and the fiber in mm
    # positive is right or up, negative is left or down
    OFFSET_X_1 = 5
    OFFSET_Y_1 = -5

    OFFSET_X_2 = -2
    OFFSET_Y_2 = -2

    OFFSET_X_3 = -10
    OFFSET_Y_3 = 3

    OFFSET_X_4 = 5
    OFFSET_Y_4 = 10

    OFFSETS = [[OFFSET_X_1, OFFSET_X_2, OFFSET_X_3, OFFSET_X_4], [OFFSET_Y_1, OFFSET_Y_2, OFFSET_Y_3, OFFSET_Y_4]]

    # these are computer specific information
    MACHINE = "moon"
    MACHINE_TYPE = "linux"

    if MACHINE_TYPE == "windows":
        DIRECTORY_DELIM = "\\"
    else:
        DIRECTORY_DELIM = "/"

    # telescope specific information
    OTTO_STRUVE_PLATE_SCALE = 7.23  # arcsec / mm
    OTTO_STRUVE_FIELD_OF_VIEW_ARCMIN = 7  # arcmin
    OTTO_STRUVE_FIELD_OF_VIEW_DEG = OTTO_STRUVE_FIELD_OF_VIEW_ARCMIN / 60.

    # this is instrument specific information
    UM_TO_MM = 0.001
    DFPS_PIXEL_SCALE = 7.4  # micron / pixel
    DFPS_GUIDE_CAMERA_X = 520  # pixels
    DFPS_GUIDE_CAMERA_Y = 700  # pixels
    DFPS_GUIDE_CAMERA_FOV_X = DFPS_GUIDE_CAMERA_X * DFPS_PIXEL_SCALE * UM_TO_MM * OTTO_STRUVE_PLATE_SCALE / 3600
    DFPS_GUIDE_CAMERA_FOV_Y = DFPS_GUIDE_CAMERA_X * DFPS_PIXEL_SCALE * UM_TO_MM * OTTO_STRUVE_PLATE_SCALE / 3600
    DFPS_GUIDE_CAMERA_DIST = 45  # mm

    # these are TIC search specific information
    SEARCH_RADIUS_ARCMIN = OTTO_STRUVE_FIELD_OF_VIEW_ARCMIN + 3  # add an X arcmin buffer
    SEARCH_RADIUS_DEG = SEARCH_RADIUS_ARCMIN / 60. / 2.  # convert to degrees and divide by 2 to get the radius
    MAGNITUDE_CUTOFF = 16  # this is the lower limit of the magnitudes to keep

    # this is the directory information
    WORKING_DIRECTORY = "/home/oelkerrj/Development/dfps_sky/"
    ANALYSIS_DIRECTORY = WORKING_DIRECTORY + 'analysis/'
    LOG_DIRECTORY = WORKING_DIRECTORY + 'logs/'

    # input paths for data etc
    DATA_DIRECTORY = WORKING_DIRECTORY + "data/"

    # directory_list
    DIRECTORIES = [ANALYSIS_DIRECTORY, DATA_DIRECTORY, LOG_DIRECTORY]

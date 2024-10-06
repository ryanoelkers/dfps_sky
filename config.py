""" This serves as the configuration file for the DFPS Sky Positioner. """


class Configuration:

    # these are star field specific informations
    FIELD_NAME = "Albireo"
    RA_DEG = 292.6803333
    DEC_DEG = 27.9596750

    # update the offsets between the center of each guide camera and the fiber in mm
    # positive is right or up, negative is left or down
    OFFSET_X_1 = 20
    OFFSET_Y_1 = -20

    OFFSET_X_2 = -10
    OFFSET_Y_2 = -20

    OFFSET_X_3 = -15
    OFFSET_Y_3 = 20

    OFFSET_X_4 = 15
    OFFSET_Y_4 = 20

    OFFSETS = [[OFFSET_X_1, OFFSET_X_2, OFFSET_X_3, OFFSET_X_4], [OFFSET_Y_1, OFFSET_Y_2, OFFSET_Y_3, OFFSET_Y_4]]

    # these are computer specific informations
    MACHINE = "moon"
    MACHINE_TYPE = "windows"

    if MACHINE_TYPE == "windows":
        DIRECTORY_DELIM = "\\"
    else:
        DIRECTORY_DELIM = "/"

    # this is instrument specific information
    DFPS_PIXEL_SCALE = 7.4  # micron / pixel
    DFPS_GUIDE_CAMERA_SIZE = 30  # arcsec in diameter
    OTTO_STRUVE_PLATE_SCALE = 7.23  # arcsec / mm
    OTTO_STRUVE_FIELD_OF_VIEW_ARCMIN = 7  # arcmin
    OTTO_STRUVE_FIELD_OF_VIEW_DEG = OTTO_STRUVE_FIELD_OF_VIEW_ARCMIN / 60.

    # these are TIC search specific information
    SEARCH_RADIUS_ARCMIN = OTTO_STRUVE_FIELD_OF_VIEW_ARCMIN + 3  # add an X arcmin buffer
    SEARCH_RADIUS_DEG = SEARCH_RADIUS_ARCMIN / 60. / 2.  # convert to degrees and divide by 2 to get the radius
    MAGNITUDE_CUTOFF = 14  # this is the lower limit of the magnitudes to keep

    # this is the directory informations
    WORKING_DIRECTORY = "D:\\ryanj\\Development\\dfps_sky\\"
    ANALYSIS_DIRECTORY = WORKING_DIRECTORY + 'analysis\\'
    LOG_DIRECTORY = WORKING_DIRECTORY + 'logs\\'

    # input paths for data etc
    DATA_DIRECTORY = WORKING_DIRECTORY + "data\\"

    # directory_list
    DIRECTORIES = [ANALYSIS_DIRECTORY, DATA_DIRECTORY, LOG_DIRECTORY]

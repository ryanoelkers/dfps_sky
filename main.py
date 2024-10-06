""" This is the main script to wrap the TIC search and plotting functions for the DFPS Sky Locator."""

from utils import Utils
from config import Configuration
from scripts import Scripts

# do the necessary prep work such as making the directories
Utils.create_directories(Configuration.DIRECTORIES)

# search the TIC at the given position for stars
stars = Scripts.tic_search(Configuration.RA_DEG,
                           Configuration.DEC_DEG,
                           Configuration.SEARCH_RADIUS_DEG,
                           Configuration.MAGNITUDE_CUTOFF)

# generate the figure with the stars and start the position picker to allow the fiber locator
positions = Scripts.pick_n_plot(stars,
                                Configuration.OFFSETS,
                                Configuration.DFPS_PIXEL_SCALE,
                                Configuration.OTTO_STRUVE_PLATE_SCALE)


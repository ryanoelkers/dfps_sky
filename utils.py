""" This class is used to store the basic functions used by the main function."""
from config import Configuration
import logging
import os


class Utils:

    @staticmethod
    def log(statement, level):
        """ The logger function to log all activity from the program to both the screen, and a file.

        :argument statement: A string which shows want needs to be logged
        :argument level:- The type of statement: info, debug, etc

        :return - Nothing is returned, but the log is updated and possibly the log is printed to the screen
        """

        # create the logger
        logging.basicConfig(format="%(asctime)s - %(levelname)s: %(message)s",
                            filename=Configuration.LOG_DIRECTORY + "dfps.log",
                            filemode='a')
        logger = logging.getLogger()

        if not getattr(logger, 'handler_set', None):
            logger.setLevel(logging.DEBUG)

            # create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            # create the formatter
            formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

            # add formatter to ch
            ch.setFormatter(formatter)

            # add ch to logger
            logger.addHandler(ch)

            # 'set' Handler
            logger.handler_set = True

        if level == 'info':
            logger.info(statement)
        if level == 'debug':
            logger.debug(statement)
        if level == 'warning':
            logger.warning(statement)
        if level == 'error':
            logger.error(statement)
        if level == 'critical':
            logger.critical(statement)

    @staticmethod
    def get_file_list(path, file_ext):
        """ This function will return the files in a given directory without their extension.
        :parameter path - A string with the path the file.
        :parameter file_ext - The file type to make a list, generally something like *.fits.

        :return files_no_ext - A list of files without the extension."""

        # get the files in the given path directory with the given file extension
        file_list = [f for f in os.listdir(path) if f.endswith(file_ext)]

        # sort based on the number of the image, first taken image will be first
        file_list.sort(key=len)

        return file_list

    @staticmethod
    def create_directories(directory_list):
        """ This function will check for each directory in directory list, and create it if it doesn't already exist

        :parameter directory_list - The list of directories to create

        :return - Nothing is returned but directories are created if necessary
        """

        for path in directory_list:
            # if the path does not exist then create it!
            if os.path.exists(path) is False:
                os.mkdir(path)
                Utils.log(path + ' created.', 'info')
'''
A logger for our software
'''
import os
import logging


class Logger:
    '''
    static logger class
    '''
    logger = None

    @staticmethod
    def get_logger(logger_name='logger', loglevel='INFO'):
        '''
        returns a logger
        if no logger was created yet, it will create a logger with the name
        specified in logger_name with the level specified in loglevel.
        If the logger was created for the first time the arguments do not change
        anything at the behaviour anymore
        '''
        if Logger.logger is None:
            Logger.logger = logging.getLogger(logger_name)
            Logger.logger.setLevel(loglevel)

            # Create handlers and set their logging level
            logfolder = 'zoutput/logs'
            os.makedirs(logfolder, exist_ok=True)
            # Create handlers and set their logging level
            filehandler = logging.FileHandler(logfolder + '/' + Logger.logger.name + '.log',
                                              mode='w')
            filehandler.setLevel(loglevel)
            # Add handlers to logger
            Logger.logger.addHandler(filehandler)
        return Logger.logger

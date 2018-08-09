##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Class which can be used to log things, saved locally, sent     #
# within an email, etc.                                          #
##################################################################

import logging
from logging.handlers import SMTPHandler, TimedRotatingFileHandler

# Formatting logging
formatter = logging.Formatter('[%(levelname)s] %(asctime)s: %(message)s')

class CustomLogger:
    def __init__(self, logger):
        self.logger = logger

    def set_mail_handler(self, mail_subject, level_to_catch = logging.WARNING):
        self._create_full_handler(self._create_mail_handler(mail_subject), level_to_catch)

    def set_file_handler(self, file_name, level_to_catch = logging.DEBUG):
        self._create_full_handler(self._create_file_handler(file_name), level_to_catch)

    def set_terminal_handler(self, level_to_catch = logging.INFO):
        self._create_full_handler(self._create_terminal_handler(), level_to_catch)

    def _create_mail_handler(self, mail_subject):
        return SMTPHandler("smtp.heig-vd.ch", "remi.jacquemard@heig-vd.ch", ["remi.jacquemard@heig-vd.ch"], mail_subject)   

    def _create_file_handler(self, file_name):
        return TimedRotatingFileHandler(file_name, when='midnight')

    def _create_terminal_handler(self):
        return logging.StreamHandler()

    def _create_full_handler(self, handler, level_to_catch):
        handler.setLevel(level_to_catch)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


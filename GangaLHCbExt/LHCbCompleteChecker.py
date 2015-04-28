################################################################################
# Ganga Project. http://cern.ch/ganga
#
################################################################################

from Ganga.GPIDev.Base import GangaObject
from Ganga.GPIDev.Adapters.IPostProcessor import PostProcessException, IPostProcessor
from Ganga.GPIDev.Base.Proxy import GPIProxyObject
#from Ganga.Lib.Checkers.Checker import MetaDataChecker
from Ganga.GPIDev.Adapters.IChecker import IChecker
from Ganga.GPIDev.Schema import ComponentItem, FileItem, Schema, SimpleItem, Version
from Ganga.Utility.Config import makeConfig, ConfigError, getConfig
from Ganga.Utility.Plugin import allPlugins
from Ganga.Utility.logging import getLogger, log_user_exception
import commands
import copy
import os
import string
logger = getLogger()


class LHCbCompleteChecker(IChecker):
    """
    Checks that all input files were fully processed (using the metadata).

    Example:
    job.postprocessors.append(LHCbCompleteChecker())
    """
    _schema = IChecker._schema.inherit_copy()
    _category = 'postprocessor'
    _name = 'LHCbCompleteChecker'

    def check(self, job):
        """Checks metadata of job is within a certain range."""
        try:
            nfullfiles = int(job.metadata['xmldatanumbers'].get('full', 0))
        except KeyError:
            raise PostProcessException("The metadata value 'xmldatanumbers' was not defined")
        try:
            nskipped = len(job.metadata['xmlskippedfiles'])
        except KeyError:
            raise PostProcessException("The metadata value 'xmlskippedfiles' was not defined")

        ok = (nfullfiles == len(job.inputdata)) and (nskipped == 0)
        if not ok:
            logger.info('LHCbCompleteChecker has failed job(%s)'%(job.fqid))
        return ok
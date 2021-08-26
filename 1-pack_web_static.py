#!/usr/bin/python3
""" module to compress a file """

from datetime import datetime
from fabric.api import local
import os.path


def do_pack():
    """ function to compress a file using facric"""
    dt = datetime.utcnow()
    fl = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                       dt.month,
                                                       dt.day,
                                                       dt.hour,
                                                       dt.minute,
                                                       dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(fl)).failed is True:
        return None
    return fl

#!/usr/bin/python3
""" module to deploy the archive to the server """

from fabric.api import run, put, env, local
import os.path
import datetime import datetime


env.hosts = ["34.75.251.99", "35.237.151.121"]


def deploy():
    """ fucntion to deploy the web static """
    file_name = do_pack()
    if file_name is None:
        return False
    return do_deploy(file_name)


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


def do_deploy(archive_path):
    """ function to deploy the archive to the remote server"""

    if os.path.isfile(archive_path) is False:
        return False
    file_name = archive_path.split("/")[-1]
    fn_only = file_name.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(fn_only)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(fn_only)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file_name, fn_only)).failed is True:
        return False
    if run("rm /tmp/{}".format(file_name)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".
           format(fn_only, fn_only)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(fn_only)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ "
           "/data/web_static/current".format(fn_only)).failed is True:
        return False
    return True

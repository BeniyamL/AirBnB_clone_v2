#!/usr/bin/python3
""" module to deploy the archive to the server """

from fabric.api import run, put, env, local
import os.path
from datetime import datetime


env.hosts = ["34.75.251.99", "35.237.151.121"]

env.user = "ubuntu"


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

    if os.path.exists(archive_path) is False:
        return False
    arch_name = archive_path.split("/")[-1]
    f_name = arch_name.split(".")[0]
    arch_path = "/tmp/{}".format(arch_name)
    f_path = "/data/web_static/releases/{}/".format(f_name)

    run("sudo mkdir -p {}".format(f_path))
    put(archive_path, "/tmp/")
    run("sudo tar -xzf {} -C {}".format(arch_path, f_path))
    run("sudo rm {}".format(arch_path))
    run("sudo mv -f {}web_static/* {}".format(f_path, f_path))
    run("sudo rm -rf {}web_static".format(f_path))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {} /data/web_static/current".format(f_path))
    return True

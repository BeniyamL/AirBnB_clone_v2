#!/usr/bin/python3
""" module to deploy clean the out date archive """

from fabric.api import *
import os.path

env.hosts = ["34.75.251.99", "35.237.151.121"]

env.user = "ubuntu"


def do_clean(number=0):
    """ function to clearn the out date archive"""
    if number == 0:
        number = 1
    else:
        number = int(number)
    if number >= 0:
        with lcd("versions"):
            all_files = find_out_dated(number, 'local')
            for each_file in all_files:
                local("rm -f {file}".format(file=each_file))

        with cd("/data/web_static/releases"):
            all_folders = find_out_dated(number, 'remote')
            for each_folder in all_folders:
                run("rm -rf {folder}".format(folder=each_folder))


def find_out_dated(number, tp):
    """ function to find the outdated file """
    if tp == 'local':
        all_archive = local("ls -td web_static_*", capture=True)
    elif tp == 'remote':
        all_archive = run("ls -td web_static_*")

    arch_list = all_archive.split()
    out_date_arch = arch_list[number:]
    return out_date_arch

#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["34.232.69.124", "34.207.83.226"]

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    formatted_date = dt.strftime("%Y%m%d%H%M%S")
    file = f"versions/web_static_{formatted_date}.tgz"

    if os.path.isdir("versions") and not local("tar -cvzf {} web_static".format(file)).failed:
        return file
    return None

def do_deploy(archive_path):
    """Distribute an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        False if the file doesn't exist at archive_path or an error occurs, otherwise True.
    """
    if not os.path.isfile(archive_path):
        return False

    file = os.path.basename(archive_path)
    name = os.path.splitext(file)[0]
    remote_tmp_path = "/tmp/{}".format(file)
    remote_release_path = "/data/web_static/releases/{}".format(name)

    # Upload archive to remote server
    if put(archive_path, remote_tmp_path).failed:
        return False

    # Set up release directory
    if run("sudo rm -rf {} {}".format(remote_release_path, remote_tmp_path)).failed:
        return False

    if run("sudo mkdir -p {}".format(remote_release_path)).failed:
        return False

    # Extract archive
    if run("sudo tar -xzf {} -C {}".format(remote_tmp_path, remote_release_path)).failed:
        return False

    # Clean up temporary files
    if run("sudo rm {}".format(remote_tmp_path)).failed:
        return False

    # Move contents and create symbolic link
    if run("sudo mv {}/web_static/* {}".format(remote_release_path, remote_release_path)).failed:
        return False

    if run("sudo rm -rf {}/web_static".format(remote_release_path)).failed:
        return False

    if run("sudo rm -rf /data/web_static/current").failed:
        return False

    if run("sudo ln -s {} /data/web_static/current".format(remote_release_path)).failed:
        return False

    return True

def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    return file is not None and do_deploy(file)


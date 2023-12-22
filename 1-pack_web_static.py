#!/usr/bin/python3
# Fabfile to generate a .tgz archive from contents of the  web_static.
import os
from datetime import datetime
from fabric.api import local

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    # Ensure the 'versions' directory exists
    local("mkdir -p versions")

    # Generate the filename using current date and time
    dt = datetime.utcnow()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )

    # Create the tar.gz archive
    result = local("tar -cvzf {} web_static".format(file_name))

    if result.failed:
        return None
    else:
        print("web_static packed: {}".format(file_name))
        return file_name


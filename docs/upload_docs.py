# -*- coding: utf-8 -*-
"""
Zip the docs then send them to our HostTheDocs server.
"""
import os
import sys
import zipfile
import subprocess

import requests

sys.path.insert(0, os.path.abspath('..'))
from douglib import __version__                     # noqa
from douglib import __description__                 # noqa
from douglib import __package_name__                # noqa


def zipdir(path, zip_handle):
    """
    Add all files in ``path`` to the zip file referenced by ``zip_handle``.

    Parameters
    ----------
    path : str (path to directory)
        The directory to package.
    zip_handle : :class:`zipfile.ZipFile` object
        The reference to the zip file.

    Returns
    -------
    None

    Notes
    -----
    Stolen from http://stackoverflow.com/a/1855118/1354930

    Thanks @mark-byers!
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.normpath(os.path.join(root, file))

            # create a relative path so that the full tree doesn't get added.
            archive_path = os.path.relpath(full_path, path)

            zip_handle.write(full_path, arcname=archive_path)


def create_zip(folder, file):
    """
    Create a zip file with the contents of ``folder``.

    Parameters
    ----------
    folder : str (path to directory)
        The directory to package.
    file : str
        The path of the resulting zip file. The ``.zip`` extension
        is appended if it doesn't already exist.

    Returns
    -------
    path : str (path)
        The absolute path to the zip file that was created.
    """
    # check the inputs
    ext = ".zip"
    if not os.path.isdir(folder):
        raise NotADirectoryError("`{}` is not a directory".format(folder))
    if os.path.splitext(file)[1] != ext:
        file += ext

    print("Zipping file.")
    with zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED) as myzip:
        zipdir(folder, myzip)

    return os.path.abspath(file)


def build_docs():
    """
    Builds docs using sphinx's ``make.bat`` file.

    TODO: Convert to pure python?

    set BUILDDIR=_build
    set ALLSPHINXOPTS=-d %BUILDDIR%/doctrees %SPHINXOPTS% .
    set SPHINXBUILD=python -m sphinx.__init__

    if "%1" == "html" (
      %SPHINXBUILD% -b html %ALLSPHINXOPTS% %BUILDDIR%/html
      if errorlevel 1 exit /b 1
      echo.
      echo.Build finished. The HTML pages are in %BUILDDIR%/html.
      goto end
    )

    """
    print("Building Docs")
    cmd = 'make'
    if sys.platform == 'win32':
        cmd = 'make.bat'
    args = [cmd, 'html']

    print("Running subprocess with args: {}".format(args))
    rv = subprocess.run(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    print(rv.stdout.decode('UTF-8'))

#    from sphinx import cmdline
#    cmdline.main(
#        ['C:/gitlab/dthor/wtns-web/docs',
#         '-b', 'html',
#         '-d', '_build/doctrees',
#         '_build/html',
#         ],
#    )


if __name__ == "__main__":

    build_docs()

    directory = os.path.normpath(os.path.join(os.getcwd(), "_build/html"))
    print("directory = {}".format(directory))
    file = 'html.zip'
    print("file = {}".format(file))

    zippath = create_zip(directory, file)

    data = {
        "name": __package_name__,
        "version": __version__,
        "description": __description__,
    }

    files = {
        "archive": ("archive.zip", open(zippath, 'rb'))
    }

    print("Sending POST to upload files")
    resp = requests.post(
        'http://tphweb.tph.local/rtd/hmfd',
        data=data,
        files=files,
    )

    print("Response: {}".format(resp))

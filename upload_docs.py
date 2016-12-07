# -*- coding: utf-8 -*-

import requests

from douglib import __version__, __project_name__, __description__
print(__version__)
print(__project_name__)
print(__description__)

zippath = "C:/gitlab/dthor/DougLib/docs/_build/html.zip"

data = {
    "name": __project_name__,
    "version": __version__,
    "description": __description__,
}

files = {
    "archive": ("archive.zip", open(zippath, 'rb'))
}


a = requests.post(
    'http://tphweb.tph.local/rtd/hmfd',
    data=data,
    files=files,
)

print(a)

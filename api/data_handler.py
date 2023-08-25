"""
Functions for loading neurophysiology data from publicly-shared data files with Neo.

Copyright CNRS 2023
Authors: Andrew P. Davison, Onur Ates, Shailesh Appukuttan, Hélissande Fragnaud and Corentin Fragnaud
Licence: MIT (see LICENSE)
"""

import os.path
import hashlib
from urllib.request import urlopen, urlretrieve, HTTPError
from urllib.parse import urlparse, urlunparse
from fastapi import HTTPException, status
import neo.io

from . import settings


def get_cache_path(url):
    """
    For caching, we store files in a flat directory structure, where the directory name is
    based on the URL, but files in the same directory on the original server end up in the
    same directory in our cache.
    """
    url_parts = urlparse(url)
    base_url = urlunparse(
        (
            url_parts.scheme,
            url_parts.netloc,
            os.path.dirname(url_parts.path),
            "",
            "",
            "",
        )
    )
    dir_name = hashlib.sha1(base_url.encode("utf-8")).hexdigest()
    dir_path = os.path.join(
        getattr(settings, "DOWNLOADED_FILE_CACHE_DIR", ""), dir_name
    )
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, os.path.basename(url_parts.path))


def download_neo_data(url):
    """
    Download a neo data file from the given URL.

    We do not at present handle formats that require multiple files,
    for which the URL should probably point to a zip or tar archive.
    """
    # we first open the url to resolve any redirects and have a consistent
    # address for caching.
    try:
        response = urlopen(url)
    except HTTPError as err:
        raise HTTPException(
            status_code=err.code,
            detail=f"Error retrieving {url}: {err.msg}"
        )
    resolved_url = response.geturl()

    file_path = get_cache_path(resolved_url)
    if not os.path.isfile(file_path):
        urlretrieve(resolved_url, file_path)
    # todo: wrap previous line in try..except so we can return a 404 if the file is not found
    #       or a 500 if the local disk is full

    # if we have a text file, try to download the accompanying json file
    name, ext = os.path.splitext(file_path)
    if ext[1:] in neo.io.AsciiSignalIO.extensions:  # ext has a leading '.'
        metadata_filename = file_path.replace(ext, "_about.json")
        metadata_url = resolved_url.replace(ext, "_about.json")
        try:
            urlretrieve(metadata_url, metadata_filename)
        except HTTPError:
            pass

    return file_path


def load_block(url, io_class_name=None):
    """
    Load the first block from the data file at the given URL.

    If io_class_name is provided, we use the Neo IO class with that name
    to open the file, otherwise we use Neo's `get_io()` function to
    find an appropriate class.
    """
    assert isinstance(url, str)
    file_path = download_neo_data(url)
    # todo: handle formats with multiple files, or with a directory
    if io_class_name:
        # todo: handle an invalid class name
        io_cls = getattr(neo.io, io_class_name.value)
        try:
            io = io_cls(filename=file_path)
        except ImportError:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,  # maybe use 501 Not Implemented?
                detail=f"This server does not have the {io_class_name} module installed.",
            )
        except RuntimeError as err:  # from NixIO
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Error when trying to open file with {io_class_name}: "{err}"',
            )
        except FileNotFoundError as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Associated file not found. More details: "{err}"'
            )
    else:
        # todo: handle IOError, if none of the IO classes work
        io = neo.io.get_io(file_path)

    try:
        if io.support_lazy:
            block = io.read_block(lazy=True)
        else:
            block = io.read_block()
    except AssertionError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error when trying to open file with {io.__class__.__name__}: "{err}"',
        )
    return block

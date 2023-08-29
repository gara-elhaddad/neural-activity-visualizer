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


def get_base_url_and_path(url):
    """
    Strip off any file name from a URL, and return the
    stripped URL and the stripped path part.
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
    return base_url, url_parts.path


def get_cache_path(url):
    """
    For caching, we store files in a flat directory structure, where the directory name is
    based on the URL, but files in the same directory on the original server end up in the
    same directory in our cache.
    """
    base_url, base_path = get_base_url_and_path(url)
    dir_name = hashlib.sha1(base_url.encode("utf-8")).hexdigest()
    dir_path = os.path.join(
        getattr(settings, "DOWNLOADED_FILE_CACHE_DIR", ""), dir_name
    )
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, os.path.basename(base_path))


def list_files_to_download(io_cls, resolved_url, main_path):
    file_list = [(resolved_url, main_path, True)]
    io_mode = getattr(io_cls, "rawmode", None)
    if io_mode == "one-dir":
        # In general, we don't know the names of the individual files
        # and have no way to get a directory listing from a URL
        # so we raise an exception
        if io_cls.__name__ in ("PhyIO"):
            # for the exceptions, resolved_url must represent a directory
            raise NotImplementedError  # todo: for these ios, the file names are known
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Cannot download files from a URL representing a directory. "
                    "Please provide the URL of a zip or tar archive of the directory."
                )
            )
    elif io_mode == "multi-file":
        # Here the resolved_url represents a single file, with or without the file extension.
        # By taking the base/root path and adding various extensions we get a list of files to download
        base_url, base_path = get_base_url_and_path(resolved_url)
        for extension in io_cls.extensions:
            file_list.append(
                # Neo doesn't tell us which files are required and which are optional
                # so we have to treat them all as optional at this stage
                (f"{base_url}.{extension}", f"{base_path}.{extension}", False)
            )
    elif io_mode == "one-file":
        # Here the resolved url should represent a single file,
        # which could have different possible extensions
        # todo: check the URL extension matches one of the possible extensions
        #       and raise an exception otherwise
        pass
    elif io_cls.mode == "dir":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Cannot download files from a URL representing a directory. "
                "Please provide the URL of a zip or tar archive of the directory."
            )
        )
    else:
        # we assume the resolved url represents a single file
        # certain IOs have additional metadata files
        if io_cls.__name__ == "AsciiSignalIO":
            # if we have a text file, try to download the accompanying json file
            name, ext = os.path.splitext(main_path)
            if ext[1:] in neo.io.AsciiSignalIO.extensions:  # ext has a leading '.'
                metadata_filename = main_path.replace(ext, "_about.json")
                metadata_url = resolved_url.replace(ext, "_about.json")
                file_list.append((metadata_url, metadata_filename, False))
    return file_list


def download_neo_data(url, io_cls=None):
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

    main_path = get_cache_path(resolved_url)
    if not os.path.exists(main_path):
        if io_cls:
            files_to_download = list_files_to_download(io_cls, resolved_url, main_path)
        else:
            files_to_download = [(resolved_url, main_path, True)]

        for file_url, file_path, required in files_to_download:
            try:
                urlretrieve(file_url, file_path)
            except HTTPError:
                if required:
                    # todo: may not be a 404, could also be a 500 if local disk is full
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,  # maybe use 501 Not Implemented?
                        detail=f"Problem downloading '{file_url}'"
                    )

    return main_path


def load_blocks(url, io_class_name=None):
    """
    Load the first block from the data file at the given URL.

    If io_class_name is provided, we use the Neo IO class with that name
    to open the file, otherwise we use Neo's `get_io()` function to
    find an appropriate class.
    """
    assert isinstance(url, str)
    # todo: handle formats with multiple files, or with a directory
    if io_class_name:
        io_cls = getattr(neo.io, io_class_name.value)
        main_path = download_neo_data(url, io_cls=io_cls)
        try:
            if io_cls.mode == "dir":
                io = io_cls(dirname=main_path)
            else:
                io = io_cls(filename=main_path)
        except ImportError:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,  # maybe use 501 Not Implemented?
                detail=f"This server does not have the {io_class_name} module installed.",
            )
        except (RuntimeError, TypeError, OSError) as err:  # RuntimeError from NixIO, TypeError from TdtIO, OSError from EDFIO
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
        main_path = download_neo_data(url)
        io = neo.io.get_io(main_path)

    try:
        if io.support_lazy:
            blocks = io.read(lazy=True)
        else:
            blocks = io.read()
    except (AssertionError, ValueError, IndexError, KeyError, AttributeError) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error when trying to open file with {io.__class__.__name__}: "{err}"',
        )
    return blocks

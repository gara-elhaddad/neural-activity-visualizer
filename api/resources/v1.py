"""
Implementation of endpoints, API version 1.

Copyright CNRS 2023
Authors: Andrew P. Davison, Onur Ates, Shailesh Appukuttan, Hélissande Fragnaud and Corentin Fragnaud
Licence: MIT (see LICENSE)

"""

from typing import Annotated
from pydantic import HttpUrl, PositiveInt

from fastapi import Query, HTTPException, APIRouter, status

from ..metadata import title, description
from ..data_models import (
    IOModule,
    Segment,
    AnalogSignal,
    SpikeTrain,
    BlockContainer,
)
from ..data_handler import load_block

router = APIRouter()


@router.get("/")
async def info():
    """Return information about the API."""
    return {
        "title": title,
        "description": description.strip(),
        "version": 1.7,
    }


@router.get("/blockdata/")
async def get_block_data(
    url: Annotated[
        HttpUrl, Query(description="Location of a data file that can be read by Neo.")
    ],
    type: Annotated[
        IOModule,
        Query(
            description=(
                "Specify a specific Neo IO module that should be used to open the data file."
                "If not provided, Neo will try to determine which module to use."
            )
        ),
    ] = None,
) -> BlockContainer:
    """
    Return metadata about all the blocks in a data file,
    including metadata about the segments within each block,
    but without any information about the data contained within each segment.
    """
    # here `url` is a Pydantic object, which we convert to a string
    block = load_block(str(url), type)
    return BlockContainer.from_neo(block, url)


@router.get("/segmentdata/")
async def get_segment_data(
    url: Annotated[
        HttpUrl, Query(description="Location of a data file that can be read by Neo.")
    ],
    segment_id: Annotated[
        int,
        Query(
            description="Index of the segment for which metadata should be returned."
        ),
    ],
    type: Annotated[
        IOModule,
        Query(
            description=(
                "Specify a specific Neo IO module that should be used to open the data file."
                "If not provided, Neo will try to determine which module to use."
            )
        ),
    ] = None,
) -> Segment:
    """
    Return information about an individual Segment within a block,
    including metadata about the signals contained in the segment,
    but not the signal data themselves.
    """
    block = load_block(str(url), type)
    try:
        segment = block.segments[segment_id]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IndexError on segment_id",  # todo: improve this message in next API version
        )
    return Segment.from_neo(segment, url)


@router.get("/analogsignaldata/")
async def get_analogsignal_data(
    url: Annotated[
        HttpUrl, Query(description="Location of a data file that can be read by Neo.")
    ],
    segment_id: Annotated[
        int,
        Query(description="Index of the segment in which the analog signal is found."),
    ],
    analog_signal_id: Annotated[
        int, Query(description="Index of the signal within the segment.")
    ],
    type: Annotated[
        IOModule,
        Query(
            description=(
                "Specify a specific Neo IO module that should be used to open the data file."
                "If not provided, Neo will try to determine which module to use."
            )
        ),
    ] = None,
    down_sample_factor: Annotated[
        PositiveInt,
        Query(
            description=(
                "Factor by which data should be downsampled prior to loading. "
                "Useful for faster loading of large files. Accepts positive integer values."
            )
        ),
    ] = 1,
) -> AnalogSignal:
    """Get an analog signal from a given segment, including both data and metadata."""
    block = load_block(str(url), type)
    try:
        segment = block.segments[segment_id]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IndexError on segment_id",  # todo: improve this message in next API version
        )
    if len(segment.analogsignals) > 0:
        container = segment.analogsignals
    else:
        container = segment.irregularlysampledsignals
    try:
        signal = container[analog_signal_id]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IndexError on analog_signal_id",  # todo: improve this message in next API version
        )
    return AnalogSignal.from_neo(signal, down_sample_factor)


@router.get("/spiketraindata/")
async def get_spiketrain_data(
    url: Annotated[
        HttpUrl, Query(description="Location of a data file that can be read by Neo.")
    ],
    segment_id: Annotated[
        int,
        Query(
            description="Index of the segment for which spike trains should be returned."
        ),
    ],
    type: Annotated[
        IOModule,
        Query(
            description=(
                "Specify a specific Neo IO module that should be used to open the data file."
                "If not provided, Neo will try to determine which module to use."
            )
        ),
    ] = None,
) -> dict[str, SpikeTrain]:
    """Get the spike trains from a given segment, including both data and metadata."""
    block = load_block(str(url), type)
    try:
        segment = block.segments[segment_id]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IndexError on segment_id",  # todo: improve this message in next API version
        )
    return {str(i): SpikeTrain.from_neo(st) for i, st in enumerate(segment.spiketrains)}

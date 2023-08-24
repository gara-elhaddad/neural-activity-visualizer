"""
Main file for Neo Viewer API.

Copyright CNRS 2023
Authors: Andrew P. Davison, Onur Ates, Shailesh Appukuttan, Hélissande Fragnaud and Corentin Fragnaud
Licence: MIT (see LICENSE)
"""

from typing import Annotated
from fastapi import FastAPI, Query, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import HttpUrl, PositiveInt
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from .data_models import (
    IOModule,
    Segment,
    AnalogSignal,
    SpikeTrain,
    BlockContainer,
)
from .data_handler import load_block

description = """
The Neo Viewer API transforms neurophysiology data from a large number of file formats
into JSON, for visualization in a web-browser using Javascript plotting tools.

For example, [neural-activity-visualizer-react](https://www.npmjs.com/package/neural-activity-visualizer-react)
is a React component for visualizing neural activity data, which uses the Neo Viewer API.

The API follows the [Neo](https://neo.readthedocs.io/en/latest/) container structure: the outermost container is the Block,
which contains one or more Segments (a continuous recording period,
corresponding for example to one trial or one stimulus presentation).
Each segment contains one or more AnalogSignals, each of which may be multi-channel,
and any number of SpikeTrains.

Other Neo objects like Events, Epochs, Groups, are not yet supported,
but are planned for a future version.

This project has received funding from the European Union’s Horizon 2020 Framework Programme for Research and Innovation
under the Specific Grant Agreements No. 785907 and No. 945539 (Human Brain Project SGA2 and SGA3).
"""

app = FastAPI(title="Neo Viewer API", description=description, version="1.7")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """Over-ride error handler to add "error" field, for backwards compatibility"""
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail, "error": exc.detail}),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Over-ride error handler to add "error" field, for backwards compatibility"""
    error_detail = exc.errors()
    try:
        error_messages = ", ".join(
            [f"{item['loc'][1]} parameter is {item['type']}" for item in error_detail]
        )
    except Exception:
        err_messages = str(error_detail)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": error_detail, "error": error_messages}),
    )


@app.get("/")
async def info():
    """Return information about the API."""
    return {
        "title": app.title,
        "description": app.description.strip(),
        "version": app.version,
    }


@app.get("/blockdata/")
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


@app.get("/segmentdata/")
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


@app.get("/analogsignaldata/")
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


@app.get("/spiketraindata/")
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
    block = load_block(str(url), type.value)
    try:
        segment = block.segments[segment_id]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IndexError on segment_id",  # todo: improve this message in next API version
        )
    return {str(i): SpikeTrain.from_neo(st) for i, st in enumerate(segment.spiketrains)}

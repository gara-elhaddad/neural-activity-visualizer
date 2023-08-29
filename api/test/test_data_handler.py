"""

"""

import os.path
from neo.io import BrainVisionIO
from ..data_handler import get_base_url_and_path, get_cache_path, list_files_to_download


def test_get_base_url_and_path():
    url = "https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision/File_brainvision_1.vhdr"
    base_url, base_path = get_base_url_and_path(url)
    assert (
        base_url
        == "https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision"
    )
    assert base_path == "File_brainvision_1.vhdr"

    url = "https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/src/master/maxwell/MaxOne_data/Record/000011/data.raw.h5"
    base_url, base_path = get_base_url_and_path(url)
    assert (
        base_url
        == "https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/src/master/maxwell/MaxOne_data/Record/000011"
    )
    assert base_path == "data.raw.h5"


def test_get_cache_path():
    url = "https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision/File_brainvision_1.vhdr"
    cache_path, filename = get_cache_path(url)
    assert cache_path == os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "download_cache/603fed2393f75a3f294fceac99640f7d4a42f74d",
        )
    )
    assert filename == "File_brainvision_1.vhdr"

def test_list_files_to_download():
    url = "https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision/File_brainvision_1.vhdr"
    files_to_download = list_files_to_download(url, "the_cache_dir", BrainVisionIO)
    expected = [
        (url, "the_cache_dir/File_brainvision_1.vhdr", True),
        (url.replace(".vhdr", ".eeg"), "the_cache_dir/File_brainvision_1.eeg", True),
        (url.replace(".vhdr", ".vmrk"), "the_cache_dir/File_brainvision_1.vmrk", True)
    ]
    assert files_to_download == expected

"""

"""

import os
from os.path import join
from collections import defaultdict
from urllib.parse import urlencode
from datetime import datetime
from time import time
import pickle
from importlib import import_module
import unittest
import requests
from neo.test.rawiotest.common_rawio_test import BaseTestRawIO

modules_to_test = [
    "neuroshare",
    "winedr",
    "stimfit",
    "openephys",
    "axograph",
    "axon",
    "nix",
    "plexon",
    "rawbinarysignal",
    "neohdf5",
    "elphy",
    "brainwaref32",
    "tdt",
    "klustakwik",
    "asciisignal",
    "neuroscope",
    "neuroexplorer",
    "alphaomega",
    "blackrock",
    "rawmcs",
    "kwik",
    "micromed",
    "igor",
    "brainvision",
    "asciispiketrain",
    "winwcp",
    "brainwaredam",
    "brainwaresrc",
    "intan",
    "nest",
    "spike2",
    "bci2000",
    "elan",
    "neuralynx",
]

# base_data_url = "https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/"
base_data_url = "https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/"
neo_viewer_url = "https://neo-viewer-dev.brainsimulation.eu/api/v1/"

responses = defaultdict(dict)

start_time = time()
for iomodule in modules_to_test:
    try:
        test_module = import_module("neo.test.iotest.test_{}io".format(iomodule))
    except ImportError:
        pass  # print("Unable to import {}".format(iomodule))
    else:
        for name, obj in test_module.__dict__.items():
            if (
                isinstance(obj, type)
                and issubclass(obj, unittest.TestCase)
                and not issubclass(obj, BaseTestRawIO)
            ):
                if hasattr(obj, "ioclass") and obj.entities_to_test:
                    assert iomodule in obj.ioclass.__module__
                    for filename in obj.entities_to_test:
                        assert iomodule in filename
                        data_url = join(base_data_url, filename)
                        block_url = (
                            neo_viewer_url
                            + "blockdata/?"
                            + urlencode(
                                {
                                    "url": data_url,
                                    "type": obj.ioclass.__name__,
                                }
                            )
                        )
                        response = requests.get(block_url)
                        block_status_code = response.status_code
                        if response.status_code == 200:
                            segment_url = (
                                neo_viewer_url
                                + "segmentdata/?"
                                + urlencode(
                                    {
                                        "url": data_url,
                                        "segment_id": "0",
                                        "type": obj.ioclass.__name__,
                                    }
                                )
                            )
                            response2 = requests.get(segment_url)
                            segment_status_code = response2.status_code
                            if response2.status_code == 200:
                                signal_url = (
                                    neo_viewer_url
                                    + "analogsignaldata/?"
                                    + urlencode(
                                        {
                                            "url": data_url,
                                            "segment_id": "0",
                                            "analog_signal_id": "0",
                                            "type": obj.ioclass.__name__,
                                        }
                                    )
                                )
                                response3 = requests.get(signal_url)
                                signal_status_code = response3.status_code
                            else:
                                signal_status_code = "-"
                        else:
                            segment_status_code = "-"
                            signal_status_code = "-"
                        print(
                            data_url,
                            time() - start_time,
                            block_status_code,
                            segment_status_code,
                            signal_status_code,
                        )
                        responses[response.status_code][filename] = response

print("Status code counts")
for key in responses:
    print(key, len(responses[key]))
    print()
    if key >= 300:
        print(f"# {key}")
        for name, r in responses[key].items():
            print(name, r.content.split(b"\n\n")[0])

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
with open(f"results_gin_{timestamp}.pkl", "wb") as fp:
    pickle.dump(responses, fp)


# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/winedr/File_WinEDR_1.EDR', 343.57470703125, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/winedr/File_WinEDR_2.EDR', 406.673837184906, 200, 200, 504)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/winedr/File_WinEDR_3.EDR', 430.24066615104675, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/stimfit/File_stimfit_1.h5', 431.99944615364075, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/stimfit/File_stimfit_2.h5', 433.46491503715515, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/stimfit/File_stimfit_3.h5', 434.542622089386, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/stimfit/File_stimfit_4.h5', 435.75226616859436, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/stimfit/File_stimfit_5.h5', 436.8318700790405, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/stimfit/File_stimfit_6.h5', 437.87960505485535, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/openephys/OpenEphys_SampleData_1', 438.46606516838074, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/axograph/File_axograph.axgd', 439.87526512145996, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/axon/File_axon_1.abf', 502.08061814308167, 200, 200, 504)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/axon/File_axon_2.abf', 566.5939300060272, 200, 200, 504)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/axon/File_axon_3.abf', 584.4787490367889, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/axon/File_axon_4.abf', 646.7802860736847, 200, 200, 504)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/axon/File_axon_5.abf', 704.5435080528259, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/axon/File_axon_6.abf', 726.445855140686, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/axon/File_axon_7.abf', 729.8017871379852, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/plexon/File_plexon_1.plx', 734.0235509872437, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/plexon/File_plexon_2.plx', 794.4063730239868, 504, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/plexon/File_plexon_3.plx', 857.6411371231079, 504, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/rawbinarysignal/File_rawbinary_10kHz_2channels_16bit.raw', 959.683207988739, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/elphy/ElphyExample.DAT', 960.313395023346, 415, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/elphy/ElphyExample_Mode1.dat', 961.3540730476379, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/elphy/ElphyExample_Mode2.dat', 962.2745161056519, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/elphy/ElphyExample_Mode3.dat', 963.3444330692291, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaref32/block_300ms_4rep_1clust_part_ch1.f32', 965.9617831707001, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaref32/block_500ms_5rep_empty_fullclust_ch1.f32', 967.713632106781, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaref32/block_500ms_5rep_empty_partclust_ch1.f32', 969.5349810123444, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaref32/interleaved_500ms_5rep_ch2.f32', 972.4128661155701, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaref32/interleaved_500ms_5rep_nospikes_ch1.f32', 977.4060971736908, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaref32/multi_500ms_mulitrep_ch1.f32', 981.3215980529785, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaref32/random_500ms_12rep_noclust_part_ch2.f32', 984.5162370204926, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaref32/sequence_500ms_5rep_ch2.f32', 986.464928150177, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/tdt/aep_05', 987.6529760360718, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/klustakwik/test2/base', 988.7491271495819, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/klustakwik/test2/base2', 989.4053881168365, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/asciisignal/File_asciisignal_2.txt', 990.8959012031555, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/asciisignal/File_asciisignal_3.txt', 992.1295230388641, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuroscope/test1/test1.xml', 992.6065061092377, 415, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuroexplorer/File_neuroexplorer_1.nex', 993.705087184906, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuroexplorer/File_neuroexplorer_2.nex', 995.6957621574402, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/alphaomega/File_AlphaOmega_1.map', 997.8663520812988, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/alphaomega/File_AlphaOmega_2.map', 1000.752032995224, 200, 200, 500)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/blackrock/FileSpec2.3001', 1001.2958881855011, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/rawmcs/raw_mcs_with_header_1.raw', 1002.829537153244, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/kwik/neo.kwik', 1004.6954171657562, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/micromed/File_micromed_1.TRC', 1005.2305672168732, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/igor/mac-version2.ibw', 1006.4016361236572, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/igor/win-version2.ibw', 1007.6389729976654, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision/File_brainvision_1.vhdr', 1011.5036389827728, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision/File_brainvision_2.vhdr', 1015.6663680076599, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision/File_brainvision_3_float32.vhdr', 1022.631028175354, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision/File_brainvision_3_int16.vhdr', 1028.212128162384, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainvision/File_brainvision_3_int32.vhdr', 1032.7176032066345, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/asciispiketrain/File_ascii_spiketrain_1.txt', 1034.4098720550537, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/winwcp/File_winwcp_1.wcp', 1052.7634761333466, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaredam/block_300ms_4rep_1clust_part_ch1.dam', 1053.8219740390778, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaredam/interleaved_500ms_5rep_ch2.dam', 1055.050096988678, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaredam/long_170s_1rep_1clust_ch2.dam', 1056.5989110469818, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaredam/multi_500ms_mulitrep_ch1.dam', 1060.3307621479034, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaredam/random_500ms_12rep_noclust_part_ch2.dam', 1061.9835941791534, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaredam/sequence_500ms_5rep_ch2.dam', 1062.8565120697021, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/block_300ms_4rep_1clust_part_ch1.src', 1063.730674982071, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/block_500ms_5rep_empty_fullclust_ch1.src', 1064.8823781013489, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/block_500ms_5rep_empty_partclust_ch1.src', 1066.0766310691833, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/interleaved_500ms_5rep_ch2.src', 1067.140293121338, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/interleaved_500ms_5rep_nospikes_ch1.src', 1068.1508340835571, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/interleaved_500ms_7rep_noclust_ch1.src', 1069.9386990070343, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/long_170s_1rep_1clust_ch2.src', 1077.4439430236816, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/multi_500ms_mulitrep_ch1.src', 1081.4652621746063, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/random_500ms_12rep_noclust_part_ch2.src', 1084.2070090770721, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/brainwaresrc/sequence_500ms_5rep_ch2.src', 1085.260073184967, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/intan/intan_rhs_test_1.rhs', 1108.6231281757355, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/intan/intan_rhd_test_1.rhd', 1114.6307561397552, 200, 200, 200)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/spike2/File_spike2_1.smr', 1115.134532213211, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/spike2/File_spike2_2.smr', 1116.1406362056732, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/spike2/File_spike2_3.smr', 1116.9410290718079, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/spike2/130322-1LY.smr', 1118.949949979782, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/spike2/multi_sampling.smr', 1120.2054960727692, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/elan/File_elan_1.eeg', 1184.0774340629578, 200, 200, 504)
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.5.1/original_data', 1184.6444220542908, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.6.3/original_data', 1185.4696061611176, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.7.4/original_data', 1186.1286251544952, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.5.1/original_data', 1187.8566591739655, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.6.3/original_data', 1188.3791670799255, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.7.4/original_data', 1189.5361762046814, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.5.1/original_data', 1189.9167890548706, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.6.3/original_data', 1190.379625082016, 500, '-', '-')
# ('https://web.gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/neuralynx/Cheetah_v5.7.4/original_data', 1190.9355380535126, 500, '-', '-')
# (200, 30)
# (504, 2)
# (500, 50)
# (415, 2)

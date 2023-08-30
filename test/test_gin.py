"""
Script to test installations of the Neo Viewer API.

Usage:

  python test_gin.py <api_url>

where <api_url> is something like https://neo-viewer-staging.brainsimulation.eu/api/v1/

Note that the first time you run this script it will be slower, as all of the data files
are downloaded. Subsequent runs should be faster since the data will be in the cache.
"""

import sys
from os.path import join
from collections import defaultdict
from urllib.parse import urlencode
from datetime import datetime
from time import time
import pickle
import requests

gin_data_url = "https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/"
neo_viewer_url = sys.argv[1]

if not neo_viewer_url.endswith("/"):
    # ensure there is a final slash
    neo_viewer_url += "/"


test_data_gin = {
    200: {
        "AsciiSpikeTrainIO": ["asciispiketrain/File_ascii_spiketrain_1.txt"],
        "AxographIO": [
            "axograph/AxoGraph_Graph_File",
            "axograph/AxoGraph_Digitized_File",
            "axograph/AxoGraph_X_File.axgx",
            "axograph/File_axograph.axgd",
            "axograph/episodic.axgd",
            "axograph/events_and_epochs.axgx",
            "axograph/written-by-axographio-with-linearsequence.axgx",
            "axograph/written-by-axographio-without-linearsequence.axgx",
            "axograph/corrupt-comment.axgx",
        ],
        "AxonIO": [
            "axon/File_axon_1.abf",
            "axon/File_axon_2.abf",
            "axon/File_axon_3.abf",
            "axon/File_axon_4.abf",
            "axon/File_axon_5.abf",
            "axon/File_axon_6.abf",
            "axon/File_axon_7.abf",
            "axon/test_file_edr3.abf",
        ],
        "AxonaIO": [
            "axona/axona_raw.set",
            "axona/dataset_unit_spikes/20140815-180secs.set",
            "axona/dataset_multi_modal/axona_sample.set",
        ],
        "BCI2000IO": ["bci2000/eeg1_1.dat", "bci2000/eeg1_2.dat", "bci2000/eeg1_3.dat"],
        "BiocamIO": ["biocam/biocam_hw3.0_fw1.6.brw"],
        "BlackrockIO": [
            "blackrock/FileSpec2.3001.nev",
            "blackrock/blackrock_2_1/l101210-001.nev",
            "blackrock/blackrock_3_0/file_spec_3_0.nev",
        ],
        "BlkIO": [],
        "BrainVisionIO": [
            "brainvision/File_brainvision_1.vhdr",
            "brainvision/File_brainvision_2.vhdr",
            "brainvision/File_brainvision_3_float32.vhdr",
            "brainvision/File_brainvision_3_int16.vhdr",
            "brainvision/File_brainvision_3_int32.vhdr",
        ],
        "BrainwareDamIO": [
            "brainwaredam/block_300ms_4rep_1clust_part_ch1.dam",
            "brainwaredam/interleaved_500ms_5rep_ch2.dam",
            "brainwaredam/long_170s_1rep_1clust_ch2.dam",
            "brainwaredam/multi_500ms_mulitrep_ch1.dam",
            "brainwaredam/random_500ms_12rep_noclust_part_ch2.dam",
            "brainwaredam/sequence_500ms_5rep_ch2.dam",
        ],
        "BrainwareF32IO": [
            "brainwaref32/block_300ms_4rep_1clust_part_ch1.f32",
            "brainwaref32/block_500ms_5rep_empty_fullclust_ch1.f32",
            "brainwaref32/block_500ms_5rep_empty_partclust_ch1.f32",
            "brainwaref32/interleaved_500ms_5rep_ch2.f32",
            "brainwaref32/interleaved_500ms_5rep_nospikes_ch1.f32",
            "brainwaref32/multi_500ms_mulitrep_ch1.f32",
            "brainwaref32/random_500ms_12rep_noclust_part_ch2.f32",
            "brainwaref32/sequence_500ms_5rep_ch2.f32",
        ],
        "BrainwareSrcIO": [],
        "CedIO": [],
        "EDFIO": ["edf/edf+C.edf"],
        "ElanIO": ["elan/File_elan_1.eeg"],
        "ElphyIO": [
            "elphy/DATA1.DAT",
            "elphy/ElphyExample.DAT",
            "elphy/ElphyExample_Mode1.dat",
            "elphy/ElphyExample_Mode2.dat",
            "elphy/ElphyExample_Mode3.dat",
        ],
        "IgorIO": ["igor/win-version2.ibw", "igor/mac-version2.ibw"],
        "IntanIO": [
            "intan/intan_rhs_test_1.rhs",
            "intan/intan_rhd_test_1.rhd",
        ],
        "MicromedIO": ["micromed/File_micromed_1.TRC"],
        "NeoMatlabIO": [],
        "NestIO": [
            "nest/0gid-1time-1256-0.gdf",
            "nest/0gid-1time-2Vm-1259-0.dat",
            "nest/0gid-1time-2Vm-3Iex-4Iin-1264-0.dat",
            "nest/0gid-1time-2Vm-3gex-4gin-1260-0.dat",
            "nest/0gid-1time-2gex-1262-0.dat",
            "nest/0gid-1time-2gex-3Vm-1261-0.dat",
            "nest/0gid-1time_in_steps-1258-0.gdf",
            "nest/0gid-1time_in_steps-2Vm-1263-0.dat",
            # "nest/0time-1255-0.gdf",
            # "nest/0time_in_steps-1257-0.gdf",
            # "nest/N1-0Vm-1267-0.dat",
            "nest/N1-0gid-1time-2Vm-1265-0.dat",
            # "nest/N1-0time-1Vm-1266-0.dat",
        ],
        "NeuroExplorerIO": [
            "neuroexplorer/File_neuroexplorer_1.nex",
            "neuroexplorer/File_neuroexplorer_2.nex",
        ],
        "NixIO": ["nix/generated_file_neo0.12.0.nix"],
        "PlexonIO": [
            "plexon/File_plexon_1.plx",
            "plexon/File_plexon_2.plx",
            "plexon/File_plexon_3.plx",
        ],
        "RawBinarySignalIO": [
            "rawbinarysignal/File_rawbinary_10kHz_2channels_16bit.raw"
        ],
        "RawMCSIO": ["rawmcs/raw_mcs_with_header_1.raw"],
        "Spike2IO": [
            "spike2/File_spike2_1.smr",
            "spike2/File_spike2_2.smr",
            "spike2/File_spike2_3.smr",
            "spike2/130322-1LY.smr",
            "spike2/multi_sampling.smr",
            "spike2/Two-mice-bigfile-test000.smr",
        ],
        "SpikeGadgetsIO": [
            "spikegadgets/20210225_em8_minirec2_ac.rec",
            "spikegadgets/W122_06_09_2019_1_fromSD.rec",
        ],
        "WinEdrIO": [
            "winedr/File_WinEDR_1.EDR",
            "winedr/File_WinEDR_2.EDR",
            "winedr/File_WinEDR_3.EDR",
        ],
        "WinWcpIO": ["winwcp/File_winwcp_1.wcp"],
    },
    400: {
        "block": {
            "NestIO": [
                # "nest/0gid-1time-1256-0.gdf",
                # "nest/0gid-1time-2Vm-1259-0.dat",
                # "nest/0gid-1time-2Vm-3Iex-4Iin-1264-0.dat",
                # "nest/0gid-1time-2Vm-3gex-4gin-1260-0.dat",
                # "nest/0gid-1time-2gex-1262-0.dat",
                # "nest/0gid-1time-2gex-3Vm-1261-0.dat",
                # "nest/0gid-1time_in_steps-1258-0.gdf",
                # "nest/0gid-1time_in_steps-2Vm-1263-0.dat",
                "nest/0time-1255-0.gdf",  #  "Can not sort by column ID 1. File contains only 1 columns"
                "nest/0time_in_steps-1257-0.gdf",
                "nest/N1-0Vm-1267-0.dat",
                # "nest/N1-0gid-1time-2Vm-1265-0.dat",
                "nest/N1-0time-1Vm-1266-0.dat",
            ],
            "NeuroScopeIO": [
                # xml file contains addresses of other files,
                # so we could read it and download them
                "neuroscope/test1/test1.xml"
            ],
            "NWBIO": [
                "nwb/AbfInterface_3.nwb",
                # "nwb/AxonaLFPDataInterface.nwb",
                "nwb/AxonaRecordingInterface.nwb",
                "nwb/BlackrockSortingInterface.nwb",
                "nwb/ecephys_tutorial_v2.5.0.nwb",
            ],
        },
        "segment": {
            "NWBIO": [
                # "nwb/AbfInterface_3.nwb",
                "nwb/AxonaLFPDataInterface.nwb",
                # "nwb/AxonaRecordingInterface.nwb",
                # "nwb/BlackrockSortingInterface.nwb",
                # "nwb/ecephys_tutorial_v2.5.0.nwb",
            ],
        },
        "signal": {
            "AsciiSignalIO": [
                "asciisignal/File_asciisignal_2.txt",  # 'Data contains NaN'
                "asciisignal/File_asciisignal_3.txt",  # 'Data contains NaN'
            ],
            "MaxwellIO": [
                # OSError: Can't read data (can't open directory: /usr/local/hdf5/lib/plugin)
                "maxwell/MaxOne_data/Record/000011/data.raw.h5",
                "maxwell/MaxTwo_data/Network/000028/data.raw.h5",
            ],
        },
    },
    415: {  # dependency not installed
        "KwikIO": ["kwik/neo.kwik"],
        "MEArecIO": ["mearec/mearec_test_10s.h5"],
        "Plexon2IO": [
            "plexon/File_plexon_1.plx",
            "plexon/File_plexon_2.plx",
            "plexon/File_plexon_3.plx",
        ],
        "StimfitIO": [
            "stimfit/File_stimfit_1.h5",
            "stimfit/File_stimfit_2.h5",
            "stimfit/File_stimfit_3.h5",
            "stimfit/File_stimfit_4.h5",
            "stimfit/File_stimfit_5.h5",
            "stimfit/File_stimfit_6.h5",
        ],
    },
    500: {},
    "dir": {
        "AlphaOmegaIO": ["alphaomega/mpx_map_version4"],
        "KlustaKwikIO": [
            "klustakwik/test2/base",
            "klustakwik/test2/base2",
        ],
        "MedIO": [
            "med/sine_waves.medd",
            "med/test.medd",
        ],
        "NeuralynxIO": [
            "neuralynx/BML/original_data",
            "neuralynx/BML_unfilledsplit/original_data",
            "neuralynx/Cheetah_v1.1.0/original_data",
            "neuralynx/Cheetah_v4.0.2/original_data",
            "neuralynx/Cheetah_v5.4.0/original_data",
            "neuralynx/Cheetah_v5.5.1/original_data",
            # "neuralynx/Cheetah_v5.6.3/original_data",
            "https://data-proxy.ebrains.eu/api/v1/buckets/myspace/neo-viewer-test-data/ephy_testing_data_neuralynx_Cheetah_v5.6.3_original_data.zip",
            "neuralynx/Cheetah_v5.7.4/original_data",
            "neuralynx/Cheetah_v6.3.2/incomplete_blocks",
        ],
        "OpenEphysIO": ["openephys/OpenEphys_SampleData_1"],
        "OpenEphysBinaryIO": [
            "openephysbinary/v0.5.3_two_neuropixels_stream",
            "openephysbinary/v0.4.4.1_with_video_tracking",
            "openephysbinary/v0.5.x_two_nodes",
            "openephysbinary/v0.6.x_neuropixels_multiexp_multistream",
        ],
        "PhyIO": ["phy/phy_example_0"],
        "SpikeGLXIO": [
            "spikeglx/Noise4Sam_g0",
            "spikeglx/TEST_20210920_0_g0",
            "spikeglx/multi_trigger_multi_gate/SpikeGLX/5-19-2022-CI0/5-19-2022-CI0_g0",
            "spikeglx/multi_trigger_multi_gate/SpikeGLX/5-19-2022-CI0/5-19-2022-CI0_g1",
            "spikeglx/multi_trigger_multi_gate/SpikeGLX/5-19-2022-CI0",
            "spikeglx/multi_trigger_multi_gate/SpikeGLX/5-19-2022-CI1",
            "spikeglx/multi_trigger_multi_gate/SpikeGLX/5-19-2022-CI2",
            "spikeglx/multi_trigger_multi_gate/SpikeGLX/5-19-2022-CI3",
            "spikeglx/multi_trigger_multi_gate/SpikeGLX/5-19-2022-CI4",
            "spikeglx/multi_trigger_multi_gate/SpikeGLX/5-19-2022-CI5",
        ],
        "TdtIO": [
            "tdt/aep_05",
            "tdt/dataset_0_single_block/512ch_reconly_all-181123_B24_rest.Tdx",
            "tdt/dataset_1_single_block/ECTest-220207-135355_ECTest_B1.Tdx",
            "tdt/aep_05/Block-1/aep_05_Block-1.Tdx",
        ],
    },
}

responses = {
    "block": defaultdict(dict),
    "segment": defaultdict(dict),
    "signal": defaultdict(dict),
}

start_time = time()
for io_cls, test_files in test_data_gin[200].items():
    for filename in test_files:
        data_url = join(gin_data_url, filename)
        block_url = (
            neo_viewer_url
            + "blockdata/?"
            + urlencode({"url": data_url, "type": io_cls})
        )
        response = requests.get(block_url)
        block_status_code = response.status_code
        responses["block"][block_status_code][filename] = response
        if block_status_code == 200:
            segment_url = (
                neo_viewer_url
                + "segmentdata/?"
                + urlencode({"url": data_url, "segment_id": "0", "type": io_cls})
            )
            response2 = requests.get(segment_url)
            segment_status_code = response2.status_code
            responses["segment"][segment_status_code][filename] = response2

            if response2.status_code == 200:
                segment_data = response2.json()

                if segment_data["analogsignals"]:
                    signal_url = (
                        neo_viewer_url
                        + "analogsignaldata/?"
                        + urlencode(
                            {
                                "url": data_url,
                                "segment_id": "0",
                                "analog_signal_id": "0",
                                "down_sample_factor": "10",
                                "type": io_cls,
                            }
                        )
                    )
                    response3 = requests.get(signal_url)
                    signal_status_code = response3.status_code
                    responses["signal"][signal_status_code][filename] = response3
                else:
                    signal_status_code = "-"
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

print("\n# Status code counts")
for endpoint in ("block", "segment", "signal"):
    print(f"## {endpoint}")
    for key in responses[endpoint]:
        print(key, len(responses[endpoint][key]))

print("\n\n# Error messages")
for endpoint in ("block", "segment", "signal"):
    for key in responses[endpoint]:
        if key >= 300:
            print(f"\n## {key} {endpoint}")
            for name, r in responses[endpoint][key].items():
                print(name, r.content.split(b"\n\n")[0])

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
with open(f"results_gin_{timestamp}.pkl", "wb") as fp:
    pickle.dump(responses, fp)

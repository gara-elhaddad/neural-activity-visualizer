import React from 'react';
import axios from 'axios';
import HeaderPanel from './HeaderPanel';
import GraphPanel from './GraphPanel';


const baseUrl = "https://neo-viewer.brainsimulation.eu";


export default function Visualizer(props) {
    const [segmentId, setSegmentId] = React.useState(0);
    const [signalId, setSignalId] = React.useState(0);
    const [showSpikeTrains, setShowSpikeTrains] = React.useState(false);
    const [downSampleFactor, setDownSampleFactor] = React.useState(1);
    const [graphData, setGraphData] = React.useState(""); // {}
    const [blockData, setBlockData] = React.useState({
        segments: []
    });

    function getBlockData(datafileUrl) {
        let url = baseUrl + "/blockdata/?url=" + datafileUrl;
        let config = {}
        return axios.get(url, config)
    }

    function getSegmentData(datafileUrl, segmentId) {
        let url = `${baseUrl}/segmentdata/?url=${datafileUrl}&segment_id=${segmentId}`;
        let config = {}
        return axios.get(url, config)
    }

    function getSignalData(datafileUrl, segmentId, signalId, downSampleFactor) {
        let url = `${baseUrl}/analogsignaldata/?url=${datafileUrl}&segment_id=${segmentId}&analog_signal_id=${signalId}&down_sample_factor=${downSampleFactor}`;
        let config = {}
        console.log(url);
        return axios.get(url, config)
    }

    function segmentNotLoaded(blockData, segmentId) {
        const segmentArray = blockData.segments;
        if (segmentArray.length > segmentId) {
            return (segmentArray[segmentId].analogsignals.length === 0);
        } else {
            return true;
        }
    }

    function signalNotLoaded(blockData, segmentId, signalId) {
        if (segmentNotLoaded(blockData, segmentId)) {
            return true
        } else {
            const signalArray = blockData.segments[segmentId].analogsignals;
            if (signalArray.length > signalId) {
                return (signalArray[signalId].length === 0);
            } else {
                return true;
            }
        }
    }

    React.useEffect(() => {
        if (props.segmentId) {
            setSegmentId(props.segmentId);
        }
        if (props.signalId) {
            setSignalId(props.signalId);
        }
        if (props.showSpikeTrains) {
            setShowSpikeTrains(true);
        }
        if (props.downSampleFactor) {
            setDownSampleFactor(props.downSampleFactor);
        }
        // setSegmentId and setSignalId may not be immediately executed
        // so we can't assume segmentId and signalId have been set by now
        const currentSegmentId = props.segmentId || segmentId;
        const currentSignalId = props.signalId || signalId;
        if (blockData.segments.length === 0) {
            getBlockData(props.source)
                .then(res0 => {
                    console.log("Got block data");
                    console.log(res0.data);
                    let localBlockData = res0.data["block"][0];  // todo: handle files with multiple blocks
                    //setLoading(false);
                    if (segmentNotLoaded(blockData, currentSegmentId)) {
                        getSegmentData(props.source, currentSegmentId)
                            .then(res1 => {
                                console.log("Got segment data");
                                console.log(res1.data);
                                localBlockData.segments[currentSegmentId] = res1.data;
                                if (signalNotLoaded(blockData, currentSegmentId, currentSignalId)) {
                                    getSignalData(props.source, currentSegmentId, currentSignalId, props.downSampleFactor || 1)
                                        .then(res2 => {
                                            console.log("Got signal data");
                                            console.log(res2.data);
                                            localBlockData.segments[currentSegmentId].analogsignals[currentSignalId] = res2.data;
                                            setBlockData({...blockData, ...localBlockData});
                                            updateGraphData(currentSegmentId, currentSignalId);
                                        })
                                        .catch(err => {
                                            console.log(`Error retrieving signal #${currentSignalId} from segment #${currentSegmentId}: ${err.message}`);
                                        });
                                }
                            })
                            .catch(err => {
                                console.log(`Error retrieving segment #${currentSegmentId}: ${err.message}`);
                            });
                    }
                })
                .catch(err => {
                    console.log(`Error retrieving block from ${props.source}: ${err.message}`);
                });
        }
    }, []);

    function updateGraphData(segmentId, signalId) {
        setSegmentId(segmentId);
        setSignalId(signalId);
        setGraphData(`segment=${segmentId} signal=${signalId}`);
    }

    return (
        <div>
            <HeaderPanel
                source={props.source}
                ioType={props.ioType}
                downSampleFactor={props.downSampleFactor}
                segmentId={segmentId}
                signalId={signalId}

                showSpikeTrains={showSpikeTrains}
                updateGraphData={updateGraphData}
            />
            <GraphPanel data={graphData} />
        </div>
    )

}
import React from 'react';
import DataStore from './datastore';
import HeaderPanel from './HeaderPanel';
import GraphPanel from './GraphPanel';


const baseUrl = "https://neo-viewer.brainsimulation.eu";


export default function Visualizer(props) {
    const [segmentId, setSegmentId] = React.useState(0);
    const [signalId, setSignalId] = React.useState(0);
    const [showSpikeTrains, setShowSpikeTrains] = React.useState(false);
    const [downSampleFactor, setDownSampleFactor] = React.useState(1);
    const [graphData, setGraphData] = React.useState(""); // {}
    const datastore = React.useRef(new DataStore(props.source));

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

        datastore.current.initialize()
            .then(res => {
                updateGraphData(currentSegmentId, currentSignalId);
            })
            .catch(err => {
                console.log("Error initializing datastore");
            });
    }, []);

    function updateGraphData(newSegmentId, newSignalId) {
        setSegmentId(newSegmentId);
        setSignalId(newSignalId);
        datastore.current.getSignal(0, newSegmentId, newSignalId, props.downSampleFactor)
            .then(res => {
                console.log(res);
                console.log(datastore.current);
                setGraphData(`segment=${newSegmentId} signal=${newSignalId}`);
            });
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
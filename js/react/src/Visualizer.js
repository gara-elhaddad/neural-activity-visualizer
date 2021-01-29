import React from 'react';
import DataStore from './datastore';
import HeaderPanel from './HeaderPanel';
import GraphPanel from './GraphPanel';


const baseUrl = "https://neo-viewer.brainsimulation.eu";


function generateTimes(n, tStart, samplingPeriod) {
    const times = Array(n);
    for (let i = 0; i < n; i++) {
        times[i] = i * samplingPeriod + tStart;
    }
    return times;
}


export default function Visualizer(props) {
    const [segmentId, setSegmentId] = React.useState(0);
    const [signalId, setSignalId] = React.useState(0);
    const [consistent, setConsistent] = React.useState(false);
    const [showSpikeTrains, setShowSpikeTrains] = React.useState(false);
    const [downSampleFactor, setDownSampleFactor] = React.useState(1);
    const [labels, setLabels] = React.useState([{label: "Segment #0", signalLabels: ["Signal #0"]}]);
    const [graphData, setGraphData] = React.useState([]);
    const [axisLabels, setAxisLabels] = React.useState({x: "", y: ""});
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
                setConsistent(datastore.current.isConsistentAcrossSegments(0));
                updateGraphData(currentSegmentId, currentSignalId);
            })
            .catch(err => {
                console.log("Error initializing datastore");
            });
    }, []);

    function updateGraphData(newSegmentId, newSignalId) {
        setSegmentId(newSegmentId);
        setSignalId(newSignalId);
        if (newSegmentId === "all") {
            datastore.current.getSignalsFromAllSegments(0, newSignalId, props.downSampleFactor)
                .then(results => {
                    setLabels(datastore.current.getLabels(0));
                    setGraphData(results.map(res => {
                        return {
                            x: generateTimes(res.values.length, 0.0, res.sampling_period),
                            y: res.values
                        };
                    }));
                    setAxisLabels({x: results[0].times_dimensionality, y: results[0].values_units});
                });
        } else {
            datastore.current.getSignal(0, newSegmentId, newSignalId, props.downSampleFactor)
                .then(res => {
                    console.log(res);
                    console.log(datastore.current);
                    setLabels(datastore.current.getLabels(0));
                    setGraphData([{
                        x: generateTimes(res.values.length, res.t_start, res.sampling_period),
                        y: res.values
                    }]);
                    setAxisLabels({x: res.times_dimensionality, y: res.values_units});
                });
        }
    }

    return (
        <div>
            <HeaderPanel
                source={props.source}
                ioType={props.ioType}
                downSampleFactor={props.downSampleFactor}
                segmentId={segmentId}
                signalId={signalId}
                consistent={consistent}
                labels={labels}
                showSpikeTrains={showSpikeTrains}
                updateGraphData={updateGraphData}
            />
            <GraphPanel data={graphData} axisLabels={axisLabels} />
        </div>
    )

}
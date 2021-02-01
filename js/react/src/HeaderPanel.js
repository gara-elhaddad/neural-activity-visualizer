import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';

import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles((theme) => ({
    formControl: {
      margin: theme.spacing(1),
      minWidth: 120,
    }
  }));


function SegmentSelect(props) {
    const classes = useStyles();

    let menuItemAll = "";
    if (props.consistent) {
        menuItemAll = (<MenuItem value={"all"}>All</MenuItem>);
    }

    return (
        <FormControl className={classes.formControl}>
                <InputLabel id="select-segment-label">Segment</InputLabel>
                <Select
                    labelId="select-segment-label"
                    id="select-segment"
                    value={props.segmentId}
                    onChange={props.onChange}
                >
                    {menuItemAll}
                    {
                        props.labels.map((seg, index) => {
                            return <MenuItem value={index}>{seg.label}</MenuItem>
                        })
                    }
                </Select>
            </FormControl>
    );
}

function SignalSelect(props) {
    const classes = useStyles();

    let segmentId = props.segmentId;
    if (props.segmentId === "all") {
        segmentId = 0;  // if plotting signals from all segments, the segments
                        // have been checked for consistency, so we can take
                        // the labels only from the first segment
    }

    return (
        <FormControl className={classes.formControl}>
            <InputLabel id="select-signal-label">Signal</InputLabel>
            <Select
                labelId="select-signal-label"
                id="select-signal"
                value={props.signalId}
                onChange={props.onChange}
            >
                {
                    props.labels[segmentId].signalLabels.map((label, index) => {
                        return <MenuItem value={index}>{label}</MenuItem>
                    })
                }
            </Select>
        </FormControl>
    )
}


export default function HeaderPanel(props) {
    const classes = useStyles();

    React.useEffect(() => {
        console.log(props);
    }, []);

    const handleChangeSegment = (event) => {
        console.log("change segment");
        console.log(event);
        console.log(event.target.value);
        console.log(typeof event.target.value);

        props.updateGraphData(event.target.value, props.signalId, props.showSignals, props.showSpikeTrains);
    };

    const handleChangeSignal = (event) => {
        props.updateGraphData(props.segmentId, event.target.value, props.showSignals, props.showSpikeTrains);
    };

    return (
        <FormGroup row>
            <SegmentSelect segmentId={props.segmentId} consistent={props.consistent} onChange={handleChangeSegment} labels={props.labels}/>
            <SignalSelect segmentId={props.segmentId} signalId={props.signalId} onChange={handleChangeSignal} labels={props.labels}/>
        </FormGroup>
    );
}

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

        props.updateGraphData(event.target.value, props.signalId);
    };

    const handleChangeSignal = (event) => {
        props.updateGraphData(props.segmentId, event.target.value);
    };

    return (
        <FormGroup row>
            <FormControl className={classes.formControl}>
                <InputLabel id="select-segment-label">Segment</InputLabel>
                <Select
                    labelId="select-segment-label"
                    id="select-segment"
                    value={props.segmentId}
                    onChange={handleChangeSegment}
                >
                    <MenuItem value={"all"}>All</MenuItem>
                    {
                        props.labels.map((seg, index) => {
                            return <MenuItem value={index}>{seg.label}</MenuItem>
                        })
                    }
                </Select>
            </FormControl>
            <FormControl className={classes.formControl}>
                <InputLabel id="select-signal-label">Signal</InputLabel>
                <Select
                    labelId="select-signal-label"
                    id="select-signal"
                    value={props.signalId}
                    onChange={handleChangeSignal}
                >
                    <MenuItem value={"all"}>All</MenuItem>
                    {
                        props.labels[props.segmentId].signalLabels.map((label, index) => {
                            return <MenuItem value={index}>{label}</MenuItem>
                        })
                    }
                </Select>
            </FormControl>
        </FormGroup>
    );
}

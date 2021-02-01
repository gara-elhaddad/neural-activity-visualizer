import React from 'react';
import Plot from 'react-plotly.js';

export default function SpikeTrainPanel(props) {
    const lineProperties = {
        type: 'scatter',
        mode: 'markers'
        //marker: {color: 'green'},
    };
    if (props.show) {
        const data = props.data.map(spikes => {
            return { ...lineProperties, ...spikes }
        });
        console.log(data);
        return (
            <Plot
                data={data}
                layout={{
                    width: 800,
                    height: 400,
                    xaxis: {
                        title: {
                            text: `Time (${props.axisLabels.x})`
                        }
                    },
                    yaxis: {
                        title: {
                            text: "Spike Trains"
                        }
                    },
                }}
            />
        );
    } else {
        return <div />
    }
}
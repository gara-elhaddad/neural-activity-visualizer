import React from 'react';
import Plot from 'react-plotly.js';

export default function GraphPanel(props) {
    const lineProperties = {
        type: 'scatter',
        mode: 'lines' //,
        //marker: {color: 'green'},
    };
    if (props.show) {
        const data = props.data.map(trace => {
            return { ...lineProperties, ...trace }
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
                            text: props.axisLabels.x
                        }
                    },
                    yaxis: {
                        title: {
                            text: props.axisLabels.y
                        }
                    },
                }}
            />
        );
    } else {
        return <div />
    }
}
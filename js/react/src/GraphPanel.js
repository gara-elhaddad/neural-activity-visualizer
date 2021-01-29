import React from 'react';
import Plot from 'react-plotly.js';

export default function GraphPanel(props) {
    const lineProperties = {
        type: 'scatter',
        lines: 'lines' //,
        //marker: {color: 'green'},
    };
    const data = props.data.map(trace => {
        return {...lineProperties, ...trace}
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
}
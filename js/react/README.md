# neural-activity-visualizer-react

> A ReactJS component for visualizing neural activity data

[![NPM](https://img.shields.io/npm/v/neural-activity-visualizer-react.svg)](https://www.npmjs.com/package/neural-activity-visualizer-react) [![JavaScript Style Guide](https://img.shields.io/badge/code_style-standard-brightgreen.svg)](https://standardjs.com)

## Install

```bash
npm install --save neural-activity-visualizer-react
```

## Usage

```jsx
import React from 'react';
import Visualizer from 'neural-activity-visualizer-react';

function Example {
  const source = "https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/Migliore_2018_CA1/exp_data/abf-int-bAC/Ivy_960711AHP3/96711008.abf";

  return (
    <Visualizer source={source} showSpikeTrains={false} showSignals={true}/>
  )

```

## License

MIT © [apdavison](https://github.com/apdavison)

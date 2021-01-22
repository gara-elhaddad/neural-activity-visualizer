import Visualizer from 'neural-activity-visualizer-react';

function App() {
  return (
    <div className="App">
      <Visualizer source="https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/Migliore_2018_CA1/exp_data/abf-int-bAC/Ivy_960711AHP3/96711008.abf" />
    </div>
  );
}

export default App;

import Visualizer from 'neural-activity-visualizer-react';
//import Visualizer from './Visualizer';

const source1 = "https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/Migliore_2018_CA1/exp_data/abf-int-bAC/Ivy_960711AHP3/96711008.abf";
const source2 = "https://drive.humanbrainproject.eu/f/076de9c19e0c4447a95e/?dl=1";

function App() {
  return (
    <div className="App">
      <Visualizer source={source1} showSpikeTrains={false} showSignals={true}/>
    </div>
  );
}

export default App;

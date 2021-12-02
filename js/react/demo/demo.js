// import Visualizer from 'neural-activity-visualizer-react';
import React from "react";
import ReactDOM from "react-dom";
import Visualizer from "../src";
import "./demo.css";

const source1 =
  "https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/Migliore_2018_CA1/exp_data/abf-int-bAC/Ivy_960711AHP3/96711008.abf";
const source2 =
  "https://drive.humanbrainproject.eu/f/076de9c19e0c4447a95e/?dl=1";

function App() {
  return (
    <div className="container">
      <br />
      <br />
      <div className="rounded-box">
        <div className="title-container">
          <img
            className="ebrains-icon-small"
            src="https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/EBRAINS_live_papers/resources/logos/EBRAINS.png"
            alt="EBRAINS logo"
            style={{ width: "50px", height: "50px", verticalAlign: "middle" }}
          />
          <span
            className="title-style"
            style={{ paddingLeft: "15px", verticalAlign: "middle" }}
          >
            Neural Activity Visualizer
          </span>
          <div className="subtitle-style" style={{ paddingTop: "30px" }}>
            Javascript component for visualizing neural activity data
          </div>
        </div>
      </div>
      <br />
      <br />
      <div className="App">
        <Visualizer
          source={source1}
          showSpikeTrains={false}
          showSignals={true}
          width={900}
          height={350}
        />
      </div>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById("app"));

module.hot.accept();

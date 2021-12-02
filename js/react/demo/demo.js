// import Visualizer from 'neural-activity-visualizer-react';
import React from "react";
import ReactDOM from "react-dom";
import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import Visualizer from "../src";
import SyntaxHighLighter from "react-syntax-highlighter";
import HelpOutlineIcon from "@material-ui/icons/HelpOutline";
import { docco } from "react-syntax-highlighter/dist/cjs/styles/hljs";
import "./demo.css";

const source1 =
    "https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/Migliore_2018_CA1/exp_data/abf-int-bAC/Ivy_960711AHP3/96711008.abf";
const source2 =
    "https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/test/spiketrainsx2a.nix";

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
                        style={{
                            width: "50px",
                            height: "50px",
                            verticalAlign: "middle",
                        }}
                    />
                    <span
                        className="title-style"
                        style={{ paddingLeft: "15px", verticalAlign: "middle" }}
                    >
                        Neural Activity Visualizer
                    </span>
                    <div
                        className="subtitle-style"
                        style={{ paddingTop: "30px" }}
                    >
                        Javascript component for visualizing neural activity
                        data
                    </div>
                </div>
            </div>
            <br />
            <br />
            <div className="text">
                The neural-activity-visualizer Javascript app, enables
                web-browser visualisation of electrophysiology datafiles in any
                format supported by the Neo library. It makes use of the{" "}
                <a
                    href="https://neo-viewer.brainsimulation.eu/#api_docs"
                    target="_blank"
                >
                    Neo Viewer REST API
                </a>
                .
            </div>
            <br />
            <br />
            <h2 className="text" style={{ marginLeft: 0 }}>
                Example: Basic usage
            </h2>
            <div
                className="text"
                style={{ marginLeft: 10, marginTop: 25, fontWeight: "bold" }}
            >
                Source Code:
            </div>
            <div>
                <SyntaxHighLighter
                    language="javascript"
                    style={docco}
                    codeTagProps={{ style: { fontSize: 16, lineHeight: 2 } }}
                >
                    {`import Visualizer from 'neural-activity-visualizer-react'
                      ...
                      let source_url = "${source1}"
                      <Visualizer source={source_url} />`.replace(
                        /\n +/g,
                        "\n"
                    )}
                </SyntaxHighLighter>
            </div>
            <div
                className="text"
                style={{ marginLeft: 10, marginTop: 25, fontWeight: "bold" }}
            >
                Output:
            </div>
            <div>
                <Visualizer source={source1} />
            </div>
            <br />
            <br />
            <h2 className="text" style={{ marginLeft: 0 }}>
                Example: Interactive Demo
            </h2>
            <div
                className="text"
                style={{ marginLeft: 10, marginTop: 25, fontWeight: "bold" }}
            >
                Attributes:
            </div>
            <br />
            <Box
                sx={{
                    "& .MuiTextField-root": { m: 1 },
                }}
            >
                <TextField
                    name="source_url"
                    label="File Source URL"
                    // defaultValue={this.state.name}
                    // onBlur={this.handleFieldChange}
                    variant="outlined"
                    fullWidth
                    InputProps={{
                        startAdornment: (
                            <Tooltip title="Specify the URL of the file to be visualized">
                                <InputAdornment position="start">
                                    <HelpOutlineIcon />
                                </InputAdornment>
                            </Tooltip>
                        ),
                    }}
                    InputLabelProps={{
                        style: {
                            fontSize: 16,
                            fontWeight: "bold",
                            color: "#000000",
                        },
                    }}
                />
            </Box>
            <Box
                component="form"
                sx={{
                    "& .MuiTextField-root": { m: 1, width: "25ch" },
                }}
                noValidate
                autoComplete="off"
            >
                <div>
                    <TextField
                        name="width"
                        label="Width"
                        type="number"
                        // defaultValue={this.state.name}
                        // onBlur={this.handleFieldChange}
                        variant="outlined"
                        InputProps={{
                            startAdornment: (
                                <Tooltip title="Set width of visualization panel; inherits from parent as default">
                                    <InputAdornment position="start">
                                        <HelpOutlineIcon />
                                    </InputAdornment>
                                </Tooltip>
                            ),
                            inputProps: {
                                min: 0,
                                max: 9999,
                                maxLength: 4,
                            },
                        }}
                        InputLabelProps={{
                            style: {
                                fontSize: 16,
                                fontWeight: "bold",
                                color: "#000000",
                            },
                        }}
                    />
                    <TextField
                        name="height"
                        label="Height"
                        type="number"
                        // defaultValue={this.state.name}
                        // onBlur={this.handleFieldChange}
                        variant="outlined"
                        InputProps={{
                            startAdornment: (
                                <Tooltip title="Set height of visualization panel; inherits from parent (max 450px) as default">
                                    <InputAdornment position="start">
                                        <HelpOutlineIcon />
                                    </InputAdornment>
                                </Tooltip>
                            ),
                            inputProps: {
                                min: 0,
                                max: 9999,
                                maxLength: 4,
                            },
                        }}
                        InputLabelProps={{
                            style: {
                                fontSize: 16,
                                fontWeight: "bold",
                                color: "#000000",
                            },
                        }}
                    />
                    <TextField
                        name="downsample_Factor"
                        label="Downsampling Factor"
                        type="number"
                        // defaultValue={this.state.name}
                        // onBlur={this.handleFieldChange}
                        variant="outlined"
                        InputProps={{
                            startAdornment: (
                                <Tooltip title="Set the downsampling factor for loading data">
                                    <InputAdornment position="start">
                                        <HelpOutlineIcon />
                                    </InputAdornment>
                                </Tooltip>
                            ),
                            inputProps: {
                                min: 0,
                                max: 99,
                                maxLength: 2,
                            },
                        }}
                        InputLabelProps={{
                            style: {
                                fontSize: 16,
                                fontWeight: "bold",
                                color: "#000000",
                            },
                        }}
                    />
                </div>
            </Box>
            <div
                className="text"
                style={{ marginLeft: 10, marginTop: 25, fontWeight: "bold" }}
            >
                Source Code:
            </div>
            <div>
                <SyntaxHighLighter
                    language="javascript"
                    style={docco}
                    codeTagProps={{ style: { fontSize: 16, lineHeight: 2 } }}
                >
                    {`import Visualizer from 'neural-activity-visualizer-react'
                      ...
                      let source_url = "${source1}"
                      <Visualizer source={source_url} />`.replace(
                        /\n +/g,
                        "\n"
                    )}
                </SyntaxHighLighter>
            </div>
            <div
                className="text"
                style={{ marginLeft: 10, marginTop: 25, fontWeight: "bold" }}
            >
                Output:
            </div>
            <div>
                <Visualizer
                    source={source1}
                    showSpikeTrains={false}
                    showSignals={true}
                    disableChoice={true}
                    // width={900}
                    // height={350}
                />
            </div>
            <br />
            <br />
            <div className="rainbow-row">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
            <p className="text" style={{ marginTop: 20 }}>
                This project has received funding from the European Union’s
                Horizon 2020 Framework Programme for Research and Innovation
                under the Specific Grant Agreements No. 785907 and No. 945539
                (Human Brain Project SGA2 and SGA3).
            </p>
            <p className="text" style={{ marginTop: 20, marginBottom: 40 }}>
                If you encounter any problems,{" "}
                <a
                    href="https://github.com/NeuralEnsemble/neo-viewer/issues/new"
                    target="_blank"
                >
                    please let us know.
                </a>
            </p>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById("app"));

module.hot.accept();

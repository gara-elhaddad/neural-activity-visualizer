import DataStore from '../src/datastore';


const testUrl = "https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/Migliore_2018_CA1/exp_data/abf-int-bAC/Ivy_960711AHP3/96711008.abf";

test('newly created DataStore is not initialized', () => {
    const ds = new DataStore(testUrl);
    expect(ds.datafileUrl).toBe(testUrl);
    expect(ds.initialized).toBe(false);
});

test('initialize() returns a promise', () => {
    const ds = new DataStore(testUrl);
    const response = ds.initialize();
    expect(Promise.resolve(response)).toEqual(response);
});

test('resolving the promise returned by initialize() sets the "block" attribute', () => {
    const ds = new DataStore(testUrl);
    const target = {
        "block":{
            "annotations": {
              "abf_version": "2.4"
            },
            "description": "",
            "file_origin": "96711008.abf",
            "name": "",
            "rec_datetime": "1996-07-11T17:03:40",
            "file_name": "96711008.abf",
            "segments": [
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              },
              {
                "name": "",
                "annotations": {
                  "abf_version": "2.4"
                },
                "description": "",
                "spiketrains": [],
                "rec_datetime": null,
                "irregularlysampledsignals": [],
                "file_origin": "96711008.abf",
                "analogsignals": []
              }
            ],
            "consistency": "consistent"
          }
    };
    return ds.initialize().then(res => {
        expect(ds.blocks).toEqual([target.block]);
        expect(ds.initialized).toBe(true);
    });
});

test('getLabels() should return segment and signal labels', () => {
    const ds = new DataStore("http://fakeUrl");
    ds.initialized = true;
    ds.blocks = [
        {
            segments: [
                {
                    name: "segA",
                    analogsignals: [
                        {name: "sigA0"}, {name: "sigA1"}
                    ]
                },
                {
                    name: "segB",
                    as_prop: [
                        {name: "sigB0"}, {name: "sigB1"}, {}
                    ],
                    analogsignals: [{}, {}, {}]
                },
                {
                    name: "",  // no name, so name should be constructed
                    analogsignals: [
                        {name: "sigC0"}, {}, {name: "sigC2"}
                    ]
                }
            ]
        }
    ];
    const target = [
        {
            label: "segA",
            signalLabels: ["sigA0", "sigA1"]
        },
        {
            label: "segB",
            signalLabels: ["sigB0", "sigB1", "Signal #2"]
        },
        {
            label: "Segment #2",
            signalLabels: ["sigC0", "Signal #1", "sigC2"]
        }
    ];
    const blockId = 0;
    expect(ds.getLabels(blockId)).toEqual(target);
});

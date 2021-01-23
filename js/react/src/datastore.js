import axios from 'axios';

const baseUrl = "https://neo-viewer.brainsimulation.eu";

class DataStore {
    constructor(datafileUrl) {
        this.datafileUrl = datafileUrl;
        this.blocks = [];
        this.initialized = false;
    }

    initialize() {
        if (~this.initialized) {
            const url = `${baseUrl}/blockdata/?url=${this.datafileUrl}`;
            const config = {}
            return axios.get(url, config)
                .then(res => {
                    this.blocks = res.data.block;
                    this.initialized = true;
                    console.log(`Initialized datastore for ${this.datafileUrl}`);
                    console.log(this.blocks);
                });
        }
    }

    segmentIsLoaded(blockId, segmentId) {
        const segmentArray = this.blocks[blockId].segments;
        if (segmentArray.length > segmentId) {
            return (segmentArray[segmentId].analogsignals.length > 0);
        } else {
            return false;
        }
    }

    signalIsLoaded(blockId, segmentId, signalId) {
        if (this.segmentIsLoaded(blockId, segmentId)) {
            const signalArray = this.blocks[blockId].segments[segmentId].analogsignals;
            if (signalArray.length > signalId) {
                if (signalArray[signalId].values) {
                    return true
                } else {
                    return false
                }
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    loadSegment(blockId, segmentId) {
        const url = `${baseUrl}/segmentdata/?url=${this.datafileUrl}&segment_id=${segmentId}`;
        const config = {};
        console.log(`Trying to load segment #${segmentId}`);
        return axios.get(url, config)
            .catch(err => Promise.reject(`Error loading segment #${segmentId}: ${err.message}`));
    }

    loadSignal(blockId, segmentId, signalId, downSampleFactor) {
        const url = `${baseUrl}/analogsignaldata/?url=${this.datafileUrl}&segment_id=${segmentId}&analog_signal_id=${signalId}&down_sample_factor=${downSampleFactor || 1}`;
        const config = {};
        console.log(`Trying to load signal #${signalId} in segment #${segmentId}`);
        return axios.get(url, config)
            .catch(err => Promise.reject(`Error loading signal #${signalId} in segment #${segmentId}: ${err.message}`));
    }

    getSignal(blockId, segmentId, signalId, downSampleFactor) {
        if (this.segmentIsLoaded(blockId, segmentId)) {
            if (this.signalIsLoaded(blockId, segmentId, signalId)) {
                console.log(`1. Returning already-loaded signal #${signalId} in segment #${segmentId}`);
                return new Promise((resolve, reject) => {
                    resolve(this.blocks[blockId].segments[segmentId].analogsignals[signalId]);
                    reject();
                });
            } else {
                return this.loadSignal(blockId, segmentId, signalId, downSampleFactor)
                    .then(res => {
                        console.log(`2. Loaded signal for signal #${signalId} in segment #${segmentId}`);
                        this.blocks[blockId].segments[segmentId].analogsignals[signalId] = res.data;
                        return res.data;
                    });
            }
        } else {
            return this.loadSegment(blockId, segmentId)
                .then(res => {
                    console.log(`3a. Loaded data for segment #${segmentId}`);
                    this.blocks[blockId].segments[segmentId] = res.data;
                    return this.loadSignal(blockId, segmentId, signalId, downSampleFactor);
                })
                .then(res => {
                    console.log(`3b. Loaded signal for signal #${signalId} in segment #${segmentId}`);
                    this.blocks[blockId].segments[segmentId].analogsignals[signalId] = res.data;
                    return res.data;
                });
        }
    }

}


export default DataStore;

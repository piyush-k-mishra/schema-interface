import React, { Component } from 'react';
import isEmpty from 'lodash/isEmpty'
import RefreshIcon from '@material-ui/icons/Refresh'

import UploadModal from './UploadModal';
import Canvas from './Canvas';
import SideBar from './SideBar';

class Viewer extends Component {
    constructor(props) {
        super(props)

        this.state = {
            schemaResponse: '',
            isOpen: false,
            nodeData: {}
        }

        this.callbackFunction = this.callbackFunction.bind(this);
        this.sidebarCallback = this.sidebarCallback.bind(this);
    }

    callbackFunction(childData) {
        this.setState({ schemaResponse: childData });
    }

    sidebarCallback(data) {
        if (isEmpty(data)) {
            this.setState({
                isOpen: false,
                nodeData: data
            });
        } else {
            this.setState({
                isOpen: true,
                nodeData: data
            });
        }
    }

    render() {
        let canvas = "";
        let sidebarClassName = this.state.isOpen ? "sidebar-open" : "sidebar-closed";
        let canvasClassName = this.state.isOpen ? "canvas-shrunk": "canvas-wide";

        if (this.state.schemaResponse !== '') {
            canvas = <Canvas id="canvas"
                elements={this.state.schemaResponse}
                sidebarCallback={this.sidebarCallback}
                className={canvasClassName}
            />;
        }

        return (
            <div id="viewer">
                <UploadModal buttonLabel="Upload Schema" parentCallback={this.callbackFunction} />
                <div style={{display: 'inline-flex'}}>
                    <SideBar
                        data={this.state.nodeData}
                        isOpen={this.state.isOpen} 
                        className={sidebarClassName} />
                    {canvas}
                    <div style={{'width': '0', height: '3vh'}}>
                        <RefreshIcon color="action" fontSize='large'/>
                    </div>
                </div>
            </div>
        )
    }
}

export default Viewer;
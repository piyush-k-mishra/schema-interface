import React, { Component } from 'react';
import { Container } from 'reactstrap';

import UploadModal from './UploadModal';
import Canvas from './Canvas';

class Viewer extends Component {
    constructor(props) {
        super(props)

        this.state = {
            schemaResponse: ''
        }

        this.callbackFunction = this.callbackFunction.bind(this)
    }

    callbackFunction(childData) {
        this.setState({schemaResponse: childData})
    }

    render() {
        let canvas = "";

        if (this.state.schemaResponse !== '') {
            canvas = <Canvas elements={this.state.schemaResponse}/>
        }
        return (
            <div>
                <UploadModal buttonLabel="Click Me!!!" parentCallback={this.callbackFunction}/>
                {canvas}
            </div>
        )
    }
}

export default Viewer;
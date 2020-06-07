import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

import Background from '../public/canvas_bg.png'

class Canvas extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {

        const style = {
            width: '90vw',
            height: '75vh',
            margin: '2vh 5vw 0 5vw',
            'border-style': 'solid',
            'background-image': `url(${"/static" + Background})`
        };

        const stylesheet = [
            {
                selector: 'node',
                style: {
                    width: 20,
                    height: 20,
                    shape: 'rectangle'
                }
            },
            {
                selector: 'edge',
                style: {
                    width: 15
                }
            }
        ]

        const layout = {
            name: 'breadthfirst'
        };

        return (
            <CytoscapeComponent
                elements={this.props.elements}
                layout={layout}
                style={style}
            />
        );
    }
}

export default Canvas;
import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

import Background from '../public/canvas_bg.png'

class Canvas extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            canvasElements: CytoscapeComponent.normalizeElements(this.props.elements)
        }

        this.showDrawer = this.showDrawer.bind(this)
        this.showSubTree = this.showSubTree.bind(this)
    }

    showDrawer(data) {
        console.log('Render Drawer for' + JSON.stringify(data))
    }

    showSubTree(node) {
        console.log('Render subtree for' + JSON.stringify(node))
    }

    componentDidMount() {
        this.cy.ready(() => {
            this.cy.on('tap', event => {
                if (event.target.cy) {
                    this.showSubTree(event.target.data())
                }
            })

            this.cy.on('cxttap', event => {
                if (event.target.cy) {
                    this.showDrawer(event.target.data())
                }
            })
        })
    }

    render() {

        const style = {
            width: '90vw', 
            height: '75vh',
            borderStyle: 'solid',
            backgroundImage: `url(${"/static" + Background})`
        };

        const stylesheet = [
            {
                selector: 'node',
                style: {
                    'content': 'data(label)',
                    'shape': 'data(type)',
                    'width': '90vw',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '10vh',
                    'font-weight': 'bold',
                    'text-wrap': 'wrap',
                    'text-overflow-wrap': 'whitespace',
                    'text-max-width': '80vw',
                    'background-color': 'white',
                    'border-color': 'black',
                    'border-width': '1px',
                    'border-style': 'dotted'
                }
            },{
                selector: 'node:selected',
                style: {
                    'background-color': 'gray',
                }
            },
            {
                selector: ':parent',
                style: {
                  'text-valign': 'top',
                  'text-halign': 'center',
                }
            },
            {
                selector: 'edge',
                style: {
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'line-style': 'solid'
                }
            },
            {
                selector: '.root-edge',
                style: {
                    'line-color': '#f00'
                }
            }
        ]

        const layout = {
            name: 'breadthfirst',
            fit: true, // whether to fit the viewport to the graph
            directed: true, // whether the tree is directed downwards (or edges can point in any direction if false)
            padding: 10, // padding on fit
            circle: false, // put depths in concentric circles if true, put depths top down if false
            grid: false, // whether to create an even grid into which the DAG is placed (circle:false only)
            spacingFactor: 0.75, // positive spacing factor, larger => more space between nodes (N.B. n/a if causes overlap)
            boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
            avoidOverlap: true, // prevents node overlap, may overflow boundingBox if not enough space
            nodeDimensionsIncludeLabels: true, // Excludes the label when calculating node bounding boxes for the layout algorithm
            roots: '#root', // the roots of the trees
            maximal: true, // whether to shift nodes down their natural BFS depths in order to avoid upwards edges (DAGS only)
            rotate: 90
        };
        return (
            <div style={{margin: '2vh 5vw 0 5vw', 'display': 'inline-flex'}}>
                <CytoscapeComponent
                    elements={this.state.canvasElements}
                    layout={layout}
                    style={style}
                    stylesheet={stylesheet}
                    cy={(cy) => { this.cy = cy }}
                />
                <div style={{'width': '0', height: '3vh'}}>
                    <RefreshIcon color="action" fontSize='large' onClick={this.reloadCanvas}/>
                </div>
            </div>
        );
    }
}

export default Canvas;
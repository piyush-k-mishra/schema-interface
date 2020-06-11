import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import RefreshIcon from '@material-ui/icons/Refresh'

import Background from '../public/canvas_bg.png'
import CyStyle from './cy-style.json'

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
            this.cy.on('cxttap', event => {
                if (event.target.cy) {
                    this.showSubTree(event.target.data())
                }
            })

            this.cy.on('tap', event => {
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

        return (
            <div style={{margin: '2vh 5vw 0 5vw', 'display': 'inline-flex'}}>
                <CytoscapeComponent
                    elements={this.state.canvasElements}
                    layout={CyStyle.layout}
                    style={style}
                    stylesheet={CyStyle.stylesheet}
                    cy={(cy) => { this.cy = cy }}
                />
                <div style={{'width': '0', height: '3vh'}}>
                    <RefreshIcon color="action" fontSize='large'/>
                </div>
            </div>
        );
    }
}

export default Canvas;
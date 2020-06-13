import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

import Background from '../public/canvas_bg.png'
import CyStyle from '../public/cy-style.json'

class Canvas extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            canvasElements: CytoscapeComponent.normalizeElements(this.props.elements)
        }

        this.showSidebar = this.showSidebar.bind(this)
        this.showSubTree = this.showSubTree.bind(this)
    }

    showSidebar(data) {
        this.props.sidebarCallback(data);
    }

    showSubTree(node) {
        console.log('Render subtree for' + JSON.stringify(node))
    }

    componentDidMount() {
        this.cy.ready(() => {
            this.cy.on('cxttap', 'node', event => {
                this.showSubTree(event.target.data())
            })

            this.cy.on('tap', event => {
                this.props.sidebarCallback(event.target.data())
            })
        })
    }

    render() {
        const style = {
            width: 'inherit', 
            height: '75vh',
            borderStyle: 'solid',
            backgroundImage: `url(${"/static" + Background})`
        };

        return (
            <div className={this.props.className} style={{marginTop: '2vh', width: 'inherit'}}>
                <CytoscapeComponent
                    elements={this.state.canvasElements}
                    layout={CyStyle.layout}
                    style={style}
                    stylesheet={CyStyle.stylesheet}
                    cy={(cy) => { this.cy = cy }}
                    maxZoom={4} minZoom={0.5}
                />
            </div>
        );
    }
}

export default Canvas;
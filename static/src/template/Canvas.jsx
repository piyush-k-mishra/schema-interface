import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

import axios from 'axios';
import isNull from 'lodash/isNull';

import Background from '../public/canvas_bg.png';
import CyStyle from '../public/cy-style.json';

class Canvas extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            canvasElements: CytoscapeComponent.normalizeElements(this.props.elements),
            currentSubtree: null
        }

        this.showSidebar = this.showSidebar.bind(this);
        this.showSubTree = this.showSubTree.bind(this);
        this.removeSubTree = this.removeSubTree.bind(this);
    }

    showSidebar(data) {
        this.props.sidebarCallback(data);
    }

    showSubTree(node) {
        axios.get('/node', {
            params: {
                ID: node.id
              }
            })
            .then(res => {
                if (!isNull(this.state.currentSubtree) && this.state.currentSubtree !== res.data) {
                    this.removeSubTree(this.state.currentSubtree);
                }
                this.setState({currentSubtree: res.data});
                this.cy.add(res.data);
                let layout = this.cy.makeLayout(CyStyle.layout);
                layout.run();
            })
            .catch(err => {
                console.error(err);
            })
    }

    removeSubTree(currentSubtree) {
        const nodes = currentSubtree.nodes;
        for (let i = 0; i < nodes.length; i++) {
            if (nodes[i].data.type !== 'step' || nodes[i].data.id === 'root') {
                let el = this.cy.getElementById(nodes[i].data.id);
                this.cy.remove(el);
            }
        }
        let layout = this.cy.makeLayout(CyStyle.layout);
        layout.run();
        this.setState({currentSubtree: null});
    }

    componentDidMount() {
        this.cy.ready(() => {
            this.cy.on('tap', event => {
                if (event.target.group && event.target.group() === 'nodes') {
                    let node = event.target.data();
                    this.showSubTree(node);
                } else {
                    if (!isNull(this.state.currentSubtree)) {
                        this.removeSubTree(this.state.currentSubtree);
                    }
                }
            })

            this.cy.on('cxttap', event => {
                this.props.sidebarCallback(event.target.data());
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
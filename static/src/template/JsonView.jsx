import React, { Component } from 'react';
import ReactJson from 'react-json-view';
import axios from 'axios';

class JsonView extends Component {
    constructor(props) {
        super(props);

        this.handleAdd = this.handleAdd.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleEdit = this.handleEdit.bind(this);
    }

    handleAdd (e) {
        if (e.new_value == "error") {
            return false;
        } else if (e.new_value.indexOf(null) > -1) {
            return true;
        } else {
            axios.post("/reload", e.updated_src)
                .then(res => {
                    this.props.parentCallback(res.data);
                })
                .catch(err => {
                    console.error('reload fail');
                    return false;
                });
            return true;
        }
    }

    handleDelete (e) {
        if (e.new_value !== "error") {
            axios.post("/reload", e.updated_src)
                .then(res => {
                    this.props.parentCallback(res.data);
                })
                .catch(err => {
                    console.error('reload fail');
                    return false;
                });
        } else {
            return false;
        }
    }

    handleEdit (e) {
        if (e.new_value !== "error") {
            axios.post("/reload", e.updated_src)
                .then(res => {
                    this.props.parentCallback(res.data);
                })
                .catch(err => {
                    console.error('reload fail');
                    return false;
                });
        } else {
            return false;
        }
    }

    render () {
        const style = {
            padding: "30px", 
            backgroundColor: "white", 
            fontSize: "15px"
        }
        return (
            <div id="schema-json">
                <ReactJson 
                    name={"schema"}
                    sortKeys
                    style={style}
                    src={this.props.schemaJson}
                    collapsed={2}
                    collapseStringsAfterLength={100}
                    displayDataTypes={false}
                    onEdit={this.handleEdit}
                    onDelete={this.handleDelete}
                    onAdd={this.handleAdd}
                    displayObjectSize={true}
                />
            </div>
        )
    }
}

export default JsonView;
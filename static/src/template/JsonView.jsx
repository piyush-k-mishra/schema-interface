import React, { useState } from 'react';
import ReactJson from 'react-json-view';

function JsonView (props) {
    return (
        <div id="schema-json">
            <ReactJson sortKeys
                        style={{ padding: "30px", backgroundColor: "white" }}
                        src={props.schemaJson}
                        collapsed={2}
                        displayDataTypes={false}
                        // collapseStringsAfterLength={12}
                        onEdit={e => {
                            console.log("edit callback", e)
                            if (e.new_value == "error") {
                                return false
                            }
                        }}
                        onDelete={e => {
                            console.log("delete callback", e)
                        }}
                        onAdd={e => {
                            console.log("add callback", e)
                            if (e.new_value == "error") {
                                return false
                            }
                        }}
                        onSelect={e => {
                            console.log("select callback", e)
                            console.log(e.namespace)
                        }}
                        displayObjectSize={true}
                        name={"schema"}
                        enableClipboard={copy => {
                            console.log("you copied to clipboard!", copy)
                        }}
                        shouldCollapse={({ src, namespace, type }) => {
                            if (type === "array" && src.indexOf("test") > -1) {
                                return true
                            } else if (namespace.indexOf("moment") > -1) {
                                return true
                            }
                            return false
                        }}
            />
        </div>
    );
}

export default JsonView;
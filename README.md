# schema-interface

## Introduction

This is a web tool to visualize KAIROS Schema Format generated schemas using Cytoscape.js and React.js. The tool also allows editing of these schemas for curation purpose. Current supported KSF version is **0.71**.

**This project is currently a work in progress and is in alpha testing. Feedbacks and suggestions are welcome.**

## Getting Started

To run the project locally one needs to have following libraries installed:

* npm 6.13.4 (or latest)
* Python 3.7.3 (or latest)
* pip 20.1.1 (or latest)

First run:

* cd path/to/project/schema-interface
* sh first_run.sh

Subsequent runs:

* cd path/to/project/schema-interface
* sh run_local.sh

## Libraries

The tool mainly uses 3 resources:

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) : A Python micro web framework used for writing the backend functionality of the tool. Schema extraction and edit handling has been done in Flask.
* [React.js](https://reactjs.org/): A frontend JavaScript library responible for rendering the UI. All the interactions between the visualization and the backend framwork is handled by React.
* [Cytoscape.js](https://js.cytoscape.org/): A data visualization library that uses the extracted schema, provided by React from backend, to provide a graphical structure in a sequential order. CRUD operations on the visualizations is currently being handled by using _**[react-json-view](https://github.com/mac-s-g/react-json-view/blob/master/README.md)**_ library. This library allows updation of the schemas and Cytoscape reloads the graph with added change.

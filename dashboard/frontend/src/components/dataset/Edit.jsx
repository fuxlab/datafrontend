import React, { Component } from 'react';

import { connect } from 'react-redux';
import { datasets } from "../../actions";

import {
    Icon,
    Button,
    InputGroup,
    Dialog
} from "@blueprintjs/core";

import EditWindow from "./../base/EditWindow";

class DatasetEdit extends Component {
  
  state = {
    dataset: {},
    isOpen: false,
  }

  submitDataset = (e) => {
    if(e){
      e.preventDefault();
    }
    if (this.state.updateDatasetId === null) {
      this.props.addDataset(this.state.data).then(this.resetForm)
      this.refs.EditDatasetWindow.setState({ isOpen: false});
    } else {
      this.props.updateDataset(this.state.updateDatasetId, this.state.data);
    }
  }

  edit(id){
    console.log('edit');
    this.setState('isOpen', true);
  }

  create(){
    console.log('create');
    this.setState('isOpen', true);
  }

  render() {
    return(
      <EditWindow title="Edit Project" isOpen={this.state.isOpen} ref="EditProjectWindow" icon="box" submitMethod={this.submitProject}>
        <form ref="form" onSubmit={this.submitDataset}>
          <InputGroup
            large="true"
            value={this.state.dataset.project_id}
            placeholder="project_id"
            required
          />
          <InputGroup
            large="true"
            value={this.state.dataset.identifier}
            placeholder="Enter identifier here..."
            onChange={(e) => this.setState({data: Object.assign(this.state.dataset, { 'identifier': e.target.value })})}
            required
          />
          <InputGroup
            large="true"
            value={this.state.dataset.name}
            placeholder="Enter name here..."
            onChange={(e) => this.setState({data: Object.assign(this.state.dataset, { 'name': e.target.value })})}
            required
          />
        </form>
      </EditWindow>
    );
  }
}

const mapStateToProps = state => {
  return {
    isOpen: state.isOpen,
  }
}

const mapDispatchToProps = dispatch => {
  return {
    fetchDataset: (id) => {
      console.log('fetch');
      dispatch(datasets.fetchDataset(id));
    },
    addDataset: (data) => {
      console.log('add');
      return dispatch(datasets.addDataset(data));
    },
    updateDataset: (id, data) => {
      return dispatch(datasets.updateDataset(id, data));
    },
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(DatasetEdit);

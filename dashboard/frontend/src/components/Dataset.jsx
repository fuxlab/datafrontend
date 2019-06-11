import React, { Component } from 'react';
import { connect } from 'react-redux';
import { datasets } from "../actions";

import {
    Icon,
    Button,
    InputGroup
} from "@blueprintjs/core";

import { IconNames } from "@blueprintjs/icons";

import Layout from "./base/Layout";
import StarterCard from "./base/StarterCard";
import OverviewTable from "./base/OverviewTable";

import DatasetTree from "./dataset/Tree";
import DatasetEdit from "./dataset/Edit";

class Dataset extends Component {

  state = {
    project: {
      id: 0,
      name: ""
    },
    
    datasets: [],
    documents: [],
    
    dataset_edit_window_title: '',
    dataset_edit_window_visibility: false,
    dataset: {
      project_id: 0,

      id: 0,
      name: "",
      identifier: "",
    }
  }

  componentDidMount() {
    // ToDo: Maybe this causes trouble
    // solution? this.props.dispatch(datasets.fetchDatasets());
    this.props.fetchDatasets();
  }

  resetForm(){
    this.setState({ 'dataset': {
      project_id: this.props.match.params.id,
      
      id: 0,
      name: "",
      identifier: ""
    } });    
  }

  // Dataset Actions
  addDatasetEdit = () => {
    this.setState({'dataset_edit_window_title': 'Create Dataset'});
    this.resetForm();
    
    this.setState({'dataset_edit_window_visibility': true});
  }

  editDatasetEdit = (id) => {
    this.setState({'dataset_edit_window_title': 'Edit Dataset'});
    this.resetForm();

    this.props.fetchDataset(id).then((e) => {
      this.setState({ 'dataset': e.dataset }); 
      this.setState({ 'dataset_edit_window_visibility': true });
    });
  }

  changeDatasetEdit = (e) => {
    var type = e.target.name;
    this.setState({ dataset: Object.assign(this.state.dataset, { [type] : e.target.value }) });
  }

  submitDatasetEdit = () => {
    if(this.state.dataset.id) {
      this.props.updateDataset(this.state.dataset.id, this.state.dataset);
    } else {
      this.props.addDataset(this.state.dataset);
    }

    this.setState({'dataset_edit_window_visibility': false});
  }

  closeDatasetEdit = () => {
    this.setState({'dataset_edit_window_visibility': false});
  }

  render() {
    if (!this.props.match.params.id || this.props.match.params.id == 0) {
      document.location = '/';
    }

    var dataset_actions = [
      { 'icon': 'add', 'text': 'Add Dataset', 'action': (e) => this.addDatasetEdit(e) }
    ]

    var overview_actions = [
      { 'icon': 'edit', 'action': (e) => this.editDatasetEdit(e) },
      { 'icon': 'trash', 'action': (e) => this.props.deleteDataset(e) },
    ]

    return (
      <Layout className="datasets">
        <div className="sidebar">
          <StarterCard header="Datsets" actions={dataset_actions}>
            <DatasetTree datasets={this.props.datasets} />
          </StarterCard>
        </div>

        <div className="content">
          <StarterCard header="Dataset Overview" actions={dataset_actions}>
            <OverviewTable
              data={this.props.datasets}
              columns={['id', 'identifier', 'name']}
              actions={overview_actions}
            />
          </StarterCard>
        </div>

        <DatasetEdit
          title={this.state.dataset_edit_window_title}
          isOpen={this.state.dataset_edit_window_visibility}
          dataset={this.state.dataset}
          submitMethod={this.submitDatasetEdit}
          changeMethod={this.changeDatasetEdit}
          closeMethod={this.closeDatasetEdit}
        />
      </Layout>
    )
  }
}

const mapStateToProps = state => {
  return {
    datasets: state.datasets.all,
    dataset: state.datasets.one
  }
}

const mapDispatchToProps = dispatch => {
  return {
    addDataset: (data) => {
      return dispatch(datasets.addDataset(data));
    },
    fetchDataset: (id) => {
      return dispatch(datasets.fetchDataset(id));
    },
    updateDataset: (id, data) => {
      return dispatch(datasets.updateDataset(id, data));
    },
    deleteDataset: (id) => {
      dispatch(datasets.deleteDataset(id));
    },
    fetchDatasets: () => {
      dispatch(datasets.fetchDatasets());
    },
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Dataset);
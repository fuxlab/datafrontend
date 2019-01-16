import React, { Component } from 'react';
import { connect } from 'react-redux';
import { datasets } from "../actions";

import {
    Icon,
    Button,
    InputGroup
} from "@blueprintjs/core";

import { IconNames } from "@blueprintjs/icons";

import Layout from "./Layout";
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
    data: {
      id: 0,
      project_id: 0,
      name: "",
      identifier: "",
    },
    updateDatasetId: null,
    dataset_detail_open: false,
  }

  resetForm = () => {
    this.setState({
      data: {
        name: "",
        identifier: "",
      },
      updateDatasetId: null
    });
  }
  
  componentDidMount() {
    this.props.fetchDatasets();
  }

  render() {
    if (!this.props.match.params.id || this.props.match.params.id == 0) {
      document.location = '/';
    }

    var dataset_actions = [
      { 'icon': 'add', 'text': 'Add Dataset', 'action': (e) => this.setState({dataset_detail_open: true}) }
    ]

    var overview_actions = [
      { 'icon': 'edit', 'action': (e) => this.setState({dataset_detail_open: true}) },
      { 'icon': 'trash', 'action': (e) => this.props.deleteDataset(e) },
    ]
    return (
      <Layout className="datasets">
        <div className="menu">
          <StarterCard header="Datsets" actions={dataset_actions}>
            <DatasetTree/>
          </StarterCard>
        </div>

        <div className="content">
          <StarterCard header="Dataset List" actions={dataset_actions}>
            <OverviewTable data={this.props.datasets} columns={['id', 'identifier', 'name']} actions={overview_actions}></OverviewTable>
          </StarterCard>
        </div>
        <DatasetEdit ref="EditDatasetWindow" id="1" isOpen={this.state.dataset_detail_open} />
      </Layout>
    )
  }
}

const mapStateToProps = state => {
  return {
    datasets: state.datasets,
  }
}

const mapDispatchToProps = dispatch => {
  return {
    deleteDataset: (id) => {
      dispatch(datasets.deleteDataset(id));
    },
    fetchDatasets: () => {
      dispatch(datasets.fetchDatasets());
    },
    addDataset: (data) => {
      return dispatch(datasets.addDataset(data));
    },
    updateDataset: (id, data) => {
      return dispatch(datasets.updateDataset(id, data));
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Dataset);
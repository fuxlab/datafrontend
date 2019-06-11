import React, { Component } from 'react';
import {connect} from 'react-redux';
import {projects} from "../actions";

import {
    InputGroup,
} from "@blueprintjs/core";

import Layout from "./base/Layout";
import StarterCard from "./base/StarterCard";
import EditWindow from "./base/EditWindow";
import OverviewTable from "./base/OverviewTable";

class Project extends Component {

  state = {
    name: "",
    updateProjectId: null,
    isOpen: false,
  }

  resetForm = () => {
    this.setState({
      name: "",
      updateProjectId: null
    });
  }

  selectProject = (index) => {
    // TODO: replace this (and all document.locations) when changing routing
    var id = this.props.projects[index].id
    document.location = '/datasets/'+id;
    return;
  }  

  selectForEdit = (index) => {
    this.refs.EditProjectWindow.setState({ isOpen: true});
    let project = this.props.projects[index];

    this.setState({
      name: project.name,
      updateProjectId: index
    });
  }

  submitProject = (e) => {
    if(e){
      e.preventDefault();
    }
    if (this.state.updateProjectId === null) {
      this.props.addProject(this.state.name).then(this.resetForm)
      this.refs.EditProjectWindow.setState({ isOpen: false});
    } else {
      this.props.updateProject(this.state.updateProjectId, this.state.name);
    }
  }
  
  actionAddProject = () => {
    this.refs.EditProjectWindow.setState({ isOpen: true});
    this.resetForm();
  }

  render() {
    var starter_actions = [
      { 'icon': 'add', 'text': 'Add Project', 'action': this.actionAddProject }
    ]
    var overview_actions = [
      { 'icon': 'play', 'action': this.selectProject },
      { 'icon': 'edit', 'action': this.selectForEdit },
      { 'icon': 'trash', 'action': (e) => this.props.deleteProject(e) },
    ]
    return (
      <Layout>
        <StarterCard header="Projects" actions={starter_actions}>
          <OverviewTable data={this.props.projects} columns={['id', 'name']} actions={overview_actions}></OverviewTable>
        </StarterCard>

        <EditWindow title="Edit Project" ref="EditProjectWindow" icon="box" submitMethod={this.submitProject}>
          <form ref="form" onSubmit={this.submitProject}>
            <InputGroup
                large="true"
                value={this.state.name}
                placeholder="Enter note here..."
                onChange={(e) => this.setState({name: e.target.value})}
                required            
            />
          </form>
        </EditWindow>
      </Layout>
    )
  }
}

const mapStateToProps = state => {
  return {
    projects: state.projects,
  }
}

const mapDispatchToProps = dispatch => {
  return {
    deleteProject: (id) => {
      dispatch(projects.deleteProject(id));
    },
    addProject: (name) => {
      return dispatch(projects.addProject(name));
    },
    updateProject: (id, name) => {
      return dispatch(projects.updateProject(id, name));
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Project);
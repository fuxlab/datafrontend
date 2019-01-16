import React, { Component } from 'react';
import {connect} from 'react-redux';

import { IconNames } from "@blueprintjs/icons";

import Menu from "./base/Menu";
import StarterCard from "./base/StarterCard";

import { projects } from "../actions";

class Dashboard extends Component {
  
  componentDidMount() {
    console.log('test');
    this.props.fetchProjects();
    console.log(this.props.projects);
  }

  render() {
    return (
      <div>
        <Menu projects={this.props.projects}/>
        <StarterCard header="Dashboard">
          Something to do.
        </StarterCard>        
      </div>
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
    fetchProjects: () => {
      dispatch(projects.fetchProjects());
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Dashboard);
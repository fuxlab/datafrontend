import React, { Component } from 'react';
import {connect} from 'react-redux';

import { IconNames } from "@blueprintjs/icons";

import Layout from "./base/Layout";
import StarterCard from "./base/StarterCard";

import { projects } from "../actions";

class Dashboard extends Component {
  render() {
    return (
      <Layout>
        <StarterCard header="Dashboard">
          Something to do.
        </StarterCard>        
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
    fetchProjects: () => {
      dispatch(projects.fetchProjects());
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Dashboard);
import React, { Component } from 'react';
import {connect} from 'react-redux';

import Menu from "./Menu";

import { projects } from "./../../actions";

class Layout extends Component {
  componentDidMount() {
    this.props.fetchProjects();
  }

  render() {
    return (
      <div className={this.props.className}>
        <Menu projects={this.props.projects}/>
        {this.props.children}
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

export default connect(mapStateToProps, mapDispatchToProps)(Layout);
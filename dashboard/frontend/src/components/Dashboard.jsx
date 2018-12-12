import React, { Component } from 'react';
import {connect} from 'react-redux';

import {
    Icon,
    Button,
    InputGroup,
} from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

import Menu from "./Menu";

class Note extends Component {

  render() {
    return (
      <div>
        <Menu />

        <h2><Icon icon="home" /> Home</h2>
        <hr />
      </div>
    )
  }
}

export default connect()(Note);
import React, { Component } from 'react';

import {
    Alignment,
    AnchorButton,
    Classes,
    Navbar,
    NavbarDivider,
    NavbarGroup,
    NavbarHeading,

} from "@blueprintjs/core";

import ProjectSelector from "./ProjectSelector";

class Menu extends Component {
  render() {
    return (
      <Navbar className={Classes.DARK}>
        <NavbarGroup align={Alignment.LEFT}>
          <NavbarHeading>datafrontend</NavbarHeading>
          <NavbarDivider />
          <AnchorButton href="/" className="bp3-minimal" icon="home" text="Home" minimal />
          <ProjectSelector projects={this.props.projects}></ProjectSelector>
          <AnchorButton href="/notes/" className="bp3-minimal" icon="document" text="Notes" to="/notes" minimal />
        </NavbarGroup>
      </Navbar>
    )
  }
}

export default Menu;
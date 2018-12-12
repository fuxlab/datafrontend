import React, { Component } from 'react';

import {
    Alignment,
    Button,
    Classes,
    H5,
    Navbar,
    NavbarDivider,
    NavbarGroup,
    NavbarHeading,
    Switch,
} from "@blueprintjs/core";

class Menu extends React.Component {
  render() {
    return (
      <Navbar>
        <Navbar.Group align={Alignment.LEFT}>
          <Navbar.Heading>datafrontend</Navbar.Heading>
          <Navbar.Divider />
          <Button className="bp3-minimal" icon="home" text="Home" href="/" />
          <Button className="bp3-minimal" icon="document" text="Notes" href="/notes" />
          <Button className="bp3-minimal" icon="box" text="Projects" />
        </Navbar.Group>
      </Navbar>
    )
  }
}

export default Menu;
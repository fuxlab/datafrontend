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
    Dialog,
    Icon,
} from "@blueprintjs/core";

class EditWindow extends Component {

  state = {
    isOpen: false
  }

  toggle(){
    this.setState({isOpen: !this.state.isOpen});
  }

  submit(e){
    if(this.props.submitMethod){
      this.props.submitMethod();
      this.setState({isOpen: false});
    }
  }

  render() {
    return (
      <Dialog ref="EditWindow" icon={this.props.icon} title={this.props.title} isOpen={this.state.isOpen} onClose={() => this.setState({isOpen: false})}>
        <div className="bp3-dialog-body">
          {this.props.children}
        </div>
        <div className="bp3-dialog-footer">
          <Button type="submit" onClick={() => this.submit()} intent="success" icon="floppy-disk" text="Save" />
        </div>
      </Dialog>
    )
  }
}

export default EditWindow;
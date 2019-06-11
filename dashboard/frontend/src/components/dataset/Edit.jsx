import React, { Component } from 'react';

import { connect } from 'react-redux';
import { datasets } from "../../actions";

import {
    Icon,
    Button,
    InputGroup,
    Dialog
} from "@blueprintjs/core";

class DatasetEdit extends Component {

  submit(){
    this.props.submitMethod();
  }

  close(){
    this.props.closeMethod();
  }

  change(id){
    this.props.changeMethod(id);
  }

  render() {
    return(
      <Dialog ref="DatasetEditWindow" icon="" title={this.props.title} isOpen={this.props.isOpen} onClose={() => this.close() }>
        <div className="bp3-dialog-body">
        <form ref="form" onSubmit={() => this.submit()}>
          <InputGroup
            name="project_id"
            large="true"
            value={this.props.dataset.project_id}
            onChange={(e) => this.change(e) }
            placeholder="project_id"
            required
          />
          <InputGroup
            name="identifier"
            large="true"
            value={this.props.dataset.identifier}
            placeholder="Enter identifier here..."
            onChange={(e) => this.change(e) }
            required
          />
          <InputGroup
            name="name"
            large="true"
            value={this.props.dataset.name}
            placeholder="Enter name here..."
            onChange={(e) => this.change(e) }
            required
          />
        </form>
        </div>
        <div className="bp3-dialog-footer">
          <Button type="submit" onClick={() => this.submit()} intent="success" icon="floppy-disk" text="Save" />
        </div>
      </Dialog>
    );
  }
}

export default (DatasetEdit);

import React, { Component } from 'react';

import { Button, ButtonGroup, HTMLTable } from "@blueprintjs/core";

class OverviewTable extends Component {

  rowActions(index){
    if(!this.props.actions || this.props.actions.length === 0) {
      return;
    }

    var actions = [];
    for (var i = 0; i < this.props.actions.length; i++) {
      var action_icon = this.props.actions[i]['icon'];
      var action_text = this.props.actions[i]['text'];

      actions.push(
        <Button icon={action_icon} key={ 'button_' + index + '_' + i } onClick={ this.props.actions[i]['action'].bind(this, index) }>
          { action_text }
        </Button>
      );
    }

    return (
      <td key={'cell_' + index}>
        <ButtonGroup>
        {actions}
        </ButtonGroup>
      </td>
    );
  }

  tableHeader(){
    var columns = [];
    if(!this.props.columns || this.props.columns.length === 0) {
      return;
    }
    for (var i = 0; i < this.props.columns.length; i++) {
      var column_name = this.props.columns[i];
      columns.push(
        <th key={'column_' + i}>{column_name}</th>
      );
    }

    return(
      <thead>
        <tr>
          {columns}
          <th width="20%">Actions</th>
        </tr>
      </thead>
    );
  }

  tableBody(){
    var rows = []
    if(!this.props.data || this.props.data.length === 0) {
      return;
    }

    for (var i = 0; i < this.props.data.length; i++) {
      var row_id = this.props.data[i]['id'];
      var columns = [];
      for (var j = 0; j < this.props.columns.length; j++) {
        columns.push(
          <td key={ 'td_' + i + '_' + j }>{this.props.data[i][this.props.columns[j]]}</td>
        );
      }
      
      columns.push(this.rowActions(i));

      rows.push(
        <tr key={ 'tr_' + i }>{columns}</tr>
      );
    }
    return(
      <tbody>{rows}</tbody>
    );
  }

  render() {
    return (
      <div>
        <HTMLTable interactive={true} width="100%">
          {this.tableHeader()}
          {this.tableBody()}
        </HTMLTable>
      </div>
    )
  }
}

export default OverviewTable;
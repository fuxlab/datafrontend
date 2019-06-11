import React, { Component } from 'react';

import { Menu, MenuItem } from "@blueprintjs/core";
import { Cell, Column, Table, Utils, SelectionModes, IMenuContext, CopyCellsMenuItem } from "@blueprintjs/table";

class DataTable extends React.Component {

  renderBodyContextMenu(context: IMenuContext){
    return (
      <Menu>
          <CopyCellsMenuItem context={context} text="Copy" />
          <MenuItem context={context} onClick={false} text="Edit" />
      </Menu>
    );
  };

  getColumns(){
    var columns = [];
    const cellRenderer = (rowIndex: number, columnIndex: number) => {
      var key = rowIndex + "_" + columnIndex;
      return (<Cell key={'cell_'+key}>{this.getCellData(rowIndex, columnIndex)}</Cell>);
    }

    for (var i = 0; i < this.props.columns.length; i++) {
      var column_name = this.props.columns[i];
      columns.push(
        <Column key={'column_'+i} name={column_name} cellRenderer={cellRenderer}></Column>
      );
    }

    columns.push(this.actionColumn());
    return columns;
  }

  getId(rowIndex: number) {
    return this.props.data[rowIndex]['id'];
  }

  getCellData(rowIndex: number, columnIndex: number){
    return this.props.data[rowIndex][this.props.columns[columnIndex]];
  }

  render() {
    const numRows = this.props.data.length;
    return (
      <div>
        <Table
          numRows={numRows}
          bodyContextMenuRenderer={this.renderBodyContextMenu}
          selectionModes={SelectionModes.ROWS_ONLY}
          allowMultipleSelection={false}
        >
          {this.getColumns()}
        </Table>
      </div>
    )
  }
}

export default DataTable;
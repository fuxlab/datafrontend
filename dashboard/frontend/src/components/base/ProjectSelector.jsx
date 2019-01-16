import { connect } from 'react-redux';
import React, { Component } from 'react';

import { Button, H5, Menu, MenuItem, Switch } from "@blueprintjs/core";
import { Select } from "@blueprintjs/select";

class ProjectSelector extends Component {
  
  state = {
    selectedProjectId: null,
    selectedProjectName: 'Projects',
  }

  handleClick(id){
    // TODO: replace this (and all document.locations) when changing routing
    document.location = '/datasets/'+id;
  }

  handleAllClick(){
    // TODO: replace this (and all document.locations) when changing routing
    document.location = '/projects/';
  }

  items(){
    const all = {
      id: '',
      name: 'All',
    }
    return(
      this.props.projects
    );
  }

  render() {
    const filter: ItemPredicate = (query, project) => {
      return `${project.id}. ${project.name.toLowerCase()}`.indexOf(query.toLowerCase()) >= 0;
    };

    const renderMenu: ItemListRenderer<Film> = ({ items, itemsParentRef, query, renderItem }) => {
        const renderedItems = items.map(renderItem).filter(item => item != null);
        return (
          <Menu ulRef={itemsParentRef}>
            {renderedItems}
            <MenuItem
              disabled={true}
              text={`Found ${renderedItems.length} items matching "${query}"`}
            />
            <MenuItem
              disabled={false}
              text='All Projects'
              onClick={ this.handleAllClick }
            />
          </Menu>
        );
    };

    const render: ItemRenderer = (project, { handleClick, modifiers, query }) => {
      if (!modifiers.matchesPredicate) {
        return null;
      }
      return (
        <MenuItem
          active={ modifiers.active }
          disabled={ modifiers.disabled }
          label={ project.id }
          key={ project.id }
          onClick={ (e) => this.handleClick(project.id) }
          text={ project.name }
        />
      );
    };

    return(
      <Select
        items={ this.items() }
        itemPredicate={ filter }
        itemRenderer={ render }
        itemListRenderer={renderMenu}
        noResults={ <MenuItem disabled={true} text="No results." /> }
      >
        <Button text={this.state.selectedProjectName} icon="box" rightIcon="double-caret-vertical" />
      </Select>
    );
  }
}

export default connect()(ProjectSelector);
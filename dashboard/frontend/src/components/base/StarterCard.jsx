import React, { Component } from 'react';
import {connect} from 'react-redux';

import { Button, ButtonGroup, Card } from "@blueprintjs/core";

export class StartCard extends Component {
  
  actions(){
    if(!this.props.actions || this.props.actions.length === 0) {
      return;
    }

    var actions = [];
    
    for (var i = 0; i < this.props.actions.length; i++) {
      var action_icon = this.props.actions[i]['icon'];
      var action_text = this.props.actions[i]['text'];

      actions.push(
        <Button icon={ action_icon } key={ 'starter_button_' + i + '_' + i } onClick={ this.props.actions[i]['action'].bind(this) }>
          { action_text }
        </Button>
      );
    }

    return (
      <ButtonGroup>
        {actions}
      </ButtonGroup>
    );
  }

  render() {
    return (
      <Card className="starter-card">
        <div className="starter-header">
          {this.props.header}
          <ButtonGroup className="pt-align-right">
            {this.actions()}
          </ButtonGroup>
        </div>
        {this.props.children}
      </Card>
    );
  }
}

export default connect()(StartCard);
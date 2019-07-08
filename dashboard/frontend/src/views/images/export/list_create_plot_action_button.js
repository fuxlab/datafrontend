import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, crudUpdateMany, startUndoable } from 'react-admin';
import { stringify } from 'query-string';

class CreatePlotButton extends Component {
    render() {
        const {  basePath, resource, selectedIds, startUndoable, filterValues } = this.props;
        const params = {
            type: filterValues.type,
            ids: [selectedIds]
        }
        const plot_link = '/api/image/plot.png?' + stringify(params)
        return (
            <Button
                label="Create Image-Plot"
                href={plot_link}
                target='_blank'
            />
        );
    }
}

export default connect(undefined, { startUndoable })(CreatePlotButton);
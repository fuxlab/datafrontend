import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, crudUpdateMany, startUndoable } from 'react-admin';
import { stringify } from 'query-string';

class CreatePlotButton extends Component {
    render() {
        const {  basePath, resource, selectedIds, startUndoable, filterValues } = this.props;
        
        const plot_link_original = '/api/image/plot.png?' + stringify({
            type: 'annotation',
            ids: [selectedIds]
        })
        const plot_link_type = '/api/image/plot.png?' + stringify({
            type: filterValues.type,
            ids: [selectedIds]
        })

        return (
            <div>
                <Button
                    label="Original Image-Plot"
                    href={plot_link_original}
                    target='_blank'
                />
                <Button
                    label="Create Image-Plot for Type"
                    href={plot_link_type}
                    target='_blank'
                />
            </div>
        );
    }
}

export default connect(undefined, { startUndoable })(CreatePlotButton);
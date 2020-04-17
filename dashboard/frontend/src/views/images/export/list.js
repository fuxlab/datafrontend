import React from 'react';
import { List, Datagrid, TextField } from 'react-admin';
import { withStyles } from '@material-ui/core/styles';

import ImagesExportListFilter from './list_filter';
import ImagesExportListAside from './list_aside';
import CreatePlotActionButton from './list_create_plot_action_button';
import ImagesExportListPreview from './list_preview'

const ExportListStyles = {
    list: {

    },
    grid: {
        padding: '2em 0',
    },
};

export const ExportList = withStyles(ExportListStyles)(({ classes, ...props }) => {
    return(
        <List
            basePath="images/export"
            resource="images/export"
            title="Export"
            className={classes.list}
            filters={<ImagesExportListFilter />}
            exporter={false}
            aside={<ImagesExportListAside />}
            bulkActionButtons={<CreatePlotActionButton />}
            {...props}
        >
            <Datagrid
                className={classes.grid}
                expand={<ImagesExportListPreview />}
            >
                <TextField
                    source="id"
                    label="UID"
                    sortable={false}
                />
                <TextField
                    source="type"
                    label="Type"
                    sortable={false}
                />
                <TextField
                    source="source"
                    label="Source"
                    sortable={false}
                />
            </Datagrid>
        </List>
    );
});
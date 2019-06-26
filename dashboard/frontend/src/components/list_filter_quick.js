import React from 'react';
import Chip from '@material-ui/core/Chip';
import { withStyles } from '@material-ui/core/styles';

const listFilterQuickStyles = {
    root: {
        marginBottom: '0.7em',
    },
};

const ListFilterQuick = withStyles(listFilterQuickStyles)(({ classes, label }) => (
        <Chip className={classes.root} label={label} />
    )
);

export default ListFilterQuick;
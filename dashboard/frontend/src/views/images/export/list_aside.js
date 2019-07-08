import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';

const ImagesExportListAsideStyles = {
    aside: {
        width: '30%',
        margin: '1em',
    },
    body: {
        marginTop: '2em',
    },
    splits: {
        margin: '0 1em 1em 1em',
        padding: 0,
    }
};

const ImagesExportListAside = withStyles(ImagesExportListAsideStyles)(({ classes, total, ...props }) => {
    var splits = [];
    if(props.filterValues['split']) {
        var items = props.filterValues['split'].split('_');
        for (const [index, item] of items.entries()) {
            var data_size = Math.floor((total / 100) * item);
            splits.push(data_size + '(' + item + '%)');
        }
    }

    return(
    <div className={classes.aside}>
        <Typography variant="title">Export Details</Typography>
        <Typography variant="body1" className={classes.body}>
            <strong>Records: {total}</strong><br/><br/>
            <strong>Splits</strong><br/>
            <ol type="A" className={classes.splits}>
                {splits.map(split => {
                    return <li>{split}</li> 
                })}
            </ol>
        </Typography>
    </div>
    );
});

export default ImagesExportListAside;
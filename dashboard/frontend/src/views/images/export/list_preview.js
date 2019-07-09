import React from 'react';
import { withStyles } from '@material-ui/core/styles';

const ImagesExportListPreviewStyles = {
    table: {
        backgroundColor: '#000',
        border: '0px solid #000',
        width: '100%',
    },
    tableColumn: {
        width: '50%',
    },
    tableRow: {
        width: '50%',
        verticalAlign: 'middle',
        textAlign: 'center',
        padding: 10,
    },
    image: {
        maxHeight: 200,
    },
    txt: {
        fontSize: 12,
        color: '#FFF',
        padding: 10,
        textTransform: 'uppercase',
    }
};

const ImagesExportListPreview = withStyles(ImagesExportListPreviewStyles)(({ classes, ...props }) => {
    var image_type = props.record.type;
    var image_url = props.record.url;
    var image_image = props.record.image;
    return(
        <table className={classes.table}>
            <tr className={classes.tableColumn}>
                <td className={classes.tableRow}>
                    <img className={classes.image} src={image_url} /><br/>
                    <span className={classes.txt}>{image_type}-Image</span>
                </td>
                <td className={classes.tableRow}>
                    <img className={classes.image} src={image_image} /><br/>
                    <span className={classes.txt}>Original-Image</span>
                </td>
            </tr>
        </table>
    );
});

export default ImagesExportListPreview;
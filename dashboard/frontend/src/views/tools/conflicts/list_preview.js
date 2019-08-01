import React from 'react';
import { withStyles } from '@material-ui/core/styles';

const ConflictsListPreviewStyles = {
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

const ConflictsListPreview = withStyles(ConflictsListPreviewStyles)(({ classes, ...props }) => {
    var message = 'not defined';
    var items = [];
    // preview for duplicate boundingboxes
    if(props.record.reason = 'annotation_boundingbox_duplicate') {
        message = props.record.message; 
        var index = 0;
        for(const bb_id of props.record.affected_ids) {
            var image_url = `/api/image/boundingbox_crop/${bb_id}.png`;
            var choice = String.fromCharCode(65 + index);
            items.push(
                <td className={classes.tableRow}>
                    <img className={classes.image} src={image_url} /><br/>
                    <span className={classes.txt}>{choice}</span>
                </td>
            );
            index = index + 1;
        }
    }

    var image_type = props.record.type;
    var image_url = props.record.url;
    var image_image = props.record.image;
    return(
        <div>
        <p><b>{props.record.reason}</b>: <i>{message}</i></p>
        <table className={classes.table}>
            <tr className={classes.tableColumn}>
                {items}
            </tr>
        </table>
        </div>
    );
});

export default ConflictsListPreview;
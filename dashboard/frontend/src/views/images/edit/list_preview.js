import React from 'react';
import { withStyles } from '@material-ui/core/styles';

const ImagesEditListPreviewStyles = {
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

const ImagesEditListPreview = withStyles(ImagesEditListPreviewStyles)(({ classes, ...props }) => {
    var type = 'Annotation';
    var image_url = '/api/image/original/'+props.record.id+'.png';
    
    if(props.type == 'segmentation'){
        type = 'Segmentation';
        image_url = '/api/image/segmentation_crop/'+props.record.id+'.png';
    } else if (props.type == 'boundingbox'){
        type = 'Boundingbox';
        image_url = '/api/image/boundingbox_crop/'+props.record.id+'.png';
    }
    
    return(
        <table className={classes.table}>
            <tr className={classes.tableColumn}>
                <td className={classes.tableRow}>
                    <img className={classes.image} src={image_url} /><br/>
                    <span className={classes.txt}>{type}-Image</span>
                </td>
            </tr>
        </table>
    );
});

export default ImagesEditListPreview;
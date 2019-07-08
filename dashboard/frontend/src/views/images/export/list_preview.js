import React from 'react';
import { withStyles } from '@material-ui/core/styles';

const ImagesExportListPreviewStyles = {

};

const ImagesExportListPreview = withStyles(ImagesExportListPreviewStyles)(({ ...props }) => {
    var image_url = props.record.url;
    return(
        <div>
            <img src={image_url} />
        </div>
    );
});

export default ImagesExportListPreview;
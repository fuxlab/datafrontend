import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';

import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import RestoreIcon from '@material-ui/icons/Restore';
import CropFreeIcon from '@material-ui/icons/CropFree';
import LayersIcon from '@material-ui/icons/Layers';

import { withStyles } from '@material-ui/core/styles';
import { SvgLoader, SvgProxy } from 'react-svgmt';


const styles = {
    card: {
        marginTop: 0,
        marginBottom: 0,
        boxShadow: 'none',
        border: '1px solid #000',
    },
    media: {
        height: 'auto',
        backgroundSize: 'auto',
        backgroundColor: '#000',
        padding: 0,
        margin: 0,
        textAlign: 'center'
    },
    media_object: {
        margin: 0,
        padding: 0
    },
};


class ImagesEditDetail extends Component {

    state = {
        error: false,
        segmentation_status: 'visable',
        boundingbox_status: 'visable',
    };

    toggleBoundingbox = () => {
        //console.log(this.svg_image);
        if(this.state.boundingbox_status == 'visable'){
            this.setState({ boundingbox_status: 'hidden' });
        } else {
            this.setState({ boundingbox_status: 'visable' });
        }
    };

    toggleSegmentation = () => {
        //console.log(this.svg_image);
        if(this.state.segmentation_status == 'visable'){
            this.setState({ segmentation_status: 'hidden' });
        } else {
            this.setState({ segmentation_status: 'visable' });
        }
    };

    svgClickSegmentation = (element) => {
        console.log(element.target.id);
    };

    render() {
        const record = this.props.record;
        const classes = styles;
        const { boundingbox_status, segmentation_status } = this.state;
        const imageUrl = record.preview;
        const overlayUrl = '/api/image/preview/' + record.id + '.svg';

        return(
            <Card style={classes.card}>
                <CardMedia image={imageUrl} style={classes.media}>
                    <SvgLoader path={overlayUrl} ref={elem => this.svg_image = elem}>
                        <SvgProxy selector=".segmentation_layer" onClick={this.svgClickSegmentation} visibility={segmentation_status} />
                    </SvgLoader>
                </CardMedia>
                <CardActions style={{ justifyContent: 'flex-end' }}>
                    <Button onClick={this.toggleBoundingbox}>
                        <CropFreeIcon style={{ paddingRight: '0.5em' }} />
                        BoundingBoxes
                    </Button>
                    <Button onClick={this.toggleSegmentation}>
                        <LayersIcon style={{ paddingRight: '0.5em' }} />
                        Segmentations
                    </Button>
                </CardActions>
            </Card>
        );
    }
}

const mapStateToProps = state => ({
});

const mapDispatchToProps = {
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(
    ImagesEditDetail
));
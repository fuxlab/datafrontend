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

const styles = {
    card: {
        marginTop: '1em',
        marginBottom: '1em',
        boxShadow: 'none',
        border: '1px solid #000',
    },
    media: {
        height: '18em',
        backgroundSize: 'contain',
        backgroundColor: '#000',
        padding: '1em',
    },
};


class ImageDetail extends Component {

    state = {
        error: false,
        imageSize: 'original'
    };

    displayOriginal = () => {
        this.setState({ imageSize: 'original' });
    };

    displayBoundingbox = () => {
        this.setState({ imageSize: 'boundingbox' });
    };

    displaySegmentation = () => {
        this.setState({ imageSize: 'segmentation' });
    };

    render() {
        const { classes, record } = this.props;
        const { imageSize } = this.state;
              
        return(
            <Card className={classes.card}>
                <CardMedia image={record.image + '?type=' + imageSize} className={classes.media} />
                <CardActions style={{ justifyContent: 'flex-end' }}>
                    <Button onClick={this.displayOriginal}>
                        <RestoreIcon style={{ paddingRight: '0.5em' }} />
                        Original
                    </Button>
                    <Button onClick={this.displayBoundingbox}>
                        <CropFreeIcon style={{ paddingRight: '0.5em' }} />
                        BoundingBoxes
                    </Button>
                    <Button onClick={this.displaySegmentation}>
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
    ImageDetail
));
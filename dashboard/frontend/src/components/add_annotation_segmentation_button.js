import React from 'react';
import { Link } from 'react-router-dom';
import CompareIcon from '@material-ui/icons/Compare';
import { withStyles } from '@material-ui/core/styles';
import { Button } from 'react-admin';

const styles = {
  button: {
    marginTop: '1em'
  }
};

const AddAnnotationSegmentationButton = ({ classes, record }) => (
  <Button
    className={classes.button}
    variant="raised"
    component={Link}
    to={`/annotation-segmentations/create?annotation=${record.id}`}
    label="Add Segmentation"
    title="Add Segmentation"
  >
    <CompareIcon />
  </Button>
);

export default withStyles(styles)(AddAnnotationSegmentationButton);

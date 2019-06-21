import React from 'react';
import { Link } from 'react-router-dom';
import CropFreeIcon from '@material-ui/icons/CropFree';
import { withStyles } from '@material-ui/core/styles';
import { Button } from 'react-admin';

const styles = {
  button: {
    marginTop: '1em'
  }
};

const AddAnnotationBoundingboxButton = ({ classes, record }) => (
  <Button
    className={classes.button}
    variant="raised"
    component={Link}
    to={`/annotation-boundingboxes/create?annotation=${record.id}`}
    label="Add BoundingBox"
    title="Add BoundingBox"
  >
    <CropFreeIcon />
  </Button>
);

export default withStyles(styles)(AddAnnotationBoundingboxButton);

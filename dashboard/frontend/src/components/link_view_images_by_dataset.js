import React from 'react';
import { Link } from 'react-router-dom';
import PhotoLibraryIcon from '@material-ui/icons/PhotoLibrary';
import { withStyles } from '@material-ui/core/styles';
import { Button } from 'react-admin';
import { stringify } from 'query-string';

const styles = {
  link: {
    
  }
};

const LinkViewImagesByDataset = ({ classes, record }) => {
  return (
    <Button
      className={classes.link}
      size="small"
      color="primary"
      component={Link}
      to={{
          pathname: '/images',
          search: stringify({
              page: 1,
              perPage: 25,
              sort: 'id',
              order: 'DESC',
              filter: JSON.stringify({ dataset: record.id }),
          }),
      }}
      label=""
      title="View Images in Dataset"
    >
      <PhotoLibraryIcon />
    </Button>
  );
};

export default withStyles(styles)(LinkViewImagesByDataset);

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

const LinkViewImagesByCategoryType = withStyles(styles)(({ classes, record, ...props }) => {
  var cat_type = 'annotation';
  if(props.type != undefined){
    cat_type =  props.type;
  }
  
  var params = {};
  params[cat_type] = record.id;
  var title = "view " + cat_type + " images by category";
  
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
              filter: JSON.stringify(params),
          }),
      }}
      label=""
      title={title}
    >
      <PhotoLibraryIcon />
    </Button>
  );
});

//export default withStyles(styles)(LinkViewImagesByCategoryType);
export default LinkViewImagesByCategoryType;
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

const LinkButton = withStyles(styles)(({ classes, record, ...props }) => {
  
    var title = 'Link'
    if(props.title != undefined){
        title =  props.title;
    }

    var path = '/undefined_path/'
    if(props.path != undefined){
        path = props.path;
        path = path.replace('{id}', record.id);
    }

    var query_string = ''
    if(props.query_string != undefined){
        query_string = props.query_string;
        for (var key in record) {
            if(record[key] != ""){
                query_string = query_string.replace('{record.'+key+'}', record[key]);
            }
        }
    }
    //var query_string = 'dataset='+record.dataset+'&file_name='+record.file_name

    var handleClick = function(){
        fetch(path, {
            method: 'post',
            headers: new Headers({
                'Content-Type': 'application/x-www-form-urlencoded', // <-- Specifying the Content-Type
            }),
            body: query_string
        }).then(function(data){
            console.log(data);
            alert('submitted');
        })
    }

    return (
        <Button
            className={classes.link}
            size="small"
            color="primary"
            onClick={handleClick}
            label={title}
            title={title}
        >
        </Button>
    );
});

export default LinkButton;
import React from 'react';
import { TextField, DateField, Avatar, EditButton, ReferenceField } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';

const styles = {
  card: {
    width: 300,
    minHeight: 300,
    margin: '0.5em',
    display: 'inline-block',
    verticalAlign: 'top',
  },
  cardUrl: {
    color: '#ccc',
    fontSize: '0.8em',
    overflow: 'hidden',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    display: 'block',
  },
  mediaWrapper: {
    backgroundColor: '#000',
    padding: '0.5em',
  },
  media: {
    width: 'auto',
    marginLeft: 'auto',
    marginRight: 'auto',
    minHeight: 150,
    maxHeight: 300,
  }
};

const ImageGrid = ({ ids, data, basePath }) => (
    <div style={{ margin: '1em' }}>
      {ids.map(id =>
         <Card key={id} style={styles.card}>
            <div style={styles.mediaWrapper}>
              <CardMedia style={styles.media}
                component="img"
                alt={data[id].name}
                title={data[id].name}
                image={data[id].url}
                basePath={basePath}
                record={data[id]}
              />
            </div>
            <CardContent>
              <Typography gutterBottom variant="headline" component="h2">
                {data[id].name}
              </Typography>
              <Typography component="p">
                <a href={data[id].url} style={styles.cardUrl} target="_blank">
                  {data[id].url}
                </a>
              </Typography>
            </CardContent>
            <CardActions style={{ textAlign: 'right' }}>
              <EditButton basePath={basePath} record={data[id]} label="Edit" />
            </CardActions>
          </Card>
      )}
    </div>
);

ImageGrid.defaultProps = {
    data: {},
    ids: [],
};

export default ImageGrid;
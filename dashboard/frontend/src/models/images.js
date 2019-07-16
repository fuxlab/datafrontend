import React from 'react';
import { Filter, ReferenceInput, SelectInput } from 'react-admin';
import { List, TextInput, TextField, UrlField, EditButton } from 'react-admin';
import { Create } from 'react-admin';
import ImageGrid from './../components/image_grid';


const annotationNameRenderer = choice => `${choice.name} (${choice.annotations_count})`;
const boundingboxNameRenderer = choice => `${choice.name} (${choice.boundingboxes_count})`;
const segmentationNameRenderer = choice => `${choice.name} (${choice.segmentations_count})`;

const ImageFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
        <ReferenceInput label="Dataset" source="dataset" reference="datasets" allowEmpty perPage={1000}>
            <SelectInput optionText="name" />
        </ReferenceInput>
        <ReferenceInput
            label="Annotation"
            source="annotation"
            reference="categories"
            sort={{ field: 'name', order: 'ASC' }}
            filter={{ annotation_exists: true }}
            allowEmpty perPage={1000}>
            <SelectInput optionText={annotationNameRenderer} />
        </ReferenceInput>
        <ReferenceInput
            label="Boundingbox"
            source="boundingbox"
            reference="categories"
            filter={{ boundingbox_exists: true }}
            sort={{ field: 'name', order: 'ASC' }}
            allowEmpty perPage={1000}>
            <SelectInput optionText={boundingboxNameRenderer} />
        </ReferenceInput>
        <ReferenceInput
            label="Segmentation"
            source="segmentation"
            reference="categories"
            filter={{ segmentation_exists: true }}
            sort={{ field: 'name', order: 'ASC' }}
            allowEmpty perPage={1000}>
            <SelectInput optionText={segmentationNameRenderer} />
        </ReferenceInput>
    </Filter>
);


import Button from '@material-ui/core/Button';
import { CardActions, CreateButton } from 'react-admin';
import { Link } from 'react-router-dom';
import CloudDownloadIcon from '@material-ui/icons/CloudDownload';

const ImagesListActions = ({
    basePath,
    currentSort,
    displayedFilters,
    exporter,
    filters,
    filterValues,
    onUnselectItems,
    resource,
    selectedIds,
    showFilter,
    total
}) => (
    <CardActions>
        {filters && React.cloneElement(filters, {
            resource,
            showFilter,
            displayedFilters,
            filterValues,
            context: 'button',
        }) }
        <CreateButton basePath={basePath} />
        {/* Add your custom actions */}
        <Button
            color="primary"
            component={Link}
            to={{
              pathname: '/images/export'
            }}
            label="Export"
            title="Export Images"
        >
            <CloudDownloadIcon />
        </Button>
    </CardActions>
);


export const ImageList = props => (
    <List
        filters={<ImageFilter />}
        actions={<ImagesListActions />}
        exporter={false}
        {...props}
    >
        <ImageGrid />
    </List>
);

export const ImageCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput source="dataset" reference="datasets">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
            <TextInput source="url" />
        </SimpleForm>
    </Create>
);
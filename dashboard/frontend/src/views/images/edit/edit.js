import React from 'react';
import { 
    ReferenceInput, SelectInput, Datagrid, Edit, SimpleForm, TabbedForm,
    FormTab, ReferenceManyField, TextInput, TextField, DisabledInput, EditButton
} from 'react-admin';
import { withStyles } from '@material-ui/core/styles';

import ImagesEditDetail from './detail';
import ImagesEditListPreview from './list_preview'

const ImagesEditStyles = {
    annotationList: {
        width: '100%'
    },
    annotationBoundingboxList: {
        width: '100%'
    },
    annotationSegmentationList: {
        width: '100%'
    },
    grid: {
        padding: '2em 0',
    },
};

export const ImagesEdit = withStyles(ImagesEditStyles)(({ classes, ...props }) => {
    return(
        <Edit {...props}>
            <TabbedForm>
                <FormTab label="summary">
                    <ImagesEditDetail />
                    
                    <DisabledInput source="id" />
                    <ReferenceInput
                        source="dataset"
                        reference="datasets"
                    >
                        <SelectInput optionText="name" />
                    </ReferenceInput>
                    <TextInput source="identifier" />
                    <TextInput source="name" />
                    <TextInput source="url" />
                    <TextInput source="path" />
                </FormTab>
                
                <FormTab label="annotations">
                    <ReferenceManyField
                        reference="annotations"
                        target="image"
                        addLabel={false}
                        className={classes.annotationList}
                    >
                        <Datagrid>
                            <TextField source="id" />
                            <TextField source="category_name" />
                            <EditButton />
                        </Datagrid>
                    </ReferenceManyField>
                </FormTab>
                
                <FormTab label="boundingboxes">
                    <ReferenceManyField
                        reference="annotation-boundingboxes"
                        target="image"
                        addLabel={true}
                        className={classes.annotationBoundingboxList}
                    >
                        <Datagrid
                            expand={<ImagesEditListPreview type="boundingbox" />}
                        >
                            <TextField source="id" />
                            <TextField source="category_name" />
                            <TextField source="x_min" />
                            <TextField source="x_max" />
                            <TextField source="y_min" />
                            <TextField source="y_max" />
                            <EditButton />
                        </Datagrid>
                    </ReferenceManyField>
                </FormTab>
                
                <FormTab label="segmentations">
                    <ReferenceManyField
                        reference="annotation-segmentations"
                        target="image"
                        addLabel={true}
                        className={classes.annotationSegmentationList}
                    >
                        <Datagrid
                            expand={<ImagesEditListPreview type="segmentation"/>}
                        >
                            <TextField source="id" />
                            <TextField source="category_name" />
                            <TextField source="width" />
                            <TextField source="height" />
                            <EditButton />
                        </Datagrid>
                    </ReferenceManyField>
                </FormTab>
            </TabbedForm>
        </Edit>
    );
});
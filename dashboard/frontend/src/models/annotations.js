import React from 'react';
import { Filter, ReferenceInput, SelectInput, SelectField } from 'react-admin';
import { List, Datagrid, TextField, EditButton, ReferenceManyField } from 'react-admin';
import { Edit, SimpleForm, TextInput, DisabledInput } from 'react-admin';
import { Create } from 'react-admin';
import { Pagination } from 'react-admin';

import AddAnnotationBoundingboxButton from './../components/add_annotation_boundingbox_button';
import AddAnnotationSegmentationButton from './../components/add_annotation_segmentation_button';

const AnnotationFilter = (props) => (
    <Filter {...props}>
        <ReferenceInput label="Category" source="category" reference="categories" allowEmpty>
            <SelectInput optionText="name" />
        </ReferenceInput>
        <SelectInput label="Type" source="type" optionText="type" choices={[
               { id: 'annotation', type: 'Annotation' },
               { id: 'boundingbox', type: 'BoundingBox' },
               { id: 'segmentation', type: 'Segmentation' },
            ]} />
    </Filter>
);

export const AnnotationList = props => (
    <List filters={<AnnotationFilter />} {...props}>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="image_name" />
            <TextField source="types" />
            <EditButton />
        </Datagrid>
    </List>
);

export const AnnotationEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput source="image_id" reference="images">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput source="category" reference="categories">
                <SelectInput optionText="name" />
            </ReferenceInput>

            <ReferenceManyField pagination={<Pagination />} reference="annotation-boundingboxes" target="annotation" addLabel={true}>
                <Datagrid>
                    <TextField source="id" />
                    <TextField source="category_name" />
                    <EditButton />
                </Datagrid>
            </ReferenceManyField>
            <AddAnnotationBoundingboxButton />

        
            <ReferenceManyField pagination={<Pagination />} reference="annotation-segmentations" target="annotation" addLabel={true}>
                <Datagrid>
                    <TextField source="id" />
                    <TextField source="category_name" />
                    <EditButton />
                </Datagrid>
            </ReferenceManyField>
            <AddAnnotationSegmentationButton />

        </SimpleForm>
    </Edit>
);

export const AnnotationCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput source="image" reference="images">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <ReferenceInput source="category" reference="categories">
                <SelectInput optionText="name" />
            </ReferenceInput>
        </SimpleForm>
    </Create>
);
import React from 'react';
import { Filter, ReferenceInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, UrlField, EditButton } from 'react-admin';
import { Edit, SimpleForm, TabbedForm, FormTab, ReferenceManyField, TextInput, DisabledInput } from 'react-admin';
import { Create } from 'react-admin';
import ImageGrid from './../components/image_grid';

const ImageFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
        <ReferenceInput label="Dataset" source="dataset" reference="datasets" allowEmpty>
            <SelectInput optionText="name" />
        </ReferenceInput>
        <ReferenceInput label="Category" source="category" reference="categories" allowEmpty perPage={500}>
            <SelectInput optionText="name" />
        </ReferenceInput>
    </Filter>
);

export const ImageList = props => (
    <List filters={<ImageFilter />} {...props}>
        <ImageGrid />
    </List>
);

export const ImageEdit = props => (
    <Edit {...props}>
        <TabbedForm>
            <FormTab label="summary">
                <DisabledInput source="id" />
                <ReferenceInput source="dataset" reference="datasets">
                    <SelectInput optionText="name" />
                </ReferenceInput>
                <TextInput source="name" />
                <TextInput source="url" />
            </FormTab>
            <FormTab label="annotations">
                <ReferenceManyField filter={{ 'type' : 'annotation' }} reference="annotations" target="image" addLabel={false}>
                    <Datagrid>
                        <TextField source="id" />
                        <TextField source="category_name" />
                        <EditButton />
                    </Datagrid>
                </ReferenceManyField>
            </FormTab>
            <FormTab label="boundingboxes">
                <ReferenceManyField filter={{ 'type' : 'boundingbox' }} reference="annotations" target="image" addLabel={true}>
                    <Datagrid>
                        <TextField source="id" />
                        <TextField source="category_name" />
                        <EditButton />
                    </Datagrid>
                </ReferenceManyField>
            </FormTab>
            <FormTab label="segmentations">
                <ReferenceManyField filter={{ 'type' : 'segmentation' }} reference="annotations" target="image" addLabel={true}>
                    <Datagrid>
                        <TextField source="id" />
                        <TextField source="category_name" />
                        <EditButton />
                    </Datagrid>
                </ReferenceManyField>
            </FormTab>
        </TabbedForm>
    </Edit>
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
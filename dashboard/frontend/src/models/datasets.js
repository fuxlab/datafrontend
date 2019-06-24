import React from 'react';
import { Filter, ReferenceInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, EditButton } from 'react-admin';
import { Edit, SimpleForm, TextInput, DisabledInput, ReferenceManyField } from 'react-admin';
import { Create } from 'react-admin';

const DatasetFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
        <ReferenceInput label="Project" source="project_id" reference="projects" allowEmpty>
            <SelectInput optionText="name" />
        </ReferenceInput>
    </Filter>
);

export const DatasetList = props => (
    <List filters={<DatasetFilter />} {...props}>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="identifier" />
            <TextField source="name" />
            <TextField source="images_count" />
            <EditButton />
        </Datagrid>
    </List>
);

export const DatasetEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput source="project_id" reference="projects">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="identifier" />
            <TextInput source="name" />

            <ReferenceManyField reference="categories" target="dataset_annotation" addLabel={false}>
                <Datagrid>
                    <TextField source="id" />
                    <TextField source="name" />
                    <TextField source="annotations_count" />
                    <EditButton />
                </Datagrid>
            </ReferenceManyField>

            <ReferenceManyField reference="categories" target="dataset_boundingbox" addLabel={false}>
                <Datagrid>
                    <TextField source="id" />
                    <TextField source="name" />
                    <TextField source="boundingboxes_count" />
                    <EditButton />
                </Datagrid>
            </ReferenceManyField>

            <ReferenceManyField reference="categories" target="dataset_segmentation" addLabel={false}>
                <Datagrid>
                    <TextField source="id" />
                    <TextField source="name" />
                    <TextField source="segmentations_count" />
                    <EditButton />
                </Datagrid>
            </ReferenceManyField>

        </SimpleForm>
    </Edit>
);

export const DatasetCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput source="project_id" reference="projects">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="identifier" />
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
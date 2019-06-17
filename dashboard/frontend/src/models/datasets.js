import React from 'react';
import { Filter, ReferenceInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, EditButton } from 'react-admin';
import { Edit, SimpleForm, TextInput, DisabledInput } from 'react-admin';
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
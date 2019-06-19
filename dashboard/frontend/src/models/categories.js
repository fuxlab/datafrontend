import React from 'react';
import { Filter, ReferenceInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, EditButton } from 'react-admin';
import { Edit, SimpleForm, TextInput, DisabledInput } from 'react-admin';
import { Create } from 'react-admin';

const CategoryFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
        <ReferenceInput label="Dataset" source="dataset" reference="datasets" allowEmpty>
            <SelectInput optionText="name" />
        </ReferenceInput>
    </Filter>
);

export const CategoryList = props => (
    <List filters={<CategoryFilter />} {...props}>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="name" />
            <EditButton />
        </Datagrid>
    </List>
);

export const CategoryEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput source="dataset" reference="datasets">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Edit>
);

export const CategoryCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput source="dataset" reference="datasets">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
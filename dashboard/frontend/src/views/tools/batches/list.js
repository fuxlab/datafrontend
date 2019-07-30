import React from 'react';
import { Filter, ReferenceInput, TextInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, ShowButton, DeleteButton, DateField } from 'react-admin';

const BatchesFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
    </Filter>
);

export const BatchesList = props => (
    <List filters={<BatchesFilter />} exporter={false} {...props}>
        <Datagrid>
            <TextField source="id" />
            <TextField source="action" />
            <TextField source="status" />
            <DateField source="created_at" showTime />
            <DateField source="updated_at" showTime />
            <ShowButton />
            <DeleteButton />
        </Datagrid>
    </List>
);
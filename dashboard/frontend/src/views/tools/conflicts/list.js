import React from 'react';
import { Filter, ReferenceInput, TextInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, DeleteButton, DateField } from 'react-admin';

import ConflictsListPreview from './list_preview'

const ConflictsFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
    </Filter>
);

export const ConflictsList = props => (
    <List
        filters={<ConflictsFilter />}
        exporter={false}
        {...props}
    >
        <Datagrid
            expand={<ConflictsListPreview />}
        >
            <TextField source="id" />
            <TextField source="status" />
            <TextField source="reason" />
            <TextField source="affected_ids" />
            <DateField source="created_at" showTime />
            <DeleteButton />
        </Datagrid>
    </List>
);
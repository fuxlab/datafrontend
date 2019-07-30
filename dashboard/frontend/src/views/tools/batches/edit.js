import React from 'react';
import { Edit, SimpleForm, TextInput, DisabledInput } from 'react-admin';
import { Create } from 'react-admin';

export const BatchesEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <DisabledInput source="action" />
            <DisabledInput source="params" />
            <DisabledInput source="log" />
        </SimpleForm>
    </Edit>
);
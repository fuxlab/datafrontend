import React from 'react';
import { ReferenceInput, SelectInput } from 'react-admin';
import { TextInput } from 'react-admin';
import { Create, SimpleForm } from 'react-admin';


export const DatasetCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput source="project" reference="projects">
                <SelectInput optionText="name" />
            </ReferenceInput>

            <ReferenceInput label="Existing Folder" source="identifier" reference="folders">
                <SelectInput optionText="name" />
            </ReferenceInput>

            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
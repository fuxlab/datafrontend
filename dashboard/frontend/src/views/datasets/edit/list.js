import React from 'react';
import { Filter, ReferenceInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, EditButton } from 'react-admin';
import { Edit, TabbedForm, FormTab, TextInput, DisabledInput, ReferenceManyField } from 'react-admin';
import { Create, SimpleForm } from 'react-admin';
import LinkViewImagesByDataset from './../../../components/link_view_images_by_dataset';

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
        <Datagrid>
            <TextField source="id" />
            <TextField source="identifier" />
            <TextField source="name" />
            <TextField source="images_count" sortable={false} />
            <LinkViewImagesByDataset />
            <EditButton />
        </Datagrid>
    </List>
);



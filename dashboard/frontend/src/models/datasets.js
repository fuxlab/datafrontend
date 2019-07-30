import React from 'react';
import { Filter, ReferenceInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, EditButton } from 'react-admin';
import { Edit, TabbedForm, FormTab, TextInput, DisabledInput, ReferenceManyField } from 'react-admin';
import { Create, SimpleForm } from 'react-admin';
import LinkViewImagesByDataset from './../components/link_view_images_by_dataset';

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

export const DatasetEdit = props => (
    <Edit {...props}>
        <TabbedForm>
            <FormTab label="Information">
                <DisabledInput source="id" />
                <ReferenceInput source="project_id" reference="projects">
                    <SelectInput optionText="name" />
                </ReferenceInput>
                <TextInput source="identifier" />
                <TextInput source="name" />
            </FormTab>

            <FormTab label="Content">
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
            </FormTab>
        </TabbedForm>
    </Edit>
);

export const DatasetCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput source="project" reference="projects">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="identifier" />
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);
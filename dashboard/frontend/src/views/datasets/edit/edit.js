import React from 'react';
import { ReferenceInput, SelectInput } from 'react-admin';
import { Datagrid, TextField, EditButton, Button } from 'react-admin';
import { Edit, TabbedForm, FormTab, TextInput, DisabledInput, ReferenceManyField } from 'react-admin';

import LinkButton from './../../../components/link_button';

const PriceField = props => {
    return <TextField {...props} />;
};

export const DatasetEdit = props => (
    <Edit {...props}>
        <TabbedForm>
            <FormTab label="Information">
                <DisabledInput source="id" fullWidth />
                <ReferenceInput source="project" reference="projects" fullWidth>
                    <SelectInput optionText="name" />
                </ReferenceInput>
                <TextInput source="identifier" fullWidth />
                <TextInput source="name" fullWidth />
                <TextInput source="version" fullWidth />
                <TextInput source="description" fullWidth multiline />
                <TextInput source="contributor" fullWidth />
                <TextInput source="url" fullWidth />
                <TextInput source="release_date" fullWidth />
            </FormTab>

            <FormTab label="Content">
                <ReferenceManyField reference="categories" target="dataset_annotation" addLabel={false} fullWidth>
                    <Datagrid>
                        <TextField source="id" />
                        <TextField source="name" />
                        <TextField source="annotations_count" />
                        <EditButton />
                    </Datagrid>
                </ReferenceManyField>

                <ReferenceManyField reference="categories" target="dataset_boundingbox" addLabel={false} fullWidth>
                    <Datagrid>
                        <TextField source="id" />
                        <TextField source="name" />
                        <TextField source="boundingboxes_count" />
                        <EditButton />
                    </Datagrid>
                </ReferenceManyField>

                <ReferenceManyField reference="categories" target="dataset_segmentation" addLabel={false} fullWidth>
                    <Datagrid>
                        <TextField source="id" />
                        <TextField source="name" />
                        <TextField source="segmentations_count" />
                        <EditButton />
                    </Datagrid>
                </ReferenceManyField>

            </FormTab>
            <FormTab label="Import">
                <ReferenceManyField reference="datasets/import_files" target="dataset" addLabel={false} fullWidth>
                    <Datagrid>
                        <TextField source="file_name" sortable={false} />
                        <TextField source="size" sortable={false} />
                        <LinkButton title="Import File" path="/api/datasets/import_files/" query_string="dataset={record.dataset}&file_name={record.file_name}"/>
                    </Datagrid>
                </ReferenceManyField>
            </FormTab>
        </TabbedForm>
    </Edit>
);

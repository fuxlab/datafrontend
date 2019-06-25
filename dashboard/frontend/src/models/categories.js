import React from 'react';
import { Filter, ReferenceInput, SelectInput } from 'react-admin';
import { List, Datagrid, TextField, EditButton } from 'react-admin';
import { Edit, SimpleForm, TextInput, DisabledInput } from 'react-admin';
import { Create } from 'react-admin';
import LinkViewImagesByCategoryType from './../components/link_view_images_by_category_type';


const CategoryFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
        <ReferenceInput label="Project" source="project" reference="projects" allowEmpty>
            <SelectInput optionText="name" />
        </ReferenceInput>
    </Filter>
);

export const CategoryList = props => (
    <List filters={<CategoryFilter />} {...props}>
        <Datagrid>
            <TextField source="id" />
            <TextField source="name" />
            <TextField label="Annotation" source="annotations_count" sortable={false} />
            <LinkViewImagesByCategoryType type="annotation"/>
            <TextField label="Boundingbox" source="boundingboxes_count" sortable={false} />
            <LinkViewImagesByCategoryType type="boundingbox" />
            <TextField label="Segmentation" source="segmentations_count" sortable={false} />
            <LinkViewImagesByCategoryType type="segmentation" />
            <EditButton />
        </Datagrid>
    </List>
);

export const CategoryEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput source="project" reference="projects">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Edit>
);

export const CategoryCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <ReferenceInput source="project" reference="projects">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <TextInput source="name" />
        </SimpleForm>
    </Create>
);

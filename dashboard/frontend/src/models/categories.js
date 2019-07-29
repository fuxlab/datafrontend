import React from 'react';
import { Filter, ReferenceInput, SelectInput, TextInput } from 'react-admin';
import { List, Datagrid, TextField, EditButton } from 'react-admin';
import { Create } from 'react-admin';
import LinkViewImagesByCategoryType from './../components/link_view_images_by_category_type';
import ListFilterQuick from './../components/list_filter_quick';

const CategoryFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
        <ReferenceInput label="Project" source="project" reference="projects" allowEmpty>
            <SelectInput optionText="name" />
        </ReferenceInput>
        <ListFilterQuick
            label="Has Annotation"
            source="annotation_exists"
            defaultValue={true}
        />
        <ListFilterQuick
            label="Has Boundingbox"
            source="boundingbox_exists"
            defaultValue={true}  
        />
        <ListFilterQuick
            label="Has Segmentation"
            source="segmentation_exists"
            defaultValue={true}
        />
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

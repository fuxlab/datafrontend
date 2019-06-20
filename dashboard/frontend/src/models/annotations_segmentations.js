import React from 'react';
import { Edit, SimpleForm, TextInput, DisabledInput, ReferenceInput, SelectInput, required } from 'react-admin';
import { Create } from 'react-admin';
import { parse } from 'query-string';

export const AnnotationSegmentationEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <ReferenceInput source="annotation" reference="annotations" validate={required()}>
                <SelectInput optionText="id" />
            </ReferenceInput>
            <TextInput source="mask validate={required()}" />
            <TextInput source="width" validate={required()} />
            <TextInput source="height" validate={required()} />
        </SimpleForm>
    </Edit>
);

export const AnnotationSegmentationCreate = props => {
    // inspired by https://codesandbox.io/s/2393m2k5rj
    // Read the annotation from the location which is injected by React Router and passed to our component by react-admin automatically
    const { annotation: annotation_string } = parse(props.location.search);

    // ra-data-fakerest uses integers as identifiers, we need to parse the querystring
    // We also must ensure we can still create a new comment without having a annotation
    // from the url by returning an empty string if annotation isn't specified
    const annotation = annotation_string ? parseInt(annotation_string, 10) : '';

    const redirect = annotation ? `/annotations/${annotation}/show/annotation-segmentations` : false;

    return(
        <Create {...props}>
            <SimpleForm
                defaultValue={{ annotation }}
                redirect={redirect}
            >
                <ReferenceInput source="annotation" reference="annotations" validate={required()}>
                    <SelectInput optionText="id" />
                </ReferenceInput>
                <TextInput source="mask" validate={required()} />
                <TextInput source="width" validate={required()} />
                <TextInput source="height" validate={required()} />
            </SimpleForm>
        </Create>
    );
};
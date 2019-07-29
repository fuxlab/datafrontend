import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';

import {
    TabbedForm, FormTab, Edit, TextInput, DisabledInput, ReferenceInput, SelectInput,
    ReferenceManyField, Datagrid, TextField
} from 'react-admin';

import { withStyles } from '@material-ui/core/styles';

const CategoriesEditStyles = {
    datasetList: {
        width: '100%'
    }
}

export const CategoriesEdit = withStyles(CategoriesEditStyles)(({ classes, ...props }) => {
    return(
        <Edit {...props}>
            <TabbedForm>
                <FormTab label="summary">
                    <DisabledInput source="id" />
                    <ReferenceInput source="project" reference="projects">
                        <SelectInput optionText="name" />
                    </ReferenceInput>
                    <TextInput source="name" />
                </FormTab>
                <FormTab label="Dataset Dependencies">
                    <ReferenceManyField
                        reference="datasets"
                        target="category"
                        className={classes.datasetList}
                    >
                        <Datagrid>
                            <TextField source="id" />
                            <TextField source="name" />
                            <TextField source="images_count" />
                        </Datagrid>
                    </ReferenceManyField>
                </FormTab>
            </TabbedForm>
        </Edit>
    );
});

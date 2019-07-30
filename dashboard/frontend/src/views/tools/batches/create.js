import React from 'react';
import { Edit, SimpleForm, NumberInput, LongTextInput, DisabledInput, SelectInput } from 'react-admin';
import { Create } from 'react-admin';

import { withStyles } from '@material-ui/core/styles';

const BatchesEditStyles = {
    datasetList: {
        width: '100%'
    }
}

export const BatchesCreate = withStyles(BatchesEditStyles)(({ classes, ...props }) => {
    return(
        <Create {...props}>
            <SimpleForm>
                <SelectInput
                    className={classes.default_input}
                    source="action"
                    label="Action"
                    choices={[
                        { id: 'update_images_dataset', name: 'update_images_dataset' },
                        { id: 'update_annotations_category', name: 'update_annotations_category' },
                        { id: 'update_annotation_boundingboxes_category', name: 'update_annotation_boundingboxes_category' },
                        { id: 'update_annotation_segmentations_category', name: 'update_annotation_segmentations_category' },
                    ]}
                    optionText="name"
                    allowEmpty={false}
                    resettable
                    alwaysOn
                />
                <LongTextInput source="params[0]" />
                <NumberInput source="params[1]" />
            </SimpleForm>
        </Create>
    );
});

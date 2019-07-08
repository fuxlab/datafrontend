import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'react-admin';

import CloudDownloadIcon from '@material-ui/icons/CloudDownload';
import HighlightOffIcon from '@material-ui/icons/HighlightOff';
import { withStyles } from '@material-ui/core/styles';
import { stringify } from 'query-string';

import { Filter, SelectInput, ReferenceArrayInput, SelectArrayInput, NumberInput } from 'react-admin';

const ImagesExportListFilterStyles = {
    filter: {
        width: '100%',
        marginBottom: '2em',
    },
    default_input: {
        minWidth: 300,
    },
    export_button: {
        clear: 'both'
    }
};

const ImagesExportListFilter = withStyles(ImagesExportListFilterStyles)(({ classes, ...props }) => {
    return(
        <Filter {...props} className={classes.filter}>
            <ReferenceArrayInput
                className={classes.default_input}
                label="Dataset"
                source="dataset"
                reference="datasets"
                allowEmpty={true}
                perPage={1000}
                sort={{ field: 'name', order: 'ASC' }}
                alwaysOn
            >
                <SelectArrayInput optionText="name" resettable />
            </ReferenceArrayInput>
            
            <ReferenceArrayInput
                className={classes.default_input}
                label="Category"
                source="category"
                reference="categories"
                allowEmpty={true}
                perPage={1000}
                sort={{ field: 'name', order: 'ASC' }}
                alwaysOn
            >
                <SelectArrayInput optionText="name" />
            </ReferenceArrayInput>

            <SelectInput
                className={classes.default_input}
                source="type"
                label="Type"
                choices={[
                    { id: 'all', name: 'All Images' },
                    { id: 'boundingbox', name: 'Only Boundingbox' },
                    { id: 'segmentation', name: 'Only Segmentations' },
                ]}
                optionText="name"
                disabled={props.filterValues.category == undefined}
                allowEmpty={false}
                resettable
                alwaysOn
            />

            <SelectInput
                className={classes.default_input}
                source="split"
                label="Split"
                choices={[
                    { id: '100', name: '100%' },
                    { id: '90_10', name: '90% | 10%' },
                    { id: '80_20', name: '80% | 20%' },
                    { id: '80_10_10', name: '80% | 10% | 10%' },
                    { id: '70_20_10', name: '70% | 20% | 10%' },
                ]}
                optionText="name"
                allowEmpty={false}
                resettable
                alwaysOn
            />

            <NumberInput
                className={classes.default_input}
                label="Count of Entries"
                source="max"
                step={100}
                alwaysOn
            />
            
            <Button
                className={classes.export_button}
                size="large"
                color="primary"
                variant="contained"
                disabled={props.total === 0}
                component={Link}
                href={ '/api/images/export.zip?' + stringify({
                        filter: JSON.stringify(props.filterValues),
                    })}
                label="Export"
                title="Export"
                alwaysOn
            >
                <CloudDownloadIcon />
            </Button>

            <Button
                size="medium"
                color="primary"
                onClick={() => props.setFilters({
                    dataset: '',
                    category: '',
                    type: '',
                    max:''
                })}
                label="Reset"
                title="Reset"
                alwaysOn
            >
                <HighlightOffIcon />
            </Button>
        </Filter>
    );
});

export default ImagesExportListFilter;
import React from 'react';
import { Show, SimpleShowLayout, TextField, RichTextField, DateField } from 'react-admin';

import { withStyles } from '@material-ui/core/styles';

const ListStyles = {
    table: {
        width: '100%',
        textAlign: 'left',
    },
    tableIndex: {
        width: '20%',
        verticalAlign: 'top',
    },
    pre: {
        maxHeight: 150,
        overflow: 'auto',
    }
}
const ParamsField = withStyles(ListStyles)(({ classes, record, ...props }) => {
    return(
        <table className={classes.table}>
            <thead>
            <tr>
                <th className={classes.tableIndex}>
                    Index
                </th>
                <th>
                    Value
                </th>
            </tr>
            </thead>
            {record.params.map((item, index) => (
                <tr>
                    <td className={classes.tableIndex}>
                        {index}
                    </td>
                    <td>
                        <div className={classes.pre}>
                            {item}
                        </div>
                    </td>
                </tr>
            ))}            
        </table>
    )
});
ParamsField.defaultProps = { addLabel: true };

const LogField = withStyles(ListStyles)(({ classes, record, ...props }) => {
    return(
        <ul>
            {record.log.map(item => (
                <li>
                    {item}
                </li>
            ))}
        </ul>
    )
});
LogField.defaultProps = { addLabel: true };

export const BatchesShow = props => (
    <Show {...props}>
        <SimpleShowLayout>
            <TextField source="id" />
            <TextField source="action" />
            <DateField label="Created" source="created_at" />
            <DateField label="Executed" source="updated_at" />
            <ParamsField label="Parameters" />
            <LogField label="Execution Log" />
        </SimpleShowLayout>
    </Show>
);
// in src/customRoutes.js
import React from 'react';
import { Route } from 'react-router-dom';
import { ExportList } from './views/images/export/list';

export default [
    <Route exact path="/images/export" component={ExportList} />
];
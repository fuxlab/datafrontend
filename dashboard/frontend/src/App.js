import React from 'react';
import DefaultLayout from './components/default_layout';
import PostIcon from '@material-ui/icons/Book';
import { Admin, Resource } from 'react-admin';

import { ProjectList, ProjectEdit, ProjectCreate } from './models/projects';
import { DatasetList, DatasetEdit, DatasetCreate } from './models/datasets';
import { ImageList, ImageEdit, ImageCreate } from './models/images';

import Dashboard from './components/dashboard';
import authProvider from './components/auth_provider';
import dataProvider from './components/data_provider';

import jsonServerProvider from 'ra-data-json-server';

const App = () => (
    <Admin dashboard={Dashboard} dataProvider={dataProvider} authProvider={authProvider} appLayout={DefaultLayout}>
        <Resource name="projects" list={ProjectList} edit={ProjectEdit} create={ProjectCreate} icon={PostIcon} />
        <Resource name="datasets" list={DatasetList} edit={DatasetEdit} create={DatasetCreate} icon={PostIcon} />
        <Resource name="images" list={ImageList} edit={ImageEdit} create={ImageCreate} icon={PostIcon} />
    </Admin>
);

export default App;
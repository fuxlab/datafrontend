// in src/App.js
import React from 'react';
import DefaultLayout from './components/default_layout';
import PostIcon from '@material-ui/icons/Book';
import { Admin, Resource } from 'react-admin';
import { DatasetList } from './components/datasets';
import Dashboard from './components/dashboard';
import authProvider from './components/auth_provider';
import jsonServerProvider from 'ra-data-json-server';


const dataProvider = jsonServerProvider('http://jsonplaceholder.typicode.com');

const App = () => (
    <Admin dashboard={Dashboard} dataProvider={dataProvider} authProvider={authProvider} appLayout={DefaultLayout}>
        <Resource name="users" list={DatasetList}  icon={PostIcon}/>
    </Admin>
);

export default App;
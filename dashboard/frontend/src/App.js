import React from 'react';
import Routes from './routes';

import DefaultLayout from './components/default_layout';

import PostIcon from '@material-ui/icons/Book';
import ShopTwoIcon from '@material-ui/icons/ShopTwo';
import LibraryBooksIcon from '@material-ui/icons/LibraryBooks';
import PhotoLibraryIcon from '@material-ui/icons/PhotoLibrary';
import CollectionsBookmarkIcon from '@material-ui/icons/CollectionsBookmark';

import { Admin, Resource } from 'react-admin';

import { ProjectList, ProjectEdit, ProjectCreate } from './models/projects';
import { DatasetList, DatasetEdit, DatasetCreate } from './models/datasets';
import { ImageList, ImageCreate } from './models/images';
import { ImagesEdit } from './views/images/edit/edit';
import { CategoryList, CategoryCreate } from './models/categories';
import { CategoriesEdit } from './views/categories/edit/edit';

import { BatchesEdit } from './views/annotations/batches/edit';
import { BatchesCreate } from './views/annotations/batches/create';
import { AnnotationEdit, AnnotationCreate } from './models/annotations';
import { AnnotationBoundingboxEdit, AnnotationBoundingboxCreate } from './models/annotation_boundingboxes';
import { AnnotationSegmentationEdit, AnnotationSegmentationCreate } from './models/annotations_segmentations';

import Dashboard from './components/dashboard';
import authProvider from './components/auth_provider';
import dataProvider from './components/data_provider';

import jsonServerProvider from 'ra-data-json-server';

import { createMuiTheme } from '@material-ui/core/styles';

const DatafrontendTheme = createMuiTheme({
    palette: {
        primary: {
            main: '#000000',
        },
    },
    overrides: {
        button: {
            border: {
                radius: 0,
            },
        },
    },
});


const App = () => (
    <Admin
        dashboard={Dashboard}
        customRoutes={Routes}
        dataProvider={dataProvider}
        authProvider={authProvider}
        appLayout={DefaultLayout}
        theme={DatafrontendTheme}
    >
        <Resource name="projects" list={ProjectList} edit={ProjectEdit} create={ProjectCreate} icon={ShopTwoIcon} />
        <Resource name="datasets" list={DatasetList} edit={DatasetEdit} create={DatasetCreate} icon={LibraryBooksIcon} />
        <Resource name="categories" list={CategoryList} edit={CategoriesEdit} create={CategoryCreate} icon={CollectionsBookmarkIcon} />
        <Resource name="images/export" />
        <Resource name="images" list={ImageList} edit={ImagesEdit} create={ImageCreate} icon={PhotoLibraryIcon} />
        
        <Resource name="batches" edit={BatchesEdit} create={BatchesCreate} />
        <Resource name="annotations" edit={AnnotationEdit} create={AnnotationCreate} />
        <Resource name="annotation-boundingboxes" edit={AnnotationBoundingboxEdit} create={AnnotationBoundingboxCreate} />
        <Resource name="annotation-segmentations" edit={AnnotationSegmentationEdit} create={AnnotationSegmentationCreate} />
    </Admin>
);

export default App;
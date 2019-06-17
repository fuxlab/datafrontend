import React from 'react';
import { Layout } from 'react-admin';
import DefaultAppBar from './default_app_bar';

const DefaultLayout = (props) => <Layout {...props} appBar={DefaultAppBar} />;

export default DefaultLayout;
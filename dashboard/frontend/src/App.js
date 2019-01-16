import React, { Component } from 'react';
import './App.css';

import {Route, Switch, BrowserRouter} from 'react-router-dom';

import Dashboard from "./components/Dashboard";
import Note from "./components/Note";
import Project from "./components/Project";
import Dataset from "./components/Dataset";
import NotFound from "./components/NotFound";

import { Provider } from "react-redux";
import { createStore, applyMiddleware, compose } from "redux";

import dashboardAppReducers from "./reducers";
import thunk from "redux-thunk";

const composeEnhancer = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

let store = createStore(
  dashboardAppReducers,
  composeEnhancer(applyMiddleware(thunk)),
);

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <Switch>
            <Route exact path="/" component={Dashboard} />
            <Route exact path="/notes" component={Note} />
            <Route exact path="/projects" component={Project} />
            <Route exact path="/datasets/:id" component={Dataset} />
            <Route component={NotFound} />
          </Switch>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;

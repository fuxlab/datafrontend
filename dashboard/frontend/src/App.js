import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import {Route, Switch, BrowserRouter} from 'react-router-dom';
import Note from "./components/Note";
import NotFound from "./components/NotFound";

import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";

import ponyApp from "./reducers";
import thunk from "redux-thunk";

let store = createStore(ponyApp, applyMiddleware(thunk));

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <Switch>
            <Route exact path="/" component={Note} />
            <Route component={NotFound} />
          </Switch>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;
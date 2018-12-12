import { combineReducers } from 'redux';
import notes from "./notes";

const dashboardApp = combineReducers({
  notes,
})

export default dashboardApp;
import { combineReducers } from 'redux';
import notes from "./notes";
import projects from "./projects";
import datasets from "./datasets";

const dashboardAppReducers = combineReducers({
  notes,
  projects,
  datasets,
})

export default dashboardAppReducers;
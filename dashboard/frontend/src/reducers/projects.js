const initialState = [];

export default function projects(state=initialState, action) {
  let projectList = state.slice();

  switch (action.type) {

    case 'ADD_PROJECT':
      return [...state, action.project];

    case 'FETCH_PROJECTS':
      return [...state, ...action.projects];

    case 'UPDATE_PROJECT':
      let projectToUpdate = projectList[action.index]
      projectToUpdate.name = action.project.name;
      projectList.splice(action.index, 1, projectToUpdate);
      return projectList;

    case 'DELETE_PROJECT':
      projectList.splice(action.index, 1);
      return projectList;

    default:
      return state;
  }
}

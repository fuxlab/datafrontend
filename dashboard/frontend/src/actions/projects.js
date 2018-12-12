export const fetchprojects = () => {
  return dispatch => {
    let headers = {"Content-Type": "application/json"};
    return fetch("/api/projects/", {headers, })
      .then(res => res.json())
      .then(projects => {
        return dispatch({
          type: 'FETCH_PROJECTS',
          projects
        })
      })
  }
}

export const addProject = text => {
  return dispatch => {
    let headers = {"Content-Type": "application/json"};
    let body = JSON.stringify({text, });
    return fetch("/api/projects/", {headers, method: "POST", body})
      .then(res => res.json())
      .then(project => {
        return dispatch({
          type: 'ADD_PROJECT',
          project
        })
      })
  }
}

export const updateProject = (index, text) => {
  return (dispatch, getState) => {

    let headers = {"Content-Type": "application/json"};
    let body = JSON.stringify({text, });
    let projectId = getState().projects[index].id;

    return fetch(`/api/projects/${projectId}/`, {headers, method: "PUT", body})
      .then(res => res.json())
      .then(project => {
        return dispatch({
          type: 'UPDATE_PROJECT',
          project,
          index
        })
      })
  }
}

export const deleteProject = index => {
  return (dispatch, getState) => {

    let headers = {"Content-Type": "application/json"};
    let projectId = getState().projects[index].id;

    return fetch(`/api/projects/${projectId}/`, {headers, method: "DELETE"})
      .then(res => {
        if (res.ok) {
          return dispatch({
            type: 'DELETE_PROJECT',
            index
          })
        }
      })
  }
}
export const fetchProjects = () => {
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

export const addProject = name => {
  return dispatch => {
    let headers = {"Content-Type": "application/json"};
    let body = JSON.stringify({name, });
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

export const updateProject = (index, name) => {
  return (dispatch, getState) => {

    let headers = {"Content-Type": "application/json"};
    let body = JSON.stringify({name, });
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
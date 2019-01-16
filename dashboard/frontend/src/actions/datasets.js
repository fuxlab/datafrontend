export const fetchDatasets = () => {
  return dispatch => {
    let headers = {"Content-Type": "application/json"};
    return fetch("/api/datasets/", {headers, })
      .then(res => res.json())
      .then(datasets => {
        return dispatch({
          type: 'FETCH_DATASETS',
          datasets
        })
      })
  }
}

export const fetchDataset = (id) => {
  return dispatch => {
    let headers = {"Content-Type": "application/json"};
    return fetch("/api/datasets/"+id, {headers, })
      .then(res => res.json())
      .then(dataset => {
        return dispatch({
          type: 'FETCH_DATASET',
          dataset
        })
      })
  }
}

export const addDataset = data => {
  return dispatch => {
    let headers = {"Content-Type": "application/json"};
    let body = JSON.stringify(data);
    return fetch("/api/datasets/", {headers, method: "POST", body})
      .then(res => res.json())
      .then(dataset => {
        return dispatch({
          type: 'ADD_DATASET',
          dataset
        })
      })
  }
}

export const updateDataset = (id, data) => {
  return (dispatch, getState) => {

    let headers = {"Content-Type": "application/json"};
    let body = JSON.stringify(data);

    return fetch(`/api/datasets/${id}/`, {headers, method: "PUT", body})
      .then(res => res.json())
      .then(dataset => {
        return dispatch({
          type: 'UPDATE_DATASET',
          dataset,
          id
        })
      })
  }
}

export const deleteDataset = id => {
  return (dispatch, getState) => {

    let headers = {"Content-Type": "application/json"};

    return fetch(`/api/datasets/${id}/`, {headers, method: "DELETE"})
      .then(res => {
        if (res.ok) {
          return dispatch({
            type: 'DELETE_DATASET',
            id
          })
        }
      })
  }
}
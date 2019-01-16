export const fetchDocuments = () => {
  return dispatch => {
    let headers = {"Content-Type": "application/json"};
    return fetch("/api/documents/", {headers, })
      .then(res => res.json())
      .then(documents => {
        return dispatch({
          type: 'FETCH_DOCUMENTS',
          documents
        })
      })
  }
}

export const addDocument = data => {
  return dispatch => {
    let headers = {"Content-Type": "application/json"};
    let body = JSON.stringify(data);
    return fetch("/api/documents/", {headers, method: "POST", body})
      .then(res => res.json())
      .then(document => {
        return dispatch({
          type: 'ADD_DOCUMENT',
          document
        })
      })
  }
}

export const updateDocument = (index, data) => {
  return (dispatch, getState) => {
    let headers = {"Content-Type": "application/json"};
    let body = JSON.stringify(data);
    let documentId = getState().documents[index].id;

    return fetch(`/api/documents/${documentId}/`, {headers, method: "PUT", body})
      .then(res => res.json())
      .then(document => {
        return dispatch({
          type: 'UPDATE_DOCUMENT',
          document,
          index
        })
      })
  }
}

export const deleteDocument = index => {
  return (dispatch, getState) => {

    let headers = {"Content-Type": "application/json"};
    let documentId = getState().documents[index].id;

    return fetch(`/api/documents/${documentId}/`, {headers, method: "DELETE"})
      .then(res => {
        if (res.ok) {
          return dispatch({
            type: 'DELETE_DOCUMENT',
            index
          })
        }
      })
  }
}
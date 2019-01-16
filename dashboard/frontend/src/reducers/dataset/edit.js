const initialState = [];

// could be replaced to { type, payload }
export default function datasets(state=initialState, action) {
  let datasetList = state.slice();

  switch (action.type) {

    case 'ADD_DATASET':
      return [...state, action.dataset];

    case 'FETCH_DATASETS':
      return [...state, ...action.datasets];

    case 'UPDATE_DATASET':
      let datasetToUpdate = datasetList[action.index]
      datasetToUpdate.project_id = action.dataset.project_id;
      datasetToUpdate.name = action.dataset.name;
      datasetToUpdate.identifier = action.dataset.identifier;
      datasetList.splice(action.index, 1, datasetToUpdate);
      return datasetList;

    case 'DELETE_DATASET':
      datasetList.splice(action.index, 1);
      return datasetList;

    default:
      return state;
  }
}

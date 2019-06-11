const initialState = {
  'all': [],
  'one': {}
};

export default function datasets(state=initialState, action) {
  switch (action.type) {

    case 'ADD_DATASET':
      return [...state, action.dataset];

    case 'FETCH_DATASET':
      state.one = {
        'id': action.dataset.id,
        'name': action.dataset.name,
        'identifier': action.dataset.identifier,
      }
      return state;

    case 'UPDATE_DATASET':
      let indexToUpdate = state.all.findIndex(dataset => (dataset.id === action.id));
      console.log(indexToUpdate);
      let datasetToUpdate = state['all'][indexToUpdate]
      
      datasetToUpdate.project_id = action.dataset.project_id;
      datasetToUpdate.name = action.dataset.name;
      datasetToUpdate.identifier = action.dataset.identifier;

      state['all'].splice(indexToUpdate, 1, datasetToUpdate);
      console.log(state);
      return state;
      

    case 'DELETE_DATASET':
      //datasetList.splice(action.id, 1);
      return state;

    case 'FETCH_DATASETS':
      state.all = action.datasets;
      return state;

    default:
      return state;
  }
}

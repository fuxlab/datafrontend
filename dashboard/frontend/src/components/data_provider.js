// in src/dataProvider
import {
    GET_LIST,
    GET_ONE,
    GET_MANY,
    GET_MANY_REFERENCE,
    CREATE,
    UPDATE,
    DELETE,
    fetchUtils,
} from 'react-admin';
import { stringify } from 'query-string';

const API_URL = '/api';

/**
 * @param {String} type One of the constants appearing at the top of this file, e.g. 'UPDATE'
 * @param {String} resource Name of the resource to fetch, e.g. 'posts'
 * @param {Object} params The Data Provider request params, depending on the type
 * @returns {Object} { url, options } The HTTP request parameters
 */
const convertDataProviderRequestToHTTP = (type, resource, params) => {
    switch (type) {
    case GET_LIST: {
        const { page, perPage } = params.pagination;
        const { field, order } = params.sort;
        const query = {
            sort: JSON.stringify([field, order]),
            range: JSON.stringify([(page - 1) * perPage, page * perPage - 1]),
            filter: JSON.stringify(params.filter),
        };
        return {
            url: `${API_URL}/${resource}/?${stringify(query)}`
        };
    }
    case GET_ONE:
        return {
            url: `${API_URL}/${resource}/${params.id}/`
        };
    case GET_MANY: {
        const query = {
            filter: JSON.stringify({ id: params.ids }),
        };
        return {
            url: `${API_URL}/${resource}/?${stringify(query)}`
        };
    }
    case GET_MANY_REFERENCE: {
        const { page, perPage } = params.pagination;
        const { field, order } = params.sort;
        const query = {
            sort: JSON.stringify([field, order]),
            range: JSON.stringify([(page - 1) * perPage, (page * perPage) - 1]),
            filter: JSON.stringify({ ...params.filter, [params.target]: params.id }),
        };
        return {
            url: `${API_URL}/${resource}/?${stringify(query)}`
        };
    }
    case UPDATE:
        const formData = new FormData();
        Object.keys(params.data).forEach(function(key) {
            formData.append(key, params.data[key]);
        });
        // formData.append('file', params.files[0]);
        return {
            url: `${API_URL}/${resource}/${params.id}/`,
            options: {
                method: 'PUT',
                body: formData
            }
        };
    case CREATE:
        return {
            url: `${API_URL}/${resource}/`,
            options: {
                method: 'POST',
                body: JSON.stringify(params.data)
            },
        };
    case DELETE:
        return {
            url: `${API_URL}/${resource}/${params.id}/`,
            options: {
                method: 'DELETE'
            },
        };
    default:
        throw new Error(`Unsupported fetch action type ${type}`);
    }
};

/**
 * @param {Object} response HTTP response from fetch()
 * @param {String} type One of the constants appearing at the top of this file, e.g. 'UPDATE'
 * @param {String} resource Name of the resource to fetch, e.g. 'posts'
 * @param {Object} params The Data Provider request params, depending on the type
 * @returns {Object} Data Provider response
 */
const convertHTTPResponseToDataProvider = (response, type, resource, params) => {
    const { headers, json } = response;
    switch (type) {
    case GET_LIST:
        var mapped_data = [];
        var total = 0;

        if(json.length > 0) {
            mapped_data = json.map(x => x);
        }
        if(headers.get('content-range')){
            total = parseInt(headers.get('content-range').split('/').pop(), 10);
        }
        
        return {
            data: mapped_data,
            total: total,
        };
    case CREATE:
        return { data: { ...params.data, id: json.id } };
    default:
        return { data: json };
    }
};

/**
 * @param {string} type Request type, e.g GET_LIST
 * @param {string} resource Resource name, e.g. "posts"
 * @param {Object} payload Request parameters. Depends on the request type
 * @returns {Promise} the Promise for response
 */
export default (type, resource, params) => {
    const { fetchJson } = fetchUtils;
    const { url, options } = convertDataProviderRequestToHTTP(type, resource, params);
    return fetchJson(url, options)
        .then(response => convertHTTPResponseToDataProvider(response, type, resource, params));
};
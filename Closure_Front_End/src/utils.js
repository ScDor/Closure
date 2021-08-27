
/** A mapping between API "semester" values to the "semester" property used in the front-end,
    which indicates their positioning.
 */
export const API_SEMESTER_TO_PROP_INT = new Map(Object.entries({
  FIRST: 1,
  SECOND: 2
}))

/** A mapping between the "semester" property values used in the front-end, to their corresponding
 *  values in the backend API
 */
export const PROP_INT_TO_API_SEMESTER = new Map(Array.from(API_SEMESTER_TO_PROP_INT, a => a.reverse()))

 
export function isString(x) {
  return Object.prototype.toString.call(x) === "[object String]"
}


export function groupBy(xs, key) {
  return xs.reduce(function (rv, x) {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;
  }, {});
}

/**
 * A function used to query a list endpoint from Django Rest Framework(DRF), 
 * and return an array of objects suitable for passing into Multiselect component 'options'.
 * 
 * @param {import("axios").AxiosInstance} http used to create requests
 * @param {string} url URL of a DRF 'list' retrieval endpoint
 * @param {(obj: any) => string} objToLabel Extracts the label(shown in Select) of a model object
 * @returns {[any]} Array of multiselect options
 */
export async function fetchDjangoListIntoSelectOptions(http, url, objToLabel) {
      console.log('multiselect fetching from', url);
      const response = await http.get(url);
      const values = response.data.results;
      return values.map(value => { return {
        value, label: objToLabel(value)
      }});
}

export function isString(x) {
  return Object.prototype.toString.call(x) === "[object String]"
}


export function groupBy(xs, key) {
  return xs.reduce(function (rv, x) {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;
  }, {});
}

export const MODEL_COURSE_TYPE_TO_STRING = new Map([
  ["MUST", "חובה"],
  ["CHOICE", "בחירה"],
  ["CHOOSE_FROM_LIST", "חובת בחירה"],
  ["CORNER_STONE", "אבן פינה"],
  ["SUPPLEMENTARY", "לימודים משלימים"]
]);

export const MODEL_SEMESTER_TO_STRING = new Map([
    ['FIRST', "ראשון"],
    ['SECOND', "שני"],
    ['SUMMER', "קיץ"],
    ['EITHER', "כל"],
    ['ANNUAL', "שנתי"],
    // TODO: standardize model types in the code to avoid this
    // duplictation
    [1, "ראשון"],
    [2, "שני"]
]);

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

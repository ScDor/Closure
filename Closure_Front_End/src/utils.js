
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

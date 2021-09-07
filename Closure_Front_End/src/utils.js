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
    ['FIRST', "סמסטר א'"],
    ['SECOND', "סמסטר ב'"],
    ['SUMMER', "קורס קיץ"],
    ['EITHER', "סמסטר א'/ב'"],
    ['ANNUAL', "קורס שנתי"],
    // TODO: standardize model types in the code to avoid this
    // duplictation
    [1, "סמסטר א'"],
    [2, "סמסטר ב'"]
]);


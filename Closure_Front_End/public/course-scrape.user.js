// ==UserScript==
// @name     HUJI Registered Course Scraper
// @version  1
// @grant    none
// @match https://www.huji.ac.il/dataj/controller/*STUZIYUNIM*
// ==/UserScript==

'use strict'

// TODO: determine this url dynamically
const IFRAME_ORIGIN = "http://localhost:8080"
const IFRAME_URL = `${IFRAME_ORIGIN}/course-scrape-iframe.html`;

/**
 * An asynchronous function that drives this script, which includes:
 * - Creating a status iframe within the Closure website
 * - Fetching the courses documents for all available years
 * - Parsing those documents into a list of courses
 * - Notifying the iframe of those courses, which shall then POST them to the backend.
 */
async function start() {

  if (!isRunningInRegisteredCoursesPage()) {
    console.error("HUJI registered course scraper script ran on incorrect page");
    return;
  }

  const iframe = attachStatusIframe();

  try {
    const docs = await getDocumentsForAllYears();
    iframe.contentWindow.postMessage({
      "type": "gotDocs",
      "numDocs": docs.length
    }, IFRAME_ORIGIN);
    const courses = docs.flatMap(getCoursesForDocument);
    console.log(`Fetched ${courses.length} courses`);
    iframe.contentWindow.postMessage({
      "type": "gotCourses",
      "courses": courses
    }, IFRAME_ORIGIN);
    console.log(`A total of ${courses.length} courses were parsed in this document`);
  }
  catch (err) {
    iframe.contentWindow.postMessage({
      "type": "error",
      "errorMessage": err.message
    }, IFRAME_ORIGIN);
  }

}

/**
 * Creates an iframe for communication with our front-end as well as visually displaying
 * the script's status
 * @returns {HTMLIFrameElement} IFrame element
 */
function attachStatusIframe() {
  const iframe = document.createElement("iframe");
  iframe.style.overflow = "hidden";
  iframe.style.width = "100%";
  iframe.style.height = "400";
  iframe.scrolling = "no";
  iframe.style.border = 0;
  iframe.id = "courseScrapeIframe";
  iframe.src = IFRAME_URL;
  document.body.prepend(iframe);
  return iframe
}

/**
 * @returns {boolean} Are we currently on a registered courses page
 */
function isRunningInRegisteredCoursesPage() {
  const title = document.querySelectorAll(".gen_title");
  for (const elm of title) {
    if (elm.textContent.includes("פרוט קורסים וציונים")) {
      return true;
    }
  }
  return false;
}

/**
 * Fetches documents for all available years (in no particular order)
 * @returns {Array<HTMLDocument>} Documents containing courses
 */
async function getDocumentsForAllYears () {
  const yearSelector = document.querySelector("form#ziyunim select[name='yearsafa']")
  const curYear = Number.parseInt(yearSelector.value)
  const otherYears = [...yearSelector.options].map(el => Number.parseInt(el.value)).filter(year => year !== curYear)

  console.log(`Document year is ${curYear}, other years are ${otherYears}`)

  const promises = [ Promise.resolve(document)].concat(
    otherYears.map(async (year) => {
      const urlData = new URLSearchParams({
        "yearsafa": year
      });

      const response = await fetch(document.ziyunim.action, {
        method: 'POST',
        body: urlData,

      });

      if (!response.ok) {
        throw Error(`Error while fetching courses for year ${year}: ${response.status} - ${response.statusText}`);
      }

      const textDecoder = new TextDecoder("windows-1255");
      const byteBuff = await response.arrayBuffer();
      const html = textDecoder.decode(byteBuff);
      const parser = new DOMParser();
      return parser.parseFromString(html, "text/html");

      
    })
  );

  return await Promise.all(promises);
}


/**
 * Returns a list of course objects within the given document
 * @param {HTMLDocument} doc Document to scrape for registered courses
 * @returns An array of course objects
 */
function getCoursesForDocument (doc) {
  console.log('Beginning to parse courses')

  // find all tables containing registered courses(there may be several depending on num of chugs)
  const tdIt = doc.evaluate("//tbody[tr[td[contains(text(), 'סמל קורס')]]]", doc, null, XPathResult.ANY_TYPE, null)

  const courses = []

  let tbody = tdIt.iterateNext()
  while (tbody) {
    const tableResults = parseCourseTable(tbody)
    courses.push(...tableResults)
    tbody = tdIt.iterateNext()
  }

  return courses
}

/**
 * Extracts all course information from a registered courses table
 * @param {HTMLTableElement} tbody A 'tbody' element containing courses for some Chug
 * @returns {Array<Record<string, string | [string, string]>} An array of parsed course objects, using column headers as keys
 * and values are the text content of each matching cell,
 * or a tuple of those contents along with a URL, if a URL is available(statistics, course symbol and extra grades)
 */
function parseCourseTable (tbody) {
  const columns = [...tbody.rows[0].childNodes].filter(elm => elm instanceof HTMLElement).map(elm => elm.innerText)
  const rows = []
  for (let i = 1; i < tbody.rows.length; ++i) {
    const fields = [...tbody.rows[i].childNodes].filter(elm => elm instanceof HTMLElement).map(elm => {
      const childElements = elm.children
      if (childElements.length === 1 && childElements[0] instanceof HTMLAnchorElement) {
        const url = childElements[0].href
        return [elm.innerText, url]
      }
      return elm.innerText
    })
    if (fields.length !== columns.length) {
      console.warn(`Mismatch between header(${columns.length} entries) and row(${fields.length} entries)`)
      continue
    }
    const entry = columns.reduce((obj, key, keyIx) => ({ ...obj, [key]: fields[keyIx] }), {})

    // the year and semester aren't explicit table cells(although year is known from page),
    // but they can be derived from the statistics URL structure
    const statsUrl = entry['סטטיסטיקות'][1]
    const statsParams = new URLSearchParams(statsUrl)

    const year = statsParams.get('yearlimud')
    const semester = statsParams.get('tkufa')

    entry.year = year
    entry.semester = semester

    console.log(entry)
    rows.push(entry)
  }
  return rows
}

window.addEventListener('load', start)

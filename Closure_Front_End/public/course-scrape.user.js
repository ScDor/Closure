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
    const courses = await Promise.all(docs.flatMap(getCoursesForDocument));
    console.log(`Fetched ${courses.length} `);
    iframe.contentWindow.postMessage({
      "type": "gotCourses",
      "courses": courses
    }, IFRAME_ORIGIN);
    console.log(`A total of ${courses.length} courses were parsed`);
  }
  catch (err) {
    console.error(err)
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

const YEAR_INPUT_CSS_SELECTOR = "form#ziyunim select[name='yearsafa']"

/**
 * Fetches documents for all available years (in no particular order)
 * @returns {Array<HTMLDocument>} Documents containing courses
 */
async function getDocumentsForAllYears () {
  const yearSelector = document.querySelector(YEAR_INPUT_CSS_SELECTOR)
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

      return await responseToDocument(response)
    })
  );

  return await Promise.all(promises);
}

/**
 * Parses the given fetch response as HTML document
 * @param {Response} response Result of fetch, assumed to contain HTML text encoded in Windows-1255
 * @returns {Document} Parsed HTML document
 */
async function responseToDocument(response) {
  const textDecoder = new TextDecoder("windows-1255");
  const byteBuff = await response.arrayBuffer();
  const html = textDecoder.decode(byteBuff);
  const parser = new DOMParser();
  return parser.parseFromString(html, "text/html");
}

/**
 * Returns a generator over all HTML elements retrieved via given XPath query
 * @param {HTMLDocument} doc Document to query
 * @param {string} xpath XPath query
 * @returns {Generator<HTMLElement>} Generator over parsed elements via the XPath
 */
function* xpathQuery(doc, xpath) {
  const it = doc.evaluate(xpath, doc, null, XPathResult.ANY_TYPE, null)
  let elm = it.iterateNext()
  while (elm) {
    yield elm
    elm = it.iterateNext()
  }
}

/**
 * Returns a list of course objects within the given document
 * @param {HTMLDocument} doc Document to scrape for registered courses
 * @returns {Promise<Array<CourseParseResult>>} An array of course objects
 */
async function getCoursesForDocument(doc) {
  const docYear = Number.parseInt(doc.querySelector(YEAR_INPUT_CSS_SELECTOR).value)
  console.log(`Beginning to parse courses for year ${docYear}`)

  // find all tables containing registered courses(there may be several depending on num of chugs)
  const tdElements = [...xpathQuery(doc, "//tbody[tr[td[contains(text(), 'סמל קורס')]]]")]

  const courses = []
  for (const tbody of tdElements) {
    const tableResults = await parseCourseTable(tbody, docYear)
    courses.push(...tableResults)
  }

  return courses
}


/** 
 * A parsed course entry contains fields such as course number, course name, points and statistics.
 * Each field contains either just 1 element(the text content) or 2 elements(text content, and href)
 * @typedef {Record<string, [any] | [any, any]>} CourseParseResult */


/**
 * Extracts all course information from a registered courses table
 * @param {HTMLTableElement} tbody A 'tbody' element containing courses for some Chug
 * @param {number} docYear The year associated with the table
 * @returns {Array<CourseParseResult>} An array of parsed course objects, using column headers as keys
 * and values are the content of each matching cell,
 * or a tuple of those contents along with a URL, if a URL is available(statistics, course symbol and extra grades)
 */
async function parseCourseTable(tbody, docYear) {
  const columns = [...tbody.rows[0].childNodes].filter(elm => elm instanceof HTMLElement).map(elm => elm.innerText)
  const rows = []
  for (let i = 1; i < tbody.rows.length; ++i) {
    const fields = [...tbody.rows[i].childNodes].filter(elm => elm instanceof HTMLElement).map(elm => {
      const childElements = elm.children
      if (childElements.length === 1 && childElements[0] instanceof HTMLAnchorElement) {
        const url = childElements[0].href
        return [elm.innerText, url]
      }
      return [elm.innerText]
    })
    if (fields.length !== columns.length) {
      console.warn(`Mismatch between header(${columns.length} entries) and row(${fields.length} entries)`)
      continue
    }
    const entry = columns.reduce((obj, key, keyIx) => ({ ...obj, [key]: fields[keyIx] }), {})
    entry.year = docYear
    tryFillSemesterFromStatisticsURL(entry, docYear)
    if (!entry.semester) {
      await tryFillSemesterFromShnaton(entry)
    }

    console.log(entry)
    rows.push(entry)
  }
  return rows
}

/**
 * Tries filling semester information for given entry via Shnaton, unless Course is offered
 * in both semesters.
 * @param {CourseParseResult} entry 
 * @returns 
 */
async function tryFillSemesterFromShnaton(entry) {
  const shntaonUrlHref = entry['סמל קורס'][1]
  if (!shntaonUrlHref) {
    console.warn(`Could not find shntaon URL for entry ${JSON.stringify(entry)}`)
    return
  }
  const shnatonUrlMatch = shntaonUrlHref.match(/openWinD\('(.*)'\)/)
  if (!shnatonUrlMatch) {
    console.error(`Could not extract shntaon URL from href ${shntaonUrlHref}`)
    return
  }

  const docRes = await fetch(shntaonUrlHref)
  if (!docRes.ok) {
    const errText = await docRes.text()
    console.error(`Couldn't retrieve shnaton for entry ${JSON.stringify(entry)}: ${docRes.status} - ${errText}`)
    return
  }
  const doc = await responseToDocument(docRes)
  const semesterStrings = [...xpathQuery(doc, "//td[@class='courseTD text' and contains(text(), 'סמסטר')]")]
  if (semesterStrings.length != 1) {
    console.error(`Couldn't find semester in shntaon URL ${shnatonUrlMatch}`)
    return;
  }
  const semesterString = semesterStrings[0].textContent

  if (semesterString == "סמסטר א'") { 
    entry.semester == 1
  }
  else if (semesterString == "סמסטר ב'") { 
    entry.semester == 2 
  }
  else {
    console.log(`Ambiguous semester \"${semesterString}" for entry ${JSON.stringify(entry)}`)
  }
}

/**
 * Tries filling semester information from link to statistics page.
 * @param {CourseParseResult} entry See {@link parseCourseTable}
 * @param docYear The year in the document from which this entry is parsed, used
 *                for sanity checking.
 */
function tryFillSemesterFromStatisticsURL(entry, docYear) {
    // the year and semester aren't explicit table cells(although year is known from page),
    // but they can be derived from the statistics URL structure
    const statsUrl = entry['סטטיסטיקות'][1]
    if (!statsUrl) {
      console.log(`Entry ${JSON.stringify(entry)} has no statistics`)
      return;
    }
    const statsParams = new URLSearchParams(statsUrl)

    const year = Number.parseInt(statsParams.get('yearlimud'))
    const semester = Number.parseInt(statsParams.get('tkufa'))

    if (!year || !semester) {
      console.error(`Entry ${JSON.stringify(entry)} has a statistics URL with no year/semester params: ${statsUrl}`)
      return
    }

    if (year != docYear) {
      console.warn(`Entry ${JSON.stringify(entry)} has year ${year} while the document's year is ${docYear}`)
    }

    entry.semester = semester
}

window.addEventListener('load', start)

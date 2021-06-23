// ==UserScript==
// @name     HUJI Registered Course Scraper
// @version  1
// @author Daniel Kerbel
// @grant    none
// @match https://www.huji.ac.il/dataj/controller/*STUZIYUNIM*
// ==/UserScript==

'use strict'

console.log(`Scrape script initialized`)

// TODO: determine this url at build time
const FRONTEND_ORIGIN = "http://localhost:8094"




/**
 * This function tries to find the Window object of the front-end website that (supposedly) opened this website.
 * 
 * This is done by recursively traversing the chain of all openers - this is required because the process of
 * logging into HUJI's personal information website and reaching the personal grades website may involve several pop-ups.
 * 
 * Because of cross-origin security, we cannot simply invoke the `opener.origin` property, so we use a simple
 * handshaking protocol to determine which opener belongs to the front-end
 */
function findFrontendOpener() {
  let opener = window.opener
  let level = 0
  if (!opener) {
    window.alert(`You must run this script from the pop-up given by our site`)
  }
  while (opener) {
    level++
    try {
      console.log(`Trying to communicate with level ${level}`)
      opener.postMessage({
        type: "tryHook", level
      }, FRONTEND_ORIGIN)
    } catch (e) {
      console.error(`Error while trying to post message: ${e}`)
    }
    opener = opener.opener
  }
}



let opener = null

async function messageHandler(event) {
  console.log(`Got message ${JSON.stringify(event)}`)
  if (event.origin != FRONTEND_ORIGIN) {
    console.error(`Got message ${JSON.stringify(event.data)} from unknown origin ${event.origin}`)
    return
  }
  if (event.data === "hooked") {
    opener = event.source 
    console.log(`Hooked into frontend.`)
  }
  if (event.data === "start") {
    event.source.postMessage("started", FRONTEND_ORIGIN)
    await beginScrape()
    event.source.postMessage("finishedParsing", FRONTEND_ORIGIN)
  }

}



function postParseEntry(entry) {
  opener.postMessage({
    "type": "gotCourse",
    "course": entry
  }, FRONTEND_ORIGIN);
}


if (isRunningInGradesPage()) {
    findFrontendOpener()
}

async function beginScrape() {

  if (!isRunningInGradesPage()) {
    console.error("HUJI registered course scraper script ran on incorrect page");
    return;
  }

  try {
    const docs = await getDocumentsForAllYears();
    opener.postMessage({
      "type": "gotDocs",
      "numDocs": docs.length
    }, FRONTEND_ORIGIN);

    const courses = (await Promise.all(docs.map(getCoursesForDocument))).flat()
    console.log(`A total of ${courses.length} documents were parsed from ${docs.length} documents.`);
  }
  catch (err) {
    console.error(err)
    opener.postMessage({
      "type": "error",
      "errorMessage": err.message
    }, FRONTEND_ORIGIN);
  }

}

/**
 * @returns {boolean} Are we currently on a registered courses page
 */
function isRunningInGradesPage() {
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

  return await Promise.all(tdElements.map(tbody => parseCourseTable(tbody, docYear)))
}


/** 
 * A parsed course entry contains fields such as course number, course name, points and statistics.
 * @typedef {Record<string, any>} CourseParseResult */


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
      console.error(`Mismatch between header(${columns.length} entries) and row(${fields.length} entries)`)
      continue
    }
    const entry = columns.reduce((obj, key, keyIx) => ({ ...obj, [key]: fields[keyIx] }), {})
    const engEntry = {
      "course_id": Number.parseInt(entry["סמל קורס"][0]),
      "name": entry["קורס"][0],
      "year": docYear,
      "points": Number.parseInt(entry["נקודות זכות"][0])
    }
    if (entry["סטטיסטיקות"].length === 2) {
      engEntry.statistics_url = entry["סטטיסטיקות"][1]
      const urlParams = new URLSearchParams(engEntry.statistics_url)
      let [year, semester] = [ urlParams.get("yearlimud"), urlParams.get("tkufa")]
      year = Number.parseInt(year)
      semester = Number.parseInt(semester)
      
      if (!year || !semester) {
        console.error(`Couldn't determine year and/or semester from statistics URL ${engEntry.statistics_url}`)
      } else {
        engEntry.semester = TKUFA_TO_SEMESTER[semester]
        if (year !== docYear) {
          console.error(`Mismatch between statistics URL year(=${year}) and doc year(=${docYear})`)
          engEntry.year = docYear
        }
      }
    }
    entry.year = docYear
    postParseEntry(engEntry)
    // console.log(entry)
    rows.push(engEntry)
  }
  return rows
}


const TKUFA_TO_SEMESTER = {
  1: "FIRST",
  2: "SECOND",
}

window.addEventListener("load", function() {
  if (!isRunningInGradesPage()) {
    console.warn(`Script is not running within the grades page`)
    return
  }
  window.addEventListener("message", messageHandler);
  console.log(`Attached message handler`)
  findFrontendOpener()

})
// ==UserScript==
// @name     HUJI Registered courses import script
// @version  1
// @author Daniel Kerbel
// @grant    none
// @match https://www.huji.ac.il/dataj/controller/*/stu/*
// ==/UserScript==

'use strict'


const FRONTEND_ORIGIN = (typeof process !== "undefined" && process.env.VUE_APP_AUTH0_REDIRECT_URI) || "http://localhost:8080"


console.log(`Import script was loaded, origin of front-end is ${FRONTEND_ORIGIN}`)

let opener = null

function error(msg, critical) {
  if (opener) {
    opener.postMessage({
      "type": "error",
      "errorMessage": msg,
      "critical": critical,
    }, FRONTEND_ORIGIN);
  }
  console.error(msg)
  window.alert(msg)
  if (critical) {
    throw new Error(msg)
  }
}

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



let startedScrape = false
/**
 * Creates a message handler for handling cross-origin messages from the front-end,
 * which will begin scraping from the given document once communication with the front-end has been established.
 * @param {HTMLDocument} doc Documenet containing registered courses & grads
 * @returns {Promise<(this: Window, event: MessageEvent) => void>} Handler of cross-origin communication messages
 */
const mkMessageHandler = (doc) => async function messageHandler(event) {
  console.log(`Got message ${JSON.stringify(event)}`)
  if (event.origin != FRONTEND_ORIGIN) {
    console.error(`\tfrom unknown origin ${event.origin}`)
    return
  }
  if (event.data === "hooked") {
    opener = event.source 
    console.log("Hooked into frontend, starting scrape")
    window.alert("מתחיל ייבוא קורסים")
    startedScrape = true
    event.source.postMessage("started", FRONTEND_ORIGIN)
    await beginScrape(doc)
    console.log("Finished scrape")
    event.source.postMessage("finishedParsing", FRONTEND_ORIGIN)
  }
}



function postParseEntry(entry) {
  opener.postMessage({
    "type": "gotCourse",
    "course": entry
  }, FRONTEND_ORIGIN);
}


/**
 * Begins scraping the registered courses website, posting them to the front-end
 * @param {HTMLDocument} doc Doument containing student courses & grades(in any year)
 */
async function beginScrape(doc) {
  try {
    console.log("Fetching documents")
    const docs = (await getDocumentsForAllYears(doc)).filter(doc => doc);
    console.log(`Fetched ${docs.length} documents containing courses`)
    console.log(docs)

    const courses = (await Promise.all(docs.map(getCoursesForDocument))).flat()
    console.log(`Got a total of ${courses.length} courses`)
  }
  catch (err) {
    error(
      "חלה שגיאה קריטית במהלך קליטת קורסים מאתר האוניברסיטה" 
      + ":\n" + err
    , true)
  }

}


/**
 * Given a document under the 'personal information' section of HUJI, 
 * retrieves the document containing the registered courses and grades.
 * @param {HTMLDocument} doc Document under the personal information site
 * @returns {HTMLDocument} document containing years
 */
async function fetchCoursesAndGradesDocument(doc) {
  if (doc.location.origin !== "https://www.huji.ac.il" ||
      !doc.location.pathname.startsWith("/dataj/controller")) {
    const err = "This script must be ran within HUJI's personal information site"

    error(
      "יש להריץ את הסקריפט מאתר המידע האישי של האוניברסיטה"
    )
  }

  if (doc.location.pathname.match(/\/stu\/?$/)) {
    const res = await fetch("STU-STUZIYUNIM")
    if (!res.ok) {
      const msg = await res.text()
      throw Error(`Error while courses document: ${res.status} - ${msg}`)
    }
    const doc = await responseToDocument(res)
    return doc
  } else if (doc.location.pathname.includes("/stu/STU-STUZIYUNIM")) {
    return doc
  }
}

/**
 * @param {HTMLDocument} doc The document
 * @returns {boolean} Is the document a registered courses & grades page
 */
function isCoursesAndGradesDocument(doc) {
  const title = doc.querySelectorAll(".gen_title");
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
 * @param {HTMLDocument} doc Doument containing student grades(in any year)
 * @returns {Array<HTMLDocument>} Documents containing courses
 */
async function getDocumentsForAllYears (doc) {
  if (!isCoursesAndGradesDocument(doc)) {
    error("getDocumentForAllYears must be ran on grades page")
  }
  const yearSelector = doc.querySelector(YEAR_INPUT_CSS_SELECTOR)
  const curYear = Number.parseInt(yearSelector.value)
  const otherYears = [...yearSelector.options].map(el => Number.parseInt(el.value)).filter(year => year !== curYear)

  console.log(`Document year is ${curYear}, other years are ${otherYears}`)

  const promises = [ Promise.resolve(doc)].concat(
    otherYears.map(async (year) => {
      const urlData = new URLSearchParams({
        "yearsafa": year
      });
      try {
          const response = await fetch(doc.ziyunim.action, {
          method: 'POST',
          body: urlData,

        });

        if (!response.ok) {
          const errText = await response.text()
          throw new Error(`Bad response: ${response.status} - ${response.statusText}\nContents: ${errText}`)
        }
        return await responseToDocument(response)
      }
      catch (ex) {
        error(
          `חלה שגיאה בעת הניסיון להשיג את המסמך של שנה ${year}: ${ex}`
        , false)
        return null
      }
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

  const results = (await Promise.all(tdElements.map(tbody => parseCourseTable(tbody, docYear)))).flat()
  console.log(`Got ${results.length} courses for year ${docYear}`)
  return results
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
    rows.push(engEntry)
  }
  return rows
}


// TODO: support annual and summer courses
const TKUFA_TO_SEMESTER = {
  1: "FIRST",
  2: "SECOND",
}


let loaded = false

const NOT_LOADED_ERROR_TIMEOUT_MS = 3000

async function startScript() {
  if (loaded) {
    console.log(`Attempted to start script twice`)
    return
  }
  loaded = true
  console.log(`Scrape script startScript() begun`)
  const coursesDoc = await fetchCoursesAndGradesDocument(window.document)
  const messageHandler = mkMessageHandler(coursesDoc)
  window.addEventListener("message", messageHandler);
  console.log(`Attached message handler`)
  findFrontendOpener()
  setTimeout(() => {
    if (!startedScrape) {
      error(
        "יש להריץ את הסקריפט מתוך החלון שנפתח על ידי לחיצת הכפתור מאתר Closure", true
      )
    }
  }, NOT_LOADED_ERROR_TIMEOUT_MS)
  console.log(`Found frontend`)
}


if (document.readyState === "complete") {
  startScript();
} else {
  window.addEventListener("load", startScript)
}


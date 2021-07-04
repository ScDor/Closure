
import { postParsedEntry, postFinishedParsing } from './course-scrape-communication.js'
import { ScrapeError, warning } from './course-scrape-errors.js'

/**
 * Begins scraping the registered courses website, posting them to the front-end
 * @param {Document} doc Doument containing student courses & grades(in any year)
 */
export async function beginScrape(doc) {
    try {
        console.log("Fetching documents from document: ", doc)
        const docs = (await getDocumentsForAllYears(doc)).filter(doc => doc);
        console.log(`Fetched ${docs.length} documents containing courses`)
        console.log(docs)
        const courses = (await Promise.all(docs.map(getCoursesForDocument))).flat()
        console.log(`Got a total of ${courses.length} courses:`, courses)
        postFinishedParsing()
    }
    catch (err) {
        throw new ScrapeError("חלה שגיאה קריטית במהלך קליטת קורסים מאתר האוניברסיטה", err)
    }

}



/**
 * Checks the given response, if it's not OK, throws an error
 * @param {Response} res 
 */
async function handleErrorResponse(res) {
    if (!res.ok) {
        const msg = await res.text()
        throw new ScrapeError("חלה שגיאת תקשורת עם אתר האוניברסיטה",
            { ...res, msg })
    }
}

const EXPECTED_DOC_ORIGIN = "https://www.huji.ac.il"
const HUJI_PI_PATHNAME_REGEX = new RegExp(/(\/dataj\/controller\/[^/]+\/stu)/)
const GRADES_URI_COMPONENT = "/STU-STUZIYUNIM"


/**
 * Given a document under the 'personal information' section of HUJI, 
 * retrieves the document containing the registered courses and grades.
 * @param {Document} doc Document under the personal information site
 * @returns {Document} document containing years
 */
export async function fetchCoursesAndGradesDocument(doc) {

    const hebErr = "יש להריץ את הסקריפט מאתר המידע האישי של האוניברסיטה"

    if (doc.location.origin !== EXPECTED_DOC_ORIGIN) {
        throw new ScrapeError(hebErr, new Error(`Expected origin ${EXPECTED_DOC_ORIGIN}, gotten origin ${doc.location.origin}`))
    }
    const match = doc.location.pathname.match(HUJI_PI_PATHNAME_REGEX)
    if (!match) {
        throw new ScrapeError(hebErr, new Error(`Pathname should match regex ${HUJI_PI_PATHNAME_REGEX}, got ${doc.location.pathname} instead.`))
    }
    if (doc.location.pathname.includes(GRADES_URI_COMPONENT)) {
        console.log("Running within grades page")
        return doc
    }

    const gradesPathname = match[1] + GRADES_URI_COMPONENT
    const gradesUrl = new URL(gradesPathname, doc.location.origin)
    console.log(`Running within HUJI personal information site, will fetch documents from ${gradesUrl}`)
    const res = await fetch(gradesUrl)
    await handleErrorResponse(res)
    const gradesDoc = await responseToDocument(res)
    console.log("Fetched grades document: ", gradesDoc)
    return gradesDoc
}

/**
 * @param {Document} doc The document
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
 * @param {Document} doc Doument containing student grades(in any year)
 * @returns {Array<Document>} Documents containing courses
 */
async function getDocumentsForAllYears(doc) {
    if (!isCoursesAndGradesDocument(doc)) {
        throw new ScrapeError("getDocumentForAllYears must be ran on grades page")
    }
    const yearSelector = doc.querySelector(YEAR_INPUT_CSS_SELECTOR)
    const curYear = Number.parseInt(yearSelector.value)
    const otherYears = [...yearSelector.options].map(el => Number.parseInt(el.value)).filter(year => year !== curYear)

    console.log(`Document year is ${curYear}, other years are ${otherYears}`)

    const promises = [Promise.resolve(doc)].concat(
        otherYears.map(async (year) => {
            const urlData = new URLSearchParams({
                "yearsafa": year
            });
            try {
                const response = await fetch(doc.ziyunim.action, {
                    method: 'POST',
                    body: urlData,

                });

                await handleErrorResponse(response)
                return await responseToDocument(response)
            }
            catch (exception) {
                warning(
                    `חלה שגיאה בעת הניסיון להשיג את המסמך של שנה ${year}`, { exception }
                )
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
 * @param {Document} doc Document to query
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
 * @param {Document} doc Document to scrape for registered courses
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
            "points": Number.parseInt(entry["נקודות זכות"][0]) || 0
        }
        if (entry["סטטיסטיקות"].length === 2) {
            engEntry.statistics_url = entry["סטטיסטיקות"][1]
            const urlParams = new URLSearchParams(engEntry.statistics_url)
            let [year, semester] = [urlParams.get("yearlimud"), urlParams.get("tkufa")]
            year = Number.parseInt(year)
            semester = Number.parseInt(semester)

            if (!year || !semester) {
                console.error(`Couldn't determine year and/or semester from statistics URL ${engEntry.statistics_url}`)
            } else {
                engEntry.semester = TKUFA_TO_SEMESTER.get(semester) ?? "FIRST"
                if (year !== docYear) {
                    console.error(`Mismatch between statistics URL year(=${year}) and doc year(=${docYear})`)
                    engEntry.year = docYear
                }
            }
        }
        entry.year = docYear
        postParsedEntry(engEntry)
        rows.push(engEntry)
    }
    return rows
}


// TODO: support annual and summer courses
const TKUFA_TO_SEMESTER = new Map([
    [1, "FIRST"],
    [2, "SECOND"]
])
/** This module is responsible for communication from the bookmarklet(injected on HUJI's website)
 *  into the front-end site(Closure) via `Window.postMessage` API
 * 
 * @module
 **/

import { ScrapeError } from "./course-scrape-errors.js"



/** @type {string} */
export const FRONTEND_ORIGIN = new URL(import.meta.env.VITE_AUTH0_REDIRECT_URI).origin


const HOOKING_TIMEOUT_MS = 3000



export const TRY_HOOK_MESSAGE_TYPE = "tryHook"
export const HOOKED_MESSAGE_TYPE = "hooked"
export const STARTED_MESSAGE_TYPE = "started"
export const GOT_COURSE_MESSAGE_TYPE = "gotCourse"
export const FINISHED_PARSING_MESSAGE_TYPE = "finishedParsing"



/**
 * This function tries to initiate communication with the front-end website that
 * (supposedly) opened this website, by recursively traversing the chain of all openers
 * and sending them a "try hook" message.
 * 
 * This is required because the process of logging into HUJI's personal information website and reaching the personal grades website may involve 
 * several pop-ups, and only one of them is the front-end.
 * Because of cross-origin security, we cannot simply invoke the `opener.origin` property, so we use a basic
 * handshaking protocol to determine which opener belongs to the front-end - this is the opener that is returned from
 * the 'install' function.
 * 
 */
function tryHookAllOpeners() {
    let opener = window.opener
    let level = 0
    while (opener) {
        level++
        try {
            console.log(`Trying to communicate with level ${level}`)
            opener.postMessage({
                type: TRY_HOOK_MESSAGE_TYPE, level
            }, FRONTEND_ORIGIN)
        } catch (e) {
            console.error(`Error while trying to post message: ${e}`)
        }
        opener = opener.opener
    }
    console.log(`Finished sending tryHook messages to ${level} windows`)
}


/**
 * @param {number} ms Timeout in miliseconds
 * @param {() => any} error Error object constructor
 * @returns {Promise<void>} A promise that rejects once the specified time passes
 */
function timeout(ms, error) {
    return new Promise((resolve, reject) => setTimeout(() => {
        reject(error())
    }, ms));
}


/** @type {?WindowProxy} */
let feOpener = null


/**
 * Installs a message handler that deals with messages from the front-end origin, 
 * and tries to hook into the front-end.
 * 
 * @returns {Promise<WindowProxy>} A promise that resolves with the window of the front-end origin
 * once hooking is successful, or rejects if no 
 */
export function install() {
    if (feOpener !== null) {
        console.warn("Already hooked into font-end, re-hooking.")
        feOpener = null
    }

    const timeoutPromise = timeout(HOOKING_TIMEOUT_MS,
        () => new ScrapeError(
            "האם הרצת את הסקריפט מהחלון הנכון, אשר נפתח דרך אתר Closure?",
            new Error(`Did not receive hook message from frontend within ${HOOKING_TIMEOUT_MS} miliseconds`)
        )
    )

    const hookedPromise = new Promise(resolve => {
        /** @type {(event: MessageEvent) => void }*/
        const messageHandler = (event) => {
            if (new URL(event.origin).origin !== FRONTEND_ORIGIN) {
                console.warn(`got a message from an unknown origin ${event.origin}, expected origin ${FRONTEND_ORIGIN}`)
                return
            }
            if (event.data?.type === HOOKED_MESSAGE_TYPE) {
                console.log(`Hooked into frontend`)
                feOpener = event.source
                resolve(event.source)
                window.removeEventListener("message", messageHandler)
            } else {
                console.error(`Got unexpected message from front-end before hooking: ${JSON.stringify(event)}`)
            }

        }
        window.addEventListener("message", messageHandler)
    })

    tryHookAllOpeners()
    return Promise.race([timeoutPromise, hookedPromise])

}


function getOpener() {
    if (!feOpener) {
        throw new Error("Frontend opener isn't defined, must wait for install() to succeed before posting messages")
    }
    return feOpener
}

export function postStarted() {
    const opener = getOpener()
    opener.postMessage({ type: STARTED_MESSAGE_TYPE }, FRONTEND_ORIGIN)
}

export function postParsedEntry(course) {
    const opener = getOpener()
    opener.postMessage({
        type: GOT_COURSE_MESSAGE_TYPE,
        course
    }, FRONTEND_ORIGIN)
}

export function postFinishedParsing() {
    const opener = getOpener()
    opener.postMessage({ type: FINISHED_PARSING_MESSAGE_TYPE }, FRONTEND_ORIGIN)
}
import { reactive, shallowReadonly} from 'vue'


const allWarnings = reactive([])

/** A critical error that may be thrown during scraping */
export class ScrapeError extends Error {
    constructor(message, cause) {
        super(message)
        this.cause = cause
        this.name = 'ScrapeError'
    }
}

/**
 * Reports a warning to console
 * @param {string} message 
 * @param  {...any} args Other arguments
 */
export function warning(message, ...args) {
    console.warn(message, ...args)
    allWarnings.push({ message, ...args})
}

export const warnings = shallowReadonly(allWarnings)
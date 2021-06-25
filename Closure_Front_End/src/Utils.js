/**
 * check if the status code of an HTTP response is 'Ok'.
 * @param statusCode - the status code of an HTTP response
 * @returns {boolean|boolean} 'true' if the status code is an 'Ok' status code. 'false' otherwise.
 */
function validateStatusCode (statusCode) {
    return statusCode >= 200 && statusCode < 400
}

/**
 * pop out an alert with generic error message. we call it when there was an error while performing an operation.
 */
function popOutStatusCodeError(){
    alert("Error occurred. Couldn't perform the operation.")
}

export default {
    validateStatusCode,
    popOutStatusCodeError
}
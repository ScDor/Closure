/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {  
  publicPath: process.env.NODE_ENV === 'production'
    ? '/closuretest.duckdns.org/'
    : '/'
}

// URL must not have a trailing slash. 
// It may be empty if the API lives in the same domain as 
// the front-end server.
process.env.VUE_APP_API_URL = process.env.NODE_ENV === 'production'
  ? 'https://closure-service-y46le24bra-ew.a.run.app/api/v1'
  : 'http://localhost:8000/api/v1'
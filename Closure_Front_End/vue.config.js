/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {  
  publicPath: process.env.NODE_ENV === 'production'
    ? '/closuretest.duckdns.org/'
    : '/'
}

process.env.VUE_APP_API_URL = process.env.NODE_ENV === 'production'
  ? 'https://closure-service-y46le24bra-ew.a.run.app/'
  : 'http://localhost:8000/'
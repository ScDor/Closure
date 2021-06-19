# Closure Project - Front End

This folder contains the web front-end of the project, using the Vue.js framework.

## Requirements


An up-to-date version of Node.js(and the npm package manager) is required in order to run this project.
The easiest way to install it would be via your operating system's package manager, as explained [here](https://nodejs.org/en/download/package-manager/).

On Windows, you can also use the "Chocolatey" package manager; a script which installs Chocolatey and then all the npm dependencies is provided, to use it,
simply run `Closure_Front_End/windows_setup.bat` as administrator.


## Project Setup


1. First, it is assumed you cloned the entire Closure project (via `git clone https://github.com/ScDor/Closure.git`) 
2. Follow the instructions for the backend at the project's root README to ensure you can run the API server.
3. Within the `Closure_Front_End` folder, download all dependencies via `npm install`
   
   (This is unnecessary if you ran the Windows install script) 


## Running in Development mode

First, you should start the backend API server(as explained in the project's README)

Now, run `npm run serve` within the `Closure_Front_End` folder. This will start a web server and automatically open the project via your browser. 
The server supports hot-reloading, that is, any change in the code would be automatically reflected in the opened website without having to refresh.

## Compiling for production

You can run `npm run build` within the `Closure_Front_End` folder to create an optimized and minified version of the code, which by default will
appear at the `dist` folder. You can then serve this folder with any web-server. For quickly previewing the production build locally, you can use Python's standard http-server module, by running:

`python -m http.server --directory dist 8080`

And then visting http://localhost:8080

## Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

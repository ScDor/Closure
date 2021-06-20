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

4. There are various settings at `Closure_Front_End/.env`, if you wish to override them, it is
   recommended you create a file `Closure_Front_End/.env.local`, which will be loaded after the `.env`.
   
   Likewise, for production, there is `Closure_Front_End/.env.production`, which is currently geared for
   cloud deployment. 
   
   <a name="localProd"></a>If you wish to create a production build but run it locally(with an API that runs locally),
   it is recommended you create a `Closure_Front_End/.env.production.local` file


### Some notes about .env

- [Read this](https://cli.vuejs.org/guide/mode-and-env.html#modes) to learn more about how .env files are loaded

- Unlike the backend, it is OK to commit .env files as they contain no secrets. However,
  you should only commit things if you change the format of the file(add/remove fields, add comments, etc),
  and not because you adapted it to your own machine, for that purpose use `.env.local` files

## Running in Development mode

First, you should start the backend API server(as explained in the project's README)

Now, run `npm run serve` within the `Closure_Front_End` folder. This will start a web server and automatically open the project via your browser. 
The server supports hot-reloading, that is, any change in the code would be automatically reflected in the opened website without having to refresh.

## Compiling for production

You can run `npm run build` within the `Closure_Front_End` folder to create an optimized and minified version of the code, which by default will
appear at the `dist` folder. 

 You can then serve this folder with any web-server. For quickly previewing the production build locally, 
 after having done the [appropriate configuration](#localProd), you can use Python's standard http-server module, by running:

`python -m http.server --directory dist 8080`

And then visting http://localhost:8080

## Customize configuration
- See [Configuration Reference](https://cli.vuejs.org/config/) on how to configure `Closure_Front_End/vue.config.js`

- See the included comments within the `.env` file

- ESLint is included, and will emit errors for various lint errors, even
  during serving. It is possible to turn them off(not recommended) or downgrade
  them into warnings by configuring it within the `package.json` file, or via
  some other ways, [as explained here](https://eslint.org/docs/user-guide/configuring/)

# vaccine-allocator-front

## Frontend

If baseURL is needed, specify the following in the package.json

```
"build": "vite build --base=/VaccineAllocator/",

```


This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).



## Install Node.js and Package Manager

Node.js: https://nodejs.org/

Yarn (Package Manager): https://yarnpkg.com/


## Project Setup

### Install packages

```sh
yarn install
```

### Compile and Hot-Reload for Development

```sh
yarn dev
```

### Compile and Minify for Production (e.g., served by Backend)

```sh
yarn build
```

## Backend

## Create a folder for logging

Create the "log" subfolder if it has not been created yet.

## Where is the web application?

By default, the "yarn build" command above will generate html, css, javascript files into the "dist"  subfolder (create one if needed). The files will then be served by the backend server.

## Install dependency

Option 1 (recommended): follow the official installation instructions: https://flask.palletsprojects.com/en/2.2.x/installation/


Optiono 2: inside the projet folder, run the following command

```
# if only Flask is not installed

pip install Flask


# if all packages (i.e., numpy, scipy, matplotlib, Flask) are not installed

# option 1
pip install numpy scipy matplotlib Flask

# option 2
pip install -r requirements.txt

```

## Run the script to serve the web app

Execute the following command and visit http://localhost:5000/

```

#  recommended
flask --app index run


# only work on Windows
flask --app index run --port=80

```

## Run it in production WSGI server

```

# on Windows, with waitress package installed

waitress-serve --host 127.0.0.1 --port 5000 index:app

```
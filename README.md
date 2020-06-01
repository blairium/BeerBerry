# pywebview-react-boilerplate
This is a  simple boilerplate to help you start with _pywebview_ and React. It sets up the development environment, install dependencies, as well as provides scripts for building an executable. Stack is based on pywebview, React, SASS, Parcel bundler, pyinstaller (Windows/Linux) and py2app (macOS).

## Requirements
- Python 3 (must be < python3.8 ie. python3.7.7)
- Node
- virtualenv

## Installation

``` bash
npm run init
```

This will create a virtual environment, install pip and Node dependencies.

## Usage

To launch the application.

``` bash
npm run start
```

To build an executable. The output binary will be produced in the `dist` directory.

``` bash
npm run build
```

To start a development server (only for testing frontend code).

``` bash
npm run dev
```
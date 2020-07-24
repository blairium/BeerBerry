import React from 'react'
import ReactDOM from 'react-dom'

import Editor from './components/Editor/Editor'
import Graph from './components/Graph/Graph'

import './index.scss'

const App = function () {
  return (
    <>
      <Editor />
      <Graph />
    </>
  )
}

const view = App('pywebview')

const element = document.getElementById('app')
ReactDOM.render(view, element)
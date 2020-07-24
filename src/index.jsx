import React from 'react'
import ReactDOM from 'react-dom'

import Editor from './components/Editor/Editor'

import './index.scss'

const App = function() {
  return (
    <>
      <Editor />
    </>
  )
}

const view = App('pywebview')

const element = document.getElementById('app')
ReactDOM.render(view, element)
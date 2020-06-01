import React from 'react'
import ReactDOM from 'react-dom'

import Editor from './components/Editor/Editor'
import Header from './components/Header/Header'
import Ticker from './components/Ticker/Ticker'

import './index.scss'

const App = function() {
  return (
    <>
      <Header/>
      <Ticker/>
      <Editor/>
    </>
  )
}

const view = App('pywebview')

const element = document.getElementById('app')
ReactDOM.render(view, element)
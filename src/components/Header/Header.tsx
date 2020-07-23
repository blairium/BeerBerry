import * as React from 'react'

import './Header.scss'
import logo from '../../assets/logo.png'


export default function Header() {
  return (
    <div className='header-container'>
      <img className='logo' src={logo} alt='pywebview'/>
      <h2>pywebview</h2>

    </div>
  );
};

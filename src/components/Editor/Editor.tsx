import * as React from 'react'

import './Editor.scss'

export default function Header() {
  const [content, updateContent] = React.useState("Load and Save Data")

  return (
    <div className='editor-container'>
      <div>
        {content}
      </div>
      <br />

      <button className='button' onClick={() => {
        async function openFile() {
          const x = await window.pywebview.api.open_file_dialog()
          updateContent(x)
        }
        openFile()

      }}>Load</button>

      <button className='button' onClick={() => {
        window.pywebview.api.save_content(content)
      }}>Save</button>
    </div>
  )
}

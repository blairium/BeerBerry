import * as React from 'react'

import './Login.scss'

const Login = () => {
    return(
        <div className="container">
            <div className="login text">
                <h4>PI-S02-Joe-Citizen</h4>
            </div>
            <div className="graph text">
                <h2>Graph</h2>
            </div>
            <div className="buttons text">
                <div className="button button1 text">
                    <div className="">Select Procedure File</div>
                </div>
                <div className="button button2 text">
                    <div className="">Start</div>    
                </div>                
            </div>
        </div>
    )
}

export default Login
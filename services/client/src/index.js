import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { BrowserRouter as Router } from "react-router-dom"
import * as serviceWorker from './serviceWorker';
import './index.css';
import "bootstrap/dist/css/bootstrap.css"
import "@fortawesome/fontawesome-free/css/all.min.css"

ReactDOM.render(<Router><App /></Router>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
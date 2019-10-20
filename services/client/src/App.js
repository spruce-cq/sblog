import React, { useState, useEffect } from 'react';
import { Route, Switch, Redirect } from "react-router-dom"
import { ToastContainer } from "react-toastify";
import Auth from "./services/authApi"
import  Articles  from "./components/Articles";
import Navbar from "./components/Navbar"
import { ArticleEditor } from "./components/ArticleEditor"
import NotFound from "./components/NotFound"
import LoginForm from './components/LoginForm';
import Logout from "./components/Logout"
import { ProtectedRoute } from "./components/common/ProtectedRoute"
import "react-toastify/dist/ReactToastify.css"
import './App.css';


function App() {

    const [user, setUser ] = useState("")

    useEffect(() => {
        const userInfo = Auth.getUserInfo()
        if (userInfo) {
            setUser(() => userInfo.sub.uid)
        }
    },[])

    return (
        <>
        <ToastContainer />
            <Navbar user={ user }/> 
            <main className="container">
                <Switch>
                    <Route path="/login" component={ LoginForm } />
                    <Route path="/logout" component={ Logout } />
                    <Route path="/article" component={ Articles } exact={ true }/>
                    <ProtectedRoute path="/article/:mode?/:id?" component={ ArticleEditor } />
                    <Route path="/not-found" component={ NotFound } />
                    <Redirect from="/" to="/article"  exact={ true } />
                    <Redirect to="/not-found" />
                </Switch>
            </main>
        </>
    );
}

export default App;

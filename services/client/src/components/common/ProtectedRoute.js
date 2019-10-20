import React from "react"
import { Route, Redirect } from "react-router-dom"
import Auth from "../../services/authApi"


export const ProtectedRoute = (props) => {
    const { path, render, component: Cmp, ...rest } = props

    return (
        <Route path={ path } { ...rest } render={ routeProps => {
            if (!Auth.getUserInfo()) return <Redirect to={{
                pathname: "/login",
                state: { from: props.location }
            }} />
            return Cmp ? <Cmp  { ...routeProps } /> : render(routeProps)
        } } />
    )
}
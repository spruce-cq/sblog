import React, {useEffect, useState} from "react";
import { Link } from "react-router-dom"

import { getUserStatus } from "../services/authApi"

export default function Navbar(props) {
    const [user, setUser] = useState({})

    useEffect(() => {
        const getUser = async () => {
            const {data: user} = await getUserStatus()
            setUser(user)
        }
        getUser()
    }, [])

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <Link className="navbar-brand" to="/">
                Blog
            </Link>
            <div className="navbar-nav">
                { user && <>
                    <Link className="nav-item nav-link" to="#">{user.username}</Link>
                    <Link className="nav-item nav-link" to="/logout">Logout</Link>
                    </>
                }
                { !user &&  <Link className="nav-item nav-link" to="/login">Login</Link>}
            </div>
            <div>
            </div>
        </nav>
    );
}

import React, { useEffect} from "react"

const Logout = (props) => {

    useEffect(() => {
        localStorage.removeItem("token")
        window.location = "/"
    },[])

    return null
}

export default Logout
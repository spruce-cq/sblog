import Axios from "axios"
import { toast } from "react-toastify"
import logger from "./logService"



Axios.interceptors.response.use(null, err => {
    const expectedError = err.response && err.response.status >= 400 && err.response.status < 500
    if (!expectedError) {
        logger.log("Logging the error", err)
        toast("An unexcepted error occurred")
    }
    return Promise.reject(err)
})

const withAuth = (jwt) => {
    const AUTH_TOKEN = `Bearer ${jwt}`
    Axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
}

export default { 
    get: Axios.get,
    post: Axios.post,
    put: Axios.put,
    delete: Axios.delete,
    withAuth,
}
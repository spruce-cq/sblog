import { toast } from "react-toastify"
import jwtDecode from "jwt-decode"
import Http from "./httpService"
import Config from "../config"
import Logger from "./logService"

Http.withAuth(getJwt())

export const login = async (info) => {
    try {
        const { data } = await Http.post(
            `${Config.resource}/auth/login`,
            info)
        localStorage.setItem("token", data.auth_token)
    } catch(ex) {
        if (ex.response.status === 401)
            toast(ex.response.data.message, { position: toast.POSITION.TOP_CENTER})
        else 
            Logger.log(ex)
    }
}

export const getUserStatus = async (uid) => {
    let user = {}
    try {
        user = (await Http.get(`${Config.resource}/auth/status`)).data
    } catch(ex) {}
    return user
}

function getJwt() {
    return localStorage.getItem("token")
}

function getUserInfo() {
    try{
        const userInfo = jwtDecode(getJwt())
        return userInfo
    }catch(ex) {}
}
export default  {
    login,
    getJwt,
    getUserInfo,
}
import Http from "./httpService"
import Config from "../config"


export function getCategories() {
    return Http.get(`${Config.resource}/categories`)
}
import Http from "./httpService"
import Config from "../config"

const ARTICLE_URL = `${Config.resource}/articles`

export function getArticles() {
    return Http.get(ARTICLE_URL)
}

export function getArticleById(id) {
    return Http.get(`${ARTICLE_URL}/${id}`)
}

export function saveArticle(article) {
    const { id, ...body } = article
    if (id) {
        // put
        return Http.put(ARTICLE_URL, {...body, aid: id})
    }
    return Http.post(ARTICLE_URL, body)
}

export function deleteArticle(id) {
        return Http.delete(`${ARTICLE_URL}/${id}`)
}
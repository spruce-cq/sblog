let articles = [
    {
        "id": 1,
        "title": "Qui est nesciunt minus tempora.",
        "content": "Porro quibusdam quos aut adipisci nulla quam harum distinctio est. Delectus eum eligendi suscipit. Inventore eum expedita asperiores id quis. Et aliquam optio unde similique porro dolore tenetur.",
        "status": false,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 1,
        "category": "cate1"
    },
    {
        "id": 2,
        "title": "Velit rerum sunt praesentium voluptatem.",
        "content": "Blanditiis rem voluptas libero ipsa odit. Perspiciatis debitis cupiditate tempore molestiae adipisci. Molestiae repellat saepe similique harum neque tenetur ratione ducimus ipsa. Praesentium doloribus itaque non libero quis dolore quidem sapiente sit. Quasi dolorem eligendi facilis quo quia.",
        "status": false,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 2,
        "category": "cate2"
    },
    {
        "id": 3,
        "title": "Tempora neque quo tempore ut.",
        "content": "Quos eos occaecati omnis est nesciunt nostrum. Ut id est rerum ab omnis velit tempore quam.",
        "status": true,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 3,
        "category": "cate3"
    },
    {
        "id": 4,
        "title": "Earum minima sed aliquam enim.",
        "content": "Nam non qui aperiam saepe ratione sit consequatur quia. Maiores sint commodi voluptas facere fugiat sapiente. Corporis velit molestiae consectetur perspiciatis consequatur voluptas omnis. Iure id doloribus laboriosam eum qui asperiores sed numquam voluptatibus.",
        "status": true,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 1,
        "category": "cate1"
    },
    {
        "id": 5,
        "title": "Fugit quos deserunt qui est.",
        "content": "Vitae voluptas consequatur dolores neque aut totam. Aperiam accusantium repudiandae assumenda perferendis cupiditate animi numquam qui. Et qui deserunt. Commodi culpa quis nihil exercitationem quae. Repellat mollitia saepe est ullam minus aliquam.",
        "status": true,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 2,
        "category": "cate2"
    },
    {
        "id": 6,
        "title": "Veritatis eius quod alias recusandae.",
        "content": "Ut corrupti expedita quibusdam. Modi est sequi. Odio omnis nihil earum ut.",
        "status": true,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 3,
        "category": "cate3"
    },
    {
        "id": 7,
        "title": "Sunt illo voluptatem veniam aspernatur.",
        "content": "Temporibus beatae consequatur exercitationem. Velit omnis quo blanditiis possimus cumque voluptatem porro amet.",
        "status": true,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 1,
        "category": "cate1"
    },
    {
        "id": 8,
        "title": "Et consequatur commodi id laboriosam.",
        "content": "Ut perferendis qui saepe at magni. Deleniti enim ipsam sapiente reprehenderit vero quia vitae vel. Consectetur labore repellat. Expedita impedit maxime earum deserunt impedit. Veniam magnam quia quasi recusandae ea occaecati sed.",
        "status": true,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 2,
        "category": "cate2"
    },
    {
        "id": 9,
        "title": "Dicta facilis repudiandae iure enim.",
        "content": "Nobis aliquid aut placeat ratione vitae minus. Amet aspernatur laudantium quas ex molestiae ullam ex. Nihil modi aut commodi eveniet. Et sed et quibusdam voluptas rem odit quaerat eaque. Est dolorum iste doloribus.",
        "status": true,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 3,
        "category": "cate3"
    },
    {
        "id": 10,
        "title": "Nobis a tempore molestias accusantium.",
        "content": "Consectetur rem at id magni quibusdam perspiciatis. Et voluptatem aliquid voluptatem consequuntur atque sint. Dolores voluptas unde odio et.",
        "status": false,
        "create_at": "2019-08-18T06:51:17.000Z",
        "category_id": 1,
        "category": "cate1"
    }
]
const id = 100
export function getArticles() {
    return articles
}

export function getArtcileById(id) {
    const articles = getArticles()
    const article = articles.find(a => a.id === Number(id))
    return article
}

export function saveArticle(article) {
    const articleId = Number(article.id)
    const category = getGenres().find(g => g.id === Number(article.genreId))

    if (articleId === "") {
        article.id = id + 1
        article.create_at = new Date().toString()
        article.category = category.name
        article.category_id = category.id

        articles = articles.concat([article])
        return
    }
    article.category_id = category.id
    article.category = category.name
   let newArticles =  articles.map(a => a.id === articleId ? {...a, ...article} : a)
    articles = newArticles
}


export function formatDate(dateStr) {
    const date = new Date(dateStr)
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
} 

export function transboolean(boolean) {
    return boolean ? "Yes" : "No"
}

export function getGenres() {
    return [
        {
            "id": 1,
            "name": "cate1",
            "articles_id": [
                1,
                4,
                7,
                10
            ]
        },
        {
            "id": 2,
            "name": "cate2",
            "articles_id": [
                2,
                5,
                8
            ]
        },
        {
            "id": 3,
            "name": "cate3",
            "articles_id": [
                3,
                6,
                9
            ]
        }
    ]
}
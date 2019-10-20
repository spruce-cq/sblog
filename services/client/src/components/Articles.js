import React, { Component } from "react"
import _ from "lodash"
import { toast } from "react-toastify"
import { getArticles } from "../services/articleApi";
import { getCategories } from "../services/categoryApi"
import Pagination  from "./common/Pagination";
import ListGroup from "./common/ListGroup"
import ArticleTable from "./ArticleTable";
import { paginate } from "../utils"
import { deleteArticle } from "../services/articleApi"



class Articles extends Component {
    state = {
        articles: [],
        categories: [],
        pageSize: 3,
        currentPage: 1,
        selectedCategoryId: -1 ,
        searchQueryString: "",
        sortColumn: { path: "create_at", order: "desc" }
    }

    async componentDidMount() {
        let { data: {data: categories} } = await getCategories()
        const { data: {data: articles} }= await getArticles()
        categories = [{ id: -1, name: "All Categories"}, ...categories ]
        this.setState({ articles, categories})
    }

    handleDelete = async (article) => {
        const articles  = this.state.articles
        const newArticles = this.state.articles.filter(a => a.id !== article.id)
        this.setState({ articles: newArticles})
        try {
            await deleteArticle(article.id)
        } catch(err) {
            toast("sorry, something failed in deleting article!")
            this.setState({ articles })
        }
    }

    handleCategorySelected = (category) => {
        if(this.state.searchQueryString) return
        this.setState({ selectedCategoryId: category.id, currentPage: 1 })
    }

    handlePageChange = page => {
        this.setState({ currentPage: page})
    }

    handleSort = (sortColumn) => {
        this.setState({ sortColumn: sortColumn})
    }

    handleSearchChange = (inputValue) => {
        this.setState({ searchQueryString: inputValue, selectedCategoryId: -1})
    }

    filterArtilces = () => {
        const { currentPage, pageSize, articles: allArticles, selectedCategoryId, sortColumn, searchQueryString } = this.state 
        
        let filteredArticles = allArticles
        if (searchQueryString) {
            filteredArticles = allArticles.filter(a => a.title.toLowerCase().includes(searchQueryString))
        }else if (selectedCategoryId !== -1) {
            filteredArticles = allArticles.filter(a => a.category[0] === selectedCategoryId) 
        }
        
        filteredArticles = _.orderBy(filteredArticles, [sortColumn.path], [sortColumn.order])

        const articles = paginate(filteredArticles, pageSize, currentPage)
        return { totalCount: filteredArticles.length, articles}
    }

    render() {
        const { sortColumn, pageSize, currentPage } = this.state

        if (this.state.articles.length === 0)
            return <p>There are no movies in the database.</p>
        const { totalCount, articles } = this.filterArtilces()
        
        return (
            <div className="row">
                <div className="col-2">
                    <ListGroup items={ this.state.categories } onSelected={ this.handleCategorySelected }
                        selectedItemId={ this.state.selectedCategoryId }/>
                </div>
                <div className="col">
                    <ArticleTable  
                        itemsCount={ totalCount }
                        articles={ articles } 
                        onDelete={ this.handleDelete }
                        sortColumn={ sortColumn } 
                        onSort={ this.handleSort }
                        onChange={ this.handleSearchChange } />
                    <Pagination 
                        itemsCount={ totalCount }
                        pageSize={ pageSize }
                        currentPage={ currentPage }
                        handlePageChange={ this.handlePageChange }/>
                </div>
                
            </ div>
        )
    }
}



 export default Articles
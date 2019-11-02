import React from "react"
import {  Link } from "react-router-dom";
import { formatDate, transboolean } from "./fakerService";
import Table from "./common/Table"
import Auth from "../services/authApi"


export default  function ArticleTable(props) {

    const columns = [
        { path: "title", label: "Title", content: (article) => <Link to={`/article/edit/${article.id}`}>{ article.title }</Link>},
        { path: "category[1]", label: "Category"},
        { path: "timestamp", label: "Pubdate", wrapFunc: formatDate },
        { path: "status", label: "Status", wrapFunc: transboolean },
    ]

    const deleteColumn = { key: "delete", content: (article) => 
        <button className="btn btn-danger btn-sm" onClick={() => props.onDelete(article)}>Delete</button>}

    const userInfo = Auth.getUserInfo()
    if (userInfo && userInfo.sub.admin)
        columns.push(deleteColumn)
    
    
    return (
        <>
            {userInfo.sub.uid && <Link to="/article/create" className="btn btn-primary mb-2">New Article</Link>}
            <p>Showing { props.itemsCount } in the database.</p>
            <input className="form-control my-3" placeholder="Search..." onChange={ (e) => props.onChange(e.currentTarget.value) } />
            <Table columns={ columns } articles={ props.articles } sortColumn={ props.sortColumn } onSort={ props.onSort } />
        </>
    )
}

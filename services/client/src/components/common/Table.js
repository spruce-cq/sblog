import React from "react"
import TableHeader from "./TableHeader"
import TableBody from "./TableBody"

export default function Table({ columns, articles, sortColumn, onSort }) {

    return (
        <table className="table">
            <TableHeader columns={ columns } sortColumn={ sortColumn } onSort={ onSort } />
            <TableBody items={ articles } columns={ columns }/>
        </table>
    )
}
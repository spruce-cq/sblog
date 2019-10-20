import React, { useCallback } from "react"

export default function TableHeader({ columns, sortColumn, onSort } ){

    const setSort = useCallback((path) => {
        const newSortColumn = { ...sortColumn}
        if (path === newSortColumn.path) {
            newSortColumn.order =  newSortColumn.order === "asc"  ? "desc" : "asc"
        } else {
            newSortColumn.path = path
            newSortColumn.order = "asc"
        }
        onSort(newSortColumn)
    }, [sortColumn, onSort])

    const renderSortIcon = useCallback((column) => {
        if (column.path !== sortColumn.path) return null
        if (sortColumn.order === "asc") return <i className="fas fa-sort-up"></i>
        return <i className="fas fa-sort-down"></i>
    }, [sortColumn])

    return (
        <thead>
                            <tr>
                                {columns.map(c => (
                                    <th key={ c.path || c.key } onClick={() => setSort(c.path)} >{ c.label } { renderSortIcon(c) }</th>
                                ))}
                            </tr>
        </thead>
    )
}
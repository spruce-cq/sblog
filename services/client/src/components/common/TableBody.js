import React, { useCallback }from "react"
import _ from "lodash"


export default function TableBody({ items, columns}) {
    const renderCell = useCallback((item, column) => {
        if (column.content) return column.content(item)
        if (column.wrapFunc) return column.wrapFunc(_.get(item, column.path))
        return _.get(item, column.path)
    },[])

    return (
        <tbody>
        {
            items.map(item => (
                <tr key={ item.id }>
                    {columns.map( c => (
                        <td key={ c.path || c.key }>{ renderCell(item, c)}</td>
                    ))}
                </tr>
            ))
        }
        </tbody>
    )
}
import React from "react"

const ListGroup = (props) => {
    const { items, uniqueProperty, textProperty, selectedItemId, onSelected } = props

    return (
        <ul className="list-group">
            {items.map(i => (
                <li className={`list-group-item ${ i[uniqueProperty] === selectedItemId ? "active" : ""}`} key={ i[uniqueProperty] }
                    onClick={ () => onSelected(i) }>{ i[textProperty] }</li>
            ))}
        </ul>
    )
}

ListGroup.defaultProps = {
    uniqueProperty:"id",
    textProperty: "name"
}

export default ListGroup
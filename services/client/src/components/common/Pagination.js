import React from "react"
import _ from "lodash";
import PropTypes from "prop-types";


const Pagination = props => {
    const { itemsCount, pageSize, currentPage } = props

    const pageCount = Math.ceil(itemsCount / pageSize)
    if (pageCount === 1) return null
    const pages = _.range(1, pageCount + 1)
    return (
        <nav >
            <ul className="pagination">
                { pages.map(page => (
                    <li key={ page } className={ `page-item ${ currentPage === page ? "active": ""}`}>
                        <a  className="page-link" onClick={ () => props.handlePageChange(page) }>{ page }</a>
                    </li>
                ))}    
            </ul>
        </nav>
    )
}

Pagination.propTypes = {
    itemsCount: PropTypes.number.isRequired,
    pageSize: PropTypes.number.isRequired,
    currentPage: PropTypes.number.isRequired,
    handlePageChange: PropTypes.func.isRequired
}

export default Pagination
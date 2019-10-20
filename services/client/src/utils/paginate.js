import _ from "lodash"

export function paginate(items, pageSize, currentPage) {
    const startIndex = Math.floor((currentPage - 1) * pageSize)
    const result = _(items).slice(startIndex).take(pageSize).value()
    return result
}
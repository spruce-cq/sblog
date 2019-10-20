import validator from "validator";

export const validateArticleEditor = (data) => {
    let errors = []
    if (validator.isEmpty(data.content.trim()))
        errors.push("Content required")
    return errors
}
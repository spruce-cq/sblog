import validator from "validator";

export function validateData(data, rules) {
    let errors = {};
    Object.keys(data).forEach(field => {
        if (rules.hasOwnProperty(field)) {
            let fielderrors = [];
            let val = data[field];
            if (rules[field].required && validator.isEmpty(val.trim())) {
                fielderrors.push("Value required");
            }
            if (!validator.isEmpty(data[field].trim())) {
                if (rules[field].minlength
                        && !validator.isLength(val, rules[field].minlength)) {
                    fielderrors.push(`Enter at least ${rules[field].minlength}`
                        + " characters");
                }
                if (rules[field].alpha && !validator.isAlpha(val)) {
                    fielderrors.push("Enter only letters");
                }
                if (rules[field].email && !validator.isEmail(val)) {
                    fielderrors.push("Enter a valid email address");
                }
            }
            if (fielderrors.length > 0) {
                errors[field] = fielderrors;
            }
        }
    })
    return errors;
}

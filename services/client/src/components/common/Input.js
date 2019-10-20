import React from "react"
import { ValidationMessage } from "./ValidationMessage";


export default function Input({name, value, onChange, label, ...rest }) {
    const type = rest.type ? rest.type : "text"

    return (
        <div className="form-group">
            <label htmlFor={name}>{ label }</label>
            <input type={ type } className="form-control" id={name}
                    value={ value } onChange={ onChange } name={ name } />
            <ValidationMessage field={ name } />
        </div>
    )
}
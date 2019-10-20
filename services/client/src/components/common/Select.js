import React from "react"
import { ValidationMessage } from "./ValidationMessage";


export default function Select({name, value, onChange, label, options }) {
    return (
        <div className="form-group">
                <label htmlFor={ name }>{ label }</label>
                <select  className="form-control" id={ name }
                    value={ value } onChange={ onChange } name={ name } >
                    <option value={ 0 }></option>
                    { options.map(op => <option key={ op.id } value={ op.id }>{ op.name }</option> )}
                </select>
            <ValidationMessage field={ name } />
        </div>
    )
}
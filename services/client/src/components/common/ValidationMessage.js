import React, { Component } from "react";
import { ValidationContext } from "../../ValidationContext";

export class ValidationMessage extends Component {
    static contextType = ValidationContext;

    render() {
        return this.context.getMessagesForField(this.props.field).map(err =>
            <small className=" form-text text-muted mt-1 p-1" style={{ "color": "#c04851"}}
                    key={ err } >
                { err }
            </small>
        )
    }
}
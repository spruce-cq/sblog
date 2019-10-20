import React, { Component } from "react";
import { validateData } from "../../validation";
import { ValidationContext } from "../../ValidationContext";

export class FormValidator extends Component {
    constructor(props) {
        super(props);
        this.state = {
            errors: {},
            dirty: {},
            formSubmitted: false,
            getMessagesForField: this.getMessagesForField
        }
    }

    static getDerivedStateFromProps(props, state) {
        // 单个表单验证
        state.errors = validateData(props.data, props.rules)
        // 全表验证
        if (props.validateForm) {
            if (state.formSubmitted && Object.keys(state.errors).length === 0) {
                let formErrors = props.validateForm(props.data)
                if (formErrors.length > 0)
                    state.errors.form = formErrors
            }
        }

        return state
    }

    get formValid() {
        return Object.keys(this.state.errors).length === 0;
    }

    handleChange = (ev) => {
        let name = ev.target.name;
        this.setState(state => state.dirty[name] = true);
    }
    
    handleClick = (ev) => {
        this.setState({ formSubmitted: true }, () => {
            if (this.formValid) {
                
                if (this.props.validateForm) {
                    let formErrors = this.props.validateForm(this.props.data)
                    if (formErrors.length === 0)
                        this.props.submit(this.props.data)
                        return 
                }
                this.props.submit(this.props.data)
            }
        });
    }
    getButtonClasses() {
        return this.state.formSubmitted && !this.formValid
            ? "btn-danger" : "btn-primary";
    }

    getMessagesForField = (field) => {
        return (this.state.formSubmitted || this.state.dirty[field]) ?
            this.state.errors[field] || [] : []
    }
    render() {
        return <React.Fragment>
            <ValidationContext.Provider value={ this.state }>
                <div onChange={ this.handleChange }>
                    { this.props.children }
                </div>
            </ValidationContext.Provider>
            <div className={ this.props.btnClasses }>
                <button className={ `btn ${ this.getButtonClasses() }`}
                        onClick={ this.handleClick }
                        disabled={ this.state.formSubmitted && !this.formValid } >
                    { this.props.btnLabel }
                </button>
                { this.props.cancelbtn && this.props.cancelbtn() }
            </div>
        </React.Fragment>
    }
}
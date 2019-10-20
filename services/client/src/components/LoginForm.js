import React, { useState, useCallback } from "react"
import Input from "./common/Input"
import { FormValidator } from "./common/FormValidator";
import Auth from "../services/authApi"

export default function LoginForm(props) {

    const [account, setAccount] = useState({email: "", password: ""})

    const rules = {
        email: { required: true, email: true },
        password: { required: true, minlength: 5 }
    }
    
    const submit = useCallback( async (userInfo) => {
        // call backend server -- authorizeation
        await Auth.login(userInfo)
        const { state } = props.location
        const to = state ? `${ state.from.pathname}${state.from.search}` : "/" 
        window.location = to
    }, [props.location])
    
    const handleChange = useCallback(e => {
        const {name, value} = e.currentTarget
        setAccount(account  => ({...account, [name]: value }))
    }, [])

    return (
        <div className="d-flex flex-column ">
            <FormValidator data={ account } rules={ rules } submit={ submit } btnLabel="Submit">
                <h1>Login</h1>
                <form>
                    <Input name="email" label="Email" value={ account.username } onChange={ handleChange } />
                    <Input name="password" label="Password" type="password" value={ account.password } onChange={ handleChange } />
                </form>
            </FormValidator>
        </div>
    )
}
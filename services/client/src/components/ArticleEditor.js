import React from "react"
import { Editor } from "./common/Editor";
import Input from "./common/Input"
import Select from "./common/Select";
import { FormValidator } from "./common/FormValidator";
import { ValidationMessage } from "./common/ValidationMessage";
import { getCategories } from "../services/categoryApi";
import { getArticleById, saveArticle } from "../services/articleApi"



export  class  ArticleEditor extends React.Component {

    constructor(props) {
        super(props)
        this.state= {
            article: { id: "", title: "", category: 0, body: "", status: false },
            categories: []
        }
        this.rules = {
            title: { required: true }
        }
    }

    mapModelToView(object) {
        return {
            title: object.title,
            category: object.category[0],
            body: object.body,
            status: object.status
        }
    }
    
    async setCategory() {

        const { data: {data: categories}} =  await getCategories()
        this.setState({ categories })
    }

    async redirectOrSetArticle() {
        const mode = this.props.match.params.mode
        const articleId = this.props.match.params.id

        if (mode === "create" ){
            if (articleId) return this.props.history.replace("/not-found")
            return 
        }    
        if (mode !== "edit" || !articleId ) return this.props.history.replace("/not-found")        

        let article
        try {
            article = (await getArticleById(articleId)).data.data
        } catch(ex) {
            if ( ex.response && ex.response.status === 404) return this.props.history.replace("/not-found")
        }
        this.setState({article: {...this.mapModelToView(article), id: articleId}})
    }

    async componentDidMount() {
        await this.setCategory()
        await this.redirectOrSetArticle()
    }

    handleChange = (e) => {
        const {name, value} = e.currentTarget
        this.setState(state => state.article[name] = value)
    }

    editingCallback = (html) => {
        this.setState(state => state.article.body = html)
    }

    submit = async (data) => {
        await saveArticle(data)
        this.props.history.push("/article")
    }

    renderCancelBtn = () => {
        return <button onClick={() => this.props.history.push("/article")} className="btn btn-warning ml-2">Cancel</button>
    }

    render() {
        return (
            <>
                <FormValidator data={ this.state.article } rules={ this.rules } cancelbtn={ this.renderCancelBtn }
                    btnLabel="save" btnClasses="text-center mt-2" submit={ this.submit }>   
                    <ValidationMessage field="form" />  
                    <h2>Article Form</h2>   
                    <form>  
                        <Input name="title" label="Title" onChange={ this.handleChange } value={ this.state.article.title }/>
                        <Select name="category" label="Category"
                            onChange={ this.handleChange } value={ this.state.article.category } options={ this.state.categories }/>
                    </form> 
                    <Editor editingCallback={ this.editingCallback } body={this.state.article.body } />
                </  FormValidator>
            </>
        )
    }

 }

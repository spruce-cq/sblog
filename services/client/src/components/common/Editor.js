import React from "react"
import E from "wangeditor"


export class Editor extends React.PureComponent {

    constructor(props) {
        super(props)
        this.editorRef = React.createRef()
        console.log(props.body)
    }

    componentDidMount() {
        const editor = new E(this.editorRef.current)
        editor.customConfig.onchange = (html) => { 
            this.props.editingCallback(html)
        }
        editor.create()
        this.editorRef.current.editor = editor
        editor.txt.html(this.props.body)
        this.editorRef.current.childNodes[1].style.height = "350px"
    }

    componentDidUpdate() {
        const editorDom = this.editorRef.current.editor.$textElem[0]
        console.log(editorDom)
        const contentDom = editorDom.childNodes
        if (contentDom.length === 1 && contentDom[0].innerHTML.startsWith("<br"))
            this.editorRef.current.editor.txt.html(this.props.body)
    }


    render() {
        return <div ref={ this.editorRef } className="editor-text"></div>
    }
}
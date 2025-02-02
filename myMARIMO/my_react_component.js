import React from 'react';
import ReactDOM from 'react-dom';

class MyReactComponent extends HTMLElement {
    connectedCallback() {
        ReactDOM.render(
            <div>Hello, Marimo!</div>,
            this
        );
    }
}

customElements.define('my-react-component', MyReactComponent);

import React from 'react';
import ReactDOM from 'react-dom';
import Router from './router';
//import { BrowserRouter } from "react-router-dom";

const render = () => {
  ReactDOM.render(
    <Router />,
    document.querySelector('#root')
  );
}

render();

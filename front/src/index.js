import React from 'react';
import ReactDOM from 'react-dom';
import AddFlowerPage from './pages/AddFlower'

const render = (context) => {
  ReactDOM.render(
    <AddFlowerPage context={context} />,
    document.querySelector('#root')
  );
}

const renderError = () => {
  ReactDOM.render(
    <div>
      Some error occurred - please refresh
    </div>,
    document.querySelector('#root')
  )
}

window.extAsyncInit = function () {
  console.log('messenger installed');
  // the Messenger Extensions JS SDK is done loading
  console.log('window env', window.env)
  window.MessengerExtensions.getContext(window.env.APP_ID, (context) => {
    console.log('context', context);
    render(context)
  }, (error) => {
    console.error('Error getting context: ', error)
    renderError();
  })
  ;
};

(function (d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) {
    return;
  }
  js = d.createElement(s);
  js.id = id;
  js.src = "//connect.facebook.net/en_US/messenger.Extensions.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'Messenger'));

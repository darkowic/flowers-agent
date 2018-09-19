import React from 'react';
//import { Switch, Route } from "react-router-dom";

import AddFlowerPage from './pages/AddFlower'


//{/*<Switch>*/}
//  {/*<Route exact path="/add-flower/" component={AddFlowerPage} />*/}
//  {/*<Route component={NotFoundPage} />*/}
//{/*</Switch>*/}

class Router extends React.Component {
  render(props) {
    return (
      <AddFlowerPage />
    )
  }
}

export default Router

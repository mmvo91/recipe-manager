import React from 'react';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import './scss/App.scss';

import Navigation from "./components/Navigation";
import Recipes from "./pages/Recipes";

function App() {
    return (
        <Router>
            <Navigation/>
            <Switch>
                <Route exact path="/" component={Recipes}/>
                <Route exact path="/recipes" component={Recipes}/>
            </Switch>
        </Router>
    );
}

export default App;

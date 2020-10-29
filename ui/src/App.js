import React from 'react';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import './scss/App.scss';

import Navigation from "./components/Navigation";
import Recipes from "./pages/Recipes";
import Recipe from "./pages/Recipe";

function App() {
    return (
        <Router>
            <Navigation/>
            <Switch>
                <Route exact path="/" component={Recipes}/>
                <Route exact path="/recipes" component={Recipes}/>
                <Route exact path="/recipes/:id" component={Recipe}/>
            </Switch>
        </Router>
    );
}

export default App;

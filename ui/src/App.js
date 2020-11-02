import React from 'react';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import './scss/App.scss';
import {library} from '@fortawesome/fontawesome-svg-core';
import {faEdit, faPlus, faTrash} from '@fortawesome/free-solid-svg-icons';

import Navigation from "./components/Navigation";
import Recipes from "./pages/Recipes";
import Recipe from "./pages/Recipe";
import Imports from "./pages/Imports";

library.add(faTrash, faPlus, faEdit)

function App() {
    return (
        <Router>
            <Navigation/>
            <Switch>
                <Route exact path="/" component={Recipes}/>
                <Route exact path="/recipes" component={Recipes}/>
                <Route exact path="/recipes/:id" component={Recipe}/>
                <Route exact path="/import" component={Imports}/>
            </Switch>
        </Router>
    );
}

export default App;

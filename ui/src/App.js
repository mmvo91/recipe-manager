import React from 'react';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import './scss/App.scss';
import {library} from '@fortawesome/fontawesome-svg-core';
import {faEdit, faPlus, faTrash} from '@fortawesome/free-solid-svg-icons';

import PrivateRoute from "./components/PrivateRoute";
import Navigation from "./components/Navigation";
import Login from "./pages/Login";
import Recipes from "./pages/Recipes";
import Recipe from "./pages/Recipe";
import NewRecipe from "./pages/NewRecipe";
import Planner from "./pages/Planner";
import Imports from "./pages/Imports";
import ImportedRecipe from "./pages/ImportedRecipe";

library.add(faTrash, faPlus, faEdit)

function App() {
    return (
        <Router>
            <Navigation/>
            <Switch>
                <Route exact path="/login" component={Login}/>
                <PrivateRoute exact path="/" component={Recipes}/>
                <PrivateRoute exact path="/recipes" component={Recipes}/>
                <PrivateRoute exact path="/recipes/new" component={NewRecipe}/>
                <PrivateRoute exact path="/recipes/:id" component={Recipe}/>
                <PrivateRoute exact path="/planner" component={Planner}/>
                <PrivateRoute exact path="/import" component={Imports}/>
                <PrivateRoute exact path="/import/:id" component={ImportedRecipe}/>
            </Switch>
        </Router>
    );
}

export default App;

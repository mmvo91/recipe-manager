import React, {useEffect, useState} from "react";
import Container from "react-bootstrap/Container"
import Row from "react-bootstrap/Row";

import api from "../Api"
import RecipeCard from "../components/RecipeCard";

const Recipes = () => {
    const [recipes, updateRecipes] = useState([]);

    useEffect(() => {
        api.get('/recipes')
            .then(res => {
                updateRecipes(res.data)
            })
    }, []);

    return (
        <Container className="py-3">
            <Row>
                {
                    recipes.map(
                        recipe => (
                            <RecipeCard
                                key={recipe.id}
                                recipe={recipe}
                                location='/recipes/'
                            />
                        )
                    )
                }
            </Row>
        </Container>
    )
};

export default Recipes
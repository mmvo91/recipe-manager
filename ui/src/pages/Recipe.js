import React, {useState, useEffect} from "react";
import Container from "react-bootstrap/Container"
import Card from "react-bootstrap/Card"
import Image from "react-bootstrap/Image";

import api from "../Api"
import Ingredients from "../components/Ingredients";
import Instructions from "../components/Instructions";

const Recipe = (props) => {
    const [recipe, updateRecipe] = useState({})

    useEffect(() => {
        api.get('/recipes/' + props.match.params.id)
            .then(res => {
                updateRecipe(res.data)
            })
    }, [props.match.params.id]);

    return (
        <Container className="py-3">
            <Card>
                <Card.Body>
                    <div>
                        <h2>{recipe.title}</h2>
                        <h5>{recipe.description}</h5>
                        <h6>{recipe.author}</h6>
                    </div>
                    <Image className="recipe-image py-3" fluid src={recipe.image}/>
                    <Ingredients ingredients={recipe.ingredients}/>
                    <Instructions instructions={recipe.instructions}/>
                </Card.Body>
            </Card>
        </Container>
    )
}

export default Recipe
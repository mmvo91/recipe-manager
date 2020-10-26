import React from "react"
import Col from "react-bootstrap/Col";
import {LinkContainer} from "react-router-bootstrap";
import Card from "react-bootstrap/Card";
import Image from "react-bootstrap/Image";

const RecipeCard = props => {
    let recipe = props.recipe;
    let location = props.location;
    return (
        <Col>
            <LinkContainer className="clickable" to={location + recipe.id}>
                <Card>
                    <Card.Body>
                        <Card.Title>
                            {recipe.title}
                        </Card.Title>
                        <Card.Subtitle>
                            {recipe.author}
                        </Card.Subtitle>
                        <Image fluid src={recipe.image}/>
                    </Card.Body>
                </Card>
            </LinkContainer>
        </Col>
    )
};

export default RecipeCard
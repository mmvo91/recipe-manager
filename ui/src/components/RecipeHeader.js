import React from 'react'
import Form from "react-bootstrap/Form";

const RecipeHeader = props => {
    return (
        <div>
            <h5>Recipe</h5>
            <Form.Group>
                <Form.Label>
                    Title
                </Form.Label>
                <Form.Control
                    id='title'
                    name='Title'
                    type="text"
                    value={props.title}
                    onChange={props.setRecipeHeader}
                    placeholder="Title..."/>
            </Form.Group>
            <Form.Group>
                <Form.Label>
                    Description
                </Form.Label>
                <Form.Control
                    id='recipe_description'
                    name='Description'
                    type="text"
                    value={props.description}
                    onChange={props.setRecipeHeader}
                    placeholder="Description..."/>
            </Form.Group>
            <Form.Group>
                <Form.Label>
                    Author
                </Form.Label>
                <Form.Control
                    id='author'
                    name='Author'
                    type="text"
                    value={props.author}
                    onChange={props.setRecipeHeader}
                    placeholder="Author..."/>
            </Form.Group>
            <Form.Group>
                <Form.Label>
                    Source
                </Form.Label>
                <Form.Control
                    id='source'
                    name='Source'
                    type="text"
                    value={props.source}
                    onChange={props.setRecipeHeader}
                    placeholder="Source..."/>
            </Form.Group>
            <Form.Group>
                <Form.Label>
                    Servings
                </Form.Label>
                <Form.Control
                    id='servings'
                    name='Servings'
                    type="number"
                    value={props.servings}
                    onChange={props.setRecipeHeader}
                    placeholder="Servings..."/>
            </Form.Group>
        </div>
    )
};

export default RecipeHeader
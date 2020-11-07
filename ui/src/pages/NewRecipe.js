import React, {useState, useEffect} from "react";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import api from "../Api";
import RecipeHeader from "../components/RecipeHeader";
import IngredientRow from "../components/IngredientRow";
import InstructionRow from "../components/InstructionRow";

const NewRecipe = props => {
    const ingredient = {
        ingredient: "",
        amount: 0,
        unit: "",
        state: "",
    };

    const instruction = {
        step: 1,
        instruction: ""
    };

    const [recipe, updateRecipe] = useState({ingredients: [ingredient], instructions: [instruction]})
    const [message, updateMessage] = useState(null)

    useEffect(() => {
        api.get('/imports/' + props.match.params.id)
            .then(res => updateRecipe(res.data))
    }, [])

    const setIngredients = (ingredients) => {
        let updatedImportedRecipe = {...recipe}
        updatedImportedRecipe.ingredients = ingredients
        updateRecipe(updatedImportedRecipe)
    };

    const setInstructions = (instructions) => {
        let updatedImportedRecipe = {...recipe}
        updatedImportedRecipe.instructions = instructions
        updateRecipe(updatedImportedRecipe)
    };

    const setRecipeHeader = (e) => {
        let updatedImportedRecipe = {...recipe}
        updatedImportedRecipe[e.target.id] = e.target.value
        updateRecipe(updatedImportedRecipe)
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        api.post('/recipes', recipe)
            .then(() => {
                updateMessage("Recipe successfully created.")
            })
    };

    return (
        <Container className="py-3">
            <Form onSubmit={handleSubmit}>
                <RecipeHeader {...recipe} setRecipeHeader={setRecipeHeader}/>
                <IngredientRow ingredients={recipe.ingredients} setIngredients={setIngredients}/>
                <InstructionRow instructions={recipe.instructions} setInstructions={setInstructions}/>

                {
                    message !== null
                        ? <div className="text-center py-3">{message}</div>
                        : null
                }

                <div className={'text-center'}>
                    <Button type='submit'>
                        Submit
                    </Button>
                </div>
            </Form>
        </Container>
    )
}

export default NewRecipe

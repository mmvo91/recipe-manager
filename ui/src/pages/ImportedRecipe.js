import React, {useState, useEffect} from "react";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import api from "../Api";
import RecipeHeader from "../components/RecipeHeader";
import IngredientRow from "../components/IngredientRow";
import InstructionRow from "../components/InstructionRow";

const ImportedRecipe = props => {
    const [importedRecipe, updateImportedRecipe] = useState({ingredients: [], instructions: []})
    const [message, updateMessage] = useState(null)

    useEffect(() => {
        api.get('/imports/' + props.match.params.id)
            .then(res => updateImportedRecipe(res.data))
    }, [])

    const setIngredients = (ingredients) => {
        let updatedImportedRecipe = {...importedRecipe}
        updatedImportedRecipe.ingredients = ingredients
        updateImportedRecipe(updatedImportedRecipe)
    };

    const setInstructions = (instructions) => {
        let updatedImportedRecipe = {...importedRecipe}
        updatedImportedRecipe.instructions = instructions
        updateImportedRecipe(updatedImportedRecipe)
    };

    const setRecipeHeader = (e) => {
        let updatedImportedRecipe = {...importedRecipe}
        updatedImportedRecipe[e.target.id] = e.target.value
        updateImportedRecipe(updatedImportedRecipe)
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        api.post('/recipes', importedRecipe)
            .then(() => {
                api.put('/imports/' + props.match.params.id);

                updateMessage("Recipe successfully imported.")
            })
    };

    return (
        <Container className="py-3">
            <Form onSubmit={handleSubmit}>
                <RecipeHeader {...importedRecipe} setRecipeHeader={setRecipeHeader}/>
                <IngredientRow ingredients={importedRecipe.ingredients} setIngredients={setIngredients}/>
                <InstructionRow instructions={importedRecipe.instructions} setInstructions={setInstructions}/>

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

export default ImportedRecipe

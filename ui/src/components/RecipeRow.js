import React from "react";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Select from "react-select";
import Button from "react-bootstrap/Button";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

import api from "../Api"
//imports bootstrapStyle from "../utils/styles"

const RecipeRow = ({user_recipe, index, recipes, data, changeData}) => {
    const removeRecipe = idx => () => {
        api.delete('/planner/recipes/' + user_recipe.id)
            .then(res => {

            })
        changeData(data.filter((s, sidx) => idx !== sidx))
    };

    const changeRecipe = idx => event => {
        const updateRecipe = data.map(
            (recipe, sidx) => {
                if (idx !== sidx) return recipe;

                recipe.recipeId = event.id;
                recipe.recipe = event;

                return recipe;
            });

        changeData(updateRecipe);

        changeServing(idx)({target: {value: event.servings}})
    };

    const changeServing = idx => event => {
        const updateRecipe = data.map(
            (recipe, sidx) => {
                if (idx !== sidx) return recipe;

                recipe.servings = event.target.value;

                return recipe;
            });

        changeData(updateRecipe)
    };

    const defaultValue = (user_recipe) => {
        if (user_recipe.recipe.recipeTitle !== "") {
            return user_recipe.recipe
        } else {
            return null
        }
    };

    return (
        <Form.Row>
            <Form.Group as={Col} className="py-1">
                <h4 className="my-0">{index + 1}.</h4>
            </Form.Group>
            <Form.Group as={Col} className="col-8">
                <Select
                    value={defaultValue(user_recipe)}
                    placeholder="Recipes"
                    //styles={bootstrapStyle}
                    onChange={changeRecipe(index)}
                    options={recipes}
                    getOptionLabel={(option) => option.title}
                    getOptionValue={(option) => option.id}
                />
            </Form.Group>
            <Form.Group as={Col} className="col-2">
                <Form.Control
                    id={'servings_' + index + 1}
                    name={'servings'}
                    value={user_recipe.servings}
                    onChange={changeServing(index)}
                    type="number"
                    placeholder="Servings"
                />
            </Form.Group>
            <Form.Group as={Col}>
                <Button variant='danger' onClick={removeRecipe(index)}>
                    <FontAwesomeIcon icon={"trash"}/>
                </Button>
            </Form.Group>
        </Form.Row>
    )
};

export default RecipeRow
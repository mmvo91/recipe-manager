import React, {useEffect, useState} from 'react';
import Form from "react-bootstrap/Form";
import CreatableSelect from 'react-select/creatable';
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

import api from "../Api";

const ingredient = {
    ingredient: "",
    amount: 0,
    unit: "",
    state: "",
};

const IngredientRow = ({ingredients, setIngredients}) => {
    const [units, setUnits] = useState([]);
    const [states, setStates] = useState([]);

    useEffect(() => {
        api.get('/recipes/units')
            .then(res => setUnits(res.data));

        api.get('/recipes/states')
            .then(res => setStates(res.data));
    }, []);

    const addIngredient = () => {
        setIngredients(ingredients.concat(ingredient))
    };

    const changeIngredient = idx => event => {
        const updateIngredient = ingredients.map(
            (ingredient, sidx) => {
                if (idx !== sidx) return ingredient;
                return {...ingredient, [event.target.name]: event.target.value};
            });

        setIngredients(updateIngredient)
    };

    const changeIngredientCreatable = (idx, variable) => event => {
        if (event !== null) {
            const updateIngredient = ingredients.map(
                (ingredient, sidx) => {
                    if (idx !== sidx) return ingredient;
                    return {...ingredient, [variable]: event.name};
                });

            setIngredients(updateIngredient)
        }
    };

    const removeIngredient = idx => () => {
        setIngredients(ingredients.filter((s, sidx) => idx !== sidx))
    };

    const defaultValue = (ingredient, variable) => {
        if (ingredient[variable] !== "") {
            return {id: 0, name: ingredient[variable]}
        } else {
            return null
        }
    };

    return (
        <div className="py-3">
            <h5>Ingredients</h5>
            {
                ingredients.map(
                    (ingredient, idx) => (
                        <React.Fragment>
                            <Form.Row>
                                <Form.Group as={Col}>
                                    <Form.Control
                                        id={'amount_' + idx}
                                        name={'amount'}
                                        value={ingredient.amount}
                                        type="number"
                                        placeholder="Amount"
                                        onChange={changeIngredient(idx)}
                                    />
                                </Form.Group>
                                <Form.Group as={Col}>
                                    <CreatableSelect
                                        isClearable
                                        options={units}
                                        value={defaultValue(ingredient, 'unit')}
                                        placeholder="Unit"
                                        onChange={changeIngredientCreatable(idx, 'unit')}
                                        getOptionLabel={(option) => option.name}
                                        getOptionValue={(option) => option.id}
                                        getNewOptionData={(inputValue, optionLabel) => ({
                                            from: 'unit',
                                            name: optionLabel,
                                            __isNew__: true
                                        })}
                                    />
                                </Form.Group>
                                <Form.Group as={Col}>
                                    <Form.Control
                                        id={'ingredient' + idx}
                                        name='ingredient'
                                        value={ingredient.ingredient}
                                        type="text"
                                        placeholder="Item"
                                        onChange={changeIngredient(idx)}
                                    />
                                </Form.Group>
                                <Form.Group as={Col}>
                                    <CreatableSelect
                                        isClearable
                                        options={states}
                                        value={defaultValue(ingredient, 'state')}
                                        placeholder="State"
                                        onChange={changeIngredientCreatable(idx, 'state')}
                                        getOptionLabel={(option) => option.name}
                                        getOptionValue={(option) => option.id}
                                        getNewOptionData={(inputValue, optionLabel) => ({
                                            from: 'state',
                                            name: optionLabel,
                                            __isNew__: true
                                        })}
                                    />
                                </Form.Group>
                                <Form.Group>
                                    <Button variant='danger' onClick={removeIngredient(idx)}>
                                        <FontAwesomeIcon icon={"trash"}/>
                                    </Button>
                                </Form.Group>
                            </Form.Row>
                        </React.Fragment>
                    )
                )
            }
            <div className="text-center">
                <Button onClick={addIngredient}>
                    Add Ingredient
                </Button>
            </div>
        </div>
    )
};

export default IngredientRow;
import React from "react";

const Ingredients = (props) => {
    const amount_formatter = (amount) => {
        if (amount !== 0) {
            return amount
        } else {
            return ''
        }
    };

    const state_formatter = (state) => {
        if (state !== '') {
            return ', ' + state
        } else {
            return ''
        }
    };

    const formatter = (ingredient) => {
        const amount = amount_formatter(ingredient.amount);
        const state = state_formatter(ingredient.state);

        return amount + ' ' + ingredient.unit + ' ' + ingredient.ingredient + state
    };

    return (
        <div>
            <h5>Ingredients</h5>
            <ul>
                {
                    props.ingredients.map(ingredient => {
                        return <li key={ingredient.ingredient}>{formatter(ingredient)}</li>
                    })
                }
            </ul>
        </div>
    )
};

Ingredients.defaultProps = {
    ingredients: []
}

export default Ingredients;
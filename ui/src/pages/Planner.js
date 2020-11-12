import React, {useState} from "react";
import Container from "react-bootstrap/Container";
import Card from "react-bootstrap/Card";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Button from "react-bootstrap/Button";

import api from "../Api"
import Calendar from "../components/Calendar";
import TableCard from "../components/TableCard";
import RecipeRow from "../components/RecipeRow";

const headers = [
    'Amount',
    'Units',
    'Ingredients'
];

const Planner = () => {
    const [dateOption, setDateOption] = useState(null);
    const [recipes, changeRecipes] = useState([]);
    const [data, changeData] = useState([]);
    const [summary, changeSummary] = useState([]);
    const [add, setAdd] = useState(false);

    const handleChange = (dateOption) => {
        setDateOption(dateOption);
        fetchRecipes();
        fetchData(dateOption);
        fetchSummary(dateOption);
        setAdd(true)
    };

    const fetchData = (date) => {
        api.get('/planner/weeks/' + date.date)
            .then(res => {
                changeData(res.data['recipes'])
            })
    };

    const fetchSummary = (date) => {
        api.get('/planner/weeks/' + date.date + '/summary')
            .then(res => {
                changeSummary(res.data)
            })
    };

    const fetchRecipes = () => {
        api.get('/recipes')
            .then(res => {
                changeRecipes(res.data)
            });
    };

    const addRecipe = () => {
        changeData(data.concat({
            recipeId: 0,
            recipe: {recipeTitle: ""},
            order: data.length + 1,
            servings: 0,
        }));
    };

    const updateSummary = () => {
        api.put("/planner/weeks/" + dateOption.date, data)
            .then(res => {
                fetchSummary(dateOption)
            })
    };

    return (
        <Container className="py-3">
            <Card>
                <Card.Body>
                    <Card.Title>
                        Planner
                    </Card.Title>
                    <Calendar fetchData={handleChange}/>
                    {
                        data !== undefined
                            ? (
                                data.map(
                                    (user_recipe, index) => (
                                        <RecipeRow
                                            key={index}
                                            user_recipe={user_recipe}
                                            index={index}
                                            recipes={recipes}
                                            data={data}
                                            changeData={changeData}
                                        />
                                    )
                                ))
                            : <div className="text-center py-2">No recipes added!</div>
                    }
                    {
                        add ? (
                                <div className="text-center">
                                    <ButtonGroup>
                                        <Button
                                            variant="primary"
                                            onClick={addRecipe}>
                                            Add Recipes
                                        </Button>
                                        <Button
                                            variant="primary"
                                            onClick={updateSummary}>
                                            Update Summary
                                        </Button>
                                    </ButtonGroup>
                                </div>
                            )
                            : null
                    }
                </Card.Body>
            </Card>
            {
                summary.length > 0
                    ? (
                        <TableCard
                            title={"Buying List"}
                            headers={headers}
                            rows={summary}
                            className="my-2"
                        />
                    )
                    : null
            }
        </Container>
    )
};

export default Planner
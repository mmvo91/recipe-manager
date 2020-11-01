import React, {useEffect, useState} from "react";
import Container from "react-bootstrap/Container"
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";

import api from "../Api"
import RecipeCard from "../components/RecipeCard"

const Imports = () => {
    const [imports, updateImports] = useState([]);
    const [imported, updateImported] = useState([]);
    const [URL, changeURL] = useState(null)

    useEffect(() => {
        api.get('/imports?imported=false')
            .then(res => {
                updateImports(res.data)
            });
        api.get('/imports?imported=true')
            .then(res => {
                updateImported(res.data)
            });
    }, []);

    const updateURL = event => {
        changeURL(event.target.value)
    }

    const importRecipe = () => {
        api.post('/imports', {url: URL})
            .then(res => {

            })
    }

    return (
        <Container className="py-3">
            <h3 className="py-2">
                <u>To Import</u>
            </h3>
            <Row>
                {
                    imports.length !== 0
                        ? imports.map(recipe => (<RecipeCard recipe={recipe} location="/import/"/>))
                        : <Col><Card><Card.Body>Empty</Card.Body></Card></Col>
                }
            </Row>
            <h3 className="py-2">
                <u>Imported</u>
            </h3>
            <Row>
                {
                    imported.length !== 0
                        ? imported.map(recipe => (<RecipeCard recipe={recipe} location="/import/"/>))
                        : <Col><Card><Card.Body>Empty</Card.Body></Card></Col>
                }
            </Row>
        </Container>
    )
};

export default Imports
import React from "react";
import Card from "react-bootstrap/Card";
import Table from "react-bootstrap/Table";

const TableCard = props => {
    return (
        <Card className={props.className}>
            <Card.Body>
                <Card.Title>
                    {props.title}
                </Card.Title>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        {
                            props.headers.map(header => (
                                    <th key={header}>{header}</th>
                                )
                            )
                        }
                    </tr>
                    </thead>
                    <tbody>
                    {
                        props.rows.map(
                            row => (
                                <tr key={row['ingredients'] + '_' + row['units']}>
                                    <td>
                                        {row['amount']}
                                    </td>
                                    <td>
                                        {row['units']}
                                    </td>
                                    <td>
                                        {row['ingredients']}
                                    </td>
                                </tr>
                            )
                        )
                    }
                    </tbody>
                </Table>
            </Card.Body>
        </Card>
    )
};

export default TableCard
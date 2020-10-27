import React from 'react'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import NavDropdown from "react-bootstrap/NavDropdown";
import {LinkContainer} from 'react-router-bootstrap'

const NavLink = (props) => {
    return (
        <LinkContainer to={props.href}>
            <Nav.Link>{props.children}</Nav.Link>
        </LinkContainer>
    )
};

const NavDropDownItemLink = (props) => {
    return (
        <LinkContainer to={props.href}>
            <NavDropdown.Item>{props.children}</NavDropdown.Item>
        </LinkContainer>
    )
};

const Navigation = () => {
    return (
        <Navbar collapseOnSelect expand="sm" bg="primary" variant="dark" className="sticky-top">
            <Navbar.Brand href="/">
                {'Recipe App'}
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="responsive-navbar-nav"/>
            <Navbar.Collapse className="text-center" id="responsive-navbar-nav">
                <Nav className="mr-auto">
                    <NavLink href={"/"}>Home</NavLink>
                    <NavDropdown title="Recipes" id="collapsible-nav-dropdown">
                        <NavDropDownItemLink href="/recipes">Recipes</NavDropDownItemLink>
                    </NavDropdown>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    )
};

export default Navigation
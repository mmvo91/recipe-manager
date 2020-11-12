import React from 'react'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import NavDropdown from "react-bootstrap/NavDropdown";
import {LinkContainer} from 'react-router-bootstrap'
import {useCookies} from "react-cookie";

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
    const [cookie, setCookie, removeCookie] = useCookies(['access_token'])

    const loggingOut = () => {
        removeCookie('access_token')
    }

    return (
        <Navbar collapseOnSelect expand="sm" bg="primary" variant="dark" className="sticky-top">
            <Navbar.Brand href="/">
                {'Recipe App'}
            </Navbar.Brand>
            {
                cookie.access_token
                    ? (
                        <React.Fragment>
                            <Navbar.Toggle aria-controls="responsive-navbar-nav"/>
                            <Navbar.Collapse className="text-center" id="responsive-navbar-nav">
                                <Nav className="mr-auto">
                                    <NavLink href={"/"}>Home</NavLink>
                                    <NavLink href="/planner">Planner</NavLink>
                                    <NavDropdown title="Recipes" id="collapsible-nav-dropdown">
                                        <NavDropDownItemLink href="/recipes">Recipes</NavDropDownItemLink>
                                        <NavDropDownItemLink href="/recipes/new">New</NavDropDownItemLink>
                                        <NavDropDownItemLink href="/import">Import</NavDropDownItemLink>
                                    </NavDropdown>
                                </Nav>
                                <Nav>
                                    <Nav.Link href="/" onClick={loggingOut}>Logout</Nav.Link>
                                </Nav>
                            </Navbar.Collapse>
                        </React.Fragment>
                    )
                    : null
            }
        </Navbar>
    )
};

export default Navigation
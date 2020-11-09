import React, {useState} from "react";
import Container from "react-bootstrap/Container"
import Card from "react-bootstrap/Card";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import api from "../Api";
import {useCookies} from "react-cookie";

const Login = props => {
    const [cookie, setCookie, removeCookie] = useCookies(['access_token'])
    const [username, setUsername] = useState(null);
    const [password, setPassword] = useState(null);
    const [message, setMessage] = useState(null);

    const loginUser = () => {
        const data = {
            username: username,
            password: password,
        };


        api.post( '/token', data, {withCredentials: true})
            .then(res => {
                if (res.data['accessToken']) {
                    setCookie('access_token', res.data['accessToken'])
                    if (props.location.pathname !== '/login') {
                        props.history.push(props.location.pathname)
                    } else {
                        props.history.push('/')
                    }
                } else {
                    setMessage(res.data['detail'])
                }
            })
            .catch(res => console.log(res))

    };

    return (
        <Container className="py-3">
            <Card className="col-md-8 m-auto">
                <Card.Body>
                    <Card.Title>
                        Login
                    </Card.Title>
                    <Form>
                        <Form.Group controlId="username">
                            <Form.Label>Username</Form.Label>
                            <Form.Control
                                type="text"
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                                placeholder="Username..."/>
                        </Form.Group>
                        <Form.Group controlId="password">
                            <Form.Label>Password</Form.Label>
                            <Form.Control
                                type="password"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                placeholder="Password..."/>
                        </Form.Group>
                        <div className="text-center">
                            {
                                message !== null
                                    ? (
                                        <Card.Text className="py-2 text-muted">
                                            {message}
                                        </Card.Text>
                                    )
                                    : null
                            }
                            <Button onClick={loginUser}>
                                Login
                            </Button>
                        </div>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    )
};

export default Login
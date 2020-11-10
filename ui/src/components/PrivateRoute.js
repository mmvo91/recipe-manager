import {useCookies} from "react-cookie";
import {Redirect, Route} from "react-router-dom";
import React from "react";

const PrivateRoute = ({component: Component, ...rest}) => {
    const [cookie] = useCookies(['access_token'])

    return (
        <Route {...rest} render={(props) => (
            cookie['access_token']
                ? (<Component {...props} />)
                : (<Redirect to={{
                    pathname: '/login',
                    state: {from: props.location}
                }}/>)
        )}/>
    );
};

export default PrivateRoute;
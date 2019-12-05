import React, { Component } from 'react';
import { Route, Switch } from "react-router-dom";
import axios from 'axios';

import About from "./components/About";
import Form from "./components/Form";
import NavBar from "./components/NavBar";
import Logout from "./components/Logout";
import UsersList from './components/UsersList';
import UserStatus from "./components/UserStatus";

class App extends Component {
    constructor() {
        super();
        this.state = {
            users: [],
            title: "PatrickCmd.io",
            isAuthenticated: false,
        };
        this.logoutUser = this.logoutUser.bind(this);
        this.loginUser = this.loginUser.bind(this);
    }

    /*** 
     * This Lifecycle Method is deprecated. Instead of componentWillMount, use the constructor for 
     * things that do NOT produce side-effects and use componentDidMount for the things that do 
     * produce side-effects. 
    ***/
    UNSAFE_componentWillMount() {
            if (window.localStorage.getItem('authToken')) {
            this.setState({ isAuthenticated: true });
        };
    };

    componentDidMount() {
        this.getUsers();
    };

    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
        .then((res) => { this.setState({ users: res.data.data.users }); })
        .catch((err) => { console.log(err); })
    };

    loginUser(token) {
        window.localStorage.setItem("authToken", token);
        this.setState({ isAuthenticated: true });
        this.getUsers();
    };

    logoutUser() {
        window.localStorage.clear();
        this.setState({ isAuthenticated: false });
    };

    render() {
        return (
            <div>
                <NavBar 
                    title={this.state.title}
                    isAuthenticated={this.state.isAuthenticated}
                />
                <section className="section">
                    <div className="container">
                        <div className="columns">
                            <div className="column is-half">
                                <br/>
                                <Switch>
                                    <Route exact path="/" render={() => (
                                        <UsersList users={this.state.users}/>
                                    )} />
                                    <Route exact path="/about" component={About}/>
                                    <Route exact path="/register" render={()=> (
                                        <Form
                                            formType={"Register"}
                                            isAuthenticated={this.state.isAuthenticated}
                                            loginUser={this.loginUser}
                                        />
                                    )} />
                                    <Route exact path="/login" render={()=> (
                                        <Form
                                            formType={"Login"}
                                            isAuthenticated={this.state.isAuthenticated}
                                            loginUser={this.loginUser}
                                        />
                                    )} />
                                    <Route exact path="/logout" render={() => (
                                        <Logout
                                            logoutUser={this.logoutUser}
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )} />
                                    <Route exact path="/status" render={() => (
                                        <UserStatus isAuthenticated={this.state.isAuthenticated}/>
                                    )} />
                                </Switch>
                                <hr/><br/>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        )
    }
};

export default App;

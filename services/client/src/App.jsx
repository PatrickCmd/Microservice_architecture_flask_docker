import React, { Component } from 'react';
import { Route, Switch } from "react-router-dom";
import axios from 'axios';

import AddUser from './components/AddUser';
import About from "./components/About";
import Form from "./components/Form";
import NavBar from "./components/NavBar";
import UsersList from './components/UsersList';

class App extends Component {
    constructor() {
        super();
        this.state = {
            users: [],
            username: '',
            email: '',
            title: "PatrickCmd.io",
            formData: {
                username: "",
                email: "",
                password: "",
            },
        };
        this.addUser = this.addUser.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
        this.getUsers();
    };

    addUser(event) {
        event.preventDefault();
        const data = {
            username: this.state.username,
            email: this.state.email
        }

        axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
        .then((res) => { 
            this.getUsers();
            this.setState({ username: '', email: '' });
         })
        .catch((err) => { console.log(err); })
    }

    handleChange(event) {
        const obj = {};
        obj[event.target.name] = event.target.value;
        this.setState(obj);
    }

    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
        .then((res) => { this.setState({ users: res.data.data.users }); })
        .catch((err) => { console.log(err); })
    }

    render() {
        return (
            <div>
                <NavBar title={this.state.title} />
                <section className="section">
                    <div className="container">
                        <div className="columns">
                            <div className="column is-half">
                                <br/>
                                <Switch>
                                    <Route exact path="/" render={() => (
                                        <div>
                                            <h1 className="title is-1 is-1">All Users</h1>
                                            <hr/><br/>
                                            <AddUser
                                                username={this.state.username}
                                                email={this.state.email}
                                                addUser={this.addUser}
                                                handleChange={this.handleChange}
                                            />
                                            <br/><br/>
                                            <UsersList users={this.state.users}/>
                                        </div>
                                    )} />
                                    <Route exact path="/about" component={About}/>
                                    <Route exact path="/register" render={()=> (
                                        <Form
                                            formType={"Register"}
                                            formData={this.state.formData}
                                        />
                                    )} />
                                    <Route exact path="/login" render={()=> (
                                        <Form
                                            formType={"Login"}
                                            formData={this.state.formData}
                                        />
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

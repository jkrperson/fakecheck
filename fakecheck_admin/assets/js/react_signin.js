class TextInput extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            inputValue: "",
        }
        this.submit = (value) => this.props.OnSubmit(value);
    }

    changeHandler(evt){
        this.setState({
            inputValue: evt.target.value
          });      
    }
}

class UsernameInput extends TextInput{
    render(){
        return(
            <div class="form-group" style={{color: 'rgb(255,255,255)'}}>
                asd
                {/* <label class="text-secondary" style={{color: 'rgb(255,255,255)'}}>Email</label>
                <input value={this.state.inputValue} onChange={evt => this.changeHandler(evt)} onSubmit={this.submit(this.state.inputValue)} class="shadow form-control" type="text" required="" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,15}$" inputmode="email" style={{'background-color': "rgb(255,255,255)"}}/> */}
            </div>
        );
    }    
}

class PasswordInput extends TextInput{
    render(){
        return(
            <div class="form-group">
                asd
                {/* <label class="text-secondary">Password</label>
                <input value={this.state.inputValue} onChange={evt => this.changeHandler(evt)} onSubmit={this.submit(this.state.inputValue)} class="border rounded shadow form-control" type="password" required=""/> */}
            </div>                
        )
    }
}

function SubmitButton(props){
    return(
        <button class="btn btn-info border-dark shadow mt-2" type="submit" style={{'background-color': '#000000', color: '#00ff19'}}>
            Log In
        </button>
    );
}

function ForgotPassword(props){
    return(
    <p class="mt-3 mb-0" style={{color: "#dfe8ee"}}>
        <a class="small" href="#" style={{color: "#dfe8ee"}}>
            Forgot your email or password?
        </a>
    </p>
    );
}

class LoginInfo extends React.Component{
    constructor(){
        super();
        this.state = {
            username: "",
            password: "",
            error: ""
        }
    }

    render(){
        return(
            <form onSubmit={this.handleSubmit()}>
                <UsernameInput onSubmit={this.fetchUsername()}/>
                <PasswordInput onSubmit={this.fetchPassword()}/>
                <SubmitButton/>
                <ForgotPassword/>                
            </form>
        )      
    }

    handleSubmit(){
        var data = {
            "username": this.state.username,
            "password": this.state.password
        };

        fetch("http://127.0.0.1:8001/admin/signup", 
        )
        .then(res => res.json())
        .then((result) => {
            this.setState({
                isLoaded: true,
                items: result.items
            });
        },(error) => {
            this.setState({
                isLoaded: true,
                    error
            });
        });
    }

    fetchUsername(username){
        var new_state = this.state;
        new_state.username = username; 
        this.setState(new_state);
    }

    fetchPassword(password){
        var new_state = this.state;
        new_state.password = password; 
        this.setState(new_state);
    }

}

ReactDOM.render(<LoginInfo/>, document.getElementById("Form_Container"));
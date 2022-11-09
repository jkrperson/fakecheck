import React from 'react';
import $ from 'jquery';
import RadialProgress from './radialprogress.js';
import './App.css';

const base_url = "http://fakescore.tech"

class NewsReport extends React.Component {

	constructor(props) {
		super(props);
	}

	render() {

		var section_label = null
		var curr_display = this.props.type;
		var report;

		if(curr_display === "article"){
			
			var message = "";
			var status = "";


			section_label = <h2 class="input-label">Status Details</h2>
						
			if(this.props.data.article_valid === true){
				status = "Safe to read and believe!! This news article has been verified by our admins, and itis real and true!";
			}else if(this.props.data.article_valid === false){
				status = "Be cautious! This news article has been verified by our admins, and it contains fake news.";
			}else{
				if(this.props.code === 206){
					status = "This news article has already been reported by other users! However, our admins have not verified it yet."
				}else if(this.props.code === 202){
					status = "This news article has not been reported yet, you can report this by pressing the button below."
				}
				if(this.props.data.model_probability >= 0 && this.props.data.model_probability < 26.0){
					message = "This news article is generally safe to read! However, please do remember that this is just the probability it has of containing fake news, so always be on guard!"; 
				}else if(this.props.data.model_probability >= 26.0  && this.props.data.model_probability < 51.0){
					message = "This news article has a chance of containing fake news.Stay alert! However, please do remember that this is just the probability it has of containing fake news."; 
				} else if(this.props.data.model_probability >= 51.0 && this.props.data.model_probability < 76.0){
					message = "Please read with caution! This news article has a high chance of containing fake news. Keep your guard up! However, please do remember that this is just the probability it has of containing fake news."; 
				}else if(this.props.data.model_probability >= 76.0 && this.props.data.model_probability <= 100.0){
					message = "BE CAUTIOUS! This news article has a very high chance of containing fake news. Stay extra alert! However, please do remember that this is just the probability it has of containing fake news."; 
				}
			}

			report = (
				<div className="col-12">
					<div className="input-thing">
						<label htmlFor="url_check">Status</label>
						<input type="text" className="form-control" id="basic-url" disabled value={status}/>
					</div>
					<label htmlFor="Bar">Fakescore</label>
					<div id="bar"></div>
					<p className="message">
						{message}
					</p>
				</div>
			);
		}else if(curr_display === "url"){
			var message = "";
			var status = "";

			section_label = <h2 class="input-label">Status Details</h2>
						
			if(this.props.data.url.url_valid === true){
				status = "Safe to read and believe!! This news article has been verified by our admins, and itis real and true!";
			}else if(this.props.data.url.url_valid === false){
				status = "Be cautious! This news article has been verified by our admins, and it contains fake news.";
			}else{
				if(this.props.code === 206){
					status = "This news article has already been reported by other users! However, our admins have not verified it yet."
				}else if(this.props.code === 202){
					status = "This news article has not been reported yet, you can report this by pressing the button below."
				}
				if(this.props.data.model_probability >= 0 && this.props.data.model_probability < 26.0){
					message = "This news article is generally safe to read! However, please do remember that this is just the probability it has of containing fake news, so always be on guard!"; 
				}else if(this.props.data.model_probability >= 26.0  && this.props.data.model_probability < 51.0){
					message = "This news article has a chance of containing fake news.Stay alert! However, please do remember that this is just the probability it has of containing fake news."; 
				} else if(this.props.data.model_probability >= 51.0 && this.props.data.model_probability < 76.0){
					message = "Please read with caution! This news article has a high chance of containing fake news. Keep your guard up! However, please do remember that this is just the probability it has of containing fake news."; 
				}else if(this.props.data.model_probability >= 76.0 && this.props.data.model_probability <= 100.0){
					message = "BE CAUTIOUS! This news article has a very high chance of containing fake news. Stay extra alert! However, please do remember that this is just the probability it has of containing fake news."; 
				}
			}
			report = (
				<div className="col-12">
					<div className="input-thing">
						<label htmlFor="url_check">Status</label>
						<input type="text" className="form-control" id="basic-url" disabled value={status}/>
					</div>
					<label htmlFor="Bar">Fakescore</label>
					<div id="bar"></div>
					<p className="message">
						{message}
					</p>
				</div>
			);
		}else if(curr_display === "default"){
			report = (
				<div className="col-12 logo-deeper-container">
					<div className="logo-container align-middle">
						<img id="backgroundLogo" className="img-fluid" src="logo512.png" alt="Logo"/>
					</div>
				</div>
			);
		}else if(curr_display === "reported"){
			report = (
				<div className="col-12 display-as-table">
					<div className="align-to-middle">
						<img src="thanks.jpg" alt="thankYou" className="img-fluid"/>
					</div>
				</div>
			);
		}

		return (
			<div className="col-6 no-gutters content-section">
				<div className="container main">
					{report}
				</div>
				
			</div>
		);
	}

	componentDidUpdate(){

		if(this.props.type === "url" || this.props.type === "article"){
			var prob = this.props.data.model_probability;
			var pred = this.props.data.model_prediction;
			var bar = new RadialProgress(document.getElementById("bar"), { colorFg: "#aa0f0f", colorBg: "#585858", colorText: "#202020", round: true, thick: 2, progress: 0.0 });
			bar.draw(true);
			bar.setValue(prob * 0.01);
			$(".rp_text").click(function(){
				bar.noPercentage = !bar.noPercentage
				bar.setText(pred)
				$(".rp_text").hide()
				$(".rp_text").fadeIn(500);
				bar.draw(true);
			});
		}
	}
}

class InputGroup extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			input_display:"buttons",
			data: null,
			status_code: null,
		};
	}

	render() {
		var input_element;
		var status_toast = null;

		if(this.state.input_display === "buttons"){
			input_element = <InputButton onClick={(i) => this.onClickButton(i)}/>
		}else if(this.state.input_display === "url"){
			input_element = <InputUrl onClick={(i) => this.onClickButton(i)} onSubmit={() => this.OnSubmitURL()}/>
		}else if(this.state.input_display === "article"){
			input_element = <InputArticle onClick={(i) => this.onClickButton(i)} onSubmit={() => this.onSubmitArticle()}/>
		}else if(this.state.input_display === "url_check"){
			input_element = <URLReport onClick={(i) => this.setDefault()} onSubmit={() => this.OnReportURL()} data={this.state.data} status_code={this.state.status_code}/>
			switch (this.state.status_code) {
				case 202:
					status_toast = (
						<div class="toast" id="warningToast">
						  	<div class="toast-header">
						  	  	<strong class="mr-auto">Fake Check</strong>
						  	  	<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
						  	  	  	<span aria-hidden="true">&times;</span>
						  	  	</button>
						  	</div>
						  	<div class="toast-body">
						  	  	The news URL has not been reported yet! The report button is available for you to report
						  	</div>
						</div>
					)
					break;
				case 206:
					status_toast = (
						<div class="toast" id="warningToast">
						  	<div class="toast-header">
						  	  	<strong class="mr-auto">Fake Check</strong>
						  	  	<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
						  	  	  	<span aria-hidden="true">&times;</span>
						  	  	</button>
						  	</div>
						  	<div class="toast-body">
						  	  	The news URL has been reported but has not yet been verified!
						  	</div>
						</div>
					)
					break;
				case 200:
					status_toast = (
						<div class="toast" id="warningToast">
						  	<div class="toast-header">
						  	  	<strong class="mr-auto">Fake Check</strong>
						  	  	<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
						  	  	  	<span aria-hidden="true">&times;</span>
						  	  	</button>
						  	</div>
						  	<div class="toast-body">
						  	  	The news URL has been report and verified!
						  	</div>
						</div>
					)
					break;
				default:
					break;
			}
		}else if(this.state.input_display === "article_check"){
			input_element = <ArticleReport onClick={(i) => this.setDefault()} onSubmit={() => this.onReportArticle()} data={this.state.data} status_code={this.state.status_code}/>
			switch (this.state.status_code) {
				case 202:
					status_toast = (
						<div class="toast" id="warningToast">
						  	<div class="toast-header">
						  	  	<strong class="mr-auto">Fake Check</strong>
						  	  	<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
						  	  	  	<span aria-hidden="true">&times;</span>
						  	  	</button>
						  	</div>
						  	<div class="toast-body">
						  	  	The news URL has not been reported yet! The report button is available for you to report
						  	</div>
						</div>
					)
					break;
				case 206:
					status_toast = (
						<div class="toast" id="warningToast">
						  	<div class="toast-header">
						  	  	<strong class="mr-auto">Fake Check</strong>
						  	  	<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
						  	  	  	<span aria-hidden="true">&times;</span>
						  	  	</button>
						  	</div>
						  	<div class="toast-body">
						  	  	The news URL has been reported but has not yet been verified!
						  	</div>
						</div>
					)
					break;
				case 200:
					status_toast = (
						<div class="toast" id="warningToast">
						  	<div class="toast-header">
						  	  	<strong class="mr-auto">Fake Check</strong>
						  	  	<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
						  	  	  	<span aria-hidden="true">&times;</span>
						  	  	</button>
						  	</div>
						  	<div class="toast-body">
						  	  	The news URL has been report and verified!
						  	</div>
						</div>
					)
					break;
				default:
					break;
			}
		}

		return (
			<div className="col-6 no-gutters">
				<div className="container main">
					<div className="col-12 bg-greyer content-section">        
						{input_element}
					</div>
				</div>
				{status_toast}
			</div>
		);
	}

	onClickButton(s){
		this.setState({input_display:s, data: null});
	}

	setDefault(){
		this.setState({input_display:"buttons", data: null});
		this.props.setDefault();
	}

	OnSubmitURL(){

		var url = base_url + "/api/urls/check/";
        var post_data = { news_url: $("#url_input").val() };
		
		var checked = (data, status, xhr) => {
			
			this.setState({
				input_display: "url_check",
				data: data,
				status_code: xhr.status,
			});

			$("#warningToast").toast({
				delay:5000,
			});

			this.props.onSubmit("url", data, xhr.status);
		}
		
		$("#backgroundLogo").addClass("anim");
		$.ajax(url, {
			type: 'POST',  // http methodtimeout: 15000
			data: post_data,  // data to submit
			success: (data, status, xhr) => checked(data, status, xhr),
			error: function (jqXhr, textStatus, errorMessage) {
				$('#report').text(errorMessage);
			}
		});	
	}
	
	OnReportURL(){
		
		var state_data = this.state.data;
		var post_data = {
			"news_url": this.state.data.url.news_url,
			"article_content": state_data.article_content,
			"model_prediction": state_data.model_prediction,
			"model_probability": state_data.model_probability
		};
		
		var url = base_url + "/api/urls/report/";

		var reported = (data, status, xhr) => {
			this.props.onSubmit("reported", null, null);
			this.setState({
				input_display: "buttons",
				data: null,
				status_code: null,
			});
		}
		// Reminder FIX SERVER CODE
		$.ajax(url, {
			type: 'POST',  // http methodtimeout: 15000
			data: post_data,  // data to submit
			success: (data, status, xhr) => reported(data, status, xhr),
			error: function (jqXhr, textStatus, errorMessage) {
				$('#report').text(errorMessage);
			}
		});
	}

	onSubmitArticle(){

		var url = base_url + "/api/articles/check/";
        var post_data = { news_article: $("#article_input").val() };
		
		var checked = (data, status, xhr) => {
			
			this.setState({
				input_display: "article_check",
				data: data,
				status_code: xhr.status,
			});

			$("#warningToast").toast({
				delay:5000,
			});

			this.props.onSubmit("article", data, xhr.status);
		}
		
		$("#backgroundLogo").addClass("anim");
		$.ajax(url, {
			type: 'POST',  // http methodtimeout: 15000
			data: post_data,  // data to submit
			success: (data, status, xhr) => checked(data, status, xhr),
			error: function (jqXhr, textStatus, errorMessage) {
				$('#report').text(errorMessage);
			}
		});
	}

	onReportArticle(){
		var post_data = this.state.data;
		var url = base_url + "/api/articles/report/";

		var reported = (data, status, xhr) => {
			this.props.onSubmit("reported", null, null);
			this.setState({
				input_display: "buttons",
				data: null,
				status_code: null,
			});
		}
		$.ajax(url, {
			type: 'POST',  // http methodtimeout: 15000
			data: post_data,  // data to submit
			success: (data, status, xhr) => reported(data, status, xhr),
			error: function (jqXhr, textStatus, errorMessage) {
				$('#report').text(errorMessage);
			}
		});
	}
}

function InputUrl(props){

	return(
		<div className="display-as-table">
			<div className="container align-to-middle">
				<h2 className="input-label">URL Input</h2>
				<p>
					Input a URL, specifically a URL that contains news in <span>FILIPINO</span>.<br/>
				</p>
				<div className="input-group  top-buffer-20">
					<input type="text" className="form-control" id="url_input" placeholder="http://www.example.com" autoComplete="off"/>
				</div>
				<button type="submit" className="btn btn-danger btn-lg top-buffer-20 btn-left" onClick={()=>props.onClick("buttons")}>
					Back
				</button>
				<button type="submit" className="btn btn-primary btn-lg top-buffer-20 btn-right" onClick={()=>props.onSubmit()}>
					Fake Check
				</button>
			</div>
		</div>
	)
}

function InputArticle(props){

	return(
		
		<div className="display-as-table">
			<div className="container align-to-middle">
				<h2 className="input-label">Article Input</h2>
				<p>
				Input a news article that is in <span>FILIPINO</span>.
				</p>
				<div className="input-group  top-buffer-20">
					<textarea className="form-control z-depth-1" id="article_input" rows="5" placeholder="Insert a news article here"></textarea>
				</div>
				<button type="submit" className="btn btn-danger btn-lg top-buffer-20 btn-left" onClick={()=>props.onClick("buttons")}>
					Back
				</button>
				<button type="submit" className="btn btn-primary btn-lg top-buffer-20 btn-right" onClick={()=>props.onSubmit()}>
					Fake Check
				</button>
			</div>               
		</div>
	);
}

function InputButton(props){
	return(
		<div className="container display-as-table">
			<div className="align-to-middle buttons-group">
				<div className="row">
					<p>
						Welcome to Fake Check!
					</p>
				</div>
				<div className="row top-buffer-15">
					<button className="btn btn-primary btn-block btn-lg btn-url" onClick={()=>props.onClick("url")}>
						Check URL
					</button>
				</div>
				<div className="row">
					<button className="btn btn-primary btn-block btn-lg btn-article top-buffer-20" onClick={()=>props.onClick("article")}>
						Check Article
					</button>
				</div>
			</div>
		</div>
	);
}

function URLReport(props){

	var url = props.data.url.news_url;
	var article = props.data.article_content;
	var status_code = props.status_code;
	return(
		<div className="top-padding-10">
			<h2 className="input-label">URL Input</h2>
			<div className="container URLReport-group">
				<div className="input-thing">
					<label htmlFor="url_check">URL</label>
					<input type="url" className="form-control" id="url_check" value={url} disabled/>
				</div>
				<label htmlFor="news_report" className="top-buffer-20">News Report</label>
				<div className="input-group">
				<textarea className="form-control z-depth-1" id="news_report" rows="4" placeholder="Insert a news article here" value={article} disabled/>
				</div>
				<button type="submit" className="btn btn-danger btn-lg top-buffer-20 btn-left" onClick={()=>props.onClick("buttons")}>
					Cancel
				</button>
				<button type="submit" className="btn btn-primary btn-lg top-buffer-20 btn-right" onClick={status_code === 202 ? ()=>props.onSubmit(): ()=>$("#warningToast").toast("show")} disabled={status_code !== 202}>
					Report
				</button>
			</div>
		</div>
	);

}

function ArticleReport(props){
	var article_content = props.data.news_article;
	var status_code = props.status_code;
	return(
		<div className="top-padding-20">
		<h2 className="input-label">Article Report</h2>
			<div className="container URLReport-group">
				<label htmlFor="news_report" className="top-buffer-10">Article Content</label>
				<div className="input-group">
				<textarea className="form-control z-depth-1" id="news_report" rows="7" placeholder="Insert a news article here" value={article_content} disabled/>
				</div>
				<button type="submit" className="btn btn-danger btn-lg top-buffer-20 btn-left" onClick={()=>props.onClick("buttons")}>
					Cancel
				</button>
				<button type="submit" className="btn btn-primary btn-lg top-buffer-20 btn-right" onClick={status_code === 202 ? ()=>props.onSubmit(): ()=>$("#warningToast").toast("show")} disabled={status_code !== 202}>
					Report
				</button>
			</div>
		</div>
	)
}

class Content extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			curr_display: "default",
			data: null,
			status_code: null
		};

	}

	render(){

		return (
			<div className="row content justify-content-center top-buffer-40">
				<InputGroup onSubmit={(type,data, status_code)=>this.setState({curr_display: type, data: data, status_code: status_code})} setDefault={()=>this.setDefault()}/>
				<NewsReport data={this.state.data} type={this.state.curr_display} code={this.state.status_code}/>
			</div>
		);
	}

	componentDidUpdate(){
		if(this.state.curr_display === "reported"){
			var z = ()=>this.setDefault();
			setTimeout(z, 5000);
		}
	}

	setDefault(){
		this.setState({
			curr_display: "default",
			data: null,
			status_code:null
		});
	}
}

function Header(props) {
	
	return (
		<div className="row header justify-content-center top-buffer-40">
			<div className="col-12 text-center no-gutters">
				<div className="container">
					<div className="appTitle bg-greyer col-12">
						Fake Check For Desktop
					</div>
				</div>
			</div>
		</div>
	);
	
}

function SideBar(props) {
	return (
		<nav className="sidebar">
        	<ul className="list-unstyled components">
        	    <li>
					<img className="img-fluid" src="logo192.png" alt="logo"/>
        	    </li>
        	</ul>
		</nav>
	);

}

function App() {

	return (
		<div className="container-fluid">
			<div className="row main">
				<div className="col-1 sidebar-col no-gutters">
					<SideBar />
				</div>
				<div className="col-11">
					<div className="container">
						<Header/>
						<Content/>
					</div>
				</div>
			</div>
		</div>
	);
}


export default App;

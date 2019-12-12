from flask import Flask, redirect, url_for, render_template, flash, request

app = Flask(__name__)



@app.route('/name')
def home():
    return render_template("index.html")

@app.route('/jump', methods=['GET', 'POST'])
def success():
	if request.method == 'POST': 
		return 'Hello! ' + request.values['username'] +' your download link is XXXXXX.' 

	return render_template('htmltry3.html')

	

if __name__ == "__main__":
	app.run()
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        D = int(request.form['D'])
        L = int(request.form['L'])
        R = int(request.form['R'])
        SS = int(request.form['SS'])
        I = int(request.form['I'])

        S = D*(L+R)+SS
        Q = S-I

        session['S'] = S
        session['Q'] = Q

        return redirect(url_for('output'))
    return  render_template('input.html')

@app.route('/output')
def output():
    return render_template('output.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port = 8000)
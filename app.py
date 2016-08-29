from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'frank123'
app.config['MYSQL_DATABASE_DB'] = 'frank'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# yelp configuration
auth = Oauth1Authenticator(
    consumer_key="kNzwIei4YkuY3za1TZ7TcA",
    consumer_secret="Uv1H4BqQZiWfk3ubVuWMxxWZZu4",
    token="pRabtTyEwpZ6kN5oVUDnrlPh25t8sgZn",
    token_secret="GoWVcigqEPnSsbiTXtFlSgrsDa4"
)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showTopEight')
def showTopEight():
    return render_template('topeight.html')

@app.route('/showBySearchTerm/<search_term>')
def showBySearchTerm(search_term):
    client = Client(auth)
    businesses = client.search('%s' % search_term).businesses
    return render_template('topeight.html', businesses=businesses)

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _email and _password:

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_create_user',(_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/searchYelp', methods=['POST','GET'])
def search_yelp():
    try:
        # need to research best way to pass back information. can this call be made on the client side (except keys are here)
        _term = request.form['search-term']
        _loc = request.form['search-loc']
        search_term = _term + '-' + _loc
        json.dumps({'message': 'made it here ' + search_term})

        client = Client(auth)
        businesses = client.search('%s' % search_term).businesses
        return render_template('topeight.html', businesses=businesses)

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        return json.dumps({'message': 'Done it'})

if __name__ == "__main__":
    app.run()
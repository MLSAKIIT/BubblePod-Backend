from flask import Flask, request, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
import run
import os



app = Flask(__name__)
app.secret_key = os.urandom(24)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='161055218764-qmgsc704kpcdn8ejsdmsu7s3mktle26n.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


# Change routing table according to how the user is entering their profile information
# and interests in the frontend, add "filepath to image" to database in a new coloumn 
# if proflie picture functionality is added.
################Routing Table################
@app.route('/')
def index():
    # return redirect(os.environ.get('frontend'))
    email = dict(session).get('profile', None)
    return f"Welcome {email.get('family_name')}"


@app.route('/')
def create_profile():
    # return redirect(os.environ.get('frontend'))
    email = dict(session).get('profile', None)
    return f"Welcome {email.get('family_name')}"


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    profile = resp.json()
    session['profile', 'token'] = profile, token
    return redirect('/')
  
  
@app.route('/bubblepod/user/',methods = ['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        content = request.get_json()
        profile = dict(session).get('profile', None)
        content['email'] = profile.get('email',None)
        content['name'] =  profile.get('given_name',None) +  profile.get('last_name',None)
        run.store_user(content)
        return "OK", redirect('/')
    else:
        content = request.get_json()
        output = run.retrieve_user(content)
        return output


@app.route('/bubblepod/similar/',methods = ['POST'])
def send_data():
    content = request.get_json()
    output = run.retrieve_recoms(content)    
    return output

  
if __name__ == '__main__':
   app.run(debug = True)
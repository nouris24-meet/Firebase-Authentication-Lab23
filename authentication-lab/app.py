from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={ "apiKey": "AIzaSyCbu4v-C1v66_YOy6YkcLzJ1GvRXj85x0s",
  "authDomain": "taylorswift1-c6783.firebaseapp.com",
  "projectId": "taylorswift1-c6783",
  "storageBucket": "taylorswift1-c6783.appspot.com",
  "messagingSenderId": "507146983430",
  "appId": "1:507146983430:web:d1bf2cbc9cb8140b3e0b87", 
  "databaseURL":"https://taylorswift1-c6783-default-rtdb.firebaseio.com/"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            updated = {"email":email, "name": name, "username":username, "bio":bio}
            db.child("Users").child(UID).update(updated)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            tweet = {"title": title,"text": text}
            db.child("Tweets").push(tweet)
        except:
            print("Couldn't add tweet")
    return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    tweets=db.child("Tweets").get().val()
    return render_template("all_tweets.html", tweets=tweets)



if __name__ == '__main__':
    app.run(debug=True)
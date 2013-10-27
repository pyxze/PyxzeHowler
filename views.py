from flask import Blueprint, request, redirect, render_template, url_for, session
from flask.views import MethodView
from project.models import User, Role, Howl
from project import db
from project import app
from flask.ext.mongoengine.wtf import model_form
from wtforms import Form, TextField, PasswordField, validators
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
    	if request.form['username'] == "pyxze" and request.form['password'] == "bacon":
            return True
    	else:
            return False

users = Blueprint('users', __name__, template_folder='templates')

class UserListView(MethodView):

    def get(self):
        users = User.objects.all()
        return render_template('users/list.html', users=users)

class UserDetailView(MethodView):

    decorators = [login_required]

    def get(self, username):
        user = User.objects.get_or_404(username=username)
        return render_template('users/detail.html', user=user)

howls = Blueprint('howls', __name__, template_folder='templates')

class HowlListView(MethodView):

    #decorators = [login_required]

    def get(self):
        howls = Howl.objects.all()
        return render_template('howls/list.html', howls=howls)

    def post(self):
        howls = Howl.objects.all()
        test = request.form['howl']
        user = User.objects.get(id=session['user_id'])
        howl = Howl(howl=request.form['howl'], user=user)
        howl.save()
        return render_template('howls/list.html', howls=howls, test=test)

class HowlDetailView(MethodView):

    def get(self, id):
        howl = Howl.objects.get_or_404(id=id)
        return render_template('howls/detail.html', howl=howl)
        
pack = Blueprint('pack', __name__, template_folder='templates')

class PackListView(MethodView):

    decorators = [login_required]

    def get(self):
        howls = Howl.objects.all()
        test = session['user_id']
        return render_template('pack/list.html', howls=howls, test=test)

auth = Blueprint('auth', __name__, template_folder='templates')

#class LoginView(MethodView):

#	def get(self):
#	    form = LoginForm()
#	    return render_template('auth/login.html', form=form)    
#
#	def post(self):
#	    form = LoginForm(username=request.form['username'])
#	    # form = LoginForm()
#	    if form.validate():
#	        session['username'] = request.form['username']
#	    	return redirect(url_for('howls.list'))
#	    return render_template('auth/login.html', form=form)            

#class LogoutView(MethodView):

#	def get(self):
#	    session.pop('username', None)
#	    form = LoginForm()
#	    return render_template('auth/login.html', form=form)

# Register the urls
howls.add_url_rule('/', view_func=HowlListView.as_view('howllist'))
howls.add_url_rule('/howl/<id>/', view_func=HowlDetailView.as_view('howldetail'))
#users.add_url_rule('/', view_func=ListView.as_view('list'))
users.add_url_rule('/user/<username>/', view_func=UserDetailView.as_view('userdetail'))
#auth.add_url_rule('/login/', view_func=LoginView.as_view('login'))
#auth.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))
pack.add_url_rule('/pack/', view_func=PackListView.as_view('pack'))

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def create_user():
    user_datastore.create_user(email='demo@demo.com', password='demo')

@app.route('/test')
@login_required
def home():
    howls = Howl.objects.all()    
    return render_template('howls/list.html', howls=howls)

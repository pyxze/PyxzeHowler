from flask import Blueprint, request, redirect, render_template, url_for, session
from flask.views import MethodView
from project.models import User, Role, Howl, Pack
from project import db
from project import app
from flask.ext.mongoengine.wtf import model_form
from wtforms import Form, TextField, PasswordField, validators
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    username = TextField('Username', [validators.Required(), validators.Regexp(r'[a-zA-Z0-9]{5,50}', message="Username must be at least five (5) characters using letters or numbers only.")])

users = Blueprint('users', __name__, template_folder='templates')

# from http://stackoverflow.com/questions/15060849/not-getting-signal-from-flask-security

from flask.ext.security.signals import user_registered

@user_registered.connect_via(app)
def user_registered_sighandler(sender, **extra):
    user = extra['user']
    pack = Pack(user=user)
    pack.save()

class UserListView(MethodView):

    def get(self):
        users = User.objects.all()
        return render_template('users/list.html', users=users)

class UserDetailView(MethodView):

    # decorators = [login_required]

    def get(self, username):
        user = User.objects.get_or_404(username=username)
        if 'user_id' in session:
            howler = User.objects.get(id=session['user_id'])
            pack = Pack.objects.get(user=howler)
            if user in pack.howlers:
        	   verb = "Remove from your pack!"
            else:
        	   verb = "Add to your pack!"
            if str(session['user_id']) == str(user.id):
        	   show_pack_button = False
            else:
        	   show_pack_button = True
            return render_template('users/detail.html', user=user, show_pack_button=show_pack_button, verb=verb)
        else:
            show_pack_button = False
            return render_template('users/detail.html', user=user, show_pack_button=show_pack_button)

    def post(self, username):
        howler = User.objects.get(id=session['user_id'])
    	pack = Pack.objects.get(user=howler)
        user = User.objects.get_or_404(username=username)
    	if user in pack.howlers:
    	    pack.howlers.remove(user)
    	else:
    	    pack.howlers.append(user)
    	pack.save()
        return redirect('/user/' + username)

howls = Blueprint('howls', __name__, template_folder='templates')

class HowlListView(MethodView):

    #decorators = [login_required]

    def get(self):
        howls = Howl.objects.all()
        return render_template('howls/list.html', howls=howls)

    def post(self):
        howls = Howl.objects.all()
        user = User.objects.get(id=session['user_id'])
        howl = Howl(howl=request.form['howl'], user=user)
        howl.save()
        user.howls.append(howl)
        user.save()
        return render_template('howls/list.html', howls=howls)

class HowlDetailView(MethodView):

    def get(self, id):
        howl = Howl.objects.get_or_404(id=id)
        return render_template('howls/detail.html', howl=howl)
        
pack = Blueprint('pack', __name__, template_folder='templates')

class PackListView(MethodView):

    decorators = [login_required]

    def get(self):
        user = User.objects.get(id=session['user_id'])
        pack = Pack.objects.get(user=user)
        howls = []
        for howler in pack.howlers:
            for howl in howler.howls:
                howls.append(howl)
        howls = sorted(howls, key=lambda i: i.created_at, reverse=True)
        return render_template('pack/list.html', howls=howls)

auth = Blueprint('auth', __name__, template_folder='templates')

# Register the urls
howls.add_url_rule('/', view_func=HowlListView.as_view('howllist'))
howls.add_url_rule('/howl/<id>/', view_func=HowlDetailView.as_view('howldetail'))
#users.add_url_rule('/', view_func=ListView.as_view('list'))
users.add_url_rule('/user/<username>/', view_func=UserDetailView.as_view('userdetail'))
pack.add_url_rule('/pack/', view_func=PackListView.as_view('pack'))

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore,
         register_form=ExtendedRegisterForm)

@app.before_first_request
def create_user():
    user_datastore.create_user(email='demo@demo.com', password='demo')

@app.route('/test')
@login_required
def home():
    howls = Howl.objects.all()    
    return render_template('howls/list.html', howls=howls)

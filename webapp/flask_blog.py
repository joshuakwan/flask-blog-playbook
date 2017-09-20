from flask import Flask, render_template_string, redirect
from sqlalchemy import create_engine, MetaData
from flask_login import UserMixin, LoginManager, login_user, logout_user
from flask_blogging import SQLAStorage, BloggingEngine
from markdown.extensions.codehilite import CodeHiliteExtension

application = Flask(__name__)
application.config["SECRET_KEY"] = "secret"  # for WTF-forms and login
application.config["BLOGGING_URL_PREFIX"] = "/blog"
application.config["BLOGGING_DISQUS_SITENAME"] = "test"
application.config["BLOGGING_SITEURL"] = "http://0.0.0.0:80"
application.config["BLOGGING_SITENAME"] = "My Site"
application.config["BLOGGING_KEYWORDS"] = ["blog", "meta", "keywords"]
application.config["FILEUPLOAD_IMG_FOLDER"] = "fileupload"
application.config["FILEUPLOAD_PREFIX"] = "/fileupload"
application.config["FILEUPLOAD_ALLOWED_EXTENSIONS"] = ["png", "jpg", "jpeg", "gif"]

# extensions
engine = create_engine('sqlite:////tmp/blog.db')
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
extn1 = CodeHiliteExtension({})
blog_engine = BloggingEngine(application, sql_storage, extensions=[extn1])
login_manager = LoginManager(application)
meta.create_all(bind=engine)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        return "Paul Dirac"  # typically the user's name

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)

index_template = """
<!DOCTYPE html>
<html>
    <head> </head>
    <body>
        {% if current_user.is_authenticated %}
            <a href="/logout/"> Logout </a>
        {% else %}
            <a href="/login/"> Login </a>
        {% endif %}
        &nbsp&nbsp<a href="/blog/"> Blog </a>
        &nbsp&nbsp<a href="/blog/sitemap.xml">Sitemap</a>
        &nbsp&nbsp<a href="/blog/feeds/all.atom.xml">ATOM</a>
        &nbsp&nbsp<a href="/fileupload/">FileUpload</a>
    </body>
</html>
"""

@application.route("/")
def index():
    return render_template_string(index_template)

@application.route("/login/")
def login():
    user = User("testuser")
    login_user(user)
    return redirect("/blog")

@application.route("/logout/")
def logout():
    logout_user()
    return redirect("/")

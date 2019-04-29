from flask import render_template, url_for, flash, redirect, request
from blog.forms import RegistrationForm, LoginForm, PostForm, CommentForm
from blog.models import User, Post, Comment
from blog import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required


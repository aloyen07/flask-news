from flask import render_template, redirect, url_for

from . import app, db
from .forms import NewsForm
from .models import Category, News

@app.route('/')
def index():
    categories = Category.query.all()
    news_list = News.query.all()
    return render_template('index.html',
                           news=news_list,
                           categories=categories)


@app.route('/news_detail/<int:id>')
def news_detail(id):
    news_det = News.query.get(id)
    categories = Category.query.all()
    # title = news[id]['title']
    # text = news[id]['text']
    return render_template('news_detail.html',
                           news=news_det,
                           categories=categories)

@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        news.category_id = form.category.data
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_news.html',
                           form=form,
                           categories=categories)


@app.route('/category/<int:id>')
def category(id: int):
    category = Category.query.get(id)
    categories = Category.query.all()
    category_name = category.title
    news = category.news
    return render_template('category.html',
                           news=news,
                           category_name=category_name,
                           categories=categories)
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, DataRequired
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

news = [{'title': 'Удивительное событие в школе',
         'text': 'Вчера в местной школе произошло удивительное событие - все '
                 'ученики одновременно зевнули на уроке математики. '
                 'Преподаватель был так поражен этим коллективным зевком, '
                 'что решил отменить контрольную работу.'},
        {'title': 'Случай в зоопарке',
         'text': 'В зоопарке города произошел необычный случай - ленивец '
                 'решил не лениться и взобрался на самое высокое дерево в '
                 'своем вольере. Посетители зоопарка были поражены такой '
                 'активностью и начали снимать ленивца на видео. В итоге он '
                 'получил свой собственный канал на YouTube, где он размещает '
                 'свои приключения.'},
        {'title': 'Самый красивый пёс',
         'text': 'Сегодня в парке прошел необычный конкурс - "Самый красивый '
                 'пёс". Участники конкурса были так красивы, что судьи не '
                 'могли выбрать победителя. В итоге, конкурс был объявлен '
                 'ничейным, а участники получили награды за участие, '
                 'в том числе - пакетики конфет и игрушки в виде косточек. '
                 'Конкурс вызвал большой интерес у посетителей парка, '
                 'и его решили повторить в более масштабном формате.'}]

# class Category(db.Model):
#     def __repr__(self):
#         return f'Category {self.id}: ({self.title})'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     news = db.relationship("News", back_populates="category")

# class News(db.Model):
#     def __repr__(self):
#         return f'News {self.id}: ({self.title[:20]}...)'
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), unique=True, nullable=False)
#     text = db.Column(db.Text, nullable=False)
#     created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
#     category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
#     #news = db.relationship("Category", back_populates="news")
#     category = db.relationship('Category', back_populates='news')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    news = db.relationship('News', back_populates='category')

    def __repr__(self):
        return f'Category {self.id}: ({self.title})'


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', back_populates='news')

# У всех проблемы)

db.create_all()

def get_cat():
    categories = Category.query.all()
    print([(category.id, category.title) for category in categories])
    return [(category.id, category.title) for category in categories]


class NewsForm(FlaskForm):
    title = StringField(
        'Название',
        validators=[DataRequired(message="Поле не должно быть пустым"),
                    Length(max=255, message='Введите заголовок длиной до 255 символов')]
    )
    text = TextAreaField(
        'Текст',
        validators=[DataRequired(message="Поле не должно быть пустым")])
    

    category = SelectField(label="Категория", choices=get_cat())
    submit = SubmitField('Добавить')


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

if __name__ == '__main__':
    app.run()

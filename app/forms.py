from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField, TextAreaField, SelectField, SubmitField
from flask_wtf import FlaskForm

from .models import Category

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

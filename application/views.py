from application import app, db
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from sqlalchemy import or_
from .models import Book
from .forms import CreateBookForm, UpdateBookForm, DeleteBookForm
from .utils import getdata
from webargs.flaskparser import use_kwargs
from webargs import fields

@app.route('/')
def index():
    return render_template('index.html')


# функция запрашивает данные из базы
@app.route('/books/list')
def list_books():
    books = Book.query.all()
    return render_template('books/list.html', books=books)


# через роут функция будет передавать число
@app.route('/books/detail/<int:book_id>')
def detail_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    # book = Book.query.get(id=book_id) второй вариант
    return render_template('books/detail.html', book=book)


# Функция обработчик которая добавляет книжку (в декораторе нужно добавлять формы, оесть реагировать и на гет и на пост запрос) пример внизу
@app.route('/books/create', methods=('GET', 'POST'))
def create_book():
    form = CreateBookForm()

    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('list_books'))

    return render_template('books/create.html', form=form)


# функция обработчик на редактирование, для нее нужно направление как и в list
@app.route('/books/update/<int:book_id>', methods=('GET', 'POST'))
def edit_book(book_id):
    book = Book.query.get(book_id)
    form = UpdateBookForm()

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        db.session.commit()
        return redirect(url_for('list_books'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
    return render_template('books/edit.html', book=book, form=form)


# Функция обработчик на подтверждение удаления книги
@app.route('/books/delete/<int:book_id>', methods=('GET', 'POST'))
def delete_book(book_id):
    book = Book.query.get(book_id)
    form = DeleteBookForm()

    if form.validate_on_submit():
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('list_books'))

    return render_template('books/delete.html', book=book, form=form)


@app.route('/books/search')
@use_kwargs(
    {
        'val': fields.Str(required=True)
    },
    location='query'
)
def search_book(val):
    books = Book.query.filter(or_(Book.title == val, Book.author == val))
    return render_template('books/search_res.html', books=books)


# ДЗ_12_(Bitcoin rate)
@app.route('/rates')
@use_kwargs(
    {
        'currency': fields.Str(required=True)
    },
    location='query'
)
def search_value(currency):
    response = getdata()
    response = list(filter(lambda i: i['code'] == currency.upper(), response))
    return render_template('rates/searchbtc.html', response=response)

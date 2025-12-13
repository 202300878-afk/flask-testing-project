import sys
import os

# agrega la raíz del proyecto al path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

import pytest
from app import app, db
from app.models import Category, Author, Book


# fixture para flask y bd en memoria
@pytest.fixture
def app_context():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()     # crea tablas
        yield               # corre pruebas
        db.session.remove()
        db.drop_all()       # limpia todo


# prueba category
def test_create_category(app_context):
    category = Category(
        name="Tecnología",
        short_desc="Libros tech"
    )

    assert category.name == "Tecnología"
    assert category.short_desc == "Libros tech"


# prueba author
def test_create_author(app_context):
    author = Author(
        name="Mario",
        about="Autor de prueba"
    )

    assert author.name == "Mario"
    assert author.about == "Autor de prueba"


# prueba book con relaciones
def test_create_book(app_context):
    category = Category(name="Novela", short_desc="Narrativa")
    author = Author(name="Carlos", about="Autor ficticio")

    db.session.add(category)
    db.session.add(author)
    db.session.commit()

    book = Book(
        name="Un libro intenso",
        tagline="Un libro intenso",
        short_desc="Una historia sobre el insomnio",
        category_id=category.id,
        author_id=author.id
    )

    
    db.session.add(book)
    db.session.commit()

    # VALIDACIONES
    assert book.name == "Un libro intenso"
    assert book.tagline == "Un libro intenso"
    assert book.short_desc == "Una historia sobre el insomnio"
    assert book.category_id == category.id
    assert book.author_id == author.id
    assert book.uuid is not None

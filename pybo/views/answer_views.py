from datetime import datetime

from flask import Blueprint, url_for, request, abort
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer

from pybo.database import conn


import pymysql

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('POST', ))
def create(question_id):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM question
        WHERE id = %s""", (question_id,))

    question = cursor.fetchone()

    if question is None:
        abort(404)

    content = request.form['content']

    cursor.execute("""
        INSERT INTO 
        answer(question_id, content, create_date)
         VALUES(%s, %s, %s)""", (question_id, content, datetime.now()))

    conn.commit()


    return redirect(url_for('question.detail', question_id=question_id))

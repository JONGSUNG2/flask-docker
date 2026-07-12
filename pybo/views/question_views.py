from flask import Blueprint, render_template, url_for, request
from werkzeug.exceptions import abort

from werkzeug.utils import redirect

from pybo.models import Question

from datetime import datetime

from pybo.forms import QuestionForm

from pybo.database import conn

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM question
        ORDER BY create_date DESC""")

    question_list = cursor.fetchall()

    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>')
def detail(question_id):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM question
        WHERE id = %s
    """, question_id)


    question = cursor.fetchone()

    cursor.execute("""
    SELECT *
    FROM answer
    WHERE question_id = %s
    ORDER BY create_date
    """, (question_id,))

    answers = cursor.fetchall()

    if question is None:
        abort(404)

    return render_template('question/question_detail.html', question=question, answers=answers)

@bp.route('/create/', methods=('POST', ))
def create():

    cursor = conn.cursor()

    subject = request.form['subject']
    content = request.form['content']

    cursor.execute("""
        INSERT INTO question(subject, content, create_date)
        VALUES(%s, %s, %s)
    """, (subject, content, datetime.now()))

    conn.commit()

    return redirect(url_for('question._list'))
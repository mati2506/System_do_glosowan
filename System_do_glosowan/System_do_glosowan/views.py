"""
Routes and views for the flask application.
"""

import numpy as np
from flask import render_template, flash, redirect, url_for, request, session, make_response
from System_do_glosowan import app, fun_base, fun, message, fun_mail

PYTHONIOENCODING="UTF-8"

@app.route('/')
@app.route('/strona_startowa', methods=['GET','POST'])
def strona_startowa():
    if 'log_in_user_id' in session or 'activate_user_id' in session:
        loged_in = True
    else:
        loged_in = False
    session.pop('reg_error_id', None)
    session.pop('reg_success', None)
    session.pop('log_error', None)
    session.pop('forgot_code_id', None)
    session.pop('forgot_user_id', None)
    session.pop('activate_user_id', None)
    session.pop('activate_fail', None)
    session.pop('pass_change_fail', None)
    session.pop('pass_change_fail_type', None)
    return render_template('strona_startowa.html', info=message.main_page_info(), loged_in=loged_in)

@app.route('/logowanie', methods=['GET','POST'])
def logowanie():
    if 'log_in_user_id' in session or 'active_user_id' in session:
        return redirect('/zalogowany')
    session.pop('log_error', None)
    session.pop('reg_success', None)
    session.pop('forgot_code_id', None)
    session.pop('forgot_user_id', None)
    session.pop('activate_user_id', None)
    session.pop('activate_fail', None)
    session.pop('pass_change_fail', None)
    session.pop('pass_change_fail_type', None)
    session['logging'] = 'begin'
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        out = fun_base.if_loging(login, password)
        if out[0]:
            session.pop('logging', None)
            if not out[2]:
                session['log_in_user_id'] = out[1]
                return redirect('/zalogowany')
            else:
                session['activate_user_id'] = out[1]
                return redirect('/aktywacja_konta')
        else:
            session['log_error'] = "Error"
            return redirect('/blad_logowania')
    return render_template('logowanie.html', info=message.loging_info())

@app.route('/blad_logowania', methods=['GET','POST'])
def blad_logowania():
    if not 'log_error' in session:
        return redirect('/logowanie')
    return render_template('blad.html', info=message.log_in_fail_info(), site_type='logowanie')

@app.route('/rejestracja', methods=['GET','POST'])
def rejestracja():
    if 'log_in_user_id' in session or 'active_user_id' in session:
        return redirect('/zalogowany')
    session.pop('reg_error_id', None)
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('user_name')
        surname = request.form.get('user_surname')
        email = request.form.get('user_email')
        sex = request.form.get('user_sex')
        birth_year = request.form.get('user_year')
        password = request.form.get('new_password')
        out = fun_base.register(username,name,surname,sex,email,birth_year,password)
        if out == '0':
            session['reg_success'] = "Success"
            return redirect('/udana_rejestracja')
        else:
            session['reg_error_id'] = out[0]
            return redirect('/blad_rejestracji')
    return render_template('rejestracja.html', info=message.register_info())

@app.route('/blad_rejestracji', methods=['GET','POST'])
def blad_rejestracji():
    if not 'reg_error_id' in session:
        return redirect('/rejestracja')
    info = message.register_fail_info(session['reg_error_id'])
    return render_template('blad.html', info=info, site_type='rejestracja')

@app.route('/udana_rejestracja', methods=['GET','POST'])
def udana_rejestracja():
    if not 'reg_success' in session:
        return redirect('/rejestracja')
    return render_template('potwierdzenie.html', info=message.register_success_info(), site_type='rejestracja')

@app.route('/zapomniane_haslo', methods=['GET','POST'])
def zapomniane_haslo():
    if not 'logging' in session:
        return redirect('/logowanie')
    if request.method == "POST":
        email = request.form.get('user_email')
        code = fun.random_number(6)
        session['forgot_code_id'] = code
        uid = fun_base.get_user_id_for_reset(email,code)
        if len(uid) > 0:
            session['forgot_user_id'] = uid
        session.pop('loging', None)
        return redirect('reset_hasla')
    return render_template('zapomniane.html', info=message.forgotten_info())

@app.route('/reset_hasla', methods=['GET','POST'])
def reset_hasla():
    if not 'forgot_code_id' in session:
        return redirect('/logowanie')
    if request.method == "POST":
        writecode = request.form.get('reset_code')
        code = session['forgot_code_id']
        password = request.form.get('new_password')
        if 'forgot_user_id' in session:
            uid = session['forgot_user_id']
            if code == writecode:
                if not fun_base.change_password(uid,password):
                    session['pass_change_fail'] = '1'
                    session['pass_change_fail_type'] = 'reset'
                    return redirect('/blad_zmiany_hasla')
        return redirect('/koniec_resetu_hasla')
    return render_template('reset.html', info=message.reset_info())

@app.route('/koniec_resetu_hasla', methods=['GET','POST'])
def koniec_resetu_hasla():
    if not 'forgot_code_id' in session:
        return redirect('/logowanie')
    return render_template('koniec_resetu_hasla.html', info=message.after_reset_password_info())

@app.route('/anulowanie_resetu_hasla', methods=['GET','POST'])
def anulowanie_resetu_hasla():
    session.pop('forgot_code_id', None)
    session.pop('forgot_user_id', None)
    return redirect('/logowanie')

@app.route('/zalogowany', methods=['GET','POST'])
def zalogowany():
    session.pop('activate_user_id', None)
    if 'activate_user_id' in session:
        return redirect('/aktywacja_konta')
    if not 'log_in_user_id' in session:
        return redirect('/logowanie')
    session.pop('activate_success', None)
    session.pop('pass_change_success', None)
    session.pop('pass_change_fail', None)
    session.pop('pass_change_fail_type', None)
    session.pop('vote_poll_id', None)
    session.pop('voting_fail', None)
    if 'vote_poll_id' in session:
        return redirect('/opuszczenie_glosowania')
    if request.method == "POST":
        poll_id = request.form.get('choose_poll')
        session['vote_poll_id'] = poll_id
        return redirect('/glosuj')
    full_name = fun_base.get_full_name(session['log_in_user_id'])
    if fun_base.if_admin(session['log_in_user_id']):
        user_type = 0
        session['log_in_admin'] = 'admin'
    elif fun_base.if_editor(session['log_in_user_id']):
        user_type = 2
        session['log_in_editor'] = 'editor'
    else:
        user_type = 1
    return render_template('zalogowany.html', info=message.user_page_info(), name=full_name, user_type=user_type,
                           polls=fun_base.polls_for_user_to_vote(session['log_in_user_id']))

@app.route('/aktywacja_konta', methods=['GET','POST'])
def aktywacja_konta():
    if not 'activate_user_id' in session:
        return redirect('/zalogowany')
    if request.method == "POST":
        code = request.form.get('act_code')
        if fun_base.activate_user(session['activate_user_id'], code):
            session['activate_success'] = 'Success'
            return redirect('/udana_aktywacja')
        else:
            session['activate_fail'] = 'Fail'
            return redirect('/blad_aktywacji_konta')
    return render_template('aktywacja.html', info=message.activate_info())

@app.route('/udana_aktywacja', methods=['GET','POST'])
def udana_aktywacja():
    if not 'activate_success' in session:
        return redirect('/zalogowany')
    session['log_in_user_id'] = session['activate_user_id']
    return render_template('potwierdzenie.html', info=message.activate_user_success_info(), site_type='aktywacja')

@app.route('/blad_aktywacji_konta', methods=['GET','POST'])
def blad_aktywacji_konta():
    if not 'activate_fail' in session:
        return redirect('/zalogowany')
    return render_template('blad.html', info=message.activate_user_fail_info(), site_type='aktywacja')

@app.route('/wyloguj', methods=['GET','POST'])
def wyloguj():
    session.pop('log_in_user_id', None)
    session.pop('activate_user_id', None)
    session.pop('log_in_admin', None)
    session.pop('log_in_editor', None)
    return redirect('/strona_startowa')

@app.route('/zmien_haslo', methods=['GET','POST'])
def zmien_haslo():
    if not 'log_in_user_id' in session:
        return redirect('/logowanie')
    if request.method == "POST":
        previous_password = request.form.get('previous_password')
        new_password = request.form.get('new_password')
        if fun_base.if_password(session['log_in_user_id'],previous_password):
            if not fun_base.change_password(session['log_in_user_id'],new_password):
                session['pass_change_fail'] = '1'
                session['pass_change_fail_type'] = 'zmiana'
                return redirect('/blad_zmiany_hasla')
            else:
                session['pass_change_success'] = 'zmiana'
                return redirect('/poprawna_zmiana_hasla')
        else:
            session['pass_change_fail'] = '0'
            session['pass_change_fail_type'] = 'change'
            return redirect('/blad_zmiany_hasla')
    return render_template('zmiana_hasla.html', info=message.change_password_info())

@app.route('/poprawna_zmiana_hasla', methods=['GET','POST'])
def poprawna_zmiana_hasla():
    if not 'pass_change_success' in session:
        return redirect('/zmien_haslo')
    return render_template('potwierdzenie.html', info=message.change_password_success_info(), site_type='zmien_haslo')

@app.route('/blad_zmiany_hasla', methods=['GET','POST'])
def blad_zmiany_hasla():
    if not 'pass_change_fail' in session:
        return redirect('/zmien_haslo')
    info = message.change_password_fail_info(session['pass_change_fail'])
    change_type = session['pass_change_fail_type']
    return render_template('blad.html', info=info, site_type='zmien_haslo', change_type=change_type)

@app.route('/wybierz_uzytkownika', methods=['GET','POST'])
def wybierz_uzytkownika():
    if not 'log_in_admin' in session:
        return redirect('/zalogowany')
    if request.method == "POST":
        if 'edit_pid' in request.form:
            session['edit_pid'] = request.form.get('edit_pid')
            return redirect('/edytuj_uzytkownika')
        elif 'delete_pid' in request.form:
            session['delete_pid'] = request.form.get('delete_pid')
            return redirect('/usun_uzytkownika')
        elif 'template' in request.form:
            search_data = request.form.get('template')
            users = fun_base.get_email_and_username_for_edit_user(search_data)
    else:
        users = fun_base.get_email_and_username_for_edit_user()
    return render_template('wyszukiwarka.html', users=users, info=message.user_search_info())

@app.route('/edytuj_uzytkownika', methods=['GET','POST'])
def edytuj_uzytkownika():
    if not 'edit_pid' in session:
        return redirect('/zalogowany')
    data = fun_base.get_full_info_user(session['edit_pid'])
    if request.method == "POST":
        changed = 0
        name = request.form.get('user_name')
        if name == '':
            name = data[0]
        else:
            changed = 1
        surname = request.form.get('user_surname')
        if surname == '':
            surname = data[1]
        else:
            changed = 1
        role = request.form.get('role')
        if role == '':
            if data[6] is None:
                role = "Nie"
            else:
                role = data[6]
        else:
            changed = 1
        sex = request.form.get('user_sex')
        if sex == '':
            sex = data[2]
        else:
            changed = 1
        year = request.form.get('user_year')
        if year == '':
            year = data[3]
        else:
            changed = 1
        fun_base.update_user(session['edit_pid'], name, surname, role, sex, year, changed)
        session.pop('edit_pid', None)
        return redirect('/wybierz_uzytkownika')
    return render_template('edycja.html', data=data, info=message.edit_user_info())

@app.route('/anuluj_edycje_uzytkownika', methods=['GET','POST'])
def anuluj_edycje_uzytkownika():
    session.pop('edit_pid', None)
    return redirect('/wybierz_uzytkownika')

@app.route('/usun_uzytkownika', methods=['GET','POST'])
def usun_uzytkownika():
    if not 'delete_pid' in session:
        return redirect('/wybierz_uzytkownika')
    if request.method == "POST":
        fun_base.delete_user(session['delete_pid'])
        session.pop('delete_pid', None)
        return redirect('/wybierz_uzytkownika')
    return render_template('usuniecie.html', data=fun_base.get_full_info_user(session['delete_pid']),
                           info=message.delete_user_info())

@app.route('/anuluj_usuniecie_uzytkownika', methods=['GET','POST'])
def anuluj_usuniecie_uzytkownika():
    session.pop('delete_pid', None)
    return redirect('/wybierz_uzytkownika')

@app.route('/informacje_o_systemie', methods=['GET','POST'])
def informacje_o_systemie():
    if not 'log_in_admin' in session:
        return redirect('/zalogowany')
    return render_template('informacje.html', info=message.system_info())

@app.route('/usun_nieaktywnych', methods=['GET','POST'])
def usun_nieaktywnych():
    if not 'log_in_admin' in session:
        return redirect('/zalogowany')
    fun_base.delete_serially_user()
    return redirect('/informacje_o_systemie')

@app.route('/utworz_glosowanie', methods=['GET','POST'])
def utworz_glosowanie():
    if not ('log_in_admin' in session or 'log_in_editor' in session):
        return redirect('/zalogowany')
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('more')
        poll_type = request.form.get('type')
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        end_date = request.form.get('finish_date')
        end_time = request.form.get('finish_time')
        start = fun.str_for_date_and_time(start_date, start_time, False)
        end = fun.str_for_date_and_time(end_date, end_time, True)
        session['edit_poll_id'] = fun_base.create_poll(title, description, poll_type, start, end, int(session['log_in_user_id']))
        session['edit_type'] = "Dodanie"
        session['added_poll'] = "added"
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('tworzenie_glosowania.html', info=message.add_poll_info())

@app.route('/zarzadzaj_glosowaniem', methods=['GET','POST'])
def zarzadzaj_glosowaniem():
    if not 'edit_poll_id' in session:
        return redirect('/glosowanie_do_edycji')
    session.pop('edit_poll_error', None)
    if request.method == "POST":
        if 'edit_question_id' in request.form:
            session['edit_question_id'] = request.form.get('edit_question_id')
            return redirect('/edytuj_pytanie')
        elif 'delete_question_id' in request.form:
            session['delete_question_id'] = request.form.get('delete_question_id')
            return redirect('/usun_pytanie')
        elif 'edit_answer_id' in request.form:
            session['edit_answer_id'] = request.form.get('edit_answer_id')
            session['answer_question_id'] = request.form.get('answer_question_id')
            return redirect('/edytuj_odpowiedz')
        elif 'delete_answer_id' in request.form:
            session['delete_answer_id'] = request.form.get('delete_answer_id')
            session['answer_question_id'] = request.form.get('answer_question_id')
            return redirect('/usun_odpowiedz')
        elif 'question_id_for_add_answer' in request.form:
            session['question_id_for_add_answer'] = request.form.get('question_id_for_add_answer')
            return redirect('/dodaj_odpowiedz')
    return render_template('zarzadzanie_glosowaniem.html', questions=fun_base.get_all_question_with_answers_for_poll(session['edit_poll_id']),
                           data=fun_base.get_poll_full_info(session['edit_poll_id']), site_type=session['edit_type'],
                           if_not_active=fun_base.if_not_active_poll(session['edit_poll_id']), info=message.poll_menage_info())

@app.route('/zakonczenie_edycji_glosowania', methods=['GET','POST'])
def zakonczenie_edycji_glosowania():
    questions = fun_base.get_all_question_with_answers_for_poll(session['edit_poll_id'])
    added_users = fun_base.added_user_to_poll(session['edit_poll_id'])
    if questions == []:
        session['edit_poll_error'] = "No questions"
        return redirect('/blad_edycji_glosowania')
    else:
        for question in questions:
            if len(question[1]) < 2:
                session['edit_poll_error'] = "Too less answers"
                return redirect('/blad_edycji_glosowania')
    if len(added_users) < 2:
        session['edit_poll_error'] = "Too less users"
        return redirect('/blad_edycji_glosowania')
    if 'added_poll' in session:
        if session['log_in_user_id'] != 0:
            fun_mail.added_edited_deleted_poll(fun_base.get_creator_username_and_email_for_poll(session['edit_poll_id']), session['edit_type'], questions, fun_base.get_poll_full_info(session['edit_poll_id']))
        session.pop('added_poll', None)
        session.pop('edited_poll', None)
    elif 'edited_poll' in session:
        if session['log_in_user_id'] != 0:
            fun_mail.added_edited_deleted_poll(fun_base.get_creator_username_and_email_for_poll(session['edit_poll_id']), session['edit_type'], questions, fun_base.get_poll_full_info(session['edit_poll_id']))
        session.pop('edited_poll', None)
    session.pop('edit_type', None)
    session.pop('edit_poll_id', None)
    return redirect('/zalogowany')

@app.route('/blad_edycji_glosowania', methods=['GET','POST'])
def blad_edycji_glosowania():
    if not 'edit_poll_error' in session:
        return redirect('/zalogowany')
    info = message.edit_poll_error_info(session['edit_poll_error'])
    if session['edit_poll_error'] != "Too less users":
        error_type = "pytania_odpowiedzi"
    else:
        error_type = "uczestnicy"
    return render_template('blad.html', info=info, site_type='edycja_głosowania', error_type=error_type)

@app.route('/zarzadzaj_uczestnikami', methods=['GET','POST'])
def zarzadzaj_uczestnikami():
    if not 'edit_poll_id' in session:
        return redirect('/zarzadzaj_glosowaniem')
    session.pop('edit_poll_error', None)
    session.pop('copy_count', None)
    if request.method == "POST":
        if 'edit_pid' in request.form:
            add_pid_for_poll = request.form.get('edit_pid')
            fun_base.add_user_for_poll(add_pid_for_poll,session['edit_poll_id'])
            users = fun_base.get_full_name_for_add_to_poll()
        elif 'delete_pid' in request.form:
            delete_pid_from_poll = request.form.get('delete_pid')
            fun_base.delete_user_from_poll(delete_pid_from_poll,session['edit_poll_id'])
            users = fun_base.get_full_name_for_add_to_poll()
        elif 'template' in request.form:
            search_data = request.form.get('template')
            users = fun_base.get_full_name_for_add_to_poll(search_data)
    else:
        users = fun_base.get_full_name_for_add_to_poll()
    return render_template('dodawanie_uczestnikow.html', users=users, added_users=fun_base.added_user_to_poll(session['edit_poll_id']),
                           poll_id=fun_base.get_poll_name(session['edit_poll_id']), info=message.add_users_to_poll_info())

@app.route('/wybierz_grupe', methods=['GET','POST'])
def wybierz_grupe():
    if not 'edit_poll_id' in session:
        return redirect('/glosowanie_do_edycji')
    if request.method == "POST":
        if 'edit_pid' in request.form:
            session['copy_group_id'] = request.form.get('edit_pid')
            return redirect('/kopiuj_grupe')
        elif 'template' in request.form:
            search_data = request.form.get('template')
            groups = fun_base.get_group_for_select(session['edit_poll_id'], search_data)
    else:
        groups = fun_base.get_group_for_select(session['edit_poll_id'])
    return render_template('kopiuj_grupy.html', info=message.group_copy_info(), groups=groups)

@app.route('/kopiuj_grupe', methods=['GET','POST'])
def kopiuj_grupe():
    if not 'copy_group_id' in session:
        return redirect('/zarzadzaj_uczestnikami')
    if request.method == "POST":
        count = fun_base.copy_users_from_another_group(session['copy_group_id'], session['edit_poll_id'])
        session['copy_count'] = count
        session.pop('copy_group_id', None)
        return redirect('/potwierdzenie_kopiowania_grupy')
    return render_template('kopiuj_grupy_potwierdz.html', glosowanie=fun_base.get_poll_name(session['edit_poll_id']),
                           users=fun_base.get_users_full_name_from_group(session['copy_group_id']),
                           info=message.copy_group_confirmation_info())

@app.route('/potwierdzenie_kopiowania_grupy', methods=['GET','POST'])
def potwierdzenie_kopiowania_grupy():
     if not 'copy_count' in session:
        return redirect('/zarzadzaj_uczestnikami')
     return render_template('potwierdzenie.html', info=message.copy_users_info(session['copy_count']), site_type='kopiowanie_grupy')

@app.route('/anuluj_kopiowanie_grupy', methods=['GET','POST'])
def anuluj_kopiowanie_grupy():
    session.pop('copy_group_id', None)
    return redirect('/wybierz_grupe')

@app.route('/glosowanie_do_edycji', methods=['GET','POST'])
def glosowanie_do_edycji():
    if not ('log_in_admin' in session or 'log_in_editor' in session):
        return redirect('/zalogowany')
    if request.method == "POST":
        if 'edit_id' in request.form:
            session['edit_poll_id'] = request.form.get('edit_id')
            session['edit_type'] = "Edycja"
            return redirect('/zarzadzaj_glosowaniem')
        elif 'template' in request.form:
            search_data = request.form.get('template')
            polls = fun_base.get_polls_for_edit(session['log_in_user_id'], search_data)
    else:
        polls = fun_base.get_polls_for_edit(session['log_in_user_id'])
    return render_template('wybor_glosowania.html', polls=polls, info=message.poll_to_edit_info(), site_type='Edycja')

@app.route('/dodaj_pytanie', methods=['GET','POST'])
def dodaj_pytanie():
    if not 'edit_poll_id' in session:
        return redirect('/zarzadzaj_glosowaniem')
    session.pop('add_question_error', None)
    if request.method == "POST":
        question = request.form.get('question')
        for q in fun_base.get_questions_for_poll(session['edit_poll_id']):
            if q[0] == question:
                session['add_question_error'] = "Error"
                return redirect('/blad_dodania_pytania')
        fun_base.add_question(session['edit_poll_id'], fun.answer_question_split(question,38))
        session['edited_poll'] = "Edited"
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('dodawanie_pytania.html', name=fun_base.get_poll_name(session['edit_poll_id']),
                           info=message.add_questions_info())

@app.route('/blad_dodania_pytania')
def blad_dodania_pytania():
    if not 'add_question_error' in session:
        return redirect('/dodaj_pytanie')
    return render_template('blad.html', site_type='dodanie_pytania', info=message.question_error_info())

@app.route('/dodaj_odpowiedz', methods=['GET','POST'])
def dodaj_odpowiedz():
    if not 'question_id_for_add_answer' in session:
        return redirect('/zarzadzaj_glosowaniem')
    if request.method == "POST":
        answer = request.form.get('answer')
        for a in fun_base.get_answers_for_poll(session['question_id_for_add_answer']):
            if a[0] == answer:
                session['add_answer_error'] = "Error"
                return redirect('/blad_dodania_odpowiedzi')
        fun_base.add_answer(session['question_id_for_add_answer'], fun.answer_question_split(answer,35), session['edit_poll_id'])
        session.pop('question_id_for_add_answer', None)
        session['edited_poll'] = "Edited"
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('dodawanie_odpowiedzi.html', name=fun_base.get_question_name(session['question_id_for_add_answer']),
                           info=message.add_answers_info())

@app.route('/blad_dodania_odpowiedzi')
def blad_dodania_odpowiedzi():
    if not 'add_answer_error' in session:
        return redirect('/dodaj_odpowiedz')
    return render_template('blad.html', site_type='dodanie_odpowiedzi', info=message.answer_error_info())

@app.route('/edytuj_pytanie', methods=['GET','POST'])
def edytuj_pytanie():
    if not 'edit_question_id' in session:
        return redirect('/zarzadzaj_glosowaniem')
    session.pop('edit_question_error', None)
    if request.method == "POST":
        question = request.form.get('question')
        for q in fun_base.get_questions_for_poll(session['edit_poll_id']):
            if q[0] == question:
                session['edit_question_error'] = "Error"
                return redirect('/blad_edycji_pytania')
        fun_base.edit_question(session['edit_question_id'], fun.answer_question_split(question,38))
        session['edited_poll'] = "Edited"
        session.pop('edit_question_id', None)    
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('edycja_pytania_odpowiedzi.html', czy_pytanie=True, pytanie=fun_base.get_question_name(session['edit_question_id']),
                           info=message.edit_question_answer_info())

@app.route('/blad_edycji_pytania')
def blad_edycji_pytania():
    if not 'edit_question_error' in session:
        return redirect('/edytuj_pytanie')
    return render_template('blad.html', site_type='edycja_pytania', info=message.question_error_info())

@app.route('/edytuj_odpowiedz', methods=['GET','POST'])
def edytuj_odpowiedz():
    if not 'edit_answer_id' in session:
        return redirect('/zarzadzaj_glosowaniem')
    if request.method == "POST":
        answer = request.form.get('question')
        for a in fun_base.get_answers_for_poll(session['answer_question_id']):
            if a[0] == answer:
                session['edit_answer_error'] = "Error"
                return redirect('/blad_edycji_odpowiedzi')
        fun_base.edit_answer(session['edit_answer_id'], fun.answer_question_split(answer,35))
        session['edited_poll'] = "Edited"
        session.pop('edit_answer_id', None)
        session.pop('answer_question_id', None)       
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('edycja_pytania_odpowiedzi.html', czy_pytanie=False, pytanie=fun_base.get_question_name(session['answer_question_id']),
                           odpowiedz=fun_base.get_answer_name(session['edit_answer_id']), info=message.edit_question_answer_info())

@app.route('/blad_edycji_odpowiedzi')
def blad_edycji_odpowiedzi():
    if not 'edit_answer_error' in session:
        return redirect('/edytuj_odpowiedz')
    return render_template('blad.html', site_type='edycja_odpowiedzi', info=message.answer_error_info())

@app.route('/edytuj_dane_glosowania', methods=['GET','POST'])
def edytuj_dane_glosowania():
    if not 'edit_poll_id' in session:
        return redirect('/zarzadzaj_glosowaniem')
    session.pop('end_time_error', None)
    session.pop('poll_duration_error', None)
    session.pop('poll_start_time_error', None)
    data = fun_base.get_poll_full_info(session['edit_poll_id'])
    if_not_active = fun_base.if_not_active_poll(session['edit_poll_id'])
    if request.method == "POST":
        if if_not_active:
            description = request.form.get('more')
            if description == '':
                description = data[2]
            poll_type = request.form.get('type')
            if poll_type == 'Wybierz typ':
                poll_type = data[1]
            start_date = request.form.get('start_date')
            if start_date == '':
                start_date = fun.get_str_date_from_datetime(data[3])
            start_time = request.form.get('start_time')
            if start_time == '':
                start_time = fun.get_str_time_from_datetime(data[3])
            else:
                start_time = start_time + ":00"
            end_date = request.form.get('finish_date')
            if end_date == '':
                end_date = fun.get_str_date_from_datetime(data[4])
            end_time = request.form.get('finish_time')
            if end_time == '':
                end_time = fun.get_str_time_from_datetime(data[4])
            else:
                end_time = end_time + ":59"
        else:
            description = data[2]
            poll_type = data[1]
            start_date = fun.get_str_date_from_datetime(data[3])
            start_time = fun.get_str_time_from_datetime(data[3])        
            end_date = request.form.get('finish_date')
            if end_date == '':
                end_date = fun.get_str_date_from_datetime(data[4])
            end_time = request.form.get('finish_time')
            if end_time == '':
                end_time = fun.get_str_time_from_datetime(data[4])
            else:
                end_time = end_time + ":59"
            if fun.if_date_and_time_before_datetime(end_date,end_time,data[4]):
                session['end_time_error'] = "Error"
                return redirect('/blad_zmiany_daty_konca_glosowania')
        start = fun.str_date_and_time(start_date, start_time)
        end = fun.str_date_and_time(end_date, end_time)
        if fun.if_start_time_before_datetime(start) and fun.get_datetime_for_str(start) != data[3]:
            session['poll_start_time_error'] = "Error"
            return redirect('/blad_czasu_rozpoczecia_glosowania')
        elif fun.if_poll_duration_wrong(start, end):
            session['poll_duration_error'] = "Error"
            return redirect('/blad_czasu_trwania_glosowania')
        fun_base.edit_poll(session['edit_poll_id'], description, poll_type, start, end)
        session['edited_poll'] = "Edited"
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('edytuj_dane_glosowania.html', data=data, if_not_active=if_not_active, info=message.edit_poll_data_info())

@app.route('/blad_zmiany_daty_konca_glosowania', methods=['GET','POST'])
def blad_zmiany_daty_konca_glosowania():
    if not 'end_time_error' in session:
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('blad.html', site_type="zmiana_danych_głosowania", info=message.change_end_poll_date_fail_info())

@app.route('/blad_czasu_trwania_glosowania', methods=['GET','POST'])
def blad_czasu_trwania_glosowania():
    if not 'poll_duration_error' in session:
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('blad.html', site_type="zmiana_danych_głosowania", info=message.poll_duration_time_fail_info())

@app.route('/blad_czasu_rozpoczecia_glosowania', methods=['GET','POST'])
def blad_czasu_rozpoczecia_glosowania():
    if not 'poll_start_time_error' in session:
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('blad.html', site_type="zmiana_danych_głosowania", info=message.poll_start_datetime_error_info())

@app.route('/usun_pytanie', methods=['GET','POST'])
def usun_pytanie():
    if not 'delete_question_id' in session:
        return redirect('/zarzadzaj_glosowaniem')
    if request.method == "POST":
        fun_base.delete_question(session['delete_question_id'])
        session.pop('delete_question_id', None)
        session['edited_poll'] = "Edited"
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('usun_pytanie_potwierdz.html', pytanie=fun_base.get_question_name(session['delete_question_id']),
                           info=message.delete_question_info())

@app.route('/usun_odpowiedz', methods=['GET','POST'])
def usun_odpowiedz():
    if not 'delete_answer_id' in session:
        return redirect('/zarzadzaj_glosowaniem')
    if request.method == "POST":
        fun_base.delete_answer(session['delete_answer_id'])
        session.pop('delete_answer_id', None)
        session.pop('answer_question_id', None)
        session['edited_poll'] = "Edited"
        return redirect('/zarzadzaj_glosowaniem')
    return render_template('usun_odpowiedz_potwierdz.html', odpowiedz=fun_base.get_answer_name(session['delete_answer_id']),
                           info=message.delete_answer_info(fun_base.get_question_name(session['answer_question_id'])))

@app.route('/anulowanie_usuniecia_pytania', methods=['GET','POST'])
def anulowanie_usuniecia_pytania():
    session.pop('delete_question_id', None)
    return redirect('/zarzadzaj_glosowaniem')

@app.route('/anulowanie_usuniecia_odpowiedzi', methods=['GET','POST'])
def anulowanie_usuniecia_odpowiedzi():
    session.pop('delete_answer_id', None)
    session.pop('delete_answer_question_id', None)
    return redirect('/zarzadzaj_glosowaniem')

@app.route('/glosowanie_do_usuniecia', methods=['GET','POST'])
def glosowanie_do_usuniecia():
    if not 'log_in_admin' in session:
        return redirect('/zalogowany')
    if request.method == "POST":
        if 'delete_id' in request.form:
            session['delete_poll_id'] = request.form.get('delete_id')
            return redirect('/usun_glosowanie')
        elif 'cancel_id' in request.form:
            session['cancel_poll_id'] = request.form.get('cancel_id')
            return redirect('/uniewaznienie_glosowania')
        elif 'template' in request.form:
            search_data = request.form.get('template')
            polls = fun_base.get_polls_for_delete_or_cancel(search_data)
    else:
        polls = fun_base.get_polls_for_delete_or_cancel()
    return render_template('wybor_glosowania.html', polls=polls, current_datetime=fun.get_current_datetime(),
                          info=message.poll_to_delete_info(), site_type='Usunięcie')

@app.route('/usun_glosowanie', methods=['GET','POST'])
def usun_glosowanie():
    if not 'delete_poll_id' in session:
        return redirect('/glosowanie_do_usuniecia')
    if request.method == "POST":
        fun_base.delete_poll(session['delete_poll_id'])
        session.pop('delete_poll_id', None)
        return redirect('/glosowanie_do_usuniecia')
    return render_template('usuniecie_glosowania.html', questions=fun_base.get_all_question_with_answers_for_poll(session['delete_poll_id']),
                           data=fun_base.get_poll_full_info(session['delete_poll_id']), info=message.delete_poll_info(),
                           site_type='Usunięcie')

@app.route('/anulowanie_usuniecia_glosowania', methods=['GET','POST'])
def anulowanie_usuniecia_glosowania():
    if not 'delete_poll_id' in session:
        return redirect('/glosowanie_do_usuniecia')
    session.pop('delete_poll_id', None)
    return redirect('/glosowanie_do_usuniecia')

@app.route('/glosowanie_do_sledzenia', methods=['GET','POST'])
def glosowanie_do_sledzenia():
    if not ('log_in_admin' in session or 'log_in_editor' in session):
        return redirect('/zalogowany')
    if request.method == "POST":
        if 'select_id' in request.form:
            session['tracking_poll_id'] = request.form.get('select_id')
            return redirect('/sledz_glosowanie')
        elif 'template' in request.form:
            search_data = request.form.get('template')
            polls = fun_base.get_polls_for_tracking(session['log_in_user_id'], search_data)
    else:
        polls = fun_base.get_polls_for_tracking(session['log_in_user_id'])
    return render_template('wybor_glosowania.html', polls=polls, info=message.poll_to_tracking_info(), site_type='Śledzenie')

@app.route('/sledz_glosowanie', methods=['GET','POST'])
def sledz_glosowanie():
    if not 'tracking_poll_id' in session:
        return redirect('/glosowanie_do_sledzenia')
    poll = fun_base.get_poll_full_info(session['tracking_poll_id'])[0]
    cast = fun_base.vote_cast(session['tracking_poll_id'])
    invalid = fun_base.vote_cast(session['tracking_poll_id']) - fun_base.valid_votes(session['tracking_poll_id'])/fun_base.get_question_count(session['tracking_poll_id'])
    authorized = fun_base.get_authorized_users_for_vote_in_poll(session['tracking_poll_id'])
    return render_template('sledz_glosowanie.html', questions=fun_base.get_poll_with_counts(session['tracking_poll_id']),
                           poll=poll, cast=cast, invalid=invalid, authorized=authorized, info=message.track_vote_info())

@app.route('/zakoncz_sledzenie_glosowania', methods=['GET','POST'])
def zakoncz_sledzenie_glosowania():
    if not 'tracking_poll_id' in session:
        return redirect('/glosowanie_do_sledzenia')
    session.pop('tracking_poll_id', None)
    return redirect('/zalogowany')

@app.route('/glosuj', methods=['GET','POST'])
def glosuj():
    if not 'vote_poll_id' in session:
        return redirect('/zalogowany')
    data = fun_base.get_poll_full_info(session['vote_poll_id'])
    if request.method == "POST":
        answers = []
        getting_answers = request.form
        for pnr, answer in getting_answers.items():
            if pnr != 'exit':
                answers.append(int(answer))
        if not fun_base.voting(answers, data[1], session['log_in_user_id'], session['vote_poll_id']):
            session['voting_fail'] = "Fail"
            return redirect('/blad_oddania_glosu')
        session.pop('vote_poll_id', None)
        return redirect('/zalogowany')
    fun_base.begin_voting(session['vote_poll_id'], session['log_in_user_id'])
    return render_template('oddanie_glosu.html', questions=fun_base.get_all_question_with_answers_for_poll(session['vote_poll_id']),
                           data=data, info=message.voting_info())

@app.route('/blad_oddania_glosu', methods=['GET','POST'])
def blad_oddania_glosu():
    if not 'voting_fail' in session:
        return redirect('/zalogowany')
    return render_template('blad.html', site_type="oddanie_głosu", info=message.voting_fail_info())

@app.route('/anulowanie_oddania_glosu', methods=['GET','POST'])
def anulowanie_oddania_glosu():
    if not 'vote_poll_id' in session:
        return redirect('/zalogowany')
    fun_base.voting_canceled(session['vote_poll_id'], session['log_in_user_id'])
    session.pop('vote_poll_id', None)
    return redirect('/zalogowany')

@app.route('/opuszczenie_glosowania', methods=['GET','POST'])
def opuszczenie_glosowania():
    if not 'vote_poll_id':
        return redirect('/zalogowany')
    return render_template('opusc_glosowanie_potwierdz.html', glosowanie=fun_base.get_poll_full_info(session['vote_poll_id'])[0],
                           info=message.poll_out_info())

@app.route('/glosowanie_do_wynikow', methods=['GET','POST'])
def glosowanie_do_wynikow():
    if not 'log_in_user_id' in session:
        return redirect('/zalogowany')
    if request.method == "POST":
        if 'select_id' in request.form:
            session['results_poll_id'] = request.form.get('select_id')
            return redirect('/wyniki_glosowania')
        elif 'template' in request.form:
            search_data = request.form.get('template')
            polls = fun_base.get_polls_for_results(session['log_in_user_id'], search_data)
    else:
        polls = fun_base.get_polls_for_results(session['log_in_user_id'])
    return render_template('wybor_glosowania.html', polls=polls, info=message.poll_to_results_info(), site_type='Wyniki')

@app.route('/wyniki_glosowania', methods=['GET','POST'])
def wyniki_glosowania():
    if not 'results_poll_id' in session:
        return redirect('/glosowanie_do_wynikow')
    if request.method == "POST":
        if 'csv' in request.form:
            return redirect('/csv')
        elif 'pdf' in request.form:
            return redirect('/pdf')
        elif 'follow_id' in request.form:
            session['follow_answer_id'] = request.form.get('follow_id')
            return redirect('/obserwowanie_uczestnikow')   
    questions = fun_base.get_poll_for_results(session['results_poll_id'])
    cast = fun_base.vote_cast(session['results_poll_id'])
    invalid = fun_base.vote_cast(session['results_poll_id']) - fun_base.valid_votes(session['results_poll_id'])/fun_base.get_question_count(session['results_poll_id'])
    authorized = fun_base.get_authorized_users_for_vote_in_poll(session['results_poll_id'])
    return render_template('wykresy.html', data=fun_base.get_poll_full_info(session['results_poll_id']), questions=questions,
                           images=fun.gen_plots(questions), cast=cast, invalid=invalid, authorized=authorized,
                           info=message.poll_results_info())

@app.route('/zakoncz_wyniki_glosowania', methods=['GET','POST'])
def zakoncz_wyniki_glosowania():
    if not 'results_poll_id' in session:
        return redirect('/glosowanie_do_wynikow')
    session.pop('results_poll_id', None)
    return redirect('/glosowanie_do_wynikow')

@app.route('/uniewaznienie_glosowania', methods=['GET','POST'])
def uniewaznienie_glosowania():
    if not 'cancel_poll_id' in session:
        return redirect('/glosowanie_do_usuniecia')
    if request.method == "POST":
        fun_base.cancel_poll(session['cancel_poll_id'])
        session.pop('delete_poll_id', None)
        return redirect('/glosowanie_do_usuniecia')
    return render_template('usuniecie_glosowania.html', questions=fun_base.get_all_question_with_answers_for_poll(session['cancel_poll_id']),
                           data=fun_base.get_poll_full_info(session['cancel_poll_id']), info=message.cancel_poll_info(),
                           site_type='Unieważnienie')

@app.route('/anulowanie_uniewaznienia_glosowania', methods=['GET','POST'])
def anulowanie_uniewaznienia_glosowania():
    if not 'cancel_poll_id' in session:
        return redirect('/glosowanie_do_usuniecia')
    session.pop('cancel_poll_id', None)
    return redirect('/glosowanie_do_usuniecia')

@app.route('/obserwowanie_uczestnikow', methods=['GET','POST'])
def obserwowanie_uczestnikow():
    if not 'follow_answer_id' in session:
        return redirect('/wyniki_glosowania')
    return render_template('obserwuj_jawne.html', answer=fun_base.get_answer_name(session['follow_answer_id']),
                           question=fun_base.get_question_name_for_answer(session['follow_answer_id']), poll=fun_base.get_poll_name_for_answer(session['follow_answer_id']),
                           users=fun_base.get_users_for_result(session['follow_answer_id']), info=message.follow_users_for_answer_info())

@app.route('/zakoncz_obserwowanie_uczestnikow', methods=['GET','POST'])
def zakoncz_obserwowanie_uczestnikow():
    if not 'follow_answer_id' in session:
        return redirect('/wyniki_glosowania')
    session.pop('follow_answer_id', None)
    return redirect('/wyniki_glosowania')

@app.route('/csv', methods=['GET','POST'])
def csv():
    questions = fun_base.get_poll_for_results(session['results_poll_id'])
    users=fun_base.get_voters(session['results_poll_id'])
    output = make_response(fun.generate_csv(questions, users, session['log_in_user_id'], fun_base.get_poll_full_info(session['results_poll_id'])))
    output.headers["Content-Disposition"] = ("attachment; filename=raport "+fun.generate_current_datetime()+".csv")
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/pdf', methods=['GET','POST'])
def pdf():
    questions = fun_base.get_poll_for_results(session['results_poll_id'])
    cast = fun_base.vote_cast(session['results_poll_id'])
    invalid = fun_base.vote_cast(session['results_poll_id']) - fun_base.valid_votes(session['results_poll_id'])/fun_base.get_question_count(session['results_poll_id'])
    authorized = fun_base.get_authorized_users_for_vote_in_poll(session['results_poll_id'])
    html = render_template("pdf.html", data=fun_base.get_poll_full_info(session['results_poll_id']), questions=questions,
                           images=fun.gen_plots(questions), cast=cast, invalid=invalid, authorized=authorized,
                           logo=fun.logo_for_pdf(), users=fun_base.get_voters(session['results_poll_id']),
                           log_user=session['log_in_user_id'], info=message.pdf_info())
    response = make_response(fun.generate_pdf(html))
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = ("attachment; filename=raport "+fun.generate_current_datetime()+".pdf")
    return response

#przekierowanie, gdy adres URL nie istnieje
@app.errorhandler(404)
@app.errorhandler(500)
def strona_nie_istnieje(e):
    return render_template('blad.html', site_type='błąd_serwera', info=message.server_error_info(e))
from System_do_glosowan import app, fun, fun_mail
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'eu-cdbr-west-01.cleardb.com' #'localhost'
app.config['MYSQL_USER'] = 'b1146c15b19209' #'root'
app.config['MYSQL_PASSWORD'] = fun.pass_decoder('0011000001100001001101010110010000110111011000010110001101100001') #''
app.config['MYSQL_DB'] = 'heroku_310c29efb085c8d' #'voting'
mysql=MySQL(app)

def if_loging(login, password):
    cur=mysql.connection.cursor()
    cur.execute('SELECT user_id FROM users WHERE username = (%s) OR `e-mail` = (%s)',(login,login))
    us = cur.fetchone()
    if us is None:
        cur.close()
        return False, -1, False
    else:
        cur.execute('SELECT value FROM password WHERE user_id =(%s)',(us[0],))
        pas = cur.fetchone()
        if pas[0] == fun.hashing(password):
            cur.execute('SELECT * FROM inactive_user WHERE user_id=(%s)',(us[0],))
            if_inactive = cur.fetchone()
            cur.close()
            if if_inactive is None:
                return True, us[0], False
            else:
                return True, us[0], True
        else:
            cur.close()
            return False, -1, False

def register(username, name, surname, sex, email, birth_year, password):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()

    cur.execute('SELECT username FROM users WHERE username = (%s)',(username,))
    un = cur.fetchall()
    if len(un) > 0:
        cur.close()
        return '1'

    cur.execute('SELECT `e-mail` FROM users WHERE `e-mail` = (%s)',(email,))
    ue = cur.fetchall()
    if len(ue) > 0:
        cur.close()
        return '2'

    cur.execute('SELECT MAX(user_id) FROM users')
    us_max = cur.fetchone()[0]
    cur.execute('SELECT MAX(password_id) FROM password')
    pas_max = cur.fetchone()[0]
    
    code = fun.random_string(10)
    date_time = fun.generate_current_datetime()

    cur.execute('INSERT INTO users(user_id, name, surname, sex, birth_year, username, `e-mail`) VALUES(%s, %s, %s, %s, %s, %s, %s)',(us_max+1,name,surname,sex,birth_year,username,email))
    cur.execute('INSERT INTO password VALUES(%s, %s, %s)',(pas_max+1,fun.hashing(password),us_max+1))
    cur.execute('INSERT INTO inactive_user VALUES(%s, %s, %s)',(us_max+1, code, date_time))
    con.commit()
    cur.close()
    fun_mail.welcome_message(email,name,username,surname,sex,birth_year,code)
    return '0'

def get_user_id_for_reset(email,code):
    cur = mysql.connection.cursor()
    cur.execute('SELECT user_id, username FROM users WHERE `e-mail`=(%s)',(email,))
    uid = cur.fetchone()
    cur.close()
    if not uid is None:
        fun_mail.password_reset(email,uid[1],code)
        return str(uid[0])
    return ""

def change_password(uid,password):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()

    cur.execute('SELECT value FROM password WHERE user_id = (%s)',(uid,))
    current_password = cur.fetchone()

    hash = fun.hashing(password)
    
    if current_password[0] == hash:
        return False

    cur.execute('UPDATE password SET value=(%s) WHERE user_id=(%s)', (hash, uid))
    con.commit()
    cur.close()
    return True

def if_admin(uid):
    cur = mysql.connection.cursor()
    cur.execute('SELECT role_name FROM user_role WHERE user_id = (%s)',(uid,))
    role = cur.fetchone()
    cur.close()
    if not role is None:
        if role[0] == "Admin":
            return True
        return False
    return False

def if_editor(uid):
    cur = mysql.connection.cursor()
    cur.execute('SELECT role_name FROM user_role WHERE user_id = (%s)',(uid,))
    role = cur.fetchone()
    cur.close()
    if not role is None:
        if role[0] == "Edytor":
            return True
        return False
    return False

def get_full_name(uid):
    cur = mysql.connection.cursor()
    cur.execute('SELECT name, surname, username FROM users WHERE user_id = (%s)',(uid,))
    name = cur.fetchone()
    cur.close()
    return name

def if_password(uid, password):
    cur = mysql.connection.cursor()
    cur.execute('SELECT value FROM password WHERE user_id = (%s)',(uid,))
    passwd = cur.fetchone()
    cur.close()
    if passwd[0] == fun.hashing(password):
        return True
    return False

def get_email_and_username_for_edit_user(data=''):
    cur = mysql.connection.cursor()
    if data != '':
        cur.execute('SELECT user_id, `e-mail`, username FROM users WHERE (`e-mail` = (%s) OR username = (%s)) AND user_id AND name != \'NULL\' NOT IN (SELECT user_id FROM inactive_user)',(data,data))
    else:
        cur.execute('SELECT user_id, `e-mail`, username FROM users WHERE user_id != 0 AND name != \'NULL\' AND user_id NOT IN (SELECT user_id FROM inactive_user)')
    details = cur.fetchall()
    if details is None:
        details = []
    cur.close()
    return details

def get_full_info_user(uid):
    cur = mysql.connection.cursor()
    cur.execute('SELECT users.name, users.surname, users.sex, users.birth_year,users.username,users.`e-mail`,user_role.role_name FROM users LEFT JOIN user_role ON users.user_id=user_role.user_id WHERE users.user_id = (%s)',(uid,))
    data = cur.fetchone()
    cur.close()
    return data

def update_user(uid, name, surname, role, sex, year, changed):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()

    cur.execute('SELECT MAX(user_role_id) FROM user_role')
    max = cur.fetchone()[0]

    cur.execute('SELECT * FROM user_role WHERE user_id=(%s)',(uid,))
    tmp_role = cur.fetchone()
    
    cur.execute('UPDATE users SET name=(%s), surname=(%s), sex=(%s), birth_year=(%s) WHERE user_id=(%s)',(name,surname,sex,year,uid))
    
    if role == 'Tak' and tmp_role is None:
        cur.execute('INSERT INTO user_role VALUES(%s, %s, %s)',(max+1,'Edytor',uid))
    elif role == 'Nie' and not tmp_role is None:
        cur.execute('DELETE FROM user_role WHERE user_id=(%s)',(uid,))
    
    con.commit()
    cur.close()

    if changed == 1:
        email, uname =  get_email_and_username_for_user(uid)       
        fun_mail.edit_user(name, surname, role, sex, str(year), uname, email)

    return 0

def delete_user(uid):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('SELECT name, surname, sex, birth_year,username,`e-mail` FROM users WHERE user_id = (%s)',(uid,))
    data = cur.fetchone()

    cur.execute('DELETE FROM user_role WHERE user_id = (%s)',(uid,))
    cur.execute('DELETE FROM password WHERE user_id = (%s)',(uid,))
    cur.execute('UPDATE poll SET creator=NULL WHERE creator = (%s)',(uid,))
    cur.execute('UPDATE users SET name=NULL, surname=NULL, username=NULL, `e-mail`=NULL WHERE user_id = (%s)',(uid,))
    con.commit()
    cur.close()
    fun_mail.delete_user(data[0],data[1],data[2],data[3],data[4],data[5])
    return 0

def activate_user(pid, code):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('SELECT active_code FROM inactive_user WHERE user_id = (%s)',(pid,))
    base_code = cur.fetchone()

    if base_code[0] == code:
        cur.execute('DELETE FROM inactive_user WHERE user_id = (%s)',(pid,))
        con.commit()
        cur.close()
        return True
    else:
        cur.close()
        return False

def delete_serially_user():
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('SELECT inactive_user.user_id, inactive_user.register_datetime, users.username, users.`e-mail` FROM inactive_user INNER JOIN users ON users.user_id=inactive_user.user_id')
    inactive_users = cur.fetchall()

    if not inactive_users is None:
        users_to_remove = fun.inactivate_user_to_remove(inactive_users)

        for user in users_to_remove:
            cur.execute('DELETE FROM inactive_user WHERE user_id = (%s)',(user[0],))
            cur.execute('DELETE FROM password WHERE user_id = (%s)',(user[0],))
            cur.execute('DELETE FROM users WHERE user_id = (%s)',(user[0],))
            fun_mail.delete_serially_user(user[2], user[3])
        con.commit()
        cur.close()
    else:
        cur.close()
    return 0

def count_users():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM users WHERE name != \'NULL\'')
    users_count = cur.fetchone()
    cur.close()
    return users_count[0]-1 #odejmuję 1 bo rekord inicjalizacyjny w bazie

def count_inactive_users():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM inactive_user')
    inactive_users_count = cur.fetchone()
    cur.close()
    return inactive_users_count[0]

def count_poll():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM poll')
    poll_count = cur.fetchone()
    cur.close()
    return poll_count[0]-1 #odejmuję 1 bo rekord inicjalizacyjny w bazie

def count_active_poll():
    date_time = fun.generate_current_datetime()
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM poll WHERE start_datetime <= (%s) AND end_datetime >= (%s)',(date_time,date_time))
    poll_active_count = cur.fetchone()
    cur.close()
    return poll_active_count[0]

def create_poll(title, description, poll_type, start, end, creator):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()

    cur.execute('SELECT MAX(group_id) FROM `group`')
    id_max = cur.fetchone()[0]+1

    group_name = ("Grupa dla głosowania: " + title + " " + start)

    cur.execute('INSERT INTO `group`(group_id, name) VALUES(%s, %s)', (id_max, group_name))
    cur.execute('INSERT INTO poll(poll_id, title, type, description, group_id, start_datetime, end_datetime, creator) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)',(id_max, title, poll_type, description, id_max, start, end, creator))

    con.commit()
    cur.close()
    return str(id_max)

def get_full_name_for_add_to_poll(data=''):
    cur = mysql.connection.cursor()
    if data != '':
        cur.execute('SELECT user_id, name, surname, username FROM users WHERE username = (%s) AND name != \'NULL\' AND user_id NOT IN (SELECT user_id FROM inactive_user)',(data,))
    else:
        cur.execute('SELECT user_id, name, surname, username FROM users WHERE user_id != 0 AND name != \'NULL\' AND user_id NOT IN (SELECT user_id FROM inactive_user)')
    full_name = cur.fetchall()
    if full_name is None:
        full_name = []
    cur.close()
    return full_name

def added_user_to_poll(poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT user_id FROM user_group WHERE group_id = (%s)',(poll_id,))
    added_user = cur.fetchall()
    if added_user is None:
        added_user = []
    cur.close()
    added_user = fun.list_of_added_user(added_user)
    return added_user

def add_user_for_poll(pid, poll_id):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('SELECT MAX(user_group_id) FROM user_group')
    max_id = cur.fetchone()[0]+1
    cur.execute('INSERT INTO user_group(user_group_id, user_id, group_id, if_voted) VALUES(%s, %s, %s, \'0\')',(max_id,pid,poll_id))
    con.commit()
    cur.close()
    return 0

def delete_user_from_poll(pid, poll_id):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('DELETE FROM user_group WHERE user_id=(%s) AND group_id=(%s)',(pid,poll_id))
    con.commit()
    cur.close()
    return 0

def get_poll_name(poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT title FROM poll WHERE poll_id = (%s)',(poll_id,))
    poll_name = cur.fetchone()[0]
    cur.close()
    return poll_name

def get_group_for_select(current_group, name=''):
    cur = mysql.connection.cursor()
    if name == '':
        cur.execute('SELECT group_id, name FROM `group` WHERE group_id != 0 AND group_id != (%s) ORDER BY group_id DESC',(current_group,))
    else:
        cur.execute('SELECT group_id, name FROM `group` WHERE group_id != 0 AND group_id != (%s) AND name LIKE (%s) ORDER BY group_id DESC',(current_group,("%"+name+"%")))
    groups = cur.fetchall()
    cur.close()
    if groups is None:
        groups = []
    return groups

def get_users_full_name_from_group(group_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT users.name, users.surname, users.username FROM users INNER JOIN user_group ON user_group.user_id=users.user_id WHERE user_group.group_id=(%s) AND users.name != \'NULL\'',(group_id,))
    users = cur.fetchall()
    cur.close()
    if users is None:
        users = []
    return users

def copy_users_from_another_group(group_id, poll_id):
    group_users = added_user_to_poll(group_id)
    poll_users = added_user_to_poll(poll_id)
    count = 0

    for i in group_users:
        if not i in poll_users:
            add_user_for_poll(i, poll_id)
            count = count+1
    return count

def get_polls_for_edit(uid, name=''):
    cur = mysql.connection.cursor()
    time = fun.generate_current_datetime()
    if uid == 0:
        if name == '':
            cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND end_datetime>(%s) ORDER BY start_datetime DESC',(time,))
        else:
            cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND title LIKE (%s) AND end_datetime>(%s) ORDER BY start_datetime DESC',("%"+name+"%",time))
    else:
        if name == '':
            cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND creator=(%s) AND end_datetime>(%s) ORDER BY start_datetime DESC',(uid,time))
        else:
            cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND creator=(%s) AND title LIKE (%s) AND end_datetime>(%s) ORDER BY start_datetime DESC',(uid,"%"+name+"%",time))
    polls = cur.fetchall()
    if polls is None:
        polls = []
    cur.close()
    return polls

def polls_for_user_to_vote(pid):
    cur = mysql.connection.cursor()
    time = fun.generate_current_datetime()
    cur.execute('SELECT poll.poll_id, poll.title, poll.end_datetime FROM poll INNER JOIN user_group ON poll.group_id=user_group.group_id WHERE user_group.user_id=(%s) AND user_group.if_voted!=(%s) AND poll.start_datetime<=(%s) AND poll.end_datetime>=(%s) AND poll.title NOT LIKE (%s) ORDER BY end_datetime ASC',(pid,'1',time,time,"%[UNIEWAŻNIONE]%"))
    polls = cur.fetchall()
    cur.close()
    return remove_wrong_poll_from_list(polls)

def add_question(poll_id, question):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('SELECT MAX(question_id) FROM `question`')
    max_id = cur.fetchone()[0]+1

    cur.execute('INSERT INTO question(question_id,content,poll_id) VALUES (%s,%s,%s)',(max_id,question,poll_id))
    con.commit()
    cur.close()
    return 0

def add_answer(question_id, answer, poll_id):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('SELECT MAX(answers_id) FROM `answers`')
    max_id = cur.fetchone()[0]+1
    
    cur.execute('INSERT INTO answers(answers_id,answer_content,question_id) VALUES(%s,%s,%s)',(max_id,answer,question_id))
    cur.execute('INSERT INTO `results`(`results_id`, `sum`, `answers_id`, `poll_id`) VALUES (%s,%s,%s,%s)',(max_id,0,max_id,poll_id))
    con.commit()
    cur.close()
    return 0

def get_question_name(question_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT content FROM `question` WHERE question_id=(%s)',(question_id,))
    question = cur.fetchone()[0]
    cur.close()
    return question

def get_answer_name(answer_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT answer_content FROM `answers` WHERE answers_id=(%s)',(answer_id,))
    answer = cur.fetchone()[0]
    cur.close()
    return answer

def edit_question(question_id, value):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('UPDATE question SET content= (%s) WHERE question_id = (%s)',(value, question_id))
    con.commit()
    cur.close()
    return 0

def edit_answer(answer_id, value):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('UPDATE answers SET answer_content=(%s) WHERE answers_id=(%s)',(value, answer_id))
    con.commit()
    cur.close()
    return 0

def get_all_answers_for_question(question_id):
    question_with_answers = []
    cur = mysql.connection.cursor()

    cur.execute('SELECT question_id,content FROM `question` WHERE question_id=(%s)',(question_id,))
    question = cur.fetchone()
    question_with_answers.append(question)

    cur.execute('SELECT answers_id,answer_content FROM `answers` WHERE question_id=(%s)',(question_id,))
    answers = cur.fetchall()
    if answers is None:
        answers = []
    question_with_answers.append(answers)

    cur.close()
    return question_with_answers

def get_all_question_with_answers_for_poll(poll_id):
    poll_questions_with_answers = []
    cur = mysql.connection.cursor()

    cur.execute('SELECT question_id FROM `question` WHERE poll_id=(%s)', (poll_id,))
    questions = cur.fetchall()
    cur.close()

    for question in questions:
        poll_questions_with_answers.append(get_all_answers_for_question(question[0]))

    return poll_questions_with_answers

def get_poll_full_info(poll_id):
    poll_questions_with_answers = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT `title`,`type`,`description`,`start_datetime`,`end_datetime`, `creator` FROM poll WHERE poll_id=(%s)',(poll_id,))
    info = cur.fetchone()
    return info

def delete_answer(answer_id):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('DELETE FROM `results` WHERE answers_id=(%s)',(answer_id,))
    cur.execute('DELETE FROM `answers` WHERE answers_id=(%s)',(answer_id,))
    con.commit()
    cur.close()
    return 0

def delete_question(question_id):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('DELETE FROM `results` WHERE answers_id IN (SELECT answers_id FROM `answers` WHERE question_id=(%s))',(question_id,))
    cur.execute('DELETE FROM `answers` WHERE question_id=(%s)',(question_id,))
    cur.execute('DELETE FROM `question` WHERE question_id=(%s)',(question_id,))
    con.commit()
    cur.close()
    return 0

def edit_poll(poll_id, description, poll_type, start, end):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('UPDATE `poll` SET `type`=(%s),`description`=(%s),`start_datetime`=(%s),`end_datetime`=(%s) WHERE `poll_id`=(%s)',(poll_type, description, start, end, poll_id))
    con.commit()
    cur.close()
    return 0

def get_creator_username_and_email_for_poll(poll_id):
    poll_questions_with_answers = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT users.username, users.`e-mail` FROM users INNER JOIN poll ON poll.creator=users.user_id WHERE poll_id=(%s)',(poll_id,))
    creator = cur.fetchone()
    cur.close()
    return creator

def get_polls_for_delete_or_cancel(name=''):
    cur = mysql.connection.cursor()
    time = fun.get_time_for_cancel_poll()
    print(time)
    if name == '':
        cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND end_datetime>(%s) AND title NOT LIKE (%s) ORDER BY end_datetime DESC',(time,"%[UNIEWAŻNIONE]%"))
    else:
        cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND title LIKE (%s) AND end_datetime>(%s) AND title NOT LIKE (%s) ORDER BY end_datetime DESC',("%"+name+"%",time,"%[UNIEWAŻNIONE]%"))
    polls = cur.fetchall()
    if polls is None:
        polls = []
    cur.close()
    return polls

def get_polls_for_tracking(pid, name=''):
    cur = mysql.connection.cursor()
    time = fun.generate_current_datetime()
    if pid == 0:
       if name == '':
           cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND end_datetime>(%s) AND start_datetime<(%s) ORDER BY end_datetime DESC',(time,time))
       else:
           cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND title LIKE (%s) AND end_datetime>(%s) AND start_datetime<(%s) ORDER BY end_datetime DESC',("%"+name+"%",time,time))
    else:
        if name == '':
            cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND creator=(%s) AND start_datetime<(%s) AND end_datetime>(%s) ORDER BY end_datetime DESC',(pid,time, time))
        else:
            cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND creator=(%s) AND title LIKE (%s) AND start_datetime<(%s) AND end_datetime>(%s) ORDER BY end_datetime DESC',(pid,"%"+name+"%",time, time))
    polls = cur.fetchall()
    if polls is None:
        polls = []
    cur.close()
    return polls

def if_not_active_poll(poll_id):
    date_time = fun.get_time_for_edit_poll()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM poll WHERE start_datetime <= (%s) AND end_datetime >= (%s) AND poll_id=(%s)',(date_time,date_time,poll_id))
    active_poll = cur.fetchone()
    cur.close()
    if active_poll is None:
        return True
    else:
        return False

def delete_poll(poll_id):
    creator = get_creator_username_and_email_for_poll(poll_id)
    questions = get_all_question_with_answers_for_poll(poll_id)
    info = get_poll_full_info(poll_id)
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('DELETE FROM `results` WHERE poll_id=(%s)',(poll_id,))
    cur.execute('DELETE FROM `answers` WHERE question_id IN (SELECT question_id FROM question WHERE poll_id=(%s))',(poll_id,))
    cur.execute('DELETE FROM `question` WHERE poll_id=(%s)',(poll_id,))
    cur.execute('DELETE FROM `poll` WHERE poll_id=(%s)',(poll_id,))
    con.commit()
    cur.close()
    fun_mail.added_edited_deleted_poll(creator,"Usunięcie",questions,info)
    return 0

def voting(answers_id, poll_type, uid, poll_id):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()

    cur.execute('SELECT if_voted FROM user_group WHERE user_id=(%s) AND group_id=(%s)',(uid,poll_id))
    voted = cur.fetchone()[0]
    if voted == '1':
         return False

    if poll_type == "Jawne":
        cur.execute('SELECT MAX(vote_id) FROM vote')
        max_id = cur.fetchone()[0]+1
    
    cur.execute('UPDATE `user_group` SET `if_voted`=(%s) WHERE user_id=(%s) AND group_id=(%s)',('1',uid,poll_id))
    for answer_id in answers_id:
        if poll_type == "Jawne":
            cur.execute('INSERT INTO `vote`(`vote_id`, `results_id`, `user_id`) VALUES (%s,%s,%s)',(max_id,answer_id,uid))
            max_id = max_id+1
        cur.execute('UPDATE `results` SET `sum`=`sum`+1 WHERE answers_id=(%s)',(answer_id,))
    
    fun_mail.vote_confirmation(get_email_and_username_for_user(uid),get_poll_full_info(poll_id))
    con.commit()
    cur.close()
    return True

def get_email_and_username_for_user(uid):
     cur = mysql.connection.cursor()
     cur.execute('SELECT `e-mail`, username FROM users WHERE user_id=(%s)',(uid,))
     email_and_username = cur.fetchone()
     cur.close()
     return email_and_username

def voting_canceled(poll_id, uid):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('UPDATE `user_group` SET `if_voted`=(%s) WHERE user_id=(%s) AND group_id=(%s)',('1',uid,poll_id))
    con.commit()
    cur.close()
    return 0

def begin_voting(poll_id, uid):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('UPDATE `user_group` SET `if_voted`=(%s) WHERE user_id=(%s) AND group_id=(%s)',('2',uid,poll_id))
    con.commit()
    cur.close()
    return 0

def get_answers_with_counts(question_id):
    question_with_answers = []
    cur = mysql.connection.cursor()

    cur.execute('SELECT content FROM `question` WHERE question_id=(%s)',(question_id,))
    question = cur.fetchone()
    question_with_answers.append(question)

    cur.execute('SELECT answers.answer_content, results.sum FROM `answers` INNER JOIN results ON answers.answers_id=results.answers_id WHERE answers.question_id=(%s);',(question_id,))
    answers = cur.fetchall()
    question_with_answers.append(answers)

    cur.close()
    return question_with_answers

def get_poll_with_counts(poll_id):
    poll_questions_with_answers = []
    cur = mysql.connection.cursor()

    cur.execute('SELECT question_id FROM `question` WHERE poll_id=(%s)', (poll_id,))
    questions = cur.fetchall()
    cur.close()

    for question in questions:
        poll_questions_with_answers.append(get_answers_with_counts(question[0]))

    return poll_questions_with_answers

def valid_votes(poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT SUM(`sum`) FROM `results` WHERE poll_id=(%s)',(poll_id,))
    cast = cur.fetchone()[0]
    cur.close()
    if cast is None:
        return 0
    return cast

def vote_cast(poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM `user_group` WHERE if_voted!=(%s) AND group_id=(%s)',('0',poll_id))
    cast = cur.fetchone()[0]
    cur.close()
    return cast

def get_question_count(poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM `question` WHERE poll_id=(%s)',(poll_id,))
    count = cur.fetchone()[0]
    cur.close()
    if count == 0:
        return 1
    return count

def get_authorized_users_for_vote_in_poll(poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM `user_group` WHERE group_id=(%s)',(poll_id,))
    cast = cur.fetchone()[0]
    cur.close()
    return cast

def get_polls_for_results(pid, name=''):
    cur = mysql.connection.cursor()
    time = fun.generate_current_datetime()
    if pid == 0:
       if name == '':
           cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND end_datetime<(%s) ORDER BY end_datetime DESC',(time,))
       else:
           cur.execute('SELECT poll_id, title, start_datetime FROM poll WHERE poll_id != 0 AND title LIKE (%s) AND end_datetime<(%s) ORDER BY end_datetime DESC',("%"+name+"%",time))
    else:
        if name == '':
            cur.execute('SELECT DISTINCT poll_id, title, start_datetime FROM poll INNER JOIN user_group ON user_group.group_id=poll.poll_id WHERE poll_id != 0 AND (user_id=(%s) OR creator=(%s)) AND end_datetime<(%s) AND (title NOT LIKE (%s) OR creator=(%s)) ORDER BY end_datetime DESC',(pid,pid,time,"%[UNIEWAŻNIONE]%",pid))
        else:
            cur.execute('SELECT DISTINCT poll_id, title, start_datetime FROM poll INNER JOIN user_group ON user_group.group_id=poll.poll_id WHERE poll_id != 0 AND (user_id=(%s) OR creator=(%s)) AND title LIKE (%s) AND end_datetime<(%s) AND (title NOT LIKE (%s) OR creator=(%s)) ORDER BY end_datetime DESC',(pid,pid,"%"+name+"%",time,"%[UNIEWAŻNIONE]%",pid))
    polls = cur.fetchall()
    if polls is None:
        polls = []
    cur.close()
    return polls

def cancel_poll(poll_id):
    con = mysql.connection
    con.autocommit = False
    cur = con.cursor()
    cur.execute('SELECT title FROM poll WHERE poll_id=(%s)',(poll_id,))
    title = (cur.fetchone()[0] + " [UNIEWAŻNIONE]")
    cur.execute('UPDATE `poll` SET `title`=(%s) WHERE poll_id=(%s)',(title,poll_id))
    con.commit()
    cur.close()
    return 0

def get_answers_for_results(question_id):
    question_with_answers = []
    cur = mysql.connection.cursor()

    cur.execute('SELECT content FROM `question` WHERE question_id=(%s)',(question_id,))
    question = cur.fetchone()
    question_with_answers.append(question)

    cur.execute('SELECT answers.answer_content, results.sum, answers.answers_id FROM `answers` INNER JOIN results ON answers.answers_id=results.answers_id WHERE answers.question_id=(%s);',(question_id,))
    answers = cur.fetchall()
    question_with_answers.append(answers)

    cur.close()
    return question_with_answers

def get_poll_for_results(poll_id):
    poll_questions_with_answers = []
    cur = mysql.connection.cursor()

    cur.execute('SELECT question_id FROM `question` WHERE poll_id=(%s)', (poll_id,))
    questions = cur.fetchall()
    cur.close()

    for question in questions:
        poll_questions_with_answers.append(get_answers_for_results(question[0]))

    return poll_questions_with_answers

def get_question_name_for_answer(answer_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT content FROM question INNER JOIN answers ON answers.question_id=question.question_id WHERE answers_id=(%s)',(answer_id,))
    name = cur.fetchone()[0]
    cur.close()
    return name

def get_poll_name_for_answer(answer_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT title FROM poll INNER JOIN results ON results.poll_id=poll.poll_id WHERE answers_id=(%s)',(answer_id,))
    name = cur.fetchone()[0]
    cur.close()
    return name

def get_users_for_result(result_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT name, surname, username FROM users INNER JOIN vote ON users.user_id=vote.user_id WHERE results_id=(%s)',(result_id,))
    users = cur.fetchall()
    cur.close()
    return users

def get_voters(poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT type FROM poll WHERE poll_id=(%s)',(poll_id,))
    poll_type = cur.fetchone()[0]

    if poll_type == 'Jawne':
        all_users = []
        cur.execute('SELECT question_id FROM question WHERE poll_id=(%s)',(poll_id,))
        questions = cur.fetchall()
        for question in questions:
            all_users.append(get_voters_for_question(question, poll_id))
    else:
        cur.execute('SELECT users.name, users.surname, user_group.if_voted FROM users RIGHT JOIN user_group ON users.user_id=user_group.user_id WHERE group_id=(%s)',(poll_id,))
        all_users = cur.fetchall()
    cur.close()
    return all_users

def get_voters_for_question(question_id, poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT users.name, users.surname, user_group.if_voted, a.answer_content FROM (SELECT users.user_id, answers.answer_content FROM users JOIN vote ON users.user_id=vote.user_id JOIN answers ON answers.answers_id=vote.results_id WHERE answers.question_id=(%s)) as a RIGHT JOIN user_group ON user_group.user_id=a.user_id LEFT JOIN users ON user_group.user_id=users.user_id WHERE user_group.group_id=(%s)',(question_id,poll_id))
    users = cur.fetchall()
    cur.close()
    return users

def remove_wrong_poll_from_list(poll_list):
    inx_to_pop=[]
    for inx, poll in enumerate(poll_list):
        questions = get_all_question_with_answers_for_poll(poll[0])
        if questions == []:
            inx_to_pop.append(inx)
        else:
            for question in questions:
                if len(question[1]) < 2:
                    inx_to_pop.append(inx)
        added_users = added_user_to_poll(poll[0])
        if len(added_users) < 2:
            inx_to_pop.append(inx)
    for i in inx_to_pop:
        poll_list.pop(i)
    return poll_list

def get_questions_for_poll(poll_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT content FROM question WHERE poll_id=(%s)',(poll_id,))
    questions = cur.fetchall()
    cur.close()
    print(questions)
    return questions

def get_answers_for_poll(question_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT answer_content FROM answers WHERE question_id=(%s)',(question_id,))
    answers = cur.fetchall()
    cur.close()
    return answers
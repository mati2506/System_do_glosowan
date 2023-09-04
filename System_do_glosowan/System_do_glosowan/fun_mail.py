from System_do_glosowan import app, fun
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'voteplus.info@gmail.com'
app.config['MAIL_PASSWORD'] = fun.pass_decoder("01010000011100100110111101101010011001010110101101110100010010010101000001011010001100100101111100110010001100000011001000110001")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

mymail = ('System VotePlus','voteplus.info@gmail.com')
footer = "<br><br><br> _____ <br> Pozdrawiamy, <br> zespół VotePlus: Mateusz Kupidura, Krzysztof Majda, Magdalena Rybarczyk i Szymon Sapiecha"

def welcome_message(email,name,username,surname,sex,birth_year, code):
    line1 = "Witaj " + username + ", <br> dziękujemy za rejestrację w systemie, mamy nadzieję, że z naszą pomocą podejmiesz same dobre wybory. <br><br>"
    line2 = "Aby móc kożystać ze swojego konta zaloguj się i podaj kod aktywacyjny dla Twojego konta: " + code + "<br><br><br>"
    line3 = "Poniżej przedstawiamy dane podane przy rejestracji: <br><br>"
    line4 = "<b>Imię i nazwisko:</b> " + name + " " + surname + "<br> <b>Płeć:</b> " + sex + "<br> <b>Rok urodzenia:</b> " + str(birth_year) + "<br><br>"
    line5 = "Jeżeli którekolwiek z przedstawionych powyżej danych się nie zgadzają lub chcesz uzyskać prawo do tworzenia głosowania, prosimy o odpowiedź na tę wiadomość."
    msg = Message("Dziękujemy za rejestrację", sender=mymail, recipients=[email])
    msg.html = (line1 + line2 + line3 + line4 + line5 + footer)
    mail.send(msg)
    return "Sent"

def password_reset(email,username,code):
    line1 = "Witaj " + username + ", <br> Twój kod do zresetowania hasła to: " + code + "<br>"
    line2 = "Jeżeli nie wysyłałeś/aś prośby o zresetowanie hasła, to zignoruj tego maila."
    msg = Message("Resetowanie hasła", sender=mymail, recipients=[email])
    msg.html = (line1 + line2 + footer)
    mail.send(msg)
    return "Sent"

def edit_user(name, surname, role, sex, birth_year, username, email):
    line1 = "Witaj " + username + ", <br> Twoje konto zostało zmodyfikowane. <br><br><br>"
    line2 = "Poniżej przedstawiamy Twoje aktualne dane: <br><br>"
    line3 = "<b>Imię i nazwisko:</b> " + name + " " + surname + "<br> <b>Płeć:</b> " + sex + "<br> <b>Rok urodzenia:</b> " + str(birth_year) + "<br>"
    line4 = "<b>Uprawnienia do tworzenia i zarządania głosowaniami:</b> " + role
    msg = Message("Twoje konto zostało zmodyfikowane", sender=mymail, recipients=[email])
    msg.html = (line1 + line2 + line3 + line4 + footer)
    mail.send(msg)
    return "Sent"

def delete_user(name, surname, sex, birth_year, username, email):
    line1 = "Witaj " + username + ", <br> Twoje konto zostało usunięte: <br><br>"
    line2 = "<b>Imię i nazwisko:</b> " + name + " " + surname + "<br> <b>Płeć:</b> " + sex + "<br> <b>Rok urodzenia:</b> " + str(birth_year) + "<br><br>"
    line3 = "Dziękujemy, że skorzystałeś/aś z usług naszego systemu."
    msg = Message("Twoje konto zostało usunięte", sender=mymail, recipients=[email])
    msg.html = (line1 + line2 + line3 + footer)
    mail.send(msg)
    return "Sent"

def delete_serially_user(username, email):
    line1 = "Witaj " + username + ", <br>"
    line2 = "Ani razu nie zalogowałeś/aś się na swoje konto i nie potwiedziłes rejestracji, dlatego Twoje konto zostało usunięte z naszej bazy. <br>"
    line3 = "Jeżeli chcesz się zarejestrować jeszcze raz, twój adres e-mail oraz nazwa użytkownika zostały odblokowane."
    msg = Message("Twoje konto zostało usunięte", sender=mymail, recipients=[email])
    msg.html = (line1 + line2 + line3 + footer)
    mail.send(msg)
    return "Sent"

def added_edited_deleted_poll(creator, type, questions, poll):
    line1 = "Witaj " + creator[0] + ", <br>"
    line3 = "<b>Tytuł:</b> " + poll[0] + "<br> <b>Opis:</b> " + poll[2] + "<br> <b>Typ:</b> " + poll[1] + "<br> <b>Początek:</b> " + fun.str_for_datetime(poll[3]) + "<br> <b>Koniec:</b> " + fun.str_for_datetime(poll[4]) + "<br><br>"
    line4 = "Lista pytań z odpowiedziami: <br>"
    for question_answers in questions:
        question = question_answers[0][1]
        answers = question_answers[1]
        line4 = line4 + question + "<br>"
        for answer in answers:
            line4 = line4 + answer[1] + "<br>"
    if type == "Dodanie":
        line2 = "Utworzyłeś/aś nowe głosowanie. <br><br> Poniżej przedstawiamy jego dane: <br>"
        msg = Message("Głosowanie zostało utworzone", sender=mymail, recipients=[creator[1]])
    elif type == "Edycja":
        line2 = "Zedytowałeś/aś głosowanie. <br>br> Poniżej przedstawiamy jego aktualne dane: <br>"
        msg = Message("Głosowanie zostało zedytowane", sender=mymail, recipients=[creator[1]])
    elif type == "Usunięcie":
        line2 = "Jedno ze stworzonych przez Ciebie głosowań zostało usunięte. <br><br> Poniżej przedstawiamy jego dane: <br>"
        msg = Message("Głosowanie zostało usunięte", sender=mymail, recipients=[creator[1]])
    msg.html = (line1 + line2 + line3 + line4 + footer)
    mail.send(msg)
    return "Sent"

def vote_confirmation(email_username, poll):
    line1 = "Witaj " + email_username[1] + ", <br>"
    line2 = "Dziękujemy za udział w głosowaniu: <br>"
    line3 = "<b>Tytuł:</b> " + poll[0] + "<br> <b>Opis:</b> " + poll[2] + "<br> <b>Typ:</b> " + poll[1] + "<br><br>"
    line4 = "Wyniki będą możliwe do sprawdzenia na Twoim koncie po: " + fun.str_for_datetime(poll[4])
    msg = Message("Wziąłeś/aś udział w głosowaniu", sender=mymail, recipients=[email_username[0]])
    msg.html = (line1 + line2 + line3 + line4 + footer)
    mail.send(msg)
    return "Sent"
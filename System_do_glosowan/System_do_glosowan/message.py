from System_do_glosowan import app, fun_base

def register_fail_info(i):
    out = [" ", "Konto o takiej nazwie użytkownika już istnieje!", "Konto o takim adresie e-mail już istnieje!"]
    return out[int(i)]

def register_success_info():
    out = ("Udało Ci się poprawnie zarejestrować, na podany adres e-mail została wysłana wiadomość z potwierdzeniem rejestracji" +
          " wraz z kodem potrzebnym do aktywacji konta przy pierwszym logowaniu do systemu.")
    return out

def log_in_fail_info():
    out = "Podane dane logowania są nieprawidłowe!"
    return out

def after_reset_password_info():
    out = "Jeżeli dane w poprzednich krokach zostały podane prawidłowo, Twoje hasło zostało zresetowane."
    return out

def main_page_info():
    out = [" VotePlus to nasz autorski system do obsługi głosowań jawnych i niejawnych.",
           ("Nie wymaga instalacji, gdyż zarządzany jest w całości z poziomu przeglądarki internetowej." + 
            "Przeprowadzaj głosowania łatwiej niż kiedykolwiek wcześniej oraz prezentuj wyniki na przystępnych wykresach!"),
           "Wszystkie pytania prosimy kierować na adres: voteplus.info@gmail.com",
           "Aby oddać głos zaloguj się na swoje konto.",
           "Nie masz konta? Zarejestruj się i korzystaj z pełni funkcjonalności już dziś.",
           "Jesteś już zalogowany. Przejdź do swojego konta lub się wyloguj.", "O aplikacji", "Kontakt", "Sprawdź"]
    return out

def user_page_info():
    out = ["Tu możesz sprawdzić wyniki i statystyki głosowań.", "Tu możesz utworzyć nowe głosowanie.",
           "Tu możesz edytować ustawienia głosowania, pytania i możliwe odpowiedzi oraz dodawać osoby do głosowania.",
           "Tu możesz na bierząco śledzić przebieg oraz statystyki głosowania.",
           "Tu możesz zmienić swoje hasło do systemu.", "Tu możesz wylogować sie z systemu.",
           "Tu możesz nadać bądź odebrać użytkownikom uprawnienia do funkcjonalności systemu oraz usunąć konta użytkowników.",
           "Tu możesz usunąć lub unieważnić głosowanie.", "Tu możesz sprawdzić bierzące informacje o systemie.",
           "Jesteś zalogowany jako:", "Lista aktywnych głosowań:", "Głosowanie aktywne do:", "Brak aktywnych głosowań",
           "Zapraszamy wkrótce", "Utwórz głosowanie", "Edytuj głosowanie", "Śledź przebieg głosowania", "Zarządzaj użytkownikami",
           "Usuń lub unieważnij głosowanie", "Informacje o systemie", "Wyniki i statystyki", "Zmień hasło", "Wyloguj"]
    return out

def change_password_info():
    out = ["Rozpoczynasz procedurę zmiany hasła. Aby tego dokonać, wypełnij poniższy formularz.", "Dotychczasowe hasło:",
           "Nowe hasło:", "Powtórz nowe hasło:", "Siła hasła:"]
    return out

def change_password_success_info():
    out = "Hasło zostało zmienione poprawnie."
    return out

def change_password_fail_info(i):
    out = ["Błąd zmiany hasła. Obecne hasło podane niepoprawnie.", "Błąd zmiany hasła. Nowe hasło identyczne z obecnym."]
    return out[int(i)]

def reset_info():
    out = [("Na swój adres mailowy otrzymałeś/aś wiadomość z kodem umożliwiającym zmianę hasła." +
           "Wpisz go poniżej oraz stwórz nowe hasło."), "Kod z wiadomości e-mail:", "Wprowadź hasło:",
           "Powtórz hasło:", "Siła hasła:", "Kod z wiadomości e-mail"]
    return out

def forgotten_info():
    out = ["Wpisz poniżej adres e-mail przypisany do Twojego konta, a my wyślemy Ci instrukcję resetowania hasła.",
           "Wpisz adres e-mail"]
    return out

def edit_user_info():
    out = ["W poniższym formularzu uzupełnij tylko te dane, które chcesz edytować.", "Edytujesz dane:", "Nazwa użytkownika:",
           "Imię i nazwisko:", "Płeć:", "Rok urodzenia:", "E-mail:", "Rola:", "Brak", "Imię:", "Nazwisko:",
           "Prawo do tworzenia głosowań:"]
    return out

def delete_user_info():
    out = ["Czy chcesz trwale usunąć to konto?", "Usuwasz konto:", "Nazwa użytkownika:", "Imię i nazwisko:", "Płeć:",
           "Rok urodzenia:", "E-mail:", "Rola:", "Brak"]
    return out

def activate_info():
    out = ["Na wprowadzony przez Ciebie adres e-mail, wysłany został kod aktywacyjny. Aby aktywować swoje konto wpisz go poniżej.",
           "Kod aktywacyjny:"]
    return out

def activate_user_fail_info():
    out = "Podany kod aktywacji konta jest nieprawidłowy. Aby ponowić próbę aktywacji, zaloguj się ponownie do systemu."
    return out

def activate_user_success_info():
    out = "Udało Ci się poprawnie aktywować konto. Możesz teraz w pełni korzystać z funkcjonalności systemu."
    return out

def system_info():
    out = ["Liczba głosowań: " + str(fun_base.count_poll()),
           "W tym głosowań aktywnych: " + str(fun_base.count_active_poll()),
           "Liczba kont użytkowników: " + str(fun_base.count_users()),
           "W tym nieaktywnych kont: " + str(fun_base.count_inactive_users()),
           "Głosowania", "Użytkownicy"]
    return out

def group_copy_info():
    out = ["Wybierz grupę, z której użytkownicy zostaną dodani do głosowania", "Brak rekordów",
           "Tu wpisz tytuł głosowania, z którego grupę chcesz skopiować"]
    return out

def copy_users_info(i):
    out = ["Kopiowanie użytkowników zakończone pomyślnie.", (str(i) + " użytkowników zostało dodanych do głosowania.")]
    return out

def delete_question_info():
    out = ["Czy na pewno chcesz usunąć pytanie:", "wraz ze wszystkimi jego odpowiedziami?"]
    return out

def delete_answer_info(question):
    out = [("Czy na pewno chcesz usunąć z pytania (" + question + "), odpowiedź:"), "?"]
    return out

def poll_to_edit_info():
    out = ["Wybierz lub wyszukaj głosowanie które chcesz edytować:", "Lista głosowań które możesz edytować:", "Brak rekordów",
           "Tu wpisz tytuł głosowania, które chcesz wyszukać"]
    return out

def poll_to_delete_info():
    out = ["Wybierz lub wyszukaj głosowanie które chcesz usunąć lub unieważnić:", "Lista głosowań które możesz usunąć lub unieważnić:",
           "Brak rekordów", "Tu wpisz tytuł głosowania, które chcesz wyszukać"]
    return out

def poll_to_tracking_info():
    out = ["Wybierz lub wyszukaj głosowanie które chcesz śledzić:", "Lista głosowań które możesz śledzić:", "Brak rekordów",
           "Tu wpisz tytuł głosowania, które chcesz wyszukać"]
    return out

def change_end_poll_date_fail_info():
    out = "Błąd zmiany czasu końca głosowania. Głosowanie nie może zostać skrócone."
    return out

def voting_fail_info():
    out = "Już wziąłeś udział w tym głosowaniu!"
    return out

def add_answers_info():
    out = ["Dodajesz odpowiedź do pytania", "Treść odpowiedzi:", "Wpisz treść odpowiedzi"]
    return out

def add_questions_info():
    out = ["Dodajesz pytanie do głosowania", "Treść pytania:", "Wpisz treść pytania"]
    return out

def add_users_to_poll_info():
    out = ["Zarządzasz listą uczestników głosowania:", "Tu wpisz nazwę użytkownika którego chcesz wyszukać", "Brak rekordów"]
    return out

def edit_question_answer_info():
    out = ["Edytujesz treść pytania:", "Edytujesz odpowiedź:", "dla pytania:", "Treść pytania:", "Treść odpowiedzi:",
           "Wpisz nową treść"]
    return out

def edit_poll_data_info():
    out = ["Uzupełnij tylko te dane, które chcesz edytować.", "Dane głosowania:", "Tytuł:", "Opis:", "Typ:", "Początek:",
           "Koniec:", "Data rozpoczęcia:", "Godzina rozpoczęcia:", "Data zakończenia:", "Godzina zakończenia:"]
    return out

def copy_group_confirmation_info():
    out = ["Czy chcesz dodać poniższych użytkowników do głosowania:", "Lista uczestników:", "Brak rekordów"]
    return out

def loging_info():
    out = ["Nazwa użytkownika lub adres email:", "Hasło:", "Zapomniałeś/aś hasła?"]
    return out

def voting_info():
    out = [("Poniżej znajduje się lista pytań wraz z możliwymi odpowiedziami. W każdym pytaniu możesz wybrać tylko jedną odpowiedź." +
           "Wybranie odpowiedzi następuje poprzez kliknięcie na pole wyboru znajdujące się przy danej odpowiedzi." +
           "Prosimy udzielić odpowiedzi na wszyskie postawione pytania." +
           "Po dokonaniu wyborów należy nacisnąć przycisk \"Zakończ i wyślij\", aby zakończyć udział w głosowaniu i przesłać swoje odpowiedzi."),
           "Bierzesz udział w głosowaniu:"]
    return out

def poll_out_info():
    out = ["Czy na pewno chcesz opuścić głosowanie:", "bez oddania głosu?", "Późniejsze oddanie głosu nie będzie możliwe."]
    return out

def register_info():
    out = ["Nazwa użytkownika:", "Imię:", "Nazwisko:", "Adres e-mail:", "Wprowadź hasło:", "Powtórz hasło:", "Płeć:",
           "Rok urodzenia:", "Siła hasła:"]
    return out

def track_vote_info():
    out = ["Śledzisz głosowanie:", "Ilość głosów oddanych:", "w tym głosów nieważnych:", "Ilość osób uprawnionych do głosowania:",
           "Ilości odpowiedzi dla poszczególnych pytaniań:", "Ilość głosów:", "Brak odpowiedzi dla tego pytania",
           "Brak pytań dla tego głosowania"]
    return out

def add_poll_info():
    out = ["Formularz tworzenia głosowania", "Typ:", "Data rozpoczęcia:", "Godzina rozpoczęcia:",
           "Data zakończenia:", "Godzina zakończenia:"]
    return out

def delete_poll_info():
    out = ["Czy chcesz usunąć poniższe głosowanie?", "Tytuł:", "Opis:", "Typ:", "Początek:", "Koniec:",
           "Lista pytań z odpowiedziami dla głosowania:", "Brak odpowiedzi dla tego pytania", "Brak pytań dla tego głosowania"]
    return out

def user_search_info():
    out = ["Użytkownicy:", "Brak rekordów", "Tu wpisz emaila lub nazwę użytkownika którego chcesz wyszukać"]
    return out

def poll_menage_info():
    out = ["Edytujesz głosowanie:", "Tytuł:", "Opis:", "Typ:", "Początek:", "Koniec:",
           "Lista pytań z odpowiedziami dla głosowania:", "Brak odpowiedzi dla tego pytania", "Brak pytań dla tego głosowania"]
    return out

def poll_to_results_info():
    out = ["Wybierz lub wyszukaj głosowanie którego wyniki chcesz zobaczyć:", "Lista głosowań których wyniki możesz zobaczyć:",
           "Brak rekordów", "Tu wpisz tytuł głosowania, które chcesz wyszukać"]
    return out

def cancel_poll_info():
    out = ["Czy chcesz unieważnić poniższe głosowanie?", "Tytuł:", "Opis:", "Typ:", "Początek:", "Koniec:",
           "Lista pytań z odpowiedziami dla głosowania:", "Brak odpowiedzi dla tego pytania", "Brak odpowiedzi dla tego pytania"]
    return out

def poll_duration_time_fail_info():
    out = "Błąd zmiany czasów ograniczających głosowanie. Głosowanie musi trwać minimum 5 minut."
    return out

def poll_start_datetime_error_info():
    out = "Błąd zmiany daty początku głosowania. Głosowanie może się zacząć najwcześniej za 10 minut od aktualnego czasu."
    return out

def follow_users_for_answer_info():
    out = ["Obserwujesz listę użytkowników, który głosowali na:", "w pytaniu:", "dla głosowania:", "Lista użytkowników:",
           "Brak użytkowników"]
    return out

def poll_results_info():
    out = ["Tytuł głosowania:", "Opis:", "Typ:", "Początek:", "Koniec:", "Liczba osób uprawnionych do głosowania:",
           "Oddanych głosów:", "w tym głosów nieważnych:", "Lista pytań z odpowiedziami dla głosowania:",
           "Brak odpowiedzi dla tego pytania", "Brak pytań dla tego głosowania"]
    return out

def edit_poll_error_info(type):
    if type == "No questions":
        info = "Nie możesz dodać głosowania bez ani jednego pytania"
    elif type == "Too less answers":
        info = "Nie możesz dodać głosowania, w którym pytania nie mają przynajmniej dwóch odpowiedzi"
    else:
        info = "Nie możesz dodać głosowania, w którym biorą udział mniej niż dwaj uczestnicy"
    return info

def server_error_info(e):
    out = ["UPS", "Coś poszło nie tak", e]
    return out

def question_error_info():
    out = "Takie pytanie już istnieje w tym głosowaniu"
    return out

def answer_error_info():
    out = "Taka odpowiedź już istnieje w tym pytaniu"
    return out

def pdf_info():
    out = ["Tytuł głosowania:", "Opis:", "Typ:", "Początek:", "Koniec:", "Liczba osób uprawnionych do głosowania:",
           "Oddanych głosów:", "w tym głosów nieważnych:", "Lista pytań z odpowiedziami:", "Brak odpowiedzi dla tego pytania",
           "Lista odpowiedzi uczestników głosowania dla pytania:", "Imię", "Nazwisko", "Wybrana odpowiedź", "NN",
           "Nie oddano głosu", "Oddano głos nieważny", "Brak pytań dla tego głosowania", "Lista uczestników głosowania:",
           "Czy na liście obecności?", "Tak", "Nie"]
    return out
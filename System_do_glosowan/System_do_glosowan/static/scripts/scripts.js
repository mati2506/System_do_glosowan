let start_date = document.getElementById('start_date');
if (typeof (start_date) != 'undefined' && start_date != null) {
    let today = new Date();
    let dd = today.getDate();
    let mm = today.getMonth() + 1; //January is 0!
    let yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd
    }
    if (mm < 10) {
        mm = '0' + mm
    }
    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById("start_date").setAttribute("min", today);

}

function setMinimumFinishDate() {
    let startdate = new Date();
    startdate = document.getElementById("start_date").value
    console.log(startdate)
    document.getElementById("finish_date").setAttribute("min", startdate);
}


let lata = document.getElementById('lata');
if (typeof (lata) != 'undefined' && lata != null) {
    let podaj = "Podaj datę urodzenia";
    let x = "",
        i;
    let data = new Date();
    x = x + "<select id=\"user_year\" name=\"user_year\" class=\"formField1\">";
    x = x + "<option selected></option>"
    for (i = 1901; i <= data.getFullYear(); i++) {
        x = x + "<option value=\"" + i + "\">" + i + "</option>"
    }
    x = x + "</select>"
    document.getElementById("lata").innerHTML = x;
}

function checkPassword(registerForm) {
    password1 = registerForm.new_password.value;
    password2 = registerForm.new_password_repeat.value;
    imie = registerForm.user_name.value;
    nazwisko = registerForm.user_surname.value;
    mail = registerForm.user_email.value;
    username = registerForm.username.value;
    if (username != 'undefined' && username != null) {
        let letterNumber = /^[0-9a-zA-Z]+$/;
        if ((!username.match(letterNumber))) {
            Swal.fire({
                title: 'Błąd!',
                text: 'Nazwa użytkownika powinna składać się wyłącznie z liter oraz cyfr!',
                icon: 'error',
                confirmButtonText: 'Powrót'
            })
        }
    }

    if (password1 != password2) {
        Swal.fire({
            title: 'Błąd!',
            text: 'Wpisane hasła nie są identyczne',
            icon: 'error',
            confirmButtonText: 'Powrót'
        })
        return false;
    }
    if (registerForm.user_year.value != 'undefined' && lata != null)
        birthyear = registerForm.user_year.value;
    if (birthyear.length == 0) {
        Swal.fire({
            title: 'Błąd!',
            text: 'Podaj rok urodzenia!',
            icon: 'error',
            confirmButtonText: 'Powrót'
        })
        return false;
    }

    if (typeof (imie) != 'undefined' && imie != null) {
        if (/[^a-zA-ZA-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\- ]/.test(imie)) {
            Swal.fire({
                title: 'Błąd!',
                text: 'Nieprawidłowe znaki w polu "Imię"!',
                icon: 'error',
                confirmButtonText: 'Powrót'
            })
            return false;
        }
    }

    if (typeof (nazwisko) != 'undefined' && nazwisko != null) {
        if (/[^a-zA-ZA-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\- ]/.test(nazwisko)) {
            Swal.fire({
                title: 'Błąd!',
                text: 'Nieprawidłowe znaki w polu Nazwisko!',
                icon: 'error',
                confirmButtonText: 'Powrót'
            })
            return false;
        }
    }

    if (typeof (mail) != 'undefined' && mail != null) {
        if (!/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(mail) || +!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail)) {
            Swal.fire({
                title: 'Błąd!',
                text: 'Nieprawidłowy adres email!',
                icon: 'error',
                confirmButtonText: 'Powrót'
            })
            return false;
        }
    }
}

let calculateComplexity = function (password) {
    let complexity = 0;
    let regExps = [
        /[a-z]/,
        /[A-Z]/,
        /[0-9]/,
        /.{8}/,
        /[!-//:-@[-`{-ÿ]/
    ];
    regExps.forEach(function (regexp) {
        if (regexp.test(password)) {
            complexity++;
        }
    });
    return {
        value: complexity,
        max: regExps.length
    };
};

let checkPasswordStregth = function (password) {
    let progress = document.querySelector('#passwordComplexity'),
        complexity = calculateComplexity(this.value);
    progress.value = complexity.value;
    progress.max = complexity.max;
};

let input = document.querySelector('#new_password');
if (typeof (input) != 'undefined' && input != null)
    input.addEventListener('keyup', checkPasswordStregth);

function checkDates() {
    let startDate = new Date(document.getElementById("start_date").value)
    let finishDate = new Date(document.getElementById("finish_date").value)
    let formStartTime = document.getElementById("start_time").value
    let formFinishTime = document.getElementById("finish_time").value
    let startTimeHour = formStartTime[0].concat(formStartTime[1])
    let startTimeMinute = formStartTime[3].concat(formStartTime[4])
    let finishTimeHour = formFinishTime[0].concat(formFinishTime[1])
    let finishTimeMinute = formFinishTime[3].concat(formFinishTime[4])
    startDate.setHours(parseInt(startTimeHour))
    startDate.setMinutes(parseInt(startTimeMinute))
    finishDate.setHours(parseInt(finishTimeHour))
    finishDate.setMinutes(parseInt(finishTimeMinute))
    let now = new Date();
    if (startDate > finishDate) {
        Swal.fire({
            title: 'Błąd!',
            text: 'Data końca głosowania jest wcześniejsza niż data rozpoczęcia!',
            icon: 'error',
            confirmButtonText: 'Powrót'
        })
        return false
    }
    if (startDate < now) {
        Swal.fire({
            title: 'Błąd!',
            text: 'Podana data rozpoczęcia głosowania jest z przeszłości. Podaj datę co najmniej o 10 minut póżniejszą od aktualnej!',
            icon: 'error',
            confirmButtonText: 'Powrót'
        })
        return false
    }
    if (finishDate - startDate < 300000) {
        Swal.fire({
            title: 'Błąd!',
            text: 'Minimalny czas trwania głosowania wynosi 5 minut!',
            icon: 'error',
            confirmButtonText: 'Powrót'
        })
        return false
    }
    if (startDate - now < 600000) {
        Swal.fire({
            title: 'Błąd!',
            text: 'Minimalny czas startu głosowania od teraz to 10 minut!',
            icon: 'error',
            confirmButtonText: 'Powrót'
        })
        return false
    }
}

function charcountusername(str) {
    let lng = str.length;
    document.getElementById("counterUsername").innerHTML = lng + '/100';
}

function charcountuser_name(str) {
    let lng = str.length;
    document.getElementById("counterUser_name").innerHTML = lng + '/50';
}

function charcountusersurname(str) {
    let lng = str.length;
    document.getElementById("counterUsersurname").innerHTML = lng + '/50';
}

function charcountTitle(str) {
    let lng = str.length;
    document.getElementById("counterTitle").innerHTML = lng + '/60';
}

function charcountMore(str) {
    let lng = str.length;
    document.getElementById("counterMore").innerHTML = lng + '/480';
}
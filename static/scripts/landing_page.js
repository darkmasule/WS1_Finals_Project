const register_cta = document.getElementById("register_cta");
const login_cta = document.getElementById("login_cta");

const registration_form = document.getElementById("registration_form");
const login_form = document.getElementById("login_form");

const register_form_swap = document.getElementById("form_register_cta")
const login_form_swap = document.getElementById("form_login_cta")

register_cta.addEventListener("click", function () {
  login_form.close();
  registration_form.showModal();
});

login_cta.addEventListener("click", function () {
  registration_form.close();
  login_form.showModal();
});

registration_form.addEventListener("click", function (event) {
  if (event.target === registration_form) {
    registration_form.close();
  }
});

login_form.addEventListener("click", function (event) {
  if (event.target === login_form) {
    login_form.close();
  }
});

register_form_swap.addEventListener("click", function () {
  login_form.close();
  registration_form.showModal();
});

form_login_cta.addEventListener("click", function () {
  registration_form.close();
  login_form.showModal();
});
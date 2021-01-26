const inp = document.querySelector("#passwordField");
const btn = document.querySelector("#show-addon");

btn.addEventListener("click", () => {
    if (btn.innerHTML == "SHOW") {
        btn.innerHTML = ""
        btn.innerHTML = "HIDE"
        inp.type = "text"
    } else if (btn.innerHTML == "HIDE") {
        btn.innerHTML = ""
        btn.innerHTML = "SHOW"
        inp.type = "password"
    }
})

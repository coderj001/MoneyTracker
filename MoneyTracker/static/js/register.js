console.log("Register js");
const usernameField = document.querySelector("#usernameField");
const userMsgBoard = document.querySelector("#username-validity-message");

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    if (usernameVal.length > 0) {
        fetch('/auth/username_validation', {
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        }).then(res => res.json()).then(data => {
            if (data.username_error) {
                if (usernameField.classList.contains("is-valid")) {
                    usernameField.classList.replace("is-valid", "is-invalid")
                } else {
                    usernameField.classList.add("is-invalid")
                }
                usernameMsg(data['username_error'], true)
            }
            else if (data.username_exists) {
                if (usernameField.classList.contains("is-valid")) {
                    usernameField.classList.replace("is-valid", "is-invalid")
                } else {
                    usernameField.classList.add("is-invalid")
                }
                usernameMsg(data['username_exists'], true)
            }
            else if (data.username_valid) {
                if (usernameField.classList.contains("is-invalid")) {
                    usernameField.classList.replace("is-invalid", "is-valid")
                } else {
                    usernameField.classList.add("is-valid")
                }
                usernameMsg("", false)
            }
        })
    } else {

        if (usernameField.classList.contains("is-invalid")) {
            usernameField.classList.remove("is-invalid")
        } else {
            usernameField.classList.remove("is-valid")
        }
    }
});

function usernameMsg(msg, stat) {
    if (stat) {
        userMsgBoard.classList.remove("visually-hidden")
        userMsgBoard.classList.add("link-danger")
        if (msg != userMsgBoard.innerHTML) {
            userMsgBoard.innerHTML = ""
            userMsgBoard.innerHTML = msg

        }
        else {
            userMsgBoard.innerHTML = msg
        }
    } else {
        userMsgBoard.classList.add("visually-hidden")
        userMsgBoard.classList.remove("link-danger")
        userMsgBoard.innerHTML = ""
    }
}

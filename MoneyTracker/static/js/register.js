const usernameField = document.querySelector("#usernameField");
const emailField = document.querySelector("#emailField");
const userMsgBoard = document.querySelector("#username-validity-message");
const emailMsgBoard = document.querySelector("#email-validity-message");

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;

  if (usernameVal.length > 0) {
    fetch("/auth/username_validation", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          if (usernameField.classList.contains("is-valid")) {
            usernameField.classList.replace("is-valid", "is-invalid");
          } else {
            usernameField.classList.add("is-invalid");
          }
          usernameMsg(data["username_error"], userMsgBoard, true);
        } else if (data.username_exists) {
          if (usernameField.classList.contains("is-valid")) {
            usernameField.classList.replace("is-valid", "is-invalid");
          } else {
            usernameField.classList.add("is-invalid");
          }
          usernameMsg(data["username_exists"], userMsgBoard, true);
        } else if (data.username_valid) {
          if (usernameField.classList.contains("is-invalid")) {
            usernameField.classList.replace("is-invalid", "is-valid");
          } else {
            usernameField.classList.add("is-valid");
          }
          usernameMsg("", userMsgBoard, false);
        }
      });
  } else {
    if (usernameField.classList.contains("is-invalid")) {
      usernameField.classList.remove("is-invalid");
    } else {
      usernameField.classList.remove("is-valid");
    }
  }
});

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  if (emailVal.length > 0) {
    fetch("/auth/email_validation", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_exists) {
          if (emailField.classList.contains("is-valid"))
            emailField.classList.replace("is-valid", "is-invalid");
          else emailField.classList.add("is-invalid");
          usernameMsg(data["email_exists"], emailMsgBoard, true);
        } else if (data.email_valid) {
          if (emailField.classList.contains("is-invalid"))
            emailField.classList.replace("is-invalid", "is-valid");
          else emailField.classList.add("is-valid");
          usernameMsg("", emailMsgBoard, false);
        }
      });
  } else {
    if (emailField.classList.contains("is-invalid")) {
      emailField.classList.remove("is-invalid");
    } else {
      emailField.classList.remove("is-valid");
    }
  }
});

function usernameMsg(msg, hml, stat) {
  if (stat) {
    hml.classList.remove("visually-hidden");
    hml.classList.add("link-danger");
    if (msg != hml.innerHTML) {
      hml.innerHTML = "";
      hml.innerHTML = msg;
    } else {
      hml.innerHTML = msg;
    }
  } else {
    hml.classList.add("visually-hidden");
    hml.classList.remove("link-danger");
    hml.innerHTML = "";
  }
}

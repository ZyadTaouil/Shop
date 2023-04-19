// Get the form element by id
        var form = document.getElementById("login-form");
        // Add an event listener for submit event
        form.addEventListener("submit", function (event){
            // Get the username and password input elements by id
            var username = document.getElementById("username");
            var password = document.getElementById("password");
            // Get the error message elements by id
            var usernameError =
                document.getElementById("username-error");
            var passwordError =
                document.getElementById("password-error");
            // Clear the error messages
            usernameError.textContent = "";
            passwordError.textContent = "";
            // Validate the username and password values
            if (username.value.length < 3) {
                // Prevent the form from submitting
                event.preventDefault();
                // Set the username error message
                usernameError.textContent = "Username must be at least 3 " +
                    "characters long";
            }
            if (password.value.length < 6) {
                // Prevent the form from submitting
                event.preventDefault();
                // Set the password error message
                passwordError.textContent = "Password must be at least 6 " +
                    "characters long";
            }
        });
// Get the form element by id
var form = document.getElementById("checkout-form");
// Add an event listener for submit event
form.addEventListener("submit", function (event) {
    // Get the input elements by id
    var name = document.getElementById("name");
    var email = document.getElementById("email");
    var phone = document.getElementById("phone");
    var address = document.getElementById("address");
    // Get the error message elements by id
    var nameError = document.getElementById("name-error");
    var emailError = document.getElementById("email-error");
    var phoneError = document.getElementById("phone-error");
    var addressError = document.getElementById("address-error");
    // Clear the error messages
    nameError.textContent = "";
    emailError.textContent = "";
    phoneError.textContent = "";
    addressError.textContent = "";
    // Validate the input values
    if (name.value.length < 3) {
        // Prevent the form from submitting
        event.preventDefault();
        // Set the name error message
        nameError.textContent = "Name must be at least 3 characters long";
    }
    if (!email.value.includes("@")) {
        // Prevent the form from submitting
        event.preventDefault();
        // Set the email error message
        emailError.textContent = "Email must be a valid email address";
    }
    if (phone.value.length < 10) {
        // Prevent the form from submitting
        event.preventDefault();
        // Set the phone error message
        phoneError.textContent = "Phone must be at least 10 digits long";
    }
    if (address.value.length < 10) {
        // Prevent the form from submitting
        event.preventDefault();
        // Set the address error message
        addressError.textContent = "Address must be at least " +
            "10 characters long";
    }
});

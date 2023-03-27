
function copyPasswordToClipboard(inputId, userID){
    var hiddenValue = document.getElementById(inputId);
    hiddenValue.select();
    document.execCommand("copy");    
    //var passtext = hiddenValue.value
    // Call local function defined in views.py
    //var passtext = get_user_password(hiddenValue.value, userID)    
    var url = "/get_user_password/" + inputId + "/"+ userID + "/";
    $.ajax({
        url: url,
        success: function(data) {
            // Copy the password to the clipboard
    navigator.clipboard.writeText(data.password)
    .then(() => {
        //alert("Copied to clipboard!");
      })
    .catch((err) => {
        console.error('Error copying text: ', err);
    });

    }
    });

}

// function copyPasswordToClipboard(){
//     const passwordField = document.getElementById("copy-password-field").innerText;
//     // Create a temporary input element to hold the password
//     var tempInput = document.createElement("input");
//     console.log(element.innerText);
//     tempInput.value = passwordField.value;
//     console.log(tempInput);
//     console.log(tempInput.value);
    
//     // Append the input element to the document
//     document.body.appendChild(tempInput);

//     // Select the input element and copy the password
//     tempInput.select();
//     document.execCommand("copy");

//     // Remove the input element from the document
//     document.body.removeChild(tempInput);
//     navigator.clipboard.writeText(passwordField)
//     //.then(() => alert("Copied to clipboard!"))
//     //.catch((err) => console.error("Could not copy password: ", err));
// }
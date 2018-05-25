function openForm(action) {

    // Hide action buttons and show form
    document.getElementsByClassName("action__select")[0].style.display = 'none';
    document.getElementsByClassName("action__form")[0].style.display = 'inline-block';

    // Include information about action in the form (in a hidden input element)
    document.getElementById("action-info").setAttribute("value", action);
}

function closeForm() {

    // Show action buttons again and hide form
    document.getElementsByClassName("action__select")[0].style.display = 'inline-block';
    document.getElementsByClassName("action__form")[0].style.display = 'none';
}
    var nameInput = document.getElementById("nome");
    var nameValue = nameInput.value.trim();
    var btnCadastrar = document.getElementById("cadastrar-btn");

    if (nameValue === "" || nameValue.length < 2) {
        btnCadastrar.disabled = true;
        return false;
    }

    btnCadastrar.disabled = false;
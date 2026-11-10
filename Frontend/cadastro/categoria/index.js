    var nameInput = document.getElementById("nome");
    var nameValue = nameInput.value.trim();
    var btnCadastrar = document.getElementById("cadastrar-btn");

    function validateName() {
        if (nameValue === "" || nameValue.length < 3) {
            nameInput.setCustomValidity("Por favor, preencha o campo Nome da categoria com pelo menos 3 caracteres.");
            btnCadastrar.disabled = true;
        } else {
            nameInput.setCustomValidity("");
            btnCadastrar.disabled = false;
        }
        nameInput.reportValidity();
    }

    nameInput.addEventListener("input", function() {
        nameValue = nameInput.value.trim();
        validateName();
    });
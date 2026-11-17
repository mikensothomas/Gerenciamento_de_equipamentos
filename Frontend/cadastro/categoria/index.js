
const nameInput = document.getElementById("nome");
const btnCadastrar = document.getElementById("cadastrar-btn");

function validateNameCategory() {
    const nameValue = nameInput.value.trim();

    if (nameValue.length < 3) {
        nameInput.setCustomValidity(
            "Por favor, preencha o campo Nome da categoria com pelo menos 3 caracteres."
        );

        btnCadastrar.disabled = true;
    } else {
        nameInput.setCustomValidity("");
        btnCadastrar.disabled = false;
    }

    nameInput.reportValidity();
}

nameInput.addEventListener("input", validateNameCategory);

btnCadastrar.addEventListener("click", async (e) => {
    e.preventDefault();

    const nameValue = nameInput.value.trim();

    if (nameValue.length < 3) {
        validateNameCategory();
        return;
    }

    const tokenType = localStorage.getItem("token_type");
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        console.error("Token de autenticação não encontrado.");
        return;
    }

    const body = JSON.stringify({
        categoria_name: nameValue
    });

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/criar_categoria",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `${tokenType || "Bearer"} ${accessToken}`
                },
                body: body
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(JSON.stringify(data));
        }

        console.log("Categoria registrada com sucesso!", data);

        window.location.href = "../../solicitacoes/index.html";

    } catch (error) {
        console.error("Erro ao cadastrar categoria:", error);
    }
});
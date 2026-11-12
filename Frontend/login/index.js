
const url_api = "http://127.0.0.1:8000/user_login";

const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");
const btn = document.getElementById("btn");

function validarEmail() {

    const email = emailInput.value.trim();

    if (email !== "") {
        senhaInput.disabled = false;
    } else {
        senhaInput.disabled = true;
        btn.disabled = true;
        senhaInput.value = "";
    }

    validarSenha();
}

function validarSenha() {

    const senha = senhaInput.value.trim();

    btn.disabled = !senha || senhaInput.disabled;
}

emailInput.addEventListener("input", validarEmail);
senhaInput.addEventListener("input", validarSenha);


btn.addEventListener("click", async () => {

    const email = emailInput.value.trim();
    const senha = senhaInput.value;

    btn.disabled = true;

    try {

        const response = await fetch(url_api, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || `Erro HTTP: ${response.status}`);
        }

        emailInput.value = "";
        senhaInput.value = "";

        validarEmail();

        console.log("Login realizado com sucesso:", data);

    } catch (error) {

        console.error("Erro ao fazer login:", error);

    } finally {

        validarEmail();

    }
});
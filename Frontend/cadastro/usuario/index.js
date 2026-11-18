const cpf = document.getElementById("cpf")
const nome = document.getElementById("nome")
const email = document.getElementById("email")
const senha = document.getElementById("senha")
const confirmaSenha = document.getElementById("confirmar-senha")
const enviarDados = document.getElementById("btn-botao")

enviarDados.addEventListener("click", async (e) => {

    e.preventDefault()

    const cpfValor = cpf.value.trim()
    const nomeValor = nome.value.trim()
    const emailValor = email.value.trim()
    const senhaValor = senha.value
    const confirSenhamValor = confirmaSenha.value

    const body = JSON.stringify({
        cpf: cpfValor,
        nome: nomeValor,
        email: emailValor,
        senha: senhaValor
    })

    if (!cpfValor || !nomeValor || !emailValor || !senhaValor || !confirSenhamValor) {
        console.log("Preencha todos os campos")
        return;
    }

    if (senhaValor !== confirSenhamValor) {
        console.log("As senhas têm que ser iguias")
        return;
    }

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/user_register",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: body
            }
        )

        const data = await response.json()

        if (!response.ok) {
            throw new Error(JSON.stringify(data));

        }

        console.log("Cadastro feito com sucesso!", data)

        window.location.href = "../../login/index.html"
    } catch (error) {
        console.error("Erro ao cadastrar o usuári!", error)
    }
})
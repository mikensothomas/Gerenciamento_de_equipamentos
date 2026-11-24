const btn = document.getElementById("btn-cadastro")
const nome = document.getElementById("nome")
const descricao = document.getElementById("descricao")
const status_perfil = document.getElementById("status")

btn.addEventListener("click", async (e) => {
    e.preventDefault()

    const pegarNome = nome.value.trim()
    const pegarDescricao = descricao.value.trim()
    const pegarStatus = status_perfil.value.trim()

    const body = JSON.stringify({
        nome: pegarNome,
        descricao: pegarDescricao,
        status: pegarStatus
    })

    try {
        const response = await fetch("http://localhost:8000/profile_register", {
            method: "post",
            headers: {
                "Content-type": "application/json"
            },
            body: body
        }
        )

        const dados = response.json()

        if(!response.ok){
            throw new Error("Erro ao registrar perfil")
        }

        console.log("Perfil cadastrado com sucesso", dados)
    } catch (error) {
        console.error("Erro", error)
    }
})
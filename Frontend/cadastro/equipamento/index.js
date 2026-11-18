
const botaoEnviar = document.getElementById("btn-enviar")
const nome = document.getElementById("nome")
const patrimonio = document.getElementById("patrimonio")
const marca = document.getElementById("marca")
const modelo = document.getElementById("modelo")
const descricao = document.getElementById("descricao")
const categoria = document.getElementById("categoria")
const quantidade = document.getElementById("quantidade")
const imagem = document.getElementById("imagem")

const tokenType = localStorage.getItem("token_type")
const accessToken = localStorage.getItem("access_token")

botaoEnviar.addEventListener("click", async (e) => {
    e.preventDefault()

    const nomeValor = nome.value.trim()
    const patrimonioValor = patrimonio.value.trim()
    const marcaValor = marca.value.trim()
    const modeloValor = modelo.value.trim()
    const descricaoValor = descricao.value.trim()
    const categoriaValor = categoria.value
    const quantidadeValor = quantidade.value.trim()
    const imagemValor = imagem.files[0]

    if (!nomeValor || !patrimonioValor || !marcaValor || !modeloValor || !descricaoValor || !categoriaValor || !quantidadeValor || !imagemValor) {
        console.log("Preencha todos os campos")
        return
    }

    const formData = new FormData()

    formData.append("nome", nomeValor)
    formData.append("patrimonio", patrimonioValor)
    formData.append("marca", marcaValor)
    formData.append("modelo", modeloValor)
    formData.append("descricao", descricaoValor)
    formData.append("equipamento_categoria_id", categoriaValor)
    formData.append("quantidade", quantidadeValor)
    formData.append("file", imagemValor)

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/salvaEquipamento", {
                method: "POST",
                headers: {
                    "Authorization": `${tokenType || "Bearer"} ${accessToken}`
                },
                body: formData
            }
        )

        const data = await response.json()

        if (!response.ok) {
            throw new Error(JSON.stringify(data))
        }

        console.log("Equipamento registrado com sucesso!", data)

        window.location.href = "../../solicitacoes/index.html"

    } catch (error) {
        console.error("Erro ao cadastrar equipamento:", error)
    }
})


async function carregarCategoria() {
    try {
        const resposta = await fetch("http://127.0.0.1:8000/listar_categoria", {
            method: "GET",
            headers: {
                "Authorization": `${tokenType || "Bearer"} ${accessToken}`
            }
        })

        if (!resposta.ok) {
            throw new Error("Erro ao buscar categorias")
        }

        const categorias = await resposta.json()

        categoria.innerHTML = ""

        categorias.forEach((element, index) => {
            const option = document.createElement("option")

            option.value = element.categoria_id
            option.textContent = element.categoria_name

            if (index === 0) {
                option.selected = true
            }

            categoria.appendChild(option)
        })

    } catch (error) {
        console.error("Erro ao carregar categoria", error)
    }
}

carregarCategoria()
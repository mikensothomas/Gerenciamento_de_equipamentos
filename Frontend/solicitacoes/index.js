
const API_URL = "http://127.0.0.1:8000"

const usuario = getUsuarioLogado()

const nomeUsuario = document.getElementById("nome-usuario")
const imagemUsuario = document.getElementById("imagem-usuario")
const inputFoto = document.getElementById("input-foto")

if (!usuario) {
    nomeUsuario.textContent = "Visitante"
} else {
    nomeUsuario.textContent = usuario.nome
}

function exibirFoto(caminho) {
    imagemUsuario.src = caminho
        ? `${API_URL}${caminho}`
        : "../Assets/user.png"
}

exibirFoto(usuario?.picture)

imagemUsuario.onerror = () => {
    imagemUsuario.onerror = null
    imagemUsuario.src = "../Assets/user.png"
}

inputFoto.addEventListener("change", async () => {

    const arquivo = inputFoto.files[0]

    if (!arquivo) return

    const accessToken = localStorage.getItem("access_token")

    if (!accessToken) {
        alert("Faça login para atualizar sua foto.")
        return
    }

    const formData = new FormData()
    formData.append("picture", arquivo)

    try {
        const response = await fetch(`${API_URL}/update_picture`, {
            method: "PATCH",
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
            body: formData
        })

        const data = await response.json()

        if (!response.ok) {
            throw new Error(data.detail || "Erro ao atualizar a foto.")
        }

        usuario.picture = data.picture_url
        localStorage.setItem("user", JSON.stringify(usuario))

        exibirFoto(usuario.picture)

    } catch (error) {
        console.error("Erro ao atualizar foto:", error)
    } finally {
        inputFoto.value = ""
    }
})
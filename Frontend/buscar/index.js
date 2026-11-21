
const API_URL = "http://127.0.0.1:8000"

const usuario = getUsuarioLogado()

const nomeUsuario = document.getElementById("nome-usuario")
const imagemUsuario = document.getElementById("imagem-usuario")
const inputFoto = document.getElementById("input-foto")
const equipaGoClick = document.getElementById("equipa-go-click")
const logout = document.getElementById("logout")
const atualizar = document.getElementById("atualizar")
const remover = document.getElementById("remover")
const menuUser = document.querySelector(".logout-removeImagem-atualizarImagem")

equipaGoClick.addEventListener("click", (e) => {
    e.preventDefault()

    window.location.href = "../inicio/index.html"
})

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

nomeUsuario.addEventListener("click", (e) => {
    e.stopPropagation()

    menuUser.classList.toggle("ativo")
})

document.addEventListener("click", (e) => {
    menuUser.classList.remove("ativo")
})

logout.addEventListener("click", async (e) => {
    e.preventDefault()

    const accessToken = localStorage.getItem("access_token");
    const refreshToken = localStorage.getItem("refresh_token");

    if (!accessToken || !refreshToken) {
        console.log("Voê não está logado, por favor faça seu login primeiro")
        window.location.href = "../login/index.html"
    }

    try {
        const response = await fetch(`${API_URL}/logout`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                refresh_token: refreshToken
            })
        })

        const data = await response.json()

        if (!response.ok) {
            throw new Error(data.detail || `Erro HTTP: ${response.status}`);
        }

        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("token_type");
        localStorage.removeItem("user");

        window.location.href = "../login/index.html";

    } catch (error) {
        console.error("Error", error)
        window.location.href = "../login/index.html";
    }
})

remover.addEventListener("click", async (e) => {
    e.preventDefault()

    const accessToken = localStorage.getItem("access_token");

    try {
        const response = await fetch(`${API_URL}/remove_pictures`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${accessToken}`
            }
        })

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        imagemUsuario.src = "../Assets/user.png"
        console.log("Foto atualizada com sucesso")

    } catch (error) {
        console.error("Erro ao atualizar a foto", error)
    }
})

atualizar.addEventListener("click", (e) => {
    e.preventDefault()

    inputFoto.click()
})
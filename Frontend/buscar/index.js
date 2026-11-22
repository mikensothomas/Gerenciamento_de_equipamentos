
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
const totalEquipa = document.getElementById("total-equipa")
const pendente = document.getElementById("equipa-pendente")
const manutencao = document.getElementById("equipa-manutencao")
const ativo = document.getElementById("equipa-ativo")
const cardEquipamento = document.getElementById("lista-equipamentos")

const detalhesOverlay = document.getElementById("detalhes-equipamento");
const fecharDetalhes = document.getElementById("fechar-detalhes");

fecharDetalhes.addEventListener("click", () => {
    detalhesOverlay.classList.remove("ativo");
});

detalhesOverlay.addEventListener("click", (e) => {
    if (e.target === detalhesOverlay) {
        detalhesOverlay.classList.remove("ativo");
    }
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        detalhesOverlay.classList.remove("ativo");
    }
});


function obterClasseStatus(status) {
    const situacoes = {
        "Disponivel": "disponivel",
        "Indisponivel": "indisponivel",
        "Manutencao": "manutencao",
        "Reservado": "reservado"
    };

    return situacoes[status] || "status-padrao";
}

async function listarEquipamento() {
    const accessToken = localStorage.getItem("access_token");

    try {
        const response = await fetch(`${API_URL}/listarEquipamento`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
        })

        if (!response.ok) {
            throw new Error("Erro ao listar equipamento")
        }

        const data = await response.json()

        console.log(data)

        return data

    } catch (error) {
        console.error("Error: ", error)
        return []
    }

}

async function mostrarEquipamentos() {
    const equipamentos = await listarEquipamento()

    cardEquipamento.innerHTML = ""

    equipamentos.forEach(element => {
        const card = document.createElement("div")

        const imagemUrl = element.picture
            ? `http://localhost:8000/${element.picture.replace(/^\/+/, "")}`
            : "../Assets/padrao.png";

        card.innerHTML = `
            <img src="${imagemUrl}" alt="${element.nome}">
            
            <p>${element.nome}</p>
            
            <p>${element.descricao}</p>
            
            <span class="status ${obterClasseStatus(element.status_equipamento)}">
                ${element.status_equipamento}
            </span>

            <div class="tag-a">
                <a href="#">Solicitar</a>
                <a href="#" class="btn-detalhes">Detalhes</a>
            </div>
        `
        cardEquipamento.appendChild(card)

        card.querySelector(".btn-detalhes").addEventListener("click", (e) => {
            e.preventDefault();
            mostrarDetalhes(element);
        });
    });
}

async function totalEquipamentos() {
    const equipamentos = await listarEquipamento()

    totalEquipa.textContent = equipamentos.length;

    ativo.textContent = equipamentos.filter(elemento =>
        elemento.status_equipamento === "Disponivel"
    ).length

    manutencao.textContent = equipamentos.filter(elemento =>
        elemento.status_equipamento === "Manutencao"
    ).length

    pendente.textContent = equipamentos.filter(elemento =>
        elemento.status_equipamento === "Reservado"
    ).length
}

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

function mostrarDetalhes(element) {
    document.getElementById("detalhe-id").textContent = element.equipamento_id;
    document.getElementById("detalhe-nome").textContent = element.nome;
    document.getElementById("detalhe-patrimonio").textContent = element.patrimonio;
    document.getElementById("detalhe-marca").textContent = element.marca;
    document.getElementById("detalhe-modelo").textContent = element.modelo;
    document.getElementById("detalhe-descricao").textContent = element.descricao;
    document.getElementById("detalhe-status").textContent = element.status_equipamento;
    document.getElementById("detalhe-categoria").textContent = element.equipamento_categoria_id;
    document.getElementById("detalhe-quantidade").textContent = element.quantidade;

    document.getElementById("detalhes-equipamento").classList.add("ativo");
}

totalEquipamentos()
mostrarEquipamentos()
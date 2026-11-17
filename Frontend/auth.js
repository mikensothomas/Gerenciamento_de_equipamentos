
function getUsuarioLogado() {
    const usuario = localStorage.getItem("user");

    if (!usuario) {
        return null;
    }

    try {
        return JSON.parse(usuario);
    } catch (error) {
        console.error("Erro ao recuperar usuário:", error);
        return null;
    }
}
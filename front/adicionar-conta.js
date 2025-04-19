document.getElementById("form-conta").addEventListener("submit", async function(event) {
    event.preventDefault();

    const dados = {
        nome_titular: document.getElementById("nome_titular").value,
        cpf: document.getElementById("cpf").value,
        data_nascimento: document.getElementById("data_nascimento").value,
        instituicao_bancaria: document.getElementById("instituicao_bancaria").value,
        numero_banco: document.getElementById("numero_banco").value,
        numero_agencia: document.getElementById("numero_agencia").value,
        numero_conta: document.getElementById("numero_conta").value,
        saldo: parseFloat(document.getElementById("saldo").value),
        tipo_chave_pix: document.getElementById("tipo_chave_pix").value,
        chave_pix: document.getElementById("chave_pix").value,
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/contas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados),
        });

        if (response.ok) {
            document.getElementById("mensagem-sucesso").style.display = "block";
            document.getElementById("mensagem-erro").style.display = "none";
            document.getElementById("form-conta").reset();
        } else {
            throw new Error("Erro ao criar conta");
        }
    } catch (error) {
        console.error(error);
        document.getElementById("mensagem-sucesso").style.display = "none";
        document.getElementById("mensagem-erro").style.display = "block";
    }
});

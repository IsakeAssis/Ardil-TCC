document.getElementById("transacaoForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const form = e.target;
    const dados = {
        id_conta_origem: parseInt(form.id_conta_origem.value),
        id_conta_destino: parseInt(form.id_conta_destino.value),
        valor: parseFloat(form.valor.value),
        descricao: form.descricao.value,
        tipo_operacao: "transferencia",
        tipo_transacao: "pix"
      };
      

    try {
      const response = await fetch("http://localhost:8000/transacoes", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
      });

      if (response.ok) {
        const resultado = await response.json();
        document.getElementById("mensagem").innerText = "Transação registrada com sucesso!";
        form.reset();
      } else {
        const erro = await response.json();
        document.getElementById("mensagem").innerText = "Erro: " + (erro.detail || "Erro ao registrar transação.");
      }
      
    } catch (err) {
      console.error(err);
      document.getElementById("mensagem").innerText = "Erro ao registrar transação.";
    }
  });
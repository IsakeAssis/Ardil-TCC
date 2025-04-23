document.getElementById("formulario-historico").addEventListener("submit", async function(e) {
    e.preventDefault();
    const idConta = document.getElementById("input-id-conta-historico").value;

    try {
      const response = await fetch(`http://localhost:8000/transacoes/${idConta}`);
      const transacoes = await response.json();
      const tabela = document.getElementById("tabela-historico-transacoes");
      const corpo = tabela.querySelector("tbody");
      corpo.innerHTML = "";

      if (Array.isArray(transacoes) && transacoes.length > 0) {
        tabela.style.display = "table";

        transacoes.forEach(tx => {
          const linha = `<tr>
            <td>${tx.id_transacao || "—"}</td>
            <td>${tx.tipo_operacao}</td>
            <td>${tx.descricao}</td>
            <td>R$ ${tx.valor.toFixed(2)}</td>
            <td>${new Date(tx.data_operacao).toLocaleString()}</td>
            <td>${tx.id_conta_destino}</td>
            <td>${tx.status_transacao}</td>
          </tr>`;
          corpo.insertAdjacentHTML("beforeend", linha);
        });

        document.getElementById("mensagem-usuario-transacao").innerText = `✅ ${transacoes.length} transação(ões) encontradas para a conta ${idConta}.`;
      } else {
        tabela.style.display = "none";
        document.getElementById("mensagem-usuario-transacao").innerText = "⚠️ Nenhuma transação encontrada para essa conta.";
      }

    } catch (err) {
      console.error(err);
      document.getElementById("mensagem-usuario-transacao").innerText = "❌ Erro ao buscar transações.";
    }
  });
async function carregarContas() {
  try {
      const response = await fetch("http://127.0.0.1:8000/contas");
      if (!response.ok) throw new Error("Erro ao buscar contas");
      const contas = await response.json();

      const lista = document.getElementById("lista-contas");
      lista.innerHTML = ""; // Limpa antes de inserir

      contas.forEach(conta => {
          const item = document.createElement("li");
          item.innerHTML = `
              <strong>Nome:</strong> ${conta.nome_titular}<br>
              <strong>CPF:</strong> ${conta.cpf}<br>
              <strong>Banco:</strong> ${conta.instituicao_bancaria}<br>
              <strong>Agência:</strong> ${conta.numero_agencia} |
              <strong>Conta:</strong> ${conta.numero_conta}<br>
              <strong>Saldo:</strong> R$ ${conta.saldo.toFixed(2)}
          `;
          lista.appendChild(item);
      });
  } catch (error) {
      console.error("Erro ao carregar contas:", error);
  }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("Sistema Bem Estar Farmacêutico Iniciado!");

    // Identifica em qual página estamos pela URL ou por um elemento único
    const path = window.location.pathname;

    if (path.includes("login.html")) {
        configurarLogin();
    } else if (path.includes("compras.html") || path.includes("home.html")) {
        configurarListaProdutos();
    } else if (path.includes("carrinho.html")) {
        renderizarCarrinho();
    }
});

// LÓGICA DE INTEGRAÇÃO 

// Função para salvar no LocalStorage (isso conecta as telas)
function adicionarAoCarrinho(nome, preco, imagem) {
    let carrinho = JSON.parse(localStorage.getItem('itensCarrinho')) || [];
    
    const novoItem = { nome, preco, imagem };
    carrinho.push(novoItem);
    
    localStorage.setItem('itensCarrinho', JSON.stringify(carrinho));
    alert(`${nome} foi adicionado ao carrinho!`);
    window.location.href = "carrinho.html";
}

// LÓGICA POR PÁGINA 

function configurarLogin() {
    const btnEntrar = document.querySelector('.btn-entrar');
    btnEntrar.addEventListener('click', (e) => {
        e.preventDefault();
        const email = document.querySelector('input[type="email"]').value;
        const senha = document.querySelector('input[type="password"]').value;

        if (email && senha) {
            // Salva o nome do usuário para mostrar no Header depois
            localStorage.setItem('usuarioLogado', email.split('@'));
            window.location.href = "home.html";
        } else {
            alert("Preencha os dados de acesso.");
        }
    });
}

function renderizarCarrinho() {
    const container = document.querySelector('.lista-itens');
    const carrinho = JSON.parse(localStorage.getItem('itensCarrinho')) || [];

    if (carrinho.length === 0) {
        container.innerHTML = "<p style='padding:20px; color:white;'>Seu carrinho está vazio.</p>";
        return;
    }

    container.innerHTML = ""; // Limpa o HTML estático

    carrinho.forEach((item, index) => {
        container.innerHTML += `
            <div class="item-carrinho">
                <div class="item-img">
                    <img src="${item.imagem}" alt="${item.nome}">
                </div>
                <div class="item-info">
                    <p class="item-nome">${item.nome}</p>
                    <div class="item-detalhes">
                        <span class="item-preco">R$ ${item.preco.toFixed(2)}</span>
                        <a href="#" class="btn-remover" onclick="removerItem(${index})">remover</a>
                    </div>
                </div>
            </div>
        `;
    });
}

function removerItem(index) {
    let carrinho = JSON.parse(localStorage.getItem('itensCarrinho'));
    carrinho.splice(index, 1);
    localStorage.setItem('itensCarrinho', JSON.stringify(carrinho));
    renderizarCarrinho();
}
document.addEventListener('DOMContentLoaded', () => {
    console.log("Sistema Bem Estar Farmacêutico Iniciado!");

    // Identifica em qual página estamos pela URL ou por um elemento único
    const path = window.location.pathname;

    
if (path.includes("login.html")) {
    configurarLogin();

} else if (path.includes("home.html")) {
    verificarAutenticacao();
    configurarListaProdutos();

}  else if (path.includes("compras.html")) {
    buscarMedicamentos();
    // configurarListaProdutos();

} else if (path.includes("carrinho.html")) {
    renderizarCarrinho();

} else if (path.includes("pagamento.html")) {
    const botao = document.querySelector(".btn-confirmar-final");
    botao.addEventListener("click", finalizarPedido);
}


});

// LÓGICA DE INTEGRAÇÃO 

// Função para salvar no LocalStorage (isso conecta as telas)

function adicionarAoCarrinho(nome, preco, imagem, id_medicamento) {
    let carrinho = JSON.parse(
        localStorage.getItem("itensCarrinho")
    ) || [];

    const novoItem = {
        id_medicamento: id_medicamento,
        nome: nome,
        preco: preco,
        imagem: imagem
    };

    carrinho.push(novoItem);

    localStorage.setItem(
        "itensCarrinho",
        JSON.stringify(carrinho)
    );

    alert(`${nome} foi adicionado ao carrinho!`);

    window.location.href = "carrinho.html";
}


// LÓGICA POR PÁGINA 


async function realizarLogin(email, senha) {
    const resposta = await fetch(
        "http://127.0.0.1:8000/auth/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                senha: senha
            })
        }
    );

    const dados = await resposta.json();


if (!resposta.ok) {
    if (resposta.status === 422) {
        throw new Error(
            "Digite um e-mail válido."
        );
    }

    if (resposta.status === 401) {
        throw new Error(
            "E-mail ou senha incorretos."
        );
    }

    throw new Error(
        "Não foi possível realizar o login."
    );
}

    return dados;
}

function configurarLogin() {
    const btnEntrar = document.querySelector(".btn-entrar");

    btnEntrar.addEventListener("click", async (e) => {
        e.preventDefault();

        const email = document.querySelector(
            'input[type="email"]'
        ).value.trim();

        const senha = document.querySelector(
            'input[type="password"]'
        ).value;

        if (!email || !senha) {
            alert("Preencha o e-mail e a senha.");
            return;
        }

        btnEntrar.disabled = true;
        btnEntrar.textContent = "ENTRANDO...";

        try {
            const resultado = await realizarLogin(email, senha);
            sessionStorage.setItem(
            "access_token",
            resultado.access_token
            );

alert(resultado.mensagem);

window.location.href = "home.html";


        } catch (erro) {
            alert(erro.message);
        } finally {
            btnEntrar.disabled = false;
            btnEntrar.textContent = "ENTRAR";
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

    const total = carrinho.reduce((soma, item) => {
        return soma + Number(item.preco);
    }, 0);

    document.getElementById("total-carrinho").textContent =
    total.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}

function removerItem(index) {
    let carrinho = JSON.parse(localStorage.getItem('itensCarrinho'));
    carrinho.splice(index, 1);
    localStorage.setItem('itensCarrinho', JSON.stringify(carrinho));
    renderizarCarrinho();
}


async function verificarAutenticacao() {
    const token = sessionStorage.getItem("access_token");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {
        const resposta = await fetch(
            "http://127.0.0.1:8000/auth/me",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!resposta.ok) {
            throw new Error("Token inválido ou expirado");
        }

        const usuario = await resposta.json();

        console.log("Usuário autenticado:", usuario.id_cliente);

    
        } catch (erro) {
        console.error("Erro na autenticação:", erro);
        alert("Erro na autenticação: " + erro.message);

        sessionStorage.removeItem("access_token");
        window.location.href = "login.html";
        }

}


async function buscarMedicamentos() {
    const lista = document.getElementById("lista-medicamentos");

    try {
        const resposta = await fetch(
            "http://127.0.0.1:8000/medicines/"
        );

        if (!resposta.ok) {
            throw new Error("Erro ao buscar medicamentos");
        }

        const medicamentos = await resposta.json();

        lista.innerHTML = "";

        if (medicamentos.length === 0) {
            lista.textContent = "Nenhum medicamento disponível.";
            return;
        }

        medicamentos.forEach((medicamento) => {
            const card = document.createElement("div");
            card.className = "card-produto-novo";

            const imagemBox = document.createElement("div");
            imagemBox.className = "card-img-box";

            const imagem = document.createElement("img");
            imagem.src = "../imagens/Logo.png";
            imagem.alt = medicamento.nome;
            imagemBox.appendChild(imagem);

            const titulo = document.createElement("p");
            titulo.className = "card-titulo";
            titulo.textContent =
                `${medicamento.nome} ${medicamento.dosagem}`;

            const preco = document.createElement("span");
            preco.className = "card-preco";
            preco.textContent = medicamento.preco.toLocaleString(
                "pt-BR",
                {
                    style: "currency",
                    currency: "BRL"
                }
            );

            const botao = document.createElement("button");
            botao.className = "btn-comprar";
            botao.textContent = "COMPRAR";

            
            botao.addEventListener("click", () => {
                adicionarAoCarrinho(
                    medicamento.nome,
                    medicamento.preco,
                    imagem.src,
                    medicamento.id_medicamento
                 );
        });


            card.appendChild(imagemBox);
            card.appendChild(titulo);
            card.appendChild(preco);
            card.appendChild(botao);

            lista.appendChild(card);
        });

    } catch (erro) {
        console.error("Erro:", erro);
        lista.textContent = "Erro ao carregar medicamentos.";
    }
}

function prepararItensCheckout() {
    const carrinho = JSON.parse(
        localStorage.getItem("itensCarrinho")
    ) || [];

    const quantidades = {};

    carrinho.forEach(item => {
        const id = item.id_medicamento;

        if (id == null) {
            return;
        }

        if (quantidades[id]) {
            quantidades[id]++;
        } else {
            quantidades[id] = 1;
        }
    });

    return Object.entries(quantidades).map(([id, quantidade]) => ({
        id_medicamento: Number(id),
        quantidade: quantidade
    }));
}


async function finalizarPedido() {
    const token = sessionStorage.getItem("access_token");
    const endereco = document.getElementById("endereco-entrega").value.trim();
    const itens = prepararItensCheckout();
    const botao = document.querySelector(".btn-confirmar-final");

    if (!token) {
        alert("Faça login para finalizar o pedido.");
        window.location.href = "login.html";
        return;
    }

    if (endereco.length < 5) {
        alert("Informe um endereço de entrega válido.");
        return;
    }

    if (itens.length === 0) {
        alert("Seu carrinho está vazio.");
        return;
    }

    botao.disabled = true;
    botao.textContent = "Processando pedido...";

    try {
        const resposta = await fetch(
            "http://127.0.0.1:8000/checkout/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    id_farmacia: 1,
                    endereco_entrega: endereco,
                    itens: itens
                })
            }
        );

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(
                dados.detail || "Não foi possível finalizar o pedido."
            );
        }

        localStorage.removeItem("itensCarrinho");

        alert(
            `Pedido #${dados.id_pedido} criado com sucesso!\n` +
            `Valor dos medicamentos: R$ ${dados.valor_total.toFixed(2)}`
        );

        window.location.href = "home.html";

    } catch (erro) {
        alert("Erro: " + erro.message);
    } finally {
        botao.disabled = false;
        botao.textContent = "Confirmar pedido";
    }
}



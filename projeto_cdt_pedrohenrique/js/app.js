// Renderiza a lista de itens e cuida do formulário.

(function () {

    "use strict";

    // Atualiza o ano do rodapé
    const anoEl = document.getElementById("ano");

    if (anoEl) {
        anoEl.textContent = new Date().getFullYear();
    }


    // Renderiza o cardápio
    const lista = document.getElementById("lista-itens");

    if (lista && Array.isArray(ITENS)) {

        lista.innerHTML = ITENS.map(function (item) {

            return (
                '<li class="card">' +
                    '<h3>' + escapar(item.nome) + '</h3>' +
                    '<p>' + escapar(item.descricao) + '</p>' +
                    '<p class="preco">R$ ' +
                        Number(item.preco).toFixed(2).replace(".", ",") +
                    '</p>' +
                '</li>'
            );

        }).join("");
    }


    // Formulário com validação
    const form = document.querySelector(".form");

    const status = document.getElementById("form-status");

    if (form) {

        form.addEventListener("submit", function (e) {

            e.preventDefault();

            const nome = form.nome.value.trim();

            const email = form.email.value.trim();


            if (!nome || !email) {

                if (status) {
                    status.textContent = "⚠ Preencha nome e e-mail.";
                    status.className = "form-status erro";
                }

                return;
            }


            if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {

                if (status) {
                    status.textContent = "⚠ E-mail inválido.";
                    status.className = "form-status erro";
                }

                return;
            }


            if (status) {
                status.textContent =
                    "✓ Mensagem enviada! Entraremos em contato.";

                status.className = "form-status ok";
            }

            form.reset();

        });
    }


    // Evita problemas com textos inseridos no HTML
    function escapar(txt) {

        const div = document.createElement("div");

        div.textContent =
            String(txt == null ? "" : txt);

        return div.innerHTML;
    }

})();
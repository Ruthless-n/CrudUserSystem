// evento para carregar a lista quando o html for carregado
document.addEventListener('DOMContentLoaded', () => {
    getUsers();
});

// pega o botão de adicionar
const addButton = document.getElementById('addButton');
// adiciona um evento de click no botão de adicionar
addButton.addEventListener('click', createUser);

// função para carregar a lista de usuários
async function getUsers() {
    const userList = document.getElementById('userList');
    userList.innerHTML = ''; // limpa a lista

    const response = await fetch('/usuarios/'); // faz a requisição para a api
    const users = await response.json(); // pega a resposta e transforma em json

    const tableBody = document.getElementById('userTable').getElementsByTagName('tbody')[0]; // pega o corpo da tabela
    tableBody.innerHTML = '';

    //tratamento para quando não houver usuários cadastrados
    if (!users.length) {
        const row = tableBody.insertRow(); // insere uma linha
        const cell = row.insertCell(); // insere uma célula
        cell.textContent = 'Nenhum usuário cadastrado';
        cell.colSpan = 3; // expande a célula para ocupar as 3 colunas
        cell.className = 'empty'; // adiciona a classe empty para estilização
    }

    // para cada usuário, cria uma linha na tabela
    users.forEach(usuario => {
        const row = tableBody.insertRow();

        const cellNome = row.insertCell(0);
        const cellEmail = row.insertCell(1);
        const cellAcoes = row.insertCell(2);
        cellAcoes.className = 'acoes';

        cellNome.textContent = usuario.nome; // adiciona o nome do usuário na célula
        cellEmail.textContent = usuario.email; // adiciona o email do usuário na célula

        const buttonAtualizar = document.createElement('button'); // criação de botão para atualizar
        buttonAtualizar.textContent = 'Atualizar';
        buttonAtualizar.onclick = function () {
            updateUser(usuario.id, usuario.nome, usuario.email);
        };

        const buttonDeletar = document.createElement('button'); // criação de botão para deletar
        buttonDeletar.textContent = 'Deletar';
        buttonDeletar.onclick = function () {
            deleteUsuario(usuario.id);
        };

        cellAcoes.appendChild(buttonAtualizar); // adiciona os botões na célula de ações
        cellAcoes.appendChild(buttonDeletar);
    });
}

// função para criar um usuário
async function createUser() {
    // pega os valores dos inputs de nome e email
    const nome = document.getElementById('name').value; 
    const email = document.getElementById('email').value;

    //tratamento de erro caso algum campo esteja vazio
    if (!nome || !email) {
        alert('Preencha todos os campos!');
        return;
    }

    // faz a requisição para a api
    await fetch('/usuariosAdd/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome, email }),
    });

    //chama a função para atualizar a lista
    getUsers();
}

// função para atualizar um usuário
async function updateUser(id, nome, email) {
    //prompt para pegar os novos valores
    const novoNome = prompt('Novo nome:', nome);
    const novoEmail = prompt('Novo email:', email);

    //tratamento de erro caso algum campo esteja vazio
    if (!novoNome || !novoEmail) {
        alert('Preencha todos os campos!');
        return;
    }

    // faz a requisição para a api enviando os novos valores
    await fetch(`/usuariosAtt/${id}?nome=${novoNome}&email=${novoEmail}`, {
        method: 'PUT',
    });

    getUsers();
}

// função para deletar um usuário

async function deleteUsuario(id) {
    const confirmacao = confirm('Tem certeza que deseja deletar este usuário?'); // confirmação para deletar
    if (confirmacao) {
        await fetch(`/usuarios/${id}`, {
            method: 'DELETE', //requisição para a api enviando o id do usuário
        });

        getUsers();
    }
}



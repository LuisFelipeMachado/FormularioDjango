document.addEventListener('DOMContentLoaded', function () {
    // Função para enviar requisição e atualizar a interface com os dados
    function fetchDashboardData() {
        // Exemplo de como pegar o token JWT (caso esteja logado)
        const token = localStorage.getItem('access_token');  // Armazenando o token no localStorage

        if (!token) {
            alert('Você precisa estar logado!');
            return;
        }

        // Requisição para pegar as métricas do dashboard
        fetch('/api/srq20/relatorio/geral/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(error => {
            console.error('Erro ao buscar os dados do dashboard:', error);
        });
    }

    // Função para atualizar os valores no HTML
    function updateDashboard(data) {
        // Preencher os cards com os valores das métricas
        document.querySelector('#total_respostas').textContent = data.total_respostas;
        document.querySelector('#media_sim').textContent = data.media_respostas_sim;
        document.querySelector('#casos_suspeitos').textContent = data.usuarios_com_potencial_transtorno;
        document.querySelector('#percentual_risco').textContent = data.percentual_de_risco;
    }

    // Adicionar event listener no botão de aplicar filtros
    document.querySelector('#filter-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const dataInicio = document.querySelector('#data_inicio').value;
        const dataFim = document.querySelector('#data_fim').value;

        // Construindo a URL com os parâmetros de filtro
        let url = '/api/srq20/relatorio/geral/?';
        if (dataInicio) url += `data_inicio=${dataInicio}&`;
        if (dataFim) url += `data_fim=${dataFim}`;

        // Requisição para aplicar os filtros no relatório
        fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(error => {
            console.error('Erro ao aplicar os filtros:', error);
        });
    });

    // Carregar os dados quando a página for carregada
    fetchDashboardData();
});

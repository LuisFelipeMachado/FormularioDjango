document.addEventListener('DOMContentLoaded', function () {

    // Função para buscar dados do dashboard
    function fetchDashboardData() {
        const token = localStorage.getItem('access_token');  // Pega o token de autenticação

        if (!token) {
            alert('Você precisa estar logado!');
            return;
        }

        // Enviar requisição para API do Django
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
            console.error('Erro ao carregar dados do dashboard:', error);
        });
    }

    // Função para atualizar as métricas do dashboard
    function updateDashboard(data) {
        document.querySelector('#total_respostas').textContent = data.total_respostas;
        document.querySelector('#media_sim').textContent = data.media_respostas_sim;
        document.querySelector('#casos_suspeitos').textContent = data.usuarios_com_potencial_transtorno;
        document.querySelector('#percentual_risco').textContent = data.percentual_de_risco;
        document.querySelector('#filtros_aplicados').textContent = JSON.stringify(data.filtros_aplicados, null, 2);
    }

    // Função para aplicar filtros ao dashboard
    document.querySelector('#filter-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const dataInicio = document.querySelector('#data_inicio').value;
        const dataFim = document.querySelector('#data_fim').value;

        let url = '/api/srq20/relatorio/geral/?';
        if (dataInicio) url += `data_inicio=${dataInicio}&`;
        if (dataFim) url += `data_fim=${dataFim}`;

        // Requisição com filtros
        fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            updateDashboard(data); // Atualizar o dashboard com os dados filtrados
        })
        .catch(error => {
            console.error('Erro ao aplicar filtros:', error);
        });
    });

    // Função para aplicar animações simples (como mudanças nos números)
    function animateValue(id, start, end, duration) {
        let range = end - start;
        let current = start;
        let increment = end > start ? 1 : -1;
        let stepTime = Math.abs(Math.floor(duration / range));

        let obj = document.querySelector(`#${id}`);
        let timer = setInterval(function () {
            current += increment;
            obj.textContent = current;
            if (current == end) {
                clearInterval(timer);
            }
        }, stepTime);
    }

    // Carregar os dados iniciais
    fetchDashboardData();

});

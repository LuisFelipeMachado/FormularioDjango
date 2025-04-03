document.addEventListener('DOMContentLoaded', () => {

    // 🎯 Botão "Comece Agora"
    const ctaButton = document.querySelector('.cta-button');

    if (ctaButton) {
        // Hover com animação suave
        ctaButton.addEventListener('mouseover', () => {
            ctaButton.style.transition = 'all 0.2s ease-in-out';
            ctaButton.style.transform = 'scale(1.05)';
            ctaButton.style.backgroundColor = '#6D28D9';
        });

        ctaButton.addEventListener('mouseout', () => {
            ctaButton.style.transform = 'scale(1)';
            ctaButton.style.backgroundColor = '#4C1D95';
        });

        // Verifica login ao clicar
        ctaButton.addEventListener('click', (e) => {
            e.preventDefault();
            const token = localStorage.getItem('access_token');

            if (token) {
                window.location.href = '/dashboard/';
            } else {
                window.location.href = '/login/';
            }
        });
    }

    // 🔽 Scroll suave para seções internas
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 60,
                    behavior: 'smooth'
                });
            }
        });
    });

    // 📬 Feedback do formulário de contato
    const form = document.querySelector('form');

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Mensagem enviada com sucesso! Entraremos em contato em breve.');
            form.reset();
        });
    }
});

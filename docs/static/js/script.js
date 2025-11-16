// Общий JavaScript для всех страниц

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeSmoothScrolling();
    initializeAnimations();
    setActiveNavigation();
});

// Плавная прокрутка
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Анимации появления элементов
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Наблюдаем за карточками, секциями и другими элементами
    document.querySelectorAll('.card, .theory-section, .tutorial-section, .concept-card, .advantage-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Установка активного состояния навигации
function setActiveNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--accent-500)';
            link.style.fontWeight = '600';
        }
    });
}

// Утилитарные функции
const Utils = {
    // Показ уведомлений
    showNotification: function(message, type = 'info') {
        const notification = document.getElementById('notification');
        if (!notification) return;
        
        notification.textContent = message;
        notification.className = `notification ${type}`;
        
        // Показываем уведомление
        setTimeout(() => {
            notification.classList.remove('hidden');
        }, 10);
        
        // Скрываем через 5 секунд
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 5000);
    },

    // Форматирование больших чисел
    formatNumber: function(num) {
        return new Intl.NumberFormat().format(num);
    },

    // Копирование в буфер обмена
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showNotification('Скопировано в буфер обмена!', 'success');
        }).catch(err => {
            console.error('Ошибка копирования: ', err);
            this.showNotification('Не удалось скопировать', 'error');
        });
    }
};

// Класс для визуализации эллиптических кривых (для страницы практики)
class EllipticCurveVisualizer {
    constructor() {
        this.canvas = document.getElementById('curveCanvas');
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.points = [];
        this.currentCurve = null;
        
        this.initializeEventListeners();
        this.calculateDefaultCurve();
    }

    initializeEventListeners() {
        const calculateBtn = document.getElementById('calculateCurve');
        const addPointsBtn = document.getElementById('addPoints');
        const doublePointBtn = document.getElementById('doublePoint');
        const multiplyPointBtn = document.getElementById('multiplyPoint');
        const generateKeysBtn = document.getElementById('generateKeys');

        if (calculateBtn) calculateBtn.addEventListener('click', () => this.calculateCurve());
        if (addPointsBtn) addPointsBtn.addEventListener('click', () => this.performOperation('add'));
        if (doublePointBtn) doublePointBtn.addEventListener('click', () => this.performOperation('double'));
        if (multiplyPointBtn) multiplyPointBtn.addEventListener('click', () => this.performOperation('multiply'));
        if (generateKeysBtn) generateKeysBtn.addEventListener('click', () => this.generateKeys());
    }

    async calculateDefaultCurve() {
        await this.calculateCurve();
    }

    async calculateCurve() {
        const a = parseInt(document.getElementById('paramA').value);
        const b = parseInt(document.getElementById('paramB').value);
        const p = parseInt(document.getElementById('paramP').value);

        try {
            const response = await fetch('/api/calculate_curve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ a, b, p })
            });

            const data = await response.json();

            if (data.success) {
                this.points = data.points;
                this.currentCurve = { a, b, p };
                
                document.getElementById('equationDisplay').textContent = data.equation;
                document.getElementById('pointsCount').textContent = `Всего точек: ${data.total_points}`;
                
                this.drawCurve();
                Utils.showNotification('Кривая успешно рассчитана', 'success');
            } else {
                Utils.showNotification('Ошибка: ' + data.error, 'error');
            }
        } catch (error) {
            Utils.showNotification('Ошибка соединения: ' + error.message, 'error');
        }
    }

    drawCurve() {
        // Очистка canvas
        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        const padding = 40;
        const scale = Math.min(
            (this.canvas.width - padding * 2) / (this.currentCurve.p + 1),
            (this.canvas.height - padding * 2) / (this.currentCurve.p + 1)
        );
        
        // Рисуем сетку
        this.ctx.strokeStyle = 'var(--primary-200)';
        this.ctx.lineWidth = 1;
        
        for (let x = 0; x <= this.currentCurve.p; x++) {
            const screenX = x * scale + padding;
            this.ctx.beginPath();
            this.ctx.moveTo(screenX, padding);
            this.ctx.lineTo(screenX, this.canvas.height - padding);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= this.currentCurve.p; y++) {
            const screenY = y * scale + padding;
            this.ctx.beginPath();
            this.ctx.moveTo(padding, screenY);
            this.ctx.lineTo(this.canvas.width - padding, screenY);
            this.ctx.stroke();
        }
        
        // Рисуем оси
        this.ctx.strokeStyle = 'var(--primary-600)';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(padding, padding);
        this.ctx.lineTo(padding, this.canvas.height - padding);
        this.ctx.moveTo(padding, this.canvas.height - padding);
        this.ctx.lineTo(this.canvas.width - padding, this.canvas.height - padding);
        this.ctx.stroke();
        
        // Подписи осей
        this.ctx.fillStyle = 'var(--primary-600)';
        this.ctx.font = '12px Inter';
        this.ctx.fillText('x', this.canvas.width - padding + 5, this.canvas.height - padding + 15);
        this.ctx.fillText('y', padding - 15, padding - 5);
        
        // Рисуем точки кривой
        this.points.forEach(point => {
            const [x, y] = point;
            const screenX = x * scale + padding;
            const screenY = (this.currentCurve.p - y) * scale + padding; // Инвертируем Y
            
            this.ctx.fillStyle = 'var(--accent-500)';
            this.ctx.beginPath();
            this.ctx.arc(screenX, screenY, 4, 0, 2 * Math.PI);
            this.ctx.fill();
            
            // Подписываем точки с координатами
            this.ctx.fillStyle = 'var(--text-secondary)';
            this.ctx.font = '10px Inter';
            this.ctx.fillText(`(${x},${y})`, screenX + 6, screenY - 6);
        });
        
        // Подписываем значения на осях
        this.ctx.fillStyle = 'var(--text-tertiary)';
        this.ctx.font = '10px Inter';
        for (let i = 0; i <= this.currentCurve.p; i++) {
            if (i % 2 === 0) { // Подписываем каждое второе значение для читаемости
                const xPos = i * scale + padding;
                const yPos = this.canvas.height - padding + 15;
                this.ctx.fillText(i.toString(), xPos - 3, yPos);
                
                const yLabelPos = padding - 5;
                this.ctx.fillText((this.currentCurve.p - i).toString(), padding - 15, (i * scale) + padding + 3);
            }
        }
    }

    async performOperation(operation) {
        if (!this.currentCurve) {
            Utils.showNotification('Сначала рассчитайте кривую', 'error');
            return;
        }

        const point1 = [
            parseInt(document.getElementById('point1X').value),
            parseInt(document.getElementById('point1Y').value)
        ];
        
        const point2 = [
            parseInt(document.getElementById('point2X').value),
            parseInt(document.getElementById('point2Y').value)
        ];
        
        const k = parseInt(document.getElementById('scalarK').value);

        try {
            const response = await fetch('/api/calculate_point_operations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    a: this.currentCurve.a,
                    b: this.currentCurve.b,
                    p: this.currentCurve.p,
                    point1: point1,
                    point2: point2,
                    k: k,
                    operation: operation
                })
            });

            const data = await response.json();

            if (data.success) {
                let resultText = '';
                
                switch(operation) {
                    case 'add':
                        resultText = `P + Q = (${point1[0]},${point1[1]}) + (${point2[0]},${point2[1]}) = ${data.result ? `(${data.result[0]},${data.result[1]})` : 'O (бесконечность)'}`;
                        break;
                    case 'double':
                        resultText = `2P = 2 * (${point1[0]},${point1[1]}) = ${data.result ? `(${data.result[0]},${data.result[1]})` : 'O (бесконечность)'}`;
                        break;
                    case 'multiply':
                        resultText = `kP = ${k} * (${point1[0]},${point1[1]}) = ${data.result ? `(${data.result[0]},${data.result[1]})` : 'O (бесконечность)'}`;
                        break;
                }
                
                document.getElementById('operationResult').textContent = resultText;
                Utils.showNotification('Операция выполнена успешно', 'success');
            } else {
                document.getElementById('operationResult').textContent = 'Ошибка: ' + data.error;
                Utils.showNotification('Ошибка операции: ' + data.error, 'error');
            }
        } catch (error) {
            Utils.showNotification('Ошибка соединения: ' + error.message, 'error');
        }
    }

    async generateKeys() {
        if (!this.currentCurve) {
            Utils.showNotification('Сначала рассчитайте кривую', 'error');
            return;
        }

        const generator = [
            parseInt(document.getElementById('generatorX').value),
            parseInt(document.getElementById('generatorY').value)
        ];

        try {
            const response = await fetch('/api/generate_ecc_keys', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    a: this.currentCurve.a,
                    b: this.currentCurve.b,
                    p: this.currentCurve.p,
                    generator: generator
                })
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById('privateKey').textContent = data.private_key;
                document.getElementById('publicKey').textContent = `(${data.public_key[0]}, ${data.public_key[1]})`;
                Utils.showNotification('Ключи успешно сгенерированы', 'success');
            } else {
                Utils.showNotification('Ошибка генерации ключей: ' + data.error, 'error');
            }
        } catch (error) {
            Utils.showNotification('Ошибка соединения: ' + error.message, 'error');
        }
    }
}

// Инициализация визуализатора на странице практики
if (document.getElementById('curveCanvas')) {
    document.addEventListener('DOMContentLoaded', () => {
        new EllipticCurveVisualizer();
    });
}
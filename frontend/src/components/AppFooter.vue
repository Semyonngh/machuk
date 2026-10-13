<template>
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h4>SOUNDSTAGE</h4>
                <p>Организация концертов и продажа билетов на музыкальные события по всей России.</p>
            </div>

            <div class="footer-section">
                <h4>Концерты</h4>
                <ul class="footer-links">
                    <li><router-link to="/">Все концерты</router-link></li>
                    <li><router-link to="/">По артистам</router-link></li>
                    <li><router-link to="/">По городам</router-link></li>
                </ul>
            </div>

            <div class="footer-section">
                <h4>Помощь</h4>
                <ul class="footer-links">
                    <li><router-link to="/">Как купить билет</router-link></li>
                    <li><router-link to="/">Возврат билетов</router-link></li>
                    <li><router-link to="/">Правила посещения</router-link></li>
                </ul>
            </div>

            <div class="footer-section">
                <h4>Партнёрам</h4>
                <ul class="footer-links">
                    <li><router-link to="/">Организаторам</router-link></li>
                    <li><router-link to="/">Артистам</router-link></li>
                    <li><router-link to="/">Реклама</router-link></li>
                </ul>
            </div>
        </div>

        <div class="copyright">
            <p>SOUNDSTAGE © 2015-2025</p>
            <div class="footer-email">concert@soundstage.ru</div>
        </div>
    </footer>
</template>
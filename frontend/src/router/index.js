import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TicketsView from '../views/TicketsView.vue'
import OrderSuccessView from '../views/OrderSuccessView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import ConcertView from '../views/ConcertView.vue'


const routes = [
    { path: '/', name: 'home', component: HomeView },
    { path: '/tickets', name: 'tickets', component: TicketsView },
    { path: '/order-success/:id', name: 'order-success', component: OrderSuccessView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/profile', name: 'profile', component: ProfileView },
    { path: '/concert/:id', name: 'concert', component: ConcertView },

]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) return savedPosition
        return { top: 0 }
    },
})

export default router
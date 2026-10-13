import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TicketsView from '../views/TicketsView.vue'
import OrderSuccessView from '../views/OrderSuccessView.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView,
    },
    {
        path: '/tickets',
        name: 'tickets',
        component: TicketsView,
    },
    {
        path: '/order-success/:id',
        name: 'order-success',
        component: OrderSuccessView,
    },
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
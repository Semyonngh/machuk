import axios from 'axios'

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
})

export default {
    getConcerts() {
        return api.get('concerts/')
    },
    getConcert(id) {
        return api.get(`concerts/${id}/`)
    },
    searchConcerts(query) {
        return api.get('concerts/search/', { params: { q: query } })
    },
    getArtists() {
        return api.get('artists/')
    },
    getVenues() {
        return api.get('venues/')
    },
    getCategories() {
        return api.get('categories/')
    },
    buyTicket(concertId, data) {
        return api.post(`concerts/${concertId}/buy/`, data)
    },
    getOrder(orderId) {
        return api.get(`orders/${orderId}/`)
    },
    getFilters() {
        return api.get('filters/')
    },
    getConcertsFiltered(params) {
        return api.get('concerts/', { params })
    },
    getOrdersByEmail(email) {
        return api.get(`orders/by-email/${email}/`)
    },
}
import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import ItemPage from '../views/ItemPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import CreateItemPage from '../views/CreateItemPage.vue';
import MyAuctionsPage from '../views/MyAuctionsPage.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        {
            path: '/items/:id',
            name: 'item',
            component: ItemPage,
            props: true,
        },
        {
            path: '/profile',
            name: 'profile',
            component: ProfilePage,
        },
        {
            path: '/create',
            name: 'create',
            component: CreateItemPage,
        },
        {
            path: '/my-auctions',
            name: 'my-auctions',
            component: MyAuctionsPage,
        },
    ],
});

export default router;
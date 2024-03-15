import VueRouter from 'vue-router';
import pageOne from "@/components/pageOne";
import HelloWorld from "@/components/HelloWorld";

export const routes = [
    {
        path: "/",
        component: HelloWorld,
        name: 'HelloWorld',
    },
    {
        path: "/page1",
        component: pageOne,
        name: 'pageOne',
    },
]

const router = new VueRouter({
    history: VueRouter.createWebHistory,
    base: process.env.BASE_URL,
    routes
})

export default router
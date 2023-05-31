import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/team',
      name: 'team',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/TeamView.vue')
    },
    {
      path: '/region',
      name: 'region',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/RegionView.vue')
    },
    {
      path: '/social-distancing',
      name: 'social-distancing',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/SocialDistancingView.vue')
    },
    {
      path: '/infection-status',
      name: 'infection-status',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/InfectionStatusView.vue')
    },
    {
      path: '/vaccine-selection',
      name: 'vaccine-selection',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineSelectionView.vue')
    },
    {
      path: '/vaccine-check',
      name: 'vaccine-check',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineCheckView.vue')
    },
    {
      path: '/vaccination-by-age', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccination-by-age',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccinationByAgeView.vue')
    },
    {
      path: '/vaccination-efficacy-precheck', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccination-efficacy-precheck',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineEfficacyPreCheckView.vue')
    },
    {
      path: '/vaccine-efficacy', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccine-efficacy',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineEfficacyView.vue')
    },
    {
      path: '/vaccine-availability', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccine-availability',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineAvailabilityTimelineView.vue')
    },
    {
      path: '/vaccine-plan-period', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccine-plan-period',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccinePlanPeriodView.vue')
    },
    {
      path: '/vaccine-strategy', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccine-strategy',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineStrategyView.vue')
    },
    {
      path: '/additional-parameters', //'/vaccination-by-age/:groupIndex?',
      name: 'additional-parameters',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AdditionalParametersView.vue')
    },
    {
      path: '/result', //'/vaccination-by-age/:groupIndex?',
      name: 'result',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ResultView.vue')
    },
    {
      path: '/reference',
      name: 'reference',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ReferenceView.vue')
    },
    {
      path: '/disclaimer',
      name: 'disclaimer',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/DisclaimerView.vue')
    },
    {
      path: '/dev-history',
      name: 'dev-history',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/DevHistoryView.vue')
    }
  ]
})

export default router

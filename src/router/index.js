import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Home',
      }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      meta: {
        title: 'About',
      }
    },
    {
      path: '/team',
      name: 'team',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/TeamView.vue'),
      meta: {
        title: 'Team',
      }
    },
    {
      path: '/region',
      name: 'region',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/RegionView.vue'),
      meta: {
        title: 'Region',
      }
    },
    {
      path: '/social-distancing',
      name: 'social-distancing',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/SocialDistancingView.vue'),
      meta: {
        title: 'Social distancing',
      }
    },
    {
      path: '/infection-status',
      name: 'infection-status',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/InfectionStatusView.vue'),
      meta: {
        title: 'Infection status',
      }
    },
    {
      path: '/vaccine-selection',
      name: 'vaccine-selection',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineSelectionView.vue'),
      meta: {
        title: 'Vaccine options',
      }
    },
    {
      path: '/vaccine-check',
      name: 'vaccine-check',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineCheckView.vue'),
      meta: {
        title: 'Vaccine situation',
      }
    },
    {
      path: '/vaccination-by-age', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccination-by-age',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccinationByAgeView.vue'),
      meta: {
        title: 'Previously vaccination',
      }
    },
    {
      path: '/vaccination-efficacy-precheck', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccination-efficacy-precheck',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineEfficacyPreCheckView.vue'),
      meta: {
        title: 'Vaccination situation',
      }
    },
    {
      path: '/vaccine-efficacy', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccine-efficacy',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineEfficacyView.vue'),
      meta: {
        title: 'Vaccine effectiveness',
      }
    },
    {
      path: '/vaccine-availability', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccine-availability',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineAvailabilityTimelineView.vue'),
      meta: {
        title: 'Vaccine availability',
      }
    },
    {
      path: '/vaccine-plan-period', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccine-plan-period',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccinePlanPeriodView.vue'),
      meta: {
        title: 'Simulation period',
      }
    },
    {
      path: '/vaccine-strategy', //'/vaccination-by-age/:groupIndex?',
      name: 'vaccine-strategy',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VaccineStrategyView.vue'),
      meta: {
        title: 'Vaccine strategy',
      }
    },
    {
      path: '/additional-parameters', //'/vaccination-by-age/:groupIndex?',
      name: 'additional-parameters',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AdditionalParametersView.vue'),
      meta: {
        title: 'Additional parameters',
      }
    },
    {
      path: '/result', //'/vaccination-by-age/:groupIndex?',
      name: 'result',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ResultView.vue'),
      meta: {
        title: 'Simulated outcome',
      }
    },
    {
      path: '/reference',
      name: 'reference',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ReferenceView.vue'),
      meta: {
        title: 'References',
      }
    },
    {
      path: '/disclaimer',
      name: 'disclaimer',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/DisclaimerView.vue'),
      meta: {
        title: 'Disclaimer',
      }
    },
    {
      path: '/dev-history',
      name: 'dev-history',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/DevHistoryView.vue'),
      meta: {
        title: 'Development history',
      }
    }
  ]
})

/*
router.beforeEach((to, from, next) => {
  //document.title = to.meta != undefined && to.meta.title != undefined? to.meta.title: 'Default Title'
  
  const titleFromParams = to.params?.pageTitle

  if (titleFromParams) {
    document.title = `${titleFromParams} - ${document.title}`
  } else {
    document.title = to.meta?.title ?? 'Default Title'
  }
  
})
*/

export default router

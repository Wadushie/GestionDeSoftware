const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'categoria', component: () => import('pages/CategoriaPage.vue') },
      { path: 'proveedor', component: () => import('pages/ProveedorPage.vue') },
      { path: 'producto', component: () => import('pages/ProductoPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes

import { AccountLayout, AccountLogin, AccountCallback } from '../account'

export default {
  path: '/account',
  component: AccountLayout,
  children: [
    { path: '', redirect: 'login' },
    { path: 'login', component: AccountLogin },
    { path: 'callback', component: AccountCallback }
  ]
}

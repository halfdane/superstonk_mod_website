<template>
  <div>
    <h1>Henlo</h1>
    <div>{{ store.user }}</div>
    <q-btn @click="setUser()">set user to something</q-btn>
    <q-btn @click="deleteUser()">delete user</q-btn>

  </div>

</template>

<script>
import { useUserStore } from 'stores/user'

export default {
  setup () {
    const store = useUserStore()
    const { rememberUser, forgetUser } = store

    const setUser = () => {
      rememberUser({ bla: 'bloo' })
    }
    const deleteUser = () => {
      forgetUser()
    }

    return {
      store,
      setUser,
      deleteUser
    }
  }
}
</script>

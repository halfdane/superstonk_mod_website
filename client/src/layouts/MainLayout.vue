<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          <q-avatar size="100px" font-size="52px" text-color="white" icon="policy"/>
          Superstonk Mod Website
        </q-toolbar-title>

        <div>
          <user-avatar></user-avatar>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-3' "
    >
      <q-scroll-area class="fit">
        <q-list>
          <EssentialLink
            v-for="link in essentialLinks"
            :key="link.title"
            v-bind="link"
          />
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <AlertMessages></AlertMessages>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import UserAvatar from 'components/UserAvatar.vue'
import AlertMessages from 'components/AlertMessages'

const linksList = [
  {
    title: 'Analytics',
    caption: 'Pretty Graphics',
    icon: 'query_stats',
    link: '/analytics'
  }
]

export default defineComponent({
  name: 'MainLayout',

  components: {
    AlertMessages,
    UserAvatar,
    EssentialLink
  },

  setup () {
    const leftDrawerOpen = ref(true)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>

<template>
  <q-page class="flex column">
    <about v-if="currentPage == 0"/>
    <team v-if="currentPage == 1"/>
    <software v-if="currentPage == 2"/>
  </q-page>
</template>

<script>
import About from '../components/tabs/About.vue'
import Team from '../components/tabs/Team.vue'
import Software from '../components/tabs/Software.vue'

export default {
  components: { Software, About, Team },
  name: 'PageIndex',
  computed: {
    currentPage: {
      get () {
        return this.$store.state.pipa.currentPage
      }
    }
  }
}
</script>

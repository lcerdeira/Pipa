<template>
  <q-page class="flex column">
    <about v-if="currentPage == 0"/>
    <software v-if="currentPage == 1"/>
    <results v-if="currentPage == 2"/>
  </q-page>
</template>

<script>
import About from '../components/tabs/About.vue'
import Results from '../components/tabs/Results.vue'
import Software from '../components/tabs/Software.vue'

export default {
  components: { Software, About, Results },
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

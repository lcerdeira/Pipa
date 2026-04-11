<template>
  <q-page>
    <transition name="page-fade" mode="out-in">
      <about v-if="currentPage == 0" key="about"/>
      <software v-else-if="currentPage == 1" key="software"/>
      <results v-else-if="currentPage == 2" key="results"/>
    </transition>
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

<style scoped>
.page-fade-enter-active, .page-fade-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.page-fade-enter, .page-fade-leave-to {
  opacity: 0;
  transform: translateY(12px);
}
</style>

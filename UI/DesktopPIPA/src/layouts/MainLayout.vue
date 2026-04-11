<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer
      v-model="drawer"
      show-if-above
      :width="300"
      :breakpoint="1100"
      content-class="gradient-dark my-drawer"
    >
      <q-scroll-area class="fit">
        <div class="column">
          <div class="column items-center q-py-lg">
            <q-img
              src="~assets/PipaLogo.jpeg"
              :height="'180px'"
              :width="'180px'"
              spinner-color="white"
              style="border-radius: 20px"
            />
            <div class="text-h6 text-white text-weight-bold q-mt-md">PIPA</div>
            <div class="text-caption" style="color: rgba(224,225,221,0.6)">Microbial Genomic Analysis</div>
          </div>
          <q-separator dark style="background: rgba(255,255,255,0.08)"/>
          <q-list dark class="q-mt-sm">
            <q-item
              v-for="(menuItem, index) in menuList"
              :key="menuItem+index"
              clickable
              v-ripple
              dark
              class="menu-item q-mx-sm"
              style="border-radius: 10px; margin-bottom: 4px"
              @click="openExternal(menuItem.link)"
            >
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" color="grey-5" size="22px"/>
              </q-item-section>
              <q-item-section style="color: rgba(224,225,221,0.9); font-size: 15px">
                {{ menuItem.label }}
              </q-item-section>
              <q-item-section side>
                <q-icon name="open_in_new" size="14px" style="color: rgba(224,225,221,0.3)"/>
              </q-item-section>
            </q-item>
          </q-list>
          <q-space/>
          <div class="q-pa-md text-center" style="color: rgba(224,225,221,0.3); font-size: 11px">
            v2.0.0
          </div>
        </div>
      </q-scroll-area>
    </q-drawer>
    <q-footer v-if="currentPage === 0" class="gradient-dark text-center" style="height: 44px; display: flex; align-items: center; justify-content: center">
      <div style="color: rgba(224,225,221,0.6); font-size: 13px">
        Copyright 2026 | DOI: <a href="https://doi.org/10.5281/zenodo.19521044" target="_blank" style="color: #52B788; text-decoration: none">10.5281/zenodo.19521044</a>
      </div>
    </q-footer>
    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script>

const menuList = [
  {
    icon: 'img:myIcons/github2.png',
    label: 'GitHub',
    link: 'https://github.com/lcerdeira/Pipa'
  },
  {
    icon: 'menu_book',
    label: 'Documentation',
    link: 'https://pipa-tool.readthedocs.io/en/latest/'
  },
  {
    icon: 'download',
    label: 'Download Desktop',
    link: 'https://github.com/lcerdeira/Pipa/releases'
  }
]

export default {
  name: 'MainLayout',
  data () {
    return {
      menuList,
      drawer: false
    }
  },
  computed: {
    currentPage: {
      get () {
        return this.$store.state.pipa.currentPage
      }
    }
  },
  methods: {
    openExternal (url) {
      if (window.__TAURI__) {
        window.__TAURI__.shell.open(url)
      } else {
        window.open(url, '_blank')
      }
    }
  }
}
</script>

<style lang="scss">
  .my-drawer {
    border-right: 1px solid rgba(255, 255, 255, 0.06);
  }
  .menu-item:hover {
    background: rgba(255, 255, 255, 0.06) !important;
  }
</style>

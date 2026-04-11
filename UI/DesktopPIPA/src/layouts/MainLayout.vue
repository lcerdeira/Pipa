<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer
      v-model="drawer"
      show-if-above
      :width="320"
      :breakpoint="1100"
      content-class="bg-primary my-drawer"
    >
      <q-scroll-area class="fit">
        <div class="column">
          <div>
            <div class="column items-center q-py-sm bg-white">
              <q-img
                src="~assets/PipaLogo.jpeg"
                :height="'300px'"
                :width="'300px'"
                spinner-color="black"
              />
            </div>
            <q-separator :key="'sep'"/>
            <q-list>
              <div v-for="(menuItem, index) in menuList" :key="menuItem+index">
                <q-item style="font-size: 16px" dark :key="index" clickable :active="menuItem.label === 'Outbox'" v-ripple @click="openExternal(menuItem.link)">
                  <q-item-section avatar>
                    <q-icon :name="menuItem.icon" color="black"/>
                  </q-item-section>
                  <q-item-section :style="{color: 'black'}">
                    {{ menuItem.label }}
                  </q-item-section>
                </q-item>
                <q-separator :key="'sep' + index"/>
              </div>
            </q-list>
          </div>
        </div>
      </q-scroll-area>
    </q-drawer>
    <q-footer v-if="currentPage === 0" class="bg-primary text-black column justify-center items-center" style="height: 40px">
      <div>Copyright 2026</div>
    </q-footer>
    <q-page-container>
      <router-view :model="currentPage"/>
    </q-page-container>
  </q-layout>
</template>

<script>

const menuList = [
  {
    icon: 'img:myIcons/github2.png',
    label: 'Github',
    link: 'https://github.com/lcerdeira/Pipa'
  },
  {
    icon: 'ion-book',
    label: 'Documentation',
    link: 'https://pipa-tool.readthedocs.io/en/latest/'
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
  .q-avatar{
    margin-right: 10px;
  }
  .q-toolbar{
    color: white;
    font-family: 'SourceSansPro';
  }
  .header{
    height: 50px;
    background-color: $primary;
  }
  .links-title{
    color: black;
    padding: 10px;
    text-transform: uppercase;
  }
  .footer{
    height: 35px;
    color: white;
    text-align: center;
    justify-content: center;
    font-weight: 300;
    font-size: 12px;
  }
  .my-drawer{
    border-right: 1px solid rgba(128, 128, 128, 0.4);
  }
</style>

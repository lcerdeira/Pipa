<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated v-if="$q.screen.width < 1100">
      <q-toolbar>
        <q-btn flat round dense icon="menu" class="q-mr-sm" @click="drawer = true"/>
        <q-toolbar-title>Pipa Project</q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="drawer"
      show-if-above
      :width="320"
      :breakpoint="1100"
      content-class="bg-black"
    >
      <q-scroll-area class="fit">
        <div class="row items-center" v-if="$q.screen.width < 1100" style="height: 50px; padding: 10px 12px">
          <q-btn flat round dense icon="menu" color="white" class="q-mr-sm" @click="drawer = false"/>
          <q-toolbar-title style="font-size: 20px" class="text-white">Pipa Project</q-toolbar-title>
        </div>
        <div class="column">
          <div>
            <div class="column items-center q-my-sm">
              <q-img
                src="~assets/PipaLogo3.png"
                :height="'250px'"
                :width="'250px'"
                spinner-color="white"
              />
            </div>
            <q-separator :key="'sep'" dark/>
            <q-toolbar class="row justify-center">
              <q-btn-toggle
                v-model="currentPage"
                flat stretch
                toggle-color="secondary"
                :options=options
                spread
                @click="closeDrawer"
                class="full-width"
              />
            </q-toolbar>
            <q-separator :key="'sep2'" dark/>
            <q-list>
              <div v-for="(menuItem, index) in menuList" :key="menuItem+index">
                <q-item dark :key="index" clickable :active="menuItem.label === 'Outbox'" v-ripple @click="openURL(menuItem.link)">
                  <q-item-section avatar>
                    <q-icon :name="menuItem.icon" color="white"/>
                  </q-item-section>
                  <q-item-section :style="{color: 'white'}">
                    {{ menuItem.label }}
                  </q-item-section>
                </q-item>
                <q-separator :key="'sep' + index" dark/>
              </div>
              <q-expansion-item
                dark
                expand-separator
                icon="ion-logo-twitter"
                label="Twitter"
              >
                <q-scroll-area style="height: 350px" :thumb-style="{backgroundColor: 'transparent'}">
                  <timeline id="lcerdeira" sourceType="profile" :options="{ theme: 'dark' }"/>
                </q-scroll-area>
              </q-expansion-item>
              <q-separator :key="'sep5'" dark/>
            </q-list>
          </div>
        </div>
        <div>
          <!-- <q-separator :key="'sep3'" dark/> -->
          <div class="footer column">
            Copyright - 2021
          </div>
        </div>
      </q-scroll-area>
    </q-drawer>
    <q-page-container>
      <router-view :model="currentPage"/>
    </q-page-container>
  </q-layout>
</template>

<script>

const menuList = [
  {
    icon: 'img:myIcons/github.png',
    label: 'Github',
    link: 'https://github.com/lcerdeira/Pipa'
  },
  {
    icon: 'ion-book',
    label: 'Wiki',
    link: 'https://github.com/lcerdeira/Pipa/wiki'
  }
]

import { Timeline } from 'vue-tweet-embed'
import { openURL } from 'quasar'

export default {
  name: 'MainLayout',
  components: { Timeline },
  data () {
    return {
      menuList,
      options: [
        { label: 'About', value: 0 },
        { label: 'Team', value: 1 }
        // { label: 'Tool', value: 2 }
      ],
      drawer: false
    }
  },
  computed: {
    currentPage: {
      get () {
        return this.$store.state.pipa.currentPage
      },
      set (val) {
        this.$store.commit('pipa/changePage', val)
      }
    }
  },
  methods: {
    openURL,
    closeDrawer () {
      if (this.$q.screen.width < 1100) {
        this.drawer = false
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
    color: white;
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
</style>

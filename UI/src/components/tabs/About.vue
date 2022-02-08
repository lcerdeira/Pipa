<template>
  <div :class="$q.screen.width < 770 ? 'q-pa-lg' : 'q-pa-xl'">
    <div class="column full-height">
      <div
        class="q-ma-none"
        style="font-weight: 400"
        :style="{fontSize: '60px'}"
      >
        Microbial Genomics
      </div>
      <div :style="{fontSize: '35px'}" class="row justify-end my-subtitle q-pt-lg">All You Need In The Same Place</div>
      <q-separator/>
    </div>
    <div class="column" style="padding-top: 50px">
      <div class="row justify-center" style="height: 100px">
        <div v-for="(label, i) in 5" :key="i+'top'" class="col-2 row justify-center">
          <div v-if="i in labelsTop" style="height: 100px" class="row items-center justify-center full-width">
            <q-spinner-orbit style="position: absolute" color="negative" size="100px"/>
            <div class="" style="position: absolute">{{labelsTop[i]}}</div>
          </div>
          <div v-else style="height: 100px"/>
        </div>
      </div>
      <div class="row justify-center" style="height: 100px">
        <div v-for="(label, i) in 5" :key="i+'top'" class="col-2">
          <div v-if="i in labelsBottom" style="height: 100px" class="row items-center justify-center full-width">
            <q-spinner-orbit style="position: absolute" color="negative" size="100px"/>
            <div class="" style="position: absolute">{{labelsBottom[i]}}</div>
          </div>
          <div v-else style="height: 100px"/>
        </div>
      </div>
    </div>
    <div style="padding-top: 50px">
      <div :style="{fontSize: '25px'}" class="justify-center row">Phases</div>
      <div style="height: 250px" class="q-pt-md">
        <q-carousel
          v-model="slide"
          transition-prev="slide-down"
          transition-next="slide-up"
          swipeable
          animated
          control-color="blue"
          prev-icon="arrow_left"
          next-icon="arrow_right"
          navigation-icon="radio_button_unchecked"
          navigation
          padding
          vertical
          :autoplay="autoplay"
          infinite
          @mouseenter="autoplay = false"
          @mouseleave="autoplay = true"
          class="text-black full-height my-carousel"
        >
          <q-carousel-slide :name="slide.name" class="column no-wrap flex-center q-pa-none" v-for="(slide, i) in carouselImages" :key="'slide'+i">
            <div class="text-center full-width full-height">
               <q-img
                  :src="'slides/' + slide.image"
                  contain
                  class="full-height"
                />
            </div>
          </q-carousel-slide>
        </q-carousel>
      </div>
    </div>
    <div class="full-width row justify-center q-mt-lg">
      <q-btn class="q-mt-lg my-button" label="Start" style="width: 250px" size="lg" @click="currentPage = 1" />
    </div>
  </div>
</template>

<script>

const carouselImages = [
  {
    name: 'slide1',
    image: 'slide1.png'
  },
  {
    name: 'slide2',
    image: 'slide2.png'
  }
]

export default {
  data () {
    return {
      carouselImages,
      slide: 'slide1',
      autoplay: true,
      labelsTop: {
        0: 'Simple',
        2: 'Fast',
        4: 'Open-Source'
      },
      labelsBottom: {
        1: 'Flexible',
        3: 'Accurate'
      }
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
  }
}
</script>

<style lang="scss" scoped>
  .logo{
    background-color: white;
    height: inherit;
  }
  .about{
    background-color: white;
    height: inherit;
  }
  .my-card{
    height: 100%;
    width: inherit;
    background-color: white;
  }
  h1{
    margin: 0;
  }
  .my-p{
    color: black;
    width: 45%;
    text-align: justify;
  }
  .my-div-img{
    height: 19%;
  }
  .my-carousel{
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 15px;
  }
  .my-subtitle{
    font-weight: 300;
  }
  .my-button{
    background-color: $primary;
    color: black;
  }
</style>

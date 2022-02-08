<template>
  <div :class="$q.screen.width < 770 ? 'q-pa-lg' : 'q-pa-xl'">
    <div class="column full-height">
      <div
        class="q-ma-none"
        style="font-weight: 400"
        :style="{fontSize: $q.platform.is.mobile ? '42px' : '65px'}"
      >
        Welcome to PiPa
      </div>
      <div class="q-pb-lg" style="font-size: 16px; font-weight: 400">Lorem ipsum dolor sit amet, consectetur adipiscing.</div>
      <div class="text-h6">About</div>
      <q-separator/>
      <div
      :class="$q.screen.width < 770 ? 'column' : 'row'"
        class="row justify-between q-pt-md">
        <div
          class="column"
          :style="{width: $q.screen.width < 770 ? '100%' : '30%'}"
          v-for="(about, index) in aboutInfo"
          :key="index+'about'">
          <div class="text-justify q-pt-xs">
            <p>{{about.info}}</p>
          </div>
        </div>
      </div>
      <div class="text-h6 q-pt-lg">Steps</div>
      <q-separator/>
    </div>
    <div class="q-pt-md">
      <div class="row q-pt-xs">
        <q-card
          :style="{width: $q.platform.is.mobile ? '100%' : $q.screen.width < 770 ? '50%' : $q.screen.width < 1540 ? '33.33%' : '20%', backgroundColor: img.color}"
          style="height: 180px"
          square
          class="my-div-img"
          v-for="(img,i) in aboutImages"
          :key="'img'+i">
          <q-img
            :src="'myIcons/' + img.image"
            spinner-color="white"
            height="100%"
            contain
            @mouseenter="mouseEnter(i)"
            @mouseleave="mouseLeave(i)"
          >
            <div v-if="img.show == true" class="fullscreen text-body-1 text-center justify-center column">
              {{img.info}}
            </div>
          </q-img>
        </q-card>
      </div>
      <div class="text-h6 q-pt-xl">Fluxogram</div>
      <q-separator/>
      <div style="height: 300px" class="q-pt-lg">
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
          class="text-white full-height my-carousel"
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
  </div>
</template>

<script>

const aboutImages = [
  {
    image: 'about1.png',
    show: false,
    color: '#96D32E',
    info: 'Sed eu consequat urna, quis finibus dui. Donec eleifend est ac lectus blandit venenatis. Ut tristique justo sit amet pellentesque feugiat. Praesent gravida eu felis a fringilla. Aliquam sed ultrices quam, ac varius turpis.'
  },
  {
    image: 'about2.png',
    show: false,
    color: '#E71D36',
    info: 'Sed eu consequat urna, quis finibus dui. Donec eleifend est ac lectus blandit venenatis. Ut tristique justo sit amet pellentesque feugiat. Praesent gravida eu felis a fringilla. Aliquam sed ultrices quam, ac varius turpis.'
  },
  {
    image: 'about3.png',
    show: false,
    color: '#1B998B',
    info: 'Sed eu consequat urna, quis finibus dui. Donec eleifend est ac lectus blandit venenatis. Ut tristique justo sit amet pellentesque feugiat. Praesent gravida eu felis a fringilla. Aliquam sed ultrices quam, ac varius turpis.'
  },
  {
    image: 'about4.png',
    show: false,
    color: '#E59500',
    info: 'Sed eu consequat urna, quis finibus dui. Donec eleifend est ac lectus blandit venenatis. Ut tristique justo sit amet pellentesque feugiat. Praesent gravida eu felis a fringilla. Aliquam sed ultrices quam, ac varius turpis.'
  },
  {
    image: 'about5.png',
    show: false,
    color: '#007AB8',
    info: 'Sed eu consequat urna, quis finibus dui. Donec eleifend est ac lectus blandit venenatis. Ut tristique justo sit amet pellentesque feugiat. Praesent gravida eu felis a fringilla. Aliquam sed ultrices quam, ac varius turpis.'
  }
]

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

const aboutInfo = [
  {
    info: 'Aenean tristique elit ac orci fermentum, id eleifend nunc placerat. Nam in est eu ipsum aliquam bibendum eu ut erat. Aenean tristique elit ac orci fermentum, id eleifend nunc placerat. Nam in est eu ipsum aliquam bibendum eu ut erat. Phasellus vehicula orci tellus, ac hendrerit erat eleifend et. Integer tempus commodo nisi non aliquet. In hac habitasse platea dictumst. Morbi iaculis, odio a luctus suscipit, velit diam semper urna, eget gravida est sem ut orci. Sed molestie, sapien non scelerisque blandit, libero eros maximus enim, quis interdum lorem ex vitae augue. Duis vitae lectus sit amet nisi vulputate suscipit dapibus quis quam. Pellentesque sollicitudin rhoncus lacus, non egestas massa finibus vitae. Sed iaculis quis urna in gravida. Nulla accumsan lobortis diam, sit amet maximus ante venenatis non. Nunc sit amet aliquam est, in hendrerit nisi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.'
  },
  {
    info: 'Aenean tristique elit ac orci fermentum, id eleifend nunc placerat. Nam in est eu ipsum aliquam bibendum eu ut erat. Aenean tristique elit ac orci fermentum, id eleifend nunc placerat. Nam in est eu ipsum aliquam bibendum eu ut erat. Phasellus vehicula orci tellus, ac hendrerit erat eleifend et. Integer tempus commodo nisi non aliquet. In hac habitasse platea dictumst. Morbi iaculis, odio a luctus suscipit, velit diam semper urna, eget gravida est sem ut orci. Sed molestie, sapien non scelerisque blandit, libero eros maximus enim, quis interdum lorem ex vitae augue. Duis vitae lectus sit amet nisi vulputate suscipit dapibus quis quam. Pellentesque sollicitudin rhoncus lacus, non egestas massa finibus vitae. Sed iaculis quis urna in gravida. Nulla accumsan lobortis diam, sit amet maximus ante venenatis non. Nunc sit amet aliquam est, in hendrerit nisi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae. Aenean tristique elit ac orci fermentum.'
  },
  {
    info: 'Pellentesque quis faucibus metus. Aenean tristique elit ac orci fermentum, id eleifend nunc placerat. Nam in est eu ipsum aliquam bibendum eu ut erat. Phasellus vehicula orci tellus, ac hendrerit erat eleifend et. Integer tempus commodo nisi non aliquet. In hac habitasse platea dictumst. Morbi iaculis, odio a luctus suscipit, velit diam semper urna, eget gravida est sem ut orci. Sed molestie, sapien non scelerisque blandit, libero eros maximus enim, quis interdum lorem ex vitae augue. Duis vitae lectus sit amet nisi vulputate suscipit dapibus quis quam. Pellentesque sollicitudin rhoncus lacus, non egestas massa finibus vitae. Sed iaculis quis urna in gravida. Nulla accumsan lobortis diam, sit amet maximus ante venenatis non. Nunc sit amet aliquam est, in hendrerit nisi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.'
  }
]

export default {
  data () {
    return {
      aboutImages,
      carouselImages,
      slide: 'slide1',
      autoplay: true,
      aboutInfo
    }
  },
  methods: {
    mouseEnter (index) {
      this.aboutImages[index].show = true
    },
    mouseLeave (index) {
      this.aboutImages[index].show = false
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
</style>

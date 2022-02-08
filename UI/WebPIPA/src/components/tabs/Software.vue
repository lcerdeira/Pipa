<template>
  <div class="column full-width justify-start" :class="$q.screen.width < 1230 ? 'q-pa-lg' : 'q-pa-xl'">
    <div class="column justify-around full-height">
      <div
        v-for="(option, index) in options"
        :key="index + option"
        class="items-center"
      >
        <div class="row full-width q-pb-lg no-wrap items-center">
          <div class="num-square" :style="{backgroundColor: option.color}">{{ index + 1 }}</div>
          <div class="text-h5">{{ option.title }}</div>
        </div>
        <div
          v-if="index == 0"
          class="row justify-between full-width"
          style="padding-bottom: 55px"
          :class="$q.screen.width < 550 ? '' : 'q-gutter-x-md'"
        >
          <q-card
            class="my-card q-mb-lg my-option"
            :class="[program.isChecked ? 'painted' : '']"
            v-for="(program, i) in programs"
            :key="i + program"
            :style="{width: $q.screen.width < 550 ? '100%' : '30%'}"
          >
            <q-card-section class="my-card-section row items-center q-mt-md justify-between" horizontal>
              <div class="row items-center no-wrap">
                <div class="my-border">
                  <q-avatar :style="{margin:'0'}" class="shadow-2">
                    <img :src="'myIcons/logos/' + program.icon">
                  </q-avatar>
                </div>
                <div class="q-pl-md text-h6">
                  <a :href="program.link" target="_blank" class="row no-wrap option-card-title" style="text-decoration: none" :class="[program.isChecked ? 'option-card-title-painted' : 'option-card-title']">
                    {{ program.name }}
                    <div class="column justify-start">
                      <q-icon size="12px" :color="program.isChecked ? 'white' : 'black'" name="eva-external-link-outline"/>
                    </div>
                  </a>
                </div>
              </div>
              <q-checkbox v-model="program.isChecked" :color="program.isChecked ? '' : 'white'"/>
            </q-card-section>
          </q-card>
        </div>
        <div
          v-if="index == 1"
          class="row justify-between full-width"
          style="padding-bottom: 55px"
          :class="$q.screen.width < 550 ? '' : 'q-gutter-x-md'"
        >
          <q-card
            class="my-file-card q-mb-lg my-option"
            v-for="(program, i) in programs"
            :key="i + program"
            :style="{width: $q.screen.width < 550 ? '100%' : '30%'}"
          >
            <div class="column my-file-picker">
              <div>
                <div class="filepicker-top">
                  <div v-if="i == 0">
                    <q-radio
                      v-for="(type, ind) in types_illumina"
                      :key="ind + type"
                      :val="type.val"
                      v-model="type_illumina"
                      :label="type.label"
                      color="secondary"
                      class="my-radio"
                      keep-color
                    />
                  </div>
                  <div v-if="i != 0">
                    <q-radio
                      v-for="(type, ind) in types_illumina.slice(0,1)"
                      :key="ind + type"
                      :val="type_aux"
                      v-model="type_aux"
                      :label="type.label"
                      color="secondary"
                      class="my-radio"
                      keep-color
                    />
                  </div>
                </div>
              </div>
              <q-file
                q-file
                v-model="program.files"
                label="Choose files"
                filled
                multiple
                clearable
                text-center
                :disable='!program.isChecked'
              >
                <template v-slot:prepend>
                  <q-icon name="cloud_upload" class="cloud-icon" @click.stop />
                </template>
                <template v-slot:append>
                  <q-icon
                    name="search"
                    @click.stop="model = null"
                    class="cursor-pointer"
                  />
                </template>
              </q-file>
            </div>
          </q-card>
        </div>
      </div>
      <div class="row justify-center">
        <q-btn
          class="my-button q-ml-md"
          :class="$q.screen.width < 770 ? 'full-width' : ''"
          icon-right="send"
          label="Submit"
          @click="getResults"
        />
      </div>
    </div>
    <results v-if="showResults" class="q-pt-lg"/>
  </div>
</template>

<script>

const programs = [
  {
    name: 'Illumina',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    isChecked: false,
    files: null,
    icon: 'illumina.jpg',
    link: 'https://www.illumina.com/'
  },
  {
    name: 'Nanopore',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    isChecked: false,
    files: null,
    icon: 'nanopore.jpg',
    link: 'https://nanoporetech.com/'
  },
  {
    name: 'Pacbio',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    isChecked: false,
    files: null,
    icon: 'pacbio.png',
    link: 'https://www.pacb.com/'
  }
]
const options = [
  {
    title: 'Choose Sequence Platforms',
    color: '#FF3116'
  },
  {
    title: 'Choose Files',
    color: '#FFBD08'
  }
  // {
  //   title: 'Run',
  //   color: '#0062F0'
  // }
]

import Results from './Results.vue'

export default {
  components: { Results },
  data () {
    return {
      options,
      programs,
      files: null,
      types_illumina: [
        { val: 0, label: 'Single-end' },
        { val: 1, label: 'Paired-end' }
      ],
      type_illumina: 0,
      type_aux: 0
    }
  },
  computed: {
    showResults: {
      set (val) {
        this.$store.commit('pipa/toggleResults', val)
      },
      get () {
        return this.$store.state.pipa.showResults
      }
    }
  },
  methods: {
    checkBox (index) {
      this.programs[index].isChecked = !this.programs[index].isChecked
    },
    getResults () {
      var files = [null, null, null]
      for (let index = 0; index < this.programs.length; index++) {
        if (this.programs[index].files !== null) {
          files[index] = this.programs[index].files
        }
      }
      this.showResults = true
    }
  }
}
</script>

<style lang="scss">
  .num-square{
    height: 25px;
    width: 25px;
    margin-right: 10px;
    color: $font;
    font-size: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .option-card-title{
    color: $primary;
    font-weight: 600;
    color: black;
  }
  .option-card-subtitle{
    color: $primary;
    font-weight: 500;
    color: black;
  }
  .option-card-subtitle-painted, .option-card-title-painted{
    color: white;
  }
  .my-card{
    background-color: #F2F2F2;
  }
  .my-option{
    min-width: 225px;
  }
  .my-button{
    height: 50px;
    background-color: $terciary;
    color: white;
    width: 30%;
  }
  .make-hidden{
    visibility: hidden;
  }
  .make-visible{
    visibility: visible;
  }
  .painted{
    border-color: $accent;
    background-color: $accent;
  }
  .my-card-section{
    padding: 0 16px 16px 16px;
  }
  .btn-program{
    text-transform: none;
  }
  .q-file{
    background-color: white;
  }
  .q-radio{
    color: white;
  }
  .my-radio{
    width: 50%;
    justify-content: center;
  }
  .cloud-icon{
    color: #616161;
  }
  .filepicker-top{
    background-color: #616161;
  }
  .my-border{
    border-radius: 50%;
    color: rgba(0, 0, 0, 0.2);
  }
  .my-file-card, .filepicker-top{
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
  }
  .btn-sp{
    font-size: 14px;
    color: rgba(0, 0, 0, 0.5);
  }
</style>

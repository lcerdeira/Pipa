<template>
  <div id="software" class="column full-width justify-start" :class="$q.screen.width < 1230 ? 'q-px-lg q-pb-lg' : 'q-px-xl q-pb-xl'">
    <div class="row justify-end q-pt-md q-gutter-x-md">
      <q-btn round color="primary" text-color="black" icon="arrow_back" size="md" @click="currentPage = 0">
        <q-tooltip anchor="center left" self="center right" :offset="[10, 10]">
          Go back
        </q-tooltip>
      </q-btn>
      <q-btn round color="blue" icon="replay" size="md" @click="restart">
        <q-tooltip>
          Reset
        </q-tooltip>
      </q-btn>
    </div>
    <div class="column justify-around full-height">
      <div
        v-for="(option, index) in options"
        :key="index + option"
        class="items-center"
      >
        <div class="row full-width q-pb-lg no-wrap items-center">
          <div class="num-square" :style="{backgroundColor: option.color}">{{ index + 1 }}</div>
          <div class="text-h6 text-weight-regular">{{ option.title }}</div>
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
                <div class="q-pl-md text-subtitle1">
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
        <q-form
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
                lazy-rules
                class="q-pb-xs"
                style="height: 55px"
                :rules="[ val => val != null || 'Please enter file']"
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
        </q-form>
      </div>
      <div class="full-width row full-height">
        <q-form
          ref="myform"
          class="q-gutter-y-md col-6"
        >
          <div>
            <div>Metadata File (Optional)</div>
            <div class="row items-center">
              <q-file
                filled
                clearable
                v-model="info.metadata"
                class="q-ma-none col-grow"
                label="Metadata file: browser file"
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
              <div class="q-pl-md">
                <q-btn round color="blue" icon="download" size="md" @click="openURL('')">
                  <q-tooltip>
                    Download template format
                  </q-tooltip>
                </q-btn>
              </div>
            </div>
          </div>
          <div>
            <div>Sample Name</div>
            <q-input
              filled
              v-model="info.sampleName"
              lazy-rules
              :rules="[ val => val && val.length > 0 || 'Please type something']"
            >
            <template v-if="info.sampleName != null" v-slot:append>
              <q-icon name="close" @click="info.sampleName = null" class="cursor-pointer" />
            </template>
            </q-input>
          </div>
          <div class="row">
            <div class="col-grow column">
              <div>Genus</div>
              <q-btn-dropdown color="primary" :label="info.genus" class="col-grow text-black">
                <q-list>
                  <q-item v-for="(gene, i) in genusItems" :key="gene+i" clickable v-close-popup @click="info.genus = gene">
                    <q-item-section>
                      <q-item-label>{{gene}}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
            </div>
            <div class="q-mx-sm"></div>
            <div class="col-grow column">
              <div>Species</div>
              <q-btn-dropdown color="primary" :label="info.species" class="col-grow text-black">
                <q-list>
                  <q-item v-for="(specie, i) in speciesItems" :key="specie+i" clickable v-close-popup @click="info.species = specie">
                    <q-item-section>
                      <q-item-label>{{specie}}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
            </div>
          </div>
          <div class="q-pb-md">
            <div>Description (Optional)</div>
            <q-input
              filled
              v-model="info.description"
              class="q-ma-none"
              lazy-rules
            >
              <template v-if="info.description != null" v-slot:append>
                <q-icon name="close" @click="info.description = null" class="cursor-pointer" />
              </template>
            </q-input>
          </div>
          <q-btn
            class="my-button full-width"
            icon-right="send"
            label="Submit"
            @click="onSubmit"
          />
        </q-form>
        <div class="col-6 q-pl-xl col-grow column">
          <q-list bordered padding class="rounded-borders col-grow">
            <q-item-label header class="text-weight-bold q-mt-xs row justify-between items-center">
              <div>Previous Jobs Run</div>
              <q-chip class="text-black q-ma-none" style="height: 20px">{{samples.length}}</q-chip>
            </q-item-label>
            <div v-for="(sample, i) in samples" :key="'samples'+i">
              <q-separator/>
              <q-item clickable v-ripple>
                <!-- <q-item-section avatar top>
                  <q-avatar icon="folder" color="primary" text-color="white" />
                </q-item-section> -->

                <q-item-section>
                  <q-item-label lines="1">{{sample.name}}</q-item-label>
                  <q-item-label caption>{{sample.date}}</q-item-label>
                </q-item-section>

                <!-- <q-item-section side>
                  <q-icon name="info" color="green" />
                </q-item-section> -->
              </q-item>
            </div>
          </q-list>
        </div>
      </div>
    </div>
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
const genusItems = ['gene1', 'gene2', 'gene3']
const speciesItems = ['specie1', 'specie2', 'specie3']
const info = {
  metadata: null,
  sampleName: 'My_Sample1',
  genus: genusItems[0],
  species: speciesItems[0],
  description: null
}
const options = [
  {
    title: 'Choose Sequence Platforms',
    color: '#FF3116'
  },
  {
    title: 'Choose Files',
    color: '#FFBD08'
  }
]

const samples = [
  {
    name: 'My_Sample_78',
    date: 'February 22nd, 2021',
    results: null
  },
  {
    name: 'My_Sample_79',
    date: 'February 23nd, 2021',
    results: null
  }
]

import { scroll, openURL } from 'quasar'
const { getScrollTarget, setScrollPosition } = scroll

export default {
  data () {
    return {
      options,
      programs,
      files: null,
      info,
      types_illumina: [
        { val: 0, label: 'Single-end' },
        { val: 1, label: 'Paired-end' }
      ],
      type_illumina: 0,
      type_aux: 0,
      genusItems,
      speciesItems,
      samples
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
      return files
    },
    restart () {
      this.info = {
        metadata: null,
        sampleName: 'My_Sample1',
        genus: genusItems[0],
        species: speciesItems[0],
        description: null
      }
      this.type_illumina = 0
      for (let i = 0; i < this.programs.length; i++) {
        this.programs[i].files = null
        this.programs[i].isChecked = false
      }
    },
    onSubmit () {
      const results = {
        illumina: this.programs[0].files,
        typeIllumina: this.type_illumina,
        nanopore: this.programs[1].files,
        pacbio: this.programs[2].files,
        metadata: this.info.metadata,
        sampleName: this.info.sampleName,
        genus: this.info.genus,
        species: this.info.species,
        description: this.info.description
      }
      const checkNull = arr => arr.every(val => val === null)
      const allNull = checkNull([results.illumina, results.nanopore, results.pacbio])

      this.$refs.myform.validate().then(success => {
        if (!allNull) {
          if (success) {
            console.log(results)
            this.currentPage = 2
          }
        } else {
          this.$q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: 'Please choose at least one sequence platform'
          })
        }
      })
    },
    handleScroll () {
      const ele = document.getElementById('software') // You need to get your element here
      const target = getScrollTarget(ele)
      const offset = ele.offsetTop - ele.scrollHeight
      const duration = 0
      setScrollPosition(target, offset, duration)
    }
  },
  mounted () {
    this.handleScroll()
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

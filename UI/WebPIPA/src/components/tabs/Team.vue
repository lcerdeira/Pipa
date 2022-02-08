<template>
  <div class="column text-left team" :class="$q.screen.width < 770 ? 'q-pa-lg' : 'q-pa-xl'">
    <h4 class="q-ma-none">Team</h4>
    <q-separator/>
    <div class="my-col q-pt-xl">
      <div
        class="full-height wrap justify-between"
        :class="$q.platform.is.mobile ? 'column' : 'row'"
      >
        <div
          class="column q-mb-xl"
          :class="$q.platform.is.mobile ? '' : 'q-mx-lg'"
          :style="{width: $q.platform.is.mobile ? '100%' : '350px'}"
          v-for="(team,index) in teamMembers"
          :key="team+index"
        >
          <div
            class="row"
            :class="$q.platform.is.mobile ? '' : 'q-pb-md'"
            :style="{height: !$q.platform.is.mobile ?'150px' : ''}"
          >
            <div class="my-team-card-left">
              <div class="full-width">
                <q-avatar square class="my-avatar full-height full-width">
                  <div class="full-height full-width" :class="index == 0 && $q.platform.is.mobile ? 'q-pb-xl' : ''">
                    <q-img contain class="full-width" :src="'team/'+team.image"/>
                  </div>
                </q-avatar>
              </div>
            </div>
            <div
              class="my-team-card-right items-start"
              :style="{paddingLeft: $q.platform.is.mobile ? '15px' : '30px'}"
            >
              <div
                class="my-separator"
                :class="$q.platform.is.mobile ? 'q-mb-sm' : ''"
              />
              <div class="row q-gutter-x-sm q-pb-md" v-if="!$q.platform.is.mobile">
                <a v-for="(social, i) in socialMedias" :key="social+i" target="_blank" :href="team.links[i]">
                  <q-icon v-ripple :name="social.image" size="26px" class="my-btn"/>
                </a>
              </div>
              <div class="column items-start">
                <p class="team-name">{{team.name}}</p>
                <p class="team-job q-ma-none">{{team.job}}</p>
              </div>
            </div>
          </div>
          <div class="row q-gutter-x-sm q-py-md" v-if="$q.platform.is.mobile">
            <a v-for="(social, i) in socialMedias" :key="social+i" target="_blank" :href="team.links[i]">
              <q-icon v-ripple :name="social.image" size="26px" class="my-btn"/>
            </a>
          </div>
          <div v-for="(inst, i) in team.instituicao" :key="i+'inst'">
            <div class="row no-wrap items-center q-mb-sm cursor-pointer" @click="openURL(team.iLinks[i])" style="height: 35px">
              <q-img style="width: 35px" contain :src="'team/'+team.iImages[i]" />
              <p class="q-pl-sm">{{inst}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { openURL } from 'quasar'

export default {
  data () {
    return {
      teamMembers: [
        {
          name: 'Louise Cerdeira',
          job: 'Researcher and Professor',
          image: 'louise.png',
          instituicao: ['Centro Universitário do Estado do Pará', 'Liverpool School of Tropical Medicine'],
          iLinks: ['https://www.cesupa.br/', 'https://www.lstmed.ac.uk/'],
          iImages: ['cesupa.png', 'lstm.png'],
          links: ['https://www.linkedin.com/in/louisecerdeira/', 'https://orcid.org/0000-0002-4495-2615', 'https://scholar.google.nl/citations?user=O2dcz5MAAAAJ&hl=pt-BR', 'https://twitter.com/lcerdeira', 'http://lattes.cnpq.br/5673401428259684']
        },
        {
          name: 'Marcos de Sousa',
          job: 'Researcher and Professor',
          image: 'mp.png',
          instituicao: ['Centro Universitário do Estado do Pará', 'Museu Paraense Emílio Goeldi'],
          iLinks: ['https://www.cesupa.br/', 'https://www.museu-goeldi.br/'],
          iImages: ['cesupa.png', 'museu.png'],
          links: ['https://www.linkedin.com/in/marcos-de-sousa-359bb813b', 'https://orcid.org/0000-0002-3379-4754', 'https://scholar.google.ca/citations?user=KWybAYcAAAAJ&hl=pt-BR&oi=ao', 'https://twitter.com/_MarcosSousa_', 'http://lattes.cnpq.br/6713232502495902']
        },
        {
          name: 'Elielson Barbosa',
          job: 'Computer Science Undergraduate Student',
          image: 'elielson.png',
          instituicao: ['Centro Universitário do Estado do Pará'],
          iLinks: ['https://www.cesupa.br/'],
          iImages: ['cesupa.png'],
          links: ['http://www.linkedin.com/in/elielson-barbosa-173323151', 'https://orcid.org/0000-0003-3609-9842', 'https://scholar.google.com.br/citations?user=keGJ6XAAAAAJ&hl=pt-BR', '', 'http://lattes.cnpq.br/7103183574612444']
        }
      ],
      socialMedias: [
        {
          image: 'img:social/social1.png'
        },
        {
          image: 'img:social/social2.png'
        },
        {
          image: 'img:social/social3.png'
        },
        {
          image: 'img:social/social4.png'
        },
        {
          image: 'img:social/social5.png'
        }
      ]
    }
  },
  methods: {
    openURL
  }
}
</script>

<style lang="scss" scoped>
  .team{
    display: flex;
    flex-flow: column;
  }
  .my-col{
    flex-grow: 1;
  }
  .my-avatar{
    margin: 0;
  }
  .my-team-card-left{
    width: 33.5%;
  }
  .my-team-card-right{
    width: 66.5%;
  }
  .my-btn{
    margin-top: 10px;
    color: $accent2;
  }
  .my-separator{
    width: 40px;
    height: 5px;
    background-color: $terciary;
  }
  p{
    margin: 0;
  }
  .team-name{
    text-transform: uppercase;
    letter-spacing: 3px;
    color: $secondary;
    font-size: 16px;
  }
  .team-job{
    font-size: 16px;
    font-style: italic;
    color: $accent;
  }
  .my-border{
    position: absolute;
    width: 100%;
    display: flex;
  }
  .my-border-line{
    border: 1px solid;
    flex-grow: 1;
    border-radius: 20px;
  }
</style>

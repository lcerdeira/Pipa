import axios from 'axios'

export async function uploadFiles ({ commit, state }, { files, illuminaType }) {
  const formData = new FormData()

  if (files.illumina && files.illumina.length) {
    for (let i = 0; i < files.illumina.length; i++) {
      formData.append('illumina', files.illumina[i])
    }
  }
  if (files.nanopore && files.nanopore.length) {
    for (let i = 0; i < files.nanopore.length; i++) {
      formData.append('nanopore', files.nanopore[i])
    }
  }
  if (files.pacbio && files.pacbio.length) {
    for (let i = 0; i < files.pacbio.length; i++) {
      formData.append('pacbio', files.pacbio[i])
    }
  }
  formData.append('illumina_type', illuminaType === 1 ? 'paired' : 'single')

  commit('setPipelineStatus', 'uploading')
  commit('setPipelineMessage', 'Uploading files...')

  console.log('[PIPA] Uploading to', state.apiBaseUrl + '/upload')

  try {
    const response = await axios.post(`${state.apiBaseUrl}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000
    })
    console.log('[PIPA] Upload response:', response.data)
    commit('setJobId', response.data.job_id)
    return response.data
  } catch (err) {
    console.error('[PIPA] Upload failed:', err.message, err.response && err.response.data)
    commit('setPipelineStatus', 'failed')
    commit('setPipelineMessage', 'Upload failed: ' + err.message)
    throw err
  }
}

export async function startPipeline ({ commit, state }, config) {
  commit('setPipelineStatus', 'running')
  commit('setPipelineMessage', 'Starting pipeline...')
  commit('setPipelineProgress', 0)

  console.log('[PIPA] Starting pipeline for job', state.jobId, config)

  try {
    const response = await axios.post(`${state.apiBaseUrl}/run`, {
      job_id: state.jobId,
      genus: config.genus,
      species: config.species,
      sample_name: config.sampleName,
      genome_size: config.genomeSize
    }, { timeout: 10000 })
    console.log('[PIPA] Run response:', response.data)
    return response.data
  } catch (err) {
    console.error('[PIPA] Run failed:', err.message, err.response && err.response.data)
    commit('setPipelineStatus', 'failed')
    commit('setPipelineMessage', 'Failed to start: ' + err.message)
    throw err
  }
}

export async function pollStatus ({ commit, state }) {
  if (!state.jobId) return null

  try {
    const response = await axios.get(`${state.apiBaseUrl}/status/${state.jobId}`, {
      timeout: 5000
    })
    const data = response.data

    commit('setPipelineStatus', data.status)
    commit('setPipelineStage', data.stage)
    commit('setPipelineMessage', data.message)
    commit('setPipelineProgress', data.progress)
    commit('setErrors', data.errors || [])

    return data
  } catch (err) {
    console.error('[PIPA] Poll failed:', err.message)
    return null
  }
}

export async function fetchResults ({ commit, state }) {
  if (!state.jobId) return null

  try {
    const response = await axios.get(`${state.apiBaseUrl}/results/${state.jobId}`, {
      timeout: 10000
    })
    const data = response.data

    commit('setResults', data.results)
    commit('setResultFiles', data.files || [])
    commit('setPipelineStatus', data.status)

    commit('addPreviousJob', {
      jobId: state.jobId,
      date: new Date().toLocaleDateString(),
      status: data.status
    })

    return data
  } catch (err) {
    console.error('[PIPA] Fetch results failed:', err.message)
    return null
  }
}

export async function fetchJobs ({ state }) {
  try {
    const response = await axios.get(`${state.apiBaseUrl}/jobs`, { timeout: 5000 })
    return response.data.jobs
  } catch (err) {
    console.error('[PIPA] Fetch jobs failed:', err.message)
    return []
  }
}

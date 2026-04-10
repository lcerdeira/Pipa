import axios from 'axios'

export async function uploadFiles ({ commit, state }, { files, illuminaType }) {
  const formData = new FormData()

  if (files.illumina) {
    files.illumina.forEach(f => formData.append('illumina', f))
  }
  if (files.nanopore) {
    files.nanopore.forEach(f => formData.append('nanopore', f))
  }
  if (files.pacbio) {
    files.pacbio.forEach(f => formData.append('pacbio', f))
  }
  formData.append('illumina_type', illuminaType === 1 ? 'paired' : 'single')

  commit('setPipelineStatus', 'uploading')
  commit('setPipelineMessage', 'Uploading files...')

  const response = await axios.post(`${state.apiBaseUrl}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

  commit('setJobId', response.data.job_id)
  return response.data
}

export async function startPipeline ({ commit, state }, config) {
  commit('setPipelineStatus', 'running')
  commit('setPipelineMessage', 'Starting pipeline...')
  commit('setPipelineProgress', 0)

  const response = await axios.post(`${state.apiBaseUrl}/run`, {
    job_id: state.jobId,
    genus: config.genus,
    species: config.species,
    sample_name: config.sampleName,
    genome_size: config.genomeSize
  })

  return response.data
}

export async function pollStatus ({ commit, state }) {
  if (!state.jobId) return null

  const response = await axios.get(`${state.apiBaseUrl}/status/${state.jobId}`)
  const data = response.data

  commit('setPipelineStatus', data.status)
  commit('setPipelineStage', data.stage)
  commit('setPipelineMessage', data.message)
  commit('setPipelineProgress', data.progress)
  commit('setErrors', data.errors || [])

  return data
}

export async function fetchResults ({ commit, state }) {
  if (!state.jobId) return null

  const response = await axios.get(`${state.apiBaseUrl}/results/${state.jobId}`)
  const data = response.data

  commit('setResults', data.results)
  commit('setResultFiles', data.files || [])
  commit('setPipelineStatus', data.status)

  // Save to previous jobs
  commit('addPreviousJob', {
    jobId: state.jobId,
    date: new Date().toLocaleDateString(),
    status: data.status
  })

  return data
}

export async function fetchJobs ({ state }) {
  const response = await axios.get(`${state.apiBaseUrl}/jobs`)
  return response.data.jobs
}

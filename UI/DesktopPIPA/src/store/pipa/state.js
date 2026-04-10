export default function () {
  return {
    currentPage: 0,
    apiBaseUrl: 'http://localhost:5000/api',
    jobId: null,
    pipelineStatus: null, // null, 'uploading', 'running', 'completed', 'completed_with_errors', 'failed'
    pipelineStage: null,
    pipelineMessage: '',
    pipelineProgress: 0,
    results: null,
    resultFiles: [],
    errors: [],
    previousJobs: []
  }
}

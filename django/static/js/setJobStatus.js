async function setJobStatus(job_id) {
  await fetch(`/api/change_job_status/${job_id}`)
  window.location.href = `/recruiter/dashboard/`
}
async function applyJob() {
  job_id = sessionStorage.getItem('job_id')
  const response = await (await fetch(`/api/apply_job/${job_id}`))
  
  if (response.ok) {
    data = await response.json()
    window.location.href = `/view_application/${data.job_application_id}`;
  } else {
    console.error('Failed to apply for the job');
  }
}
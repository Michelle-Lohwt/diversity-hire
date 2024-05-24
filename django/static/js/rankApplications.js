// Get all the checkbox inputs
const checkboxes = document.querySelectorAll('input[type="checkbox"][name="score[]"]');

// Function to handle checkbox change event
async function handleCheckboxChange(event) {
  const checkedCheckboxes = Array.from(checkboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.value);

  await fetch(`/api/get_applications/${jobId}/${status}`)
  .then(response => response.json())
  .then(data => {
    const scorecardContainer = document.getElementById('ranking_Scorecard')
    
    while (scorecardContainer.firstChild){
      scorecardContainer.removeChild(scorecardContainer.firstChild)
    }
    if(data.applications == null){
    }
    else{
      const sortedApplications = []
      data.applications.forEach(a => {
        const new_overall_score = calculateNewOverallScore(a, checkedCheckboxes)

        const applicationCard = document.createElement('div')
        applicationCard.classList.add('my-2', 'relative', 'flex', 'items-center', 'space-x-3', 'rounded-lg', 'border', 'border-gray-300', 'bg-white', 'px-6', 'py-5', 'shadow-sm', 'focus-within:ring-2', 'focus-within:ring-indigo-500', 'focus-within:ring-offset-2', 'hover:border-gray-400');

        const scoreDiv = document.createElement('div')
        scoreDiv.classList.add('flex', 'w-16', 'flex-shrink-0', 'items-center', 'justify-center', 'rounded-l-md', 'text-sm', 'font-medium');
        scoreDiv.textContent = `${new_overall_score} %`;

        const contentDiv = document.createElement('div')
        contentDiv.classList.add('min-w-0', 'flex-1')

        const link = document.createElement('a');
        link.href = `/view_application/${a.id}`;
        link.classList.add('focus:outline-none');

        const span = document.createElement('span')
        span.classList.add('absolute', 'inset-0');
        span.setAttribute('aria-hidden', 'true');

        const candidateName = document.createElement('p');
        candidateName.classList.add('text-sm', 'font-medium', 'text-gray-900');
        candidateName.textContent = a.candidate_name;

        const experienceDetails = document.createElement('p');
        experienceDetails.classList.add('text-sm', 'text-gray-500');
        experienceDetails.textContent = `${a.latest_job_title} \u2022 ${a.company}`;

        link.appendChild(span)
        link.appendChild(candidateName)
        link.appendChild(experienceDetails)

        contentDiv.appendChild(link)
        applicationCard.appendChild(scoreDiv)
        applicationCard.appendChild(contentDiv)

        sortedApplications.push({
          'application': applicationCard,
          'new_score': new_overall_score
        })
      })
      sortedApplications.sort((a, b) => b.new_score - a.new_score)
      sortedApplications.forEach(item=> {
        scorecardContainer.appendChild(item.application);
      });
    }
  })
}

function calculateNewOverallScore(application, checkedCheckboxes){
  const overall_score = parseFloat(application.overall_score)
  const skill_score = parseFloat(application.skill_score)
  const qualification_score = parseFloat(application.qualification_score)
  const social_media_score = parseFloat(application.social_media_score)
  const interview_score = parseFloat(application.interview_score)

  let new_overall_score = 0
  if(checkedCheckboxes.length == 4){
    new_overall_score = overall_score
  }
  else{
    let total_weight = 0
    if(checkedCheckboxes.includes('skill')){
      new_overall_score += skill_score
      total_weight += 1
    }
    if(checkedCheckboxes.includes('qualification')){
      new_overall_score += qualification_score
      total_weight += 1
    }
    if(checkedCheckboxes.includes('social_media')){
      new_overall_score += social_media_score
      total_weight += 1
    }
    if(checkedCheckboxes.includes('interview_performance')){
      new_overall_score += interview_score
      total_weight += 1
    }
  
    if(total_weight > 0){
      new_overall_score = (new_overall_score / total_weight).toFixed(2)
    } else{
      new_overall_score = overall_score
    }

  }
  return new_overall_score
}

// Attach event listeners to each checkbox
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', handleCheckboxChange);
});
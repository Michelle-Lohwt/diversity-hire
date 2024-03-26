function updateElementIndex(el, prefix, ndx) {
  var id_regex = new RegExp('(' + prefix + '-\\d+)');
  var replacement = prefix + '-' + ndx;
  if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
  // ToDo (high): make delete button works
  if (el.id === ('id_' + replacement + '-id')) el.value = ndx + 1
  // console.log(el.value)
  // if (el.value) el.value = ndx + 1
}

function condition(formClass, rowClass, replaceClass){
  var conditionRow = $('.' + formClass + ':not(:last)');
  conditionRow.find('.' + rowClass)
  .removeClass('bg-green-600 hover:bg-green-700').addClass('bg-gray-600 hover:bg-red-700')
  .removeClass(rowClass).addClass(replaceClass)
  .html('Delete');
}

function calculateId(selector, prefix){
  var total = $('#id_' + prefix + '-TOTAL_FORMS').val()
  $(selector).find(':input').each(function(){
    var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
    var id = 'id_' + name;
    $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
  });
  $(selector).find('label').each(function() {
    var forValue = $(this).attr('for');
    if (forValue) {
      forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
      $(this).attr({'for': forValue});
    }
  });
}

function cloneMore(selector, prefix, formClass, rowClass, replaceClass){
  var newElement = $(selector).clone(true);
  var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
  newElement.find(':input').each(function(){
    var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
    var id = 'id_' + name;
    $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
  });
  newElement.find('label').each(function() {
    var forValue = $(this).attr('for');
    if (forValue) {
      forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
      $(this).attr({'for': forValue});
    }
  });
  total++;
  $('#id_' + prefix + '-TOTAL_FORMS').val(total);
  $(selector).after(newElement);
  condition(formClass, rowClass, replaceClass)
  // var conditionRow = $('.experience-form-row:not(:last)');
  //   conditionRow.find('.add-experience-row')
  //   .removeClass('bg-green-600 hover:bg-green-700').addClass('bg-gray-600 hover:bg-red-700')
  //   .removeClass('add-experience-row').addClass('remove-experience-row')
  //   .html('Delete');
  return false;
}

function deleteForm(prefix, btn, formClass) {
  var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
  if (total > 1){
      btn.closest('.' + formClass).remove();
      var forms = $('.' + formClass);
      $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
      for (var i=0, formCount=forms.length; i<formCount; i++) {
        $(forms.get(i)).find(':input').each(function() {
          updateElementIndex(this, prefix, i);
        });
      }
  }
  return false;
}

$(document).ready(function() {
  // calculateId('skill-form-row', 'skill_belongs_to_candidate')
  condition('skill-form-row', 'add-skill-row', 'remove-skill-row')
  // calculateId('.experience-form-row', 'add-experience-row')
  condition('experience-form-row', 'add-experience-row', 'remove-experience-row')
  // calculateId('.qualification-form-row', 'add-qualification-row')
  condition('qualification-form-row', 'add-qualification-row', 'remove-qualification-row')
});

$(document).on('click', '.add-experience-row', function(e){
  e.preventDefault();
  cloneMore(
    '.experience-form-row:last', 
    'experience_belongs_to_candidate', 
    'experience-form-row', 
    'add-experience-row',
    'remove-experience-row'
  );
  return false;
});

$(document).on('click', '.remove-experience-row', function(e){
  e.preventDefault();
  deleteForm('experience_belongs_to_candidate', $(this), 'experience-form-row');
  return false;
});

$(document).on('click', '.add-qualification-row', function(e){
  e.preventDefault();
  cloneMore(
    '.qualification-form-row:last', 
    'qualification_belongs_to_candidate', 
    'qualification-form-row', 
    'add-qualification-row',
    'remove-qualification-row'
  );
  return false;
});

$(document).on('click', '.remove-qualification-row', function(e){
  e.preventDefault();
  deleteForm('qualification_belongs_to_candidate', $(this), 'qualification-form-row');
  return false;
});

$(document).on('click', '.add-skill-row', function(e){
  e.preventDefault();
  cloneMore(
    '.skill-form-row:last', 
    'skill_belongs_to_candidate', 
    'skill-form-row', 
    'add-skill-row',
    'remove-skill-row'
  );
  return false;
});

$(document).on('click', '.remove-skill-row', function(e){
  e.preventDefault();
  deleteForm('skill_belongs_to_candidate', $(this), 'skill-form-row');
  return false;
});
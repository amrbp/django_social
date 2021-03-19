$(document).ready(function(){
  $('#model-btn').click(function(){
    console.log('working');
    $('#myModal').on('shown.bs.modal', function () {
      $('#myInput').trigger('focus')
    })
  })
})


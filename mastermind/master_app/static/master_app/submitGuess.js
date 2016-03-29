/**
 * Javascript file for the Mastermind guess logic.
 *
 *
 **/


$().ready(function () {
   
   $('#new-guess').on('submit', submitGuess);


 });

function submitGuess(event) {
   event.preventDefault();

   guessData = $('#new-guess').serializeArray();

   $.ajax({
      url: "newGuess",
      type: "POST",
      data: {csrfmiddlewaretoken: guessData[0].value, the_data: JSON.stringify(guessData)},

      success: function(json) {
         location.reload();
      },
      error: function(xhr, errmsg, err) {
         console.log(xhr.status + ": " + xhr.responseText);
      }
   });

}
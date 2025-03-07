$(function() {

    $("#button").click(refreshQuestionnaireList);

    function remplirQuestionnaires(repjson) {
      console.log(JSON.stringify(repjson));
      $('#questionnaires').empty();
      $('#questionnaires').append($('<ul>'));
      console.log(repjson);
      for(questionnaire of repjson){
          console.log(questionnaire);
          $('#questionnaires ul')
                .append($('<li>')
                .append($('<a>')
                .text(questionnaire.name)
                    ).on("click", questionnaire, details)
                );
        }
      }

      function onerror(err) {
          $("#questionnaires").html("<b>Impossible de récupérer les questionnaires !</b>"+err);
      }

    function refreshQuestionnaireList(){
        $("#currentquestionnnaire").empty();
        requete = "http://127.0.0.1:5000/quiz/api/v1.0/questionnaires";
        fetch(requete)
        .then( response => {
                console.log(response+ " fezfzfezfez");
                  if (response.ok) return response.json();
                  else throw new Error('Problème ajax: '+response.status);
                }
            )
        .then(remplirQuestionnaires)
        .catch(onerror);
      }

    function details(event){
        $("#currentquestionnaire").empty();
        formQuestionnaire();
        fillFormQuestionnaire(event.data);
        showQuestions(event.data.uri);
    }

    

    class Questionnaire{
        constructor(name, uri){
            this.name = name;
            this.uri = uri;

        }
    }
    $("#tools #add").on("click", formQuestionnaire);
    $('#tools #del').on('click', delQuestionnaire);

    function formQuestionnaire(isnew){
        $("#currentquestionnaire").empty();
        $("#currentquestionnaire").append($('<form id="formquestionnaire">'))
            .append($('<span>Titre<input type="text" id="name"><br></span>'))
            .append($('<span><input type="hidden" id="uri"><br></span>'))
            .append(isnew?$('<span><input type="button" value="Save questionnaire"><br></span>').on("click", saveNewQuestionnaire)
                         :$('<span><input type="button" value="Modify questionnaire"><br></span>').on("click", saveModifiedQuestionnaire)
                );
        }

    function fillFormQuestionnaire(t){
        $("#currentquestionnaire #name").val(t.name);
        $("#currentquestionnaire #uri").val(t.uri);
    }

    function saveNewQuestionnaire(){
        var questionnaire = new Questionnaire(
            $("#currentquestionnaire #name").val(),
            $("#currentquestionnaire #uri").val()
            );
        console.log(JSON.stringify(questionnaire));
        fetch("http://127.0.0.1:5000/quiz/api/v1.0/questionnaires",{
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(questionnaire)
            })
        .then(res => { console.log('Save Success') ;
                       $("#result").text(res['contenu']);
                       refreshQuestionnaireList();
                   })
        .catch( res => { console.log(res) });
    }

    function saveModifiedQuestionnaire(){
        var questionnaire = new Questionnaire(
            $("#currentquestionnaire #name").val(),
            $("#currentquestionnaire #uri").val()
            );
        console.log("PUT");
        console.log(questionnaire.uri);
        console.log(JSON.stringify(questionnaire));
        fetch(questionnaire.uri,{
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "PUT",
        body: JSON.stringify(questionnaire)
            })
        .then(res => { console.log('Update Success');  refreshQuestionnaireList();} )
        .catch( res => { console.log(res) });
    }

    function delQuestionnaire(){
        if ($("#currentquestionnaire #uri").val()){
        url = $("#currentquestionnaire #uri").val();
        fetch(url,{
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "DELETE"
            })
        .then(res => { console.log('Delete Success:' + res); } )
        .then(refreshQuestionnaireList)
        .catch( res => { console.log(res);  });
    }
  }

  function showQuestions(uri){
    let id = uri.split('/').pop();
    fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${id}/questions`)
    .then(r => r.json())
    .then(data => {
        $("#currentquestionnaire").append($('<div id="questionsList">Liste des questions :</div>'));
        data.forEach(q => {
            $("#questionsList").append($('<div>')
              .text(q.title + " (" + q.questionType + ") ")
              .append($('<button>').text("Modifier").on("click", () => formQuestion(id, q)))
              .append($('<button>').text("Supprimer").on("click", () => deleteQuestion(id, q.id)))
            );
        });
        $("#currentquestionnaire").append($('<button>')
          .text("Ajouter une question")
          .on("click", () => formQuestion(id, null)));
    });
}

function formQuestion(qid, question){
    $("#currentquestionnaire").empty();
    $("#currentquestionnaire").append($('<input type="text" id="qTitle" placeholder="Titre Question">'))
      .append($('<button>').text(question?"Modifier":"Ajouter")
             .on("click", () => {
                 if(question) saveModifiedQuestion(qid, question.id);
                 else saveNewQuestion(qid);
             }));
    if(question){
        $("#qTitle").val(question.title);
    }
}


function saveNewQuestion(qid){
    let question = {
        title: $("#qTitle").val(),
    };
    fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${qid}/questions`, {
        headers: { 'Accept': 'application/json','Content-Type': 'application/json'},
        method: "POST",
        body: JSON.stringify(question)
    })
    .then(() => showQuestions(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${qid}`));
}

function saveModifiedQuestion(qid, questionId){
    let question = {
        title: $("#qTitle").val(),
    };
    fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${qid}/questions/${questionId}`, {
        headers: { 'Accept': 'application/json','Content-Type': 'application/json'},
        method: "PUT",
        body: JSON.stringify(question)
    })
    .then(() => showQuestions(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${qid}`));
}

function deleteQuestion(qid, questionId){
    fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${qid}/questions/${questionId}`, {
        headers: { 'Accept': 'application/json','Content-Type': 'application/json'},
        method: "DELETE"
    })
    .then(() => showQuestions(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${qid}`));
}
  

  

});

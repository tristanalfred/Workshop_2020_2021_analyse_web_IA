var start;
var end;
var page;
var application;
var estimatedTimer;
var typePage;
var user;

/*
On document ready
*/
$(document).ready(function () {


  start = new Date();
  page = $("#analysis-plugin")[0].attributes.page.value;
  application = $("#analysis-plugin")[0].attributes.application.value;
  estimatedTimer = $("#analysis-plugin")[0].attributes.estimatedTimer.value;
  typePage = $("#analysis-plugin")[0].attributes.typePage.value;

  if (getCookie("userAnalysisPluginID") == null || getCookie("userAnalysisPluginID") == "") {
    $.ajax({
      url: 'http://127.0.0.1:8000/users/',
      type: 'POST',
      dataType: 'JSON',
      contentType: 'application/json; charset=utf-8',
      crossDomain: true,
      success: function (res) {
        console.log(res);
        setCookie("userAnalysisPluginID", res.id, 30);
        user = getCookie("userAnalysisPluginID");
        console.log(console.log("user id sucess modif : " + user));
      }, error: function (err) {
        console.log(err);
      }
    });

  } else {
    user = getCookie("userAnalysisPluginID");
  }

  console.log("user id : " + user);
  console.log("Page :" + page);
  console.log("App :" + application);
  console.log("Estimated time :" + estimatedTimer);
  console.log("type page :" + typePage);

  /*
  On input element clicked
  */
  $('input').click(function (e) {
    var elementClicked = e.currentTarget.attributes[1].value;
    var typeElement = e.currentTarget.attributes[0].value;
    var action = "click";

    console.log(e);
    console.log("action : " + action);
    console.log("type element : " + typeElement);
    console.log("element clicked : " + elementClicked);

    var data = {
      "user": user,
      "element": elementClicked,
      "page": page,
      "typepage": typePage,
      "application": application,
      "estimatedTimer": estimatedTimer,
      "typeaction": action,
      "type_element": typeElement
    };

    //POST action event
    $.ajax({
      url: "http://127.0.0.1:8000/actions/",
      type: 'POST',
      dataType: 'JSON',
      async: false,
      contentType: 'application/json; charset=utf-8',
      crossDomain: true,
      data: JSON.stringify(data),
      success: function (res) {
        console.log("success");
        console.log(res);
      }, error: function (err) {
        console.log("error");
        console.log(err);
      }

    });
  });

  $('select').change(function (e) {
    var elementClicked = e.currentTarget.attributes[1].value;
    var typeElement = "select";
    var action = "change";

    console.log(e);
    console.log("action : " + action);
    console.log("type element : " + typeElement);
    console.log("element clicked : " + elementClicked);

    var data = {
      "user": user,
      "element": elementClicked,
      "page": page,
      "typepage": typePage,
      "application": application,
      "estimatedTimer": estimatedTimer,
      "typeaction": action,
      "type_element": typeElement
    };

    //POST action event
    $.ajax({
      url: "http://127.0.0.1:8000/actions/",
      type: 'POST',
      dataType: 'JSON',
      contentType: 'application/json; charset=utf-8',
      crossDomain: true,
      async: false,
      data: JSON.stringify(data),
      success: function (res) {
        console.log("success");
        console.log(res);
      }, error: function (err) {
        console.log("error");
        console.log(err);
      }

    });
  });
});


/*
On document exit
*/
window.addEventListener('beforeunload', (event) => {
  end = new Date();
  timer = end - start;
  console.log(timer);

  var data = {
    "user": user,
    "time": timer,
    "page": page,
    "typepage": typePage,
    "application": application,
    "estimatedTimer": estimatedTimer
  };

  //POST visites
  $.ajax({
    url: "http://127.0.0.1:8000/visites/",
    type: 'POST',
    dataType: 'JSON',
    contentType: 'application/json; charset=utf-8',
    crossDomain: true,
    async: false,
    data: JSON.stringify(data),
    success: function (res) {
      console.log("success");
      console.log(res);
    }, error: function (err) {
      console.log("error visites");
      console.log(err);
    }
  });
});


function setCookie(name, value, days) {
  var expires = "";
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}
function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}


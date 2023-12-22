$(document).ready(function () {
    ranking_colors();
    getJSON(backgrounds_url, change_background);
    let cells = document.getElementsByTagName("td");

    let CHAR_LIMIT = 37;
    for (let i = 0; i < cells.length; i++) {

      if (cells[i].innerHTML.length > CHAR_LIMIT && !(cells[i].innerText === "")) { 
        cells[i].innerHTML = 
            `<div class="popover-container"><span 
            word-wrap="break-word" 
            data-container="body" 
            data-toggle="popover" 
            data-placement="bottom" 
            overflow-wrap: anywhere 
            data-content="` + cells[i].innerHTML + `">` + cells[i].innerHTML.substring(0, CHAR_LIMIT - 2) + `...</span>` + `</div>`
      }
    }

    $('[data-toggle="popover"]').popover({
        trigger: "hover",
    })   

    $("tbody").sortable({
    update: function(e, ui) {
      ranking_colors();
        let table_data = document.getElementsByClassName("pr_entry");

        let arr = [];
        //gather data
        for (let i = 0; i < table_data.length; i++) {
            let entry_id = table_data[i].id;
            arr.push(entry_id);
        }

        let return_data = {
            "pr_id": table_data[0].children[0].id,
            "entries": arr
        };
        //console.log(return_data);
        upload_data(return_data);
    

        //update rank numbers
        $("tr td:nth-child(1)").text(function() {
        return $(this).parent().index("tr");
        });

  }});
});

function upload_data (partyrank_data) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", submit_url);
    xhr.setRequestHeader("Content-Type", "application/json");

    let data = JSON.stringify(partyrank_data);

    xhr.onload = () => {
        if(xhr.status != 200) {
            if(!alert('An error has occurred which requires the page to be reloaded. Your data will not be saved.')) {
                window.location.reload();
            }
        }
    };

    xhr.send(data);
}

function change_background (image) {
  document.body.style.backgroundImage = "url('" + image + "')";
}

function getJSON (url, callback) {
    fetch(url).then(async response => {

      response.json().then(data => {
        callback(data.result[Math.floor(Math.random()*data.result.length)]);
      })
    }).catch(err => {
        throw err;
    });
}


function ranking_colors () {
  let tr_list = document.getElementsByClassName("pr_entry");

  for (let j = 0; j < tr_list.length; j++) {
    switch (j) {
      case 0:
      tr_list[j].children[0].style.background = "gold";
      break;

      case 1:
      tr_list[j].children[0].style.background = "silver";
      break;

      case 2:
      tr_list[j].children[0].style.background = "brown";
      break;

      default:
      tr_list[j].children[0].style.background = "black";
      break;
    }
    }
}

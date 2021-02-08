//wait untill the web page load so that the input could be extracted 
window.onload = function () { 
    //get the input and output text
    var result = document.getElementById("result");
    //for an event of an enter key press 
    var input = document.getElementById("input").addEventListener('keypress', function (e) {
        if (e.keyCode == 13) {
            handleSend();
            e.preventDefault();
        }
    }, false);
};

//this fucntion checks the users input 
function handleSend(){
    //set the output to nothing 
    result.innerHTML = "";
    //check if the input isnt empty
    if(input.value == ""){
        alert("ERROR - Please Enter A URL Address");
    }
    else {
        //create a fetch request that send and recieves data from the server 
        fetch(`${window.location}receive/`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(input.value), //make the data in a JSON format for long and complex URLs 
            cache: "no-cache",
            headers: new Headers({"content-type" :  "application/json"})
        }).then(function(response) {
            return response.text().then(function(text) {
                //set the output to the short url that server sent 
                result.innerHTML = "<br> Here's Your New Short URL: <br> <br> <a href="+ text +">" + text + "</a>" ;;
            });
        });

    }
}
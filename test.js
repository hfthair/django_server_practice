
function jsontouri(params) {
    var query = "";
    for (key in params) {
        query += encodeURIComponent(key)+"="+encodeURIComponent(params[key])+"&";
    }
    return query;
}


var data = {
    username: 'car',
    password: 'car',
    perms: 'car'
};
var method = "POST";
var url = "http://localhost:8000/api/user/add/";

var xhr = new XMLHttpRequest();
xhr.open(method, url, true);
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
xhr.setRequestHeader("Authorization", btoa("super" + ":" + "1234"))
xhr.onloadend = function () {
    console.log('status: ' + xhr.status)
    console.log('status text' + xhr.statusText)
    console.log('res:' + JSON.stringify(xhr.response))
    console.log('res text:' + JSON.stringify(xhr.responseText))
};

if (method == "GET"){
    xhr.send();
}
else {
    xhr.send(jsontouri(data));
}

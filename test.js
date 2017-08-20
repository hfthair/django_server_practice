var xhr = new XMLHttpRequest();
xhr.open("POST", "http://localhost:8000/api/product/add/", true);
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

xhr.onloadend = function () {
    console.log('status: ' + xhr.status)
    console.log('status text' + xhr.statusText)
    console.log('res:' + JSON.stringify(xhr.response))
    console.log('res text:' + JSON.stringify(xhr.responseText))
};

var data = {
    name: 'beerA',
    desc: 'this is a test product'
}

xhr.send(JSON.stringify(data));

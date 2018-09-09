function api(endpoint, method, data) {
    return $.ajax({
        'url': endpoint,
        'method': method,
        'data': data,
        'contentType': 'application/json'
    })
}

function notify(message, type) {
    $.notify({
        message: message 
    },{
        type: type,
        allow_dismiss: false
    })
}
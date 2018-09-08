function api(endpoint, method, data) {
    return $.ajax({
        'url': 'http://localhost:8080/api/' + endpoint,
        'method': method,
        'data': data,
        'contentType': 'application/json'
    })
}
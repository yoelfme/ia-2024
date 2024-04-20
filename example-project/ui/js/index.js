document.getElementById('send').addEventListener('click', function() {
    // Get value from query input text
    var query = document.getElementById('query').value;

    // WARNING: For POST requests, body is set to null by browsers.
    var data = JSON.stringify({
        "input": {
            "question": query
        },
        "config": {},
        "kwargs": {}
    });

    axios.post("http://127.0.0.1:8000/text-to-sql/invoke", data, {
        headers: {
            "accept": "application/json",
            "Content-Type": "application/json"
        },
        withCredentials: true
    })
        .then(function(response) {
            var output = response.data.output;
            document.getElementById('response').innerHTML = output;
        })
        .catch(function(error) {
            console.error(error);
        });
});
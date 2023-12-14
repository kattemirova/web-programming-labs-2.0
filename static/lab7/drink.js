function getPrice() {
    const milk = document.querySelector('[name=milk]').checked;
    const sugar = document.querySelector('[name=sugar]').checked;
    const drink = document.querySelector('[name=drink]:checked').value;

    const obj = {
        "method": "get-price",
        "params": {
            drink: drink,
            milk: milk, 
            sugar: sugar
        }
    };

    fetch('/lab7/api', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(obj)
    })
    .then(function(resp) {
        return resp.json();
    })
    .then(function(data) {
        document.querySelector('#price').innerHTML = `Цена напитка: ${data.result} руб`;
        document.querySelector('#pay').style.display = '';
        document.querySelector('#errorr').style.display = 'none';
        document.querySelector('#resultt').style.display = 'none';
        document.querySelector('#error').style.display = 'none';
        document.querySelector('#result').style.display = 'none';
    })

}

function pay() {
    const milk = document.querySelector('[name=milk]').checked;
    const sugar = document.querySelector('[name=sugar]').checked;
    const drink = document.querySelector('[name=drink]:checked').value;
    const card_num = document.querySelector('[name=card_num]').value;
    const cvv = document.querySelector('[name=cvv]').value;

    const obj = {
        "method": "pay",
        "params": {
            drink: drink,
            milk: milk, 
            sugar: sugar, 
            card_num: card_num,
            cvv: cvv
        }
    };

    fetch('/lab7/api', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(obj)
    })
    .then(function(resp) {
        return resp.json();
    })
    .then(function(data) {
        document.querySelector('#error').innerHTML = `${data.error}`;
        document.querySelector('#result').innerHTML = `${data.result}`;
        document.querySelector('#error').style.display = '';
        document.querySelector('#result').style.display = '';
    })
}

function refund() {
    const milk = document.querySelector('[name=milk]').checked;
    const sugar = document.querySelector('[name=sugar]').checked;
    const drink = document.querySelector('[name=drink]:checked').value;
    const card_num = document.querySelector('[name=card_num]').value;
    const cvv = document.querySelector('[name=cvv]').value;

    const obj = {
        "method": "refund",
        "params": {
            drink: drink,
            milk: milk, 
            sugar: sugar,
            card_num: card_num,
            cvv: cvv
        }
    };

    fetch('/lab7/api', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(obj)
    })
    .then(function(resp) {
        return resp.json();
    })
    
    .then(function(data) {
        document.querySelector('#errorr').innerHTML = `${data.errorr}`;
        document.querySelector('#resultt').innerHTML = `${data.resultt}`;
        document.querySelector('#error').style.display = 'none';
        document.querySelector('#result').style.display = 'none';
        document.querySelector('#pay').style.display = 'none';
        document.querySelector('#errorr').style.display = '';
        document.querySelector('#resultt').style.display = '';
    })

}

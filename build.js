const path = require('path');
const fs = require('fs');
const dotenv = require('dotenv');

// Specify the path to your .env file
const envFilePath = path.resolve(__dirname, 'mysite', '.env');

// Load environment variables from .env file
dotenv.config({ path: envFilePath });

// Read the firebase template
const firebaseTemplate = fs.readFileSync(path.resolve(__dirname, 'firebase.template.json'), 'utf8');

// Replace the placeholder with the actual backend URL
const firebaseConfig = firebaseTemplate.replace('$BASE_URL', process.env.BASE_URL);

// Write the result to firebase.json
const firebaseJsonPath = path.resolve(__dirname, 'firebase.json');
fs.writeFileSync(firebaseJsonPath, firebaseConfig);

console.log('firebase.json has been generated with the backend URL.');

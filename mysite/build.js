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

// Specify the path to the public folder
const publicFolderPath = path.resolve(__dirname, 'mysite', 'public');

// Write the result to firebase.json
const firebaseJsonPath = path.resolve(__dirname, 'firebase.json');
fs.writeFileSync(firebaseJsonPath, firebaseConfig);

// Output the generated firebase.json path
console.log(`firebase.json has been generated with the backend URL.`);
console.log(`Public folder path: ${publicFolderPath}`);
console.log(`Firebase.json path: ${firebaseJsonPath}`);

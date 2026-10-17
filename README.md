<h1>Setup Instructions</h1>

**STEP 1**
<p>Install the following:</p>
<ul>
  <li>Python - https://www.python.org/downloads/</li>
  <li>MongoDB Compass - https://www.mongodb.com/products/tools/compass</li>
  <li>Git - https://git-scm.com/install/windows</li>
</ul>
<br />

**STEP 2**
<p>Clone repository:</p>
<p>Run this command:</p>
<ul>
  <li>git clone https://github.com/darkmasule/WS1_Finals_Project.git</li>
</ul>
<br />

**STEP 3**
<p>Open the project folder and create a virtual environment:</p>
<p>Make sure you're on the right directory:</p>
<ul>
  <li>cd (project folder path)</li>
</ul>

<p>Run this command:</p>
<ul>
  <li>python -m venv .venv</li>
</ul>

<p>Activate virtual environment:</p>
<p>Run this command:</p>
<ul>
  <li>.\.venv\Scripts\Activate.ps1</li>
</ul>
<br />

**STEP 4**
<p>Install dependencies:</p>
<p>Run this command:</p>
<ul>
  <li>pip install -r requirements.txt</li>
</ul>
<br />



**STEP 5**
<p>Configure MongoDB connection:</p>
<p>Run this command:</p>
<ul>
  <li>$env:MONGO_URI = "connection string I gave"</li>
</ul>
<br />

**STEP 6**
<p>Configure Flask secret key:</p>
<p>Run this command:</p>
<ul>
  <li>python -c "import secrets; print(secrets.token_hex(32))"</li>
</ul>

**SAVE THE GENERATED KEY ON A TEXT FILE**
<p>Copy the generated key and set the environment variable:</p>
<ul>
  <li>$env:SECRET_KEY = "PASTE KEY HERE"</li>
</ul>
<br />

**STEP 7**
<p>Run the application:</p>
<p>Run this command:</p>
<ul>
  <li>python app.py</li>
</ul>

<p>Open local address: (usually like this)</p>
<ul>
  <li>http://127.0.0.1:5000</li>
</ul>
<br />

**STEP 8**
<p>To stop the application:</p>
<ul>
  <li>CTRL + C</li>
</ul>

<h2>That is all. Please tell me if you're having trouble setting it up. -Lei</h2>

<!-- Project Asset Build Verified -->

<!-- Build Verification Log -->

# Setting Up a Flask CRUD App with Vue.js and MongoDB Atlas

## Prerequisites:
- Python: Ensure you have Python installed.
- Node.js and npm: Install Node.js and npm for the Vue.js frontend.
- MongoDB Atlas Account: Create a free MongoDB Atlas account.

## Setting Up the Backend (Flask)

1. Create a Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install Required Packages:

```bash
pip install Flask pymongo python-dotenv
```

3. Configure MongoDB Atlas:

- Create a new cluster on MongoDB Atlas.
- Add a database user and note the username, password, and cluster connection string.
- Create a `.env` file in the root of the project.
- Add `MONGO_URI=mongodb+srv://<your_username>:<your_password>@<your_cluster_address>.mongodb.net/` into the file, replacing with your own connection string.

4. Populate the Database
- Run `python parser.py` for the Mongo database be populated with data.json.

5. Run the server
```bash
cd server
python app.py
```

6. Run the client
- Install dependencies and run the client.

```bash
cd ../client/
npm i
npm run dev
```
- Open http://localhost:3000/
# Victory Lap Gym Management Web App
This project is a gym management web app built using Python and the Streamlit library.
We will query a databse to utilize CRUD methodologies.


1. ## Installation
#### Clone the repo:
```bash
git clone https://projectURL
cd projectName
```

2. ## Create and activate virtual environment:
#### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

3. ## Create .pth file to point python to your project
#### After venv is created...
#### Navigate to: **ProjectName/venv/lib/pythonX.XX/sitepackages**
#### Create **my_project.pth**
#### Inside of this file add the directory of your project.
#### Ex: **Users/user/projects/VictoryLapProject**
#### **NOTE:** Get this from running 'pwd' in your project terminal

4. ## Install Dependencies
#### Inside the repo run:
```bash
pip install -r requirements.txt
```

5. ## Create your own .env file
#### Ensure the .env is in the root directory, and has important credentials stored:
```bash
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

5. ## To run application use:
```bash
streamlit run app.py
```




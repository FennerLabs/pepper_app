# Predict Environmental Pollutant PERsistence (PEPPER) application

This application leverages a streamlit-based UI where users can input a .csv file containing the on a single column (names SMILES) a series of 
[SMILES](https://www.daylight.com/dayhtml/doc/theory/theory.smiles.html) and receive an image representation of each compound together with the predicted 
breakthrough of this compound on a waster water treatment plant.

## How to run it locally
1. First install [Docker Desktop](https://docs.docker.com/compose/install/)
2. Open Docker Desktop and open its terminal.
3. On the terminal:
*  Git clone this repository:
```
git clone git@github.com:FennerLabs/pepper_app.git
```
* Travel to the folder that you just cloned:
```
cd pepper_app
```
* Run the `docker compose` command:
```
docker compose up --build
```
4. On the *Container* tab you should now find the pepper_app running, it should show as follows:
![image](https://github.com/user-attachments/assets/3af55d22-e020-4fe7-90d5-b34ba97fa79c)
5. Click on the link [8501:8501](http://localhost:8501/) to access your own version of pepper_app


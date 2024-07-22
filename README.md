# MedForecast

![MedForecast Logo](static/images/medfc%20logo.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Introduction](#introduction)
- [License](#license)


## Introduction

MedForecast is a health prediction system that uses already tested data from medical datasets to help users find the underlying problem with them faster. 

For example, if you have a headache, MedForecast can help you determine whether it is a symptom of a more serious condition. 

MedForecast also provides other features, such as the top 10 trending diseases and a symptom checker.

Cool, right? 😉

## Features

- User authentication and authorization.
- Health Prediction with a model
- Checking medical history
- Short explanations about health conditions
- Admin panel managing the web application

## Installation

The project is now yet to be deployed, for the mean time in order to access the project

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Grandkojo/MedForecast.git
    ```

2. **Set up the web server:**
    - The project was built with Flask.
    - Create a new virtual environment and run the `requirements.txt` file to get the required modules
    ```bash
    pip install -r requirements.txt
    ```
    - Set up a Supabase account, to connect to the database
    - Create a .env file that has the database password and the username: kindly follow the naming in the app.py file

3. **Important**
    - The landing/home page : ```localhost:5000/```
    - The admin landing page: ```localhost:5000/admin/```

You're good to go 🥳.

## Usage

1. **User registration and / or signup**
    - Users can signup or login to the application to access the quiz questions.

2. **Health predicton**
    - Users are presented with a dynamic form for them to answer some questions along with their pressing symptom for the model to predict what might be wrong with them.

3. **View medical results history**
    - Users can also check the medica results of all their previous forms they took according to the most recent with also answers they chose with the corresponding model accuracy and predicted diagnosis for tracking purposes.


## Project Structure

MEDFORECAST/<br>
|-- views/<br>
|-- tests/<br>
|-- artifacts/<br>
|-- src/<br>
|-- static/<br>
|-- templates/<br>
|-- .env<br>
|-- .gitignore<br>
|-- app.py<br>
|-- LICENSE<br>
|-- README.md<br>
|-- requirements.txt<br>


## Technologies Used

- Flask (framework).
- Supabase (Postgresql database).
- Bootstrap: Front-end framework for responsive web design.
- Javascript: For making the app dynamic.

## License

This project is licensed under the [MIT License](LICENSE).

Built by Group 14 of COE(ACES)
1. Ghanney Caleb - 7098921
2. Essien Ernest kojo - 7098521
3. Boakye Princella - 7095421
4. Francis Redeemer - 7097921
5. Adwoa Agyapooma - 7106421
6. Nana Kwame Bediako - 7094621
7. Kpodo Michael - 7101521
8. Alex Asare Sakyi - 7108921
9. Kofi Korankye Afrifa - 7088921 
10. Helechi Carl-bright - 7100021
11. David Kwame Castel - 7096221
12. Mensah Eugene Kwame - 7102921

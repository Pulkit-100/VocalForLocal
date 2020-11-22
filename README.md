# VocalForLocal

VocalForLocal is a very simple intuitive web application that allows you to find Indian alternatives to your favourite brands. Extending to the functionality, it allows a forgiving format searchbar that enables users to even search by category names. Along with giving a small brand description it enhances the interactivity further by having an "Explore products" button for each listed brands.

_**Working**_: There is a simple search bar that let's users search by categories or brand names. Flask is used in the backend. There are three routes:
1. Response: Response route is used to get data from db, the input is first checked in 'India' table in DB, if it's found there we render page with 'The searched query is an Indian Brand' view, else then it's searched in 'Master' table if it's found there, we take its notes and search inside 'India' table to show alternatives of that Foreign Brand with it's respective notes, else we will look for notes in 'India' table and show will all Indian results of that category, else we display the "Not Found in DB" view.
2. Query: Query route is used to store response of user's query in our DB
3. landing page route '/': Used to render landing page

The database has been constructed by scraping various web-sites using automated scripts following a manual validation. It is stored in MongoDB. The UI is developed by HTML, CSS and Vanilla JS. Application Telemetrics have also been used.

## Prototype

[Check the prototype video here](https://drive.google.com/file/d/1oljkFNXavSayZS0uYjSFk86AkBN4Vx-6/view?usp=sharing)

## Getting Started

### Prerequisites

You'll be requiring Python3 and PIP for running the web application. Check these quick installation video guides

- For Windows: [Check this video](https://www.youtube.com/watch?v=oNLhg29aykc&feature=youtu.be)
- For Ubuntu: [Check this video](https://www.youtube.com/watch?v=FfkPLekXuL4&feature=youtu.be)

### Clone

Clone this repo to your local machine using `git clone https://github.com/nitin10s/vocalforlocal.git` or download it as ZIP

## Installing

1. You'll be required to first install all the necessary requirements. Follow these steps on a Terminal/Windows Power Shell:

```
cd server
pip install -r requirements.txt
```

2. After installing all the requirements, all you need to do is execute the main.py file:

```
python3 app.py
``` 
or 
```
python app.py
``` 
[Depending on the system]

and Voila! the development environment will start running 


## Authors

- [Nitin Singhal](https://github.com/nitin10s)
- [Pulkit Khurana](https://github.com/Pulkit-100)
- [Samarth Sharma](https://github.com/RoLoDeXx)


﻿# Diversity Hire

Showcase: [Youtube](https://youtu.be/mjV-2GF-nx0)

## Setup
This is for initial setup, if you have done this before, straight away jump to [Local]()
```
$ py -m venv venv
$ venv/Scripts/activate
$ cd django
$ pip install ./requirements.txt
```

## Local
Open two terminals in Visual Studio Code
```
# First terminal
$ venv/Scripts/activate
$ python ./manage.py runserver

# Second terminal
venv/Scripts/activate
$ python ./manage.py tailwind start
```

## File Directory
```
|- django                 # django directory
  |- apps                 # django apps
    |- accounts           # user accounts
    |- api                # scorecard apis
    |- jobs               # jobs CRUD
    |- qualifications     # qualifications CRUD
    |- skills             # skills CRUD
  |- core                 # django project directory
    |- settings.py        # (very important) all the django project settings
  |- scripts              # scripts to load data to database
  |- static               # images, css, and javascripts
  |- templates            # HTML
  |- theme                # tailwind
  |- manage.py
  |- requirements.txt
|- extra
  |- final_datasets       # all datasets
    |- django             # data to load into django models
    |- nlp                # data to train nlp embeddings
    |- usage              # data to load into django models
|- .gitignore
|- README.md
```

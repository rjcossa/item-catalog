# Udacity FSND Item Catalog

This repository contains the fourth project in the FSND curriculum with an item catalog that separates items by categories. It was a very interesting project that helped to hone a wide number of skills.

## Installation

### Preparing the Virtual Machine

In order to install this application you need to perform the following steps:

* Download and install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
* Fork [this](https://github.com/udacity/fullstack-nanodegree-vm) Github Repository that has the VM Configuration
* Change Directory to the vagrant folder in the repository
* Type the command `vagrant up` to start the VM
* After the vm starts successfully type the command `vagrant ssh`


### Cloning the repository

* Clone this repository and place it's contents under inside the Virtual machines `/vagrant/catalog/` directory

### Configuring Google OAUTH

* Access the [Google Developer Console](https://console.developers.google.com) (You may need to create an account if you do not have one yet)
* Create a new [Project](https://console.developers.google.com/projectcreate?)(You can name it Udacity Item Catalog)
* Go to the [API Console](https://console.developers.google.com/apis/credentials)
* Click on Create Credentials
* Choose OAUTH Client ID
* Select Web Application
* Add http://localhost:8000 to the Authorized Javascript origins and the the authorized redirect URIs
* Download the client Secret
* Rename the client secret to `client_secrets.json` and place it in the `/vagrant/catalog/` in the VM
* Copy the Client ID and place it in the `/vagrant/catalog/templates/login.html` file replacing `data-client-id`

### Adding Pixabay API Key

This project uses pixabay to search for and store item images. In order to use it to the full extent it is required that you obtain an api key from pixabay and save it to the application. Steps follow:

* Go to the [Pixabay API Page](https://pixabay.com/api/docs/
)
* Login / Sign Up to see your API key
* Return to the [Pixabay API Page](https://pixabay.com/api/docs/
) in order to see your API Key
* Replace the API key in the `/vagrant/catalog/pixabay_connector.py` file


## Running the Application

In order to run the application the following steps should be performed:

* Run the `db/database.py ` file to initialize the DB
* Run the `itemgenerator.py` file to insert sample data to the DB
* Run the `catalogOperations.py` file in order to start the web server

## Accessing the APPLICATION_NAME

In order to access the application point your favorite browser to http://localhost:8000

### Endpoints:

#### Catalog Endpoint

* Endpoint URI: http://localhost:8000/catalog/JSON
* Function: Display all of the categories and the latest items

#### Item View Endpoint

* Endpoint URI: http://localhost:8000/catalog/category_name/item_name/JSON
* Function: Display information about an item and it's category

##### Values

* category_name: Name of the Category
* item_name: Name of the Item

#### Category View Endpoint

* Endpoint URI: http://localhost:8000/catalog/category_name/items/JSON
* Function: Display information about a category and all of it's items

##### Values

* category_name: Name of the Category

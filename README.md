# SoftdeskAPI
An API using Django Rest Framework to allow the retrieval and modification of data used by the softdesk application.

## Setup and execution:
This API can be installed and deployed locally following these steps:

### Setup
1. Clone the repository using`$git clone https://github.com/Corentin-Br/Projet-10.git` or downloading [the zip file](https://github.com/Corentin-Br/Projet-10/archive/refs/heads/master.zip).
2. Create the virtual environment with `$ py -m venv env` on windows or `$ python3 -m venv env` on macos or linux.
3. Activate the virtual environment with `$ env\Scripts\activate` on windows or `$ source env/bin/activate` on macos or linux.
4. Install the dependencies with `$ pip install -r requirements.txt`.

### Execution
1. If that's not already the case, activate the virtual environment as you did during the setup.
2. Get in the folder Softdesk with `$ cd Softdesk`
3. Deploy the API locally with `$ python manage.py run server`


### Use
1. You can use your preferred tool to use the API (cURL, Postman...). The documentation for all endpoints can be found on [Postman](https://documenter.getpostman.com/view/15941590/Tzz5vetE)
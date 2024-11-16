
# Credit Approval System

This is a Credit Approval System built using Django Rest Framework (DRF) and PostgreSQL. The system manages the process of credit approval, including functionalities to create new loans, view loan details, and view loans based on customer IDs.

## Features

- Create new loans
- View loan details by loan ID
- View all loans for a specific customer
- REST API architecture built with Django Rest Framework
- User authentication (optional) for secure loan management

## Technologies Used

- **Django**: Web framework for backend development
- **Django Rest Framework (DRF)**: For creating APIs
- **PostgreSQL**: Relational database for storing loan and customer information
- **Docker**: For containerizing the application
- **Pipenv**: For managing Python dependencies

## Installation
### 1. Clone the Repository

#Clone the repository to your local machine:
git clone https://github.com/megha519/Credit-Approval-System.git
cd Credit-Approval-System



#2. Set Up Virtual Environment with Pipenv
Ensure you have Pipenv installed. If not, install it using:
pip install pipenv
#Now, create a virtual environment and activate it:
pipenv shell


#3. Install Required Dependencies
Once you're inside the virtual environment, install the required dependencies:
pip install requirements.txt


#4. Install Docker and PostgreSQL
If you haven't installed Docker and PostgreSQL yet, you can do so from the following links:
Install Docker (download and install Docker from the official website)
Install PostgreSQL (download and install PostgreSQL from the official website)
#5. Set Up Docker Containers
Once Docker is installed, you can use Docker Compose to set up and run the containers. In your terminal, run the following command to start the application:
docker-compose up
This will start the Django application and PostgreSQL database using Docker containers.

#6. Set Up the Database
After Docker is up and running, apply database migrations:
python manage.py migrate


#7. Run the Development Server
Finally, run the development server to start the API:
python manage.py runserver
The API should now be available at http://127.0.0.1:8000/api/.
Endpoints
POST /api/loans/create-loan/: Create a new loan
GET /api/loans/view-loan/{loan_id}/: View loan details by loan ID
GET /api/loans/view-loans/{customer_id}/: View all loans for a customer by customer ID
Video Demo
You can view the demo of the project here: Demo Video

Contributing
Fork the repository
Create your feature branch (git checkout -b feature-name)
Commit your changes (git commit -m 'Add new feature')
Push to the branch (git push origin feature-name)
Create a new Pull Request

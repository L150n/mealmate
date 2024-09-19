# Meal Mate

MealMate is an innovative solution for college canteens that aims to improve the efficiency of their payment systems. The project is built using Django, a popular web development framework in Python.

The application has two main modules:

- **Student Module**: 
  - Allows students to sign up, sign in, update profile information, update their password, add facial data (for recognition), and add funds to their e-wallet.
  - Students can view their transaction and order history, add items to their cart, and place orders by proceeding to checkout.
  - Secure payments are completed using a password, and students can view or download their receipt.
  - Students can also provide feedback on food items.

- **Canteen Staff Module**: 
  - Staff members can manage the menu (add, edit, delete items), place new orders by scanning the student's face, and process payments from the student's e-wallet.
  - Staff members can view both online and offline orders, student reviews, and sales statistics.

The application uses cutting-edge technology, including facial recognition and virtual wallets, to enhance convenience, security, and hygiene in the payment process.

---

## Running the Project Locally

### Prerequisites

- Python 3.10
- Django

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/mealmate.git
cd mealmate
```
### 2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
### 3. Install dependencies:

```bash
pip install -r requirements.txt
```
### 4. Run migrations:

```bash
python manage.py migrate
```
### 4. Start the development server:

```bash
python manage.py runserver
```
### 4. Access the application at http://localhost:8000

## Running the Project Using Docker

### Prerequisites

- Docker

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/mealmate.git
cd mealmate
```
### 2. Build the Docker image:

```bash
docker build -t mealmate-app .
```
### 3. Run the Docker container:

```bash
docker run -p 8000:8000 mealmate-app
```
### 4. Access the application at http://localhost:8000

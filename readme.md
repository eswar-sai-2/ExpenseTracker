# ExpenseTracker – Personal Expense Management Android App

A personal expense management Android application built using **Python, Kivy and Supabase**. It allows users to create accounts, log in and manage their daily expenses through a simple mobile interface.

The application includes expense tracking, category-wise summaries, expense editing and deletion, and cloud-based data storage.



## Features

- **User Registration** – Create a personal account using email and password.
- **User Login** – Authenticate users through Supabase Authentication.
- **Add Expenses** – Record expenses by entering an amount, category and description.
- **Edit Expenses** – Modify previously recorded expenses.
- **Delete Expenses** – Remove unwanted expense records.
- **Expense Summary** – Display total spending and the number of recorded expenses.
- **Category-wise Summary** – View spending organized by categories.
- **Recent Expenses** – View recently recorded expenses.
- **Individual User Data** – Each authenticated user accesses their own expense records.
- **Cloud Database** – Store expense records in Supabase PostgreSQL.
- **Android APK** – Package the Python application into an Android application.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and functionality |
| Kivy | Building the mobile application UI |
| Requests | Sending HTTP requests to Supabase APIs |
| Supabase | Backend platform |
| Supabase Auth | User registration and authentication |
| PostgreSQL | Database for storing expense records |
| REST API | Communication between the application and backend |
| Buildozer | Packaging the Python application into an Android APK |
| Python-for-Android | Running Python applications on Android |
| Ubuntu WSL2 | Android development and build environment |
| Git | Version control |
| GitHub | Source code hosting |

---

## Expense Categories

The application supports the following expense categories:

- Food
- Travel
- Shopping
- Education
- Bills
- Health
- Entertainment
- Other

---

## Project Architecture

```text
              Android Application
                      |
                      v
                   main.py
              Application UI
                      |
          +-----------+-----------+
          |                       |
          v                       v
       auth.py                 expense.py
  Authentication logic      Expense operations
          |                       |
          +-----------+-----------+
                      |
                      v
                  Supabase
              +-------+-------+
              |               |
              v               v
         Supabase Auth     PostgreSQL
          User Login       Expense Data
```

---

## How the Application Works

### 1. User Registration

- The user enters an email address and password.
- The application sends the registration request to Supabase Authentication.
- Supabase creates the user account.

### 2. User Login

- The user enters their login credentials.
- The application sends an authentication request.
- Supabase validates the credentials.
- After successful authentication, the application receives an access token.

### 3. Adding an Expense

- The user enters an amount.
- Selects a category.
- Enters an optional description.
- Submits the expense.
- The application sends the expense information to Supabase.
- The expense is stored in the PostgreSQL database.

### 4. Viewing Expenses

- The application retrieves the user's expense records.
- The dashboard displays total spending.
- The number of expenses is displayed.
- Category-wise spending is calculated.
- Recent expense records are displayed.

### 5. Editing an Expense

- The user selects an existing expense.
- The editing form displays its information.
- The user modifies the amount, category or description.
- The updated record is sent to Supabase.

### 6. Deleting an Expense

- The user selects the delete option.
- A confirmation dialog appears.
- After confirmation, the expense record is deleted from the database.

### 7. Logout

- The user can log out from the application.
- The current application session is cleared.

---

## Project Structure

```text
ExpenseTracker/
│
├── main.py
│   └── Application UI and main application logic
│
├── auth.py
│   └── User registration and login
│
├── expense.py
│   └── Expense database operations
│
├── supabase_config.py
│   └── Supabase configuration
│
├── requirements.txt
│   └── Python dependencies
│
├── buildozer.spec
│   └── Android application build configuration
│
├── README.md
│   └── Project documentation
│
├── .gitignore
│   └── Files excluded from Git
│
└── screenshots/
    └── Application screenshots
```

---

## File Responsibilities

### main.py

The main application file.

It is responsible for:

- Creating the user interface using Kivy.
- Login and registration screens.
- Dashboard.
- Adding expenses.
- Displaying expense records.
- Editing expenses.
- Deleting expenses.
- Displaying summaries.
- Connecting UI actions with other Python modules.

### auth.py

Responsible for authentication.

It handles:

- User registration.
- User login.
- Sending authentication requests to Supabase.
- Handling authentication responses.
- Returning the access token after successful login.

### expense.py

Responsible for expense management.

It handles:

- Retrieving expense records.
- Adding expenses.
- Updating expenses.
- Deleting expenses.
- Calculating total spending.
- Calculating category-wise totals.

### supabase_config.py

Contains the Supabase configuration required for API communication.

It provides the configuration used by the application to connect to the Supabase backend.

### requirements.txt

Contains the Python packages required by the project.

### buildozer.spec

Contains configuration required to package the Python application into an Android APK.

---

## Backend and Database

The project uses Supabase as its backend.

### Supabase Authentication

Supabase Authentication manages user registration and login.

### PostgreSQL Database

Expense information is stored in a PostgreSQL table named `expenses`.

The table contains the following fields:

| Column | Description |
|---|---|
| id | Unique expense identifier |
| user_id | User associated with the expense |
| amount | Expense amount |
| category | Expense category |
| description | Optional expense description |
| created_at | Expense creation timestamp |

### Row Level Security (RLS)

Row Level Security is enabled on the expenses table.

RLS policies restrict authenticated users from accessing other users' expense records.

The application uses the authenticated user's identity to control access to their expense data.

---

## Security

- Supabase Authentication is used for user authentication.
- PostgreSQL stores expense information.
- Row Level Security protects individual users' expense records.
- The application uses a Supabase publishable key for client-side API access.
- Supabase service-role keys must never be included in the Android application.
- Database access is controlled through authentication and RLS policies.

---

## Development Environment

The project was developed using:

- Python
- Kivy
- Supabase
- PostgreSQL
- Buildozer
- Python-for-Android
- Ubuntu 22.04 through WSL2
- Visual Studio Code

---

## Running the Application Locally

### 1. Clone the Repository

```bash
git clone https://github.com/eswar-sai-2/ExpenseTracker.git
```

### 2. Navigate to the Project

```bash
cd ExpenseTracker
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate the Virtual Environment

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Supabase

Configure the Supabase project URL and publishable key in `supabase_config.py`.

Ensure the Supabase authentication service, PostgreSQL table and RLS policies are configured.

### 7. Run the Application

```bash
python main.py
```

---

## Building the Android APK

The application uses Buildozer and Python-for-Android to create an Android APK.

Run the following command from the project directory:

```bash
buildozer -v android debug
```

After a successful build, the APK is generated in the `bin/` directory.

The APK can then be transferred to an Android device and installed.

---

## Limitations

- Internet connectivity is required for authentication and cloud database operations.
- The application currently requires users to log in again after restarting the app.
- The application is currently packaged as a debug APK.

---

## Future Improvements

- Persistent login sessions.
- Monthly and yearly expense reports.
- Expense charts and graphs.
- Budget limits.
- Notifications.
- Export expenses to CSV.
- Search and filtering.
- Dark mode.
- Production-ready Android release.

---

## Project Objective

This project was developed to gain practical experience in:

- Python application development.
- Mobile application development using Kivy.
- Backend integration.
- REST API communication.
- User authentication.
- PostgreSQL database operations.
- CRUD operations.
- Database security using Row Level Security.
- Android application packaging.
- Building and deploying Python applications to Android.

---

**Built with Python, Kivy and Supabase.**

## 📱 Download Android App

[![Download APK](https://img.shields.io/badge/Download-Android%20APK-green?style=for-the-badge&logo=android)](https://github.com/eswar-sai-2/ExpenseTracker/releases/latest)

Download and install ExpenseTracker on your Android device.
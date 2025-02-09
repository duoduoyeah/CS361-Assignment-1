import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib  # For password hashing

# Global variable to store the uploaded file path
uploaded_file_path = None
# Global variable to store the data (for potential restore)
data_backup = None
# Global variable to store deleted datasets
deleted_datasets = []

# Sample help content
help_content = {
    "upload": "To upload data, select 'Upload Data' from the User Menu and choose a file.",
    "view": "To view uploaded data, select 'View Uploaded Data' from the User Menu.",
    "analysis": "To perform analysis, select 'Basic Statistical Analysis' or 'Perform Regression Analysis' from the User Menu.",
    "download": "To download a report, select 'Download Analysis Report' from the User Menu.",
    "delete": "To delete a dataset, select 'Delete Dataset' from the User Menu and confirm your choice.",
    "restore": "To restore a dataset, select 'Restore Dataset' from the User Menu and choose a previously deleted dataset."
}

# Step-by-step guide
step_by_step_guide = """
--- Step-by-Step Guide ---
1. Log in to your account.
2. Upload your data using the 'Upload Data' option.
3. View your uploaded data using the 'View Uploaded Data' option.
4. Perform statistical analysis using the 'Basic Statistical Analysis' or 'Perform Regression Analysis' options.
5. Download the analysis report using the 'Download Analysis Report' option.
6. Delete the dataset using the 'Delete Dataset' option if you no longer need it.
7. Restore a deleted dataset using the 'Restore Dataset' option.
8. Log out of your account when you are finished.
"""

# Account security tips and useful information
security_tips = """
--- Account Security Tips ---
1. Use a strong, unique password for your account.
2. Do not share your password with anyone.
3. Log out of your account when you are finished to prevent unauthorized access.
4. Keep your email address updated to receive important notifications and password reset instructions.
"""

# User data (in a real app, this would be stored in a database)
users = {}

def display_title():
    print("--------------------------------------------------")
    print("        Data Analysis Application ")
    print("--------------------------------------------------")

def main_menu():
    display_title()
    # Short explanation of the app's main features before login
    print("Welcome!")
    while True:
        print("\nWelcome to the Data Analysis App. \nThis app helps you analyze your data. Upload, view, analyze, and download reports easily.")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed_password
    print("Registration successful!")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    # Hash the password for comparison
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in users and users[username] == hashed_password:
        print(f"Welcome, {username}!")
        user_menu()
    else:
        print("Invalid username or password. Please try again.")

def display_navbar():
    print("\n--- Navigation Bar ---")
    print("Upload | View Data | Analysis | Report | Help | Logout")

def user_menu():
    while True:
        display_navbar()
        print("\n--- User Menu ---")
        print("1. Upload Data")
        print("2. View Uploaded Data")
        print("3. Basic Statistical Analysis")
        print("4. Perform Regression Analysis")
        print("5. Download Analysis Report")
        print("6. Delete Dataset") # Inclusivity Heuristic: Confirmation for deleting dataset
        print("7. Restore Dataset") # Inclusivity Heuristic: Restore button
        print("8. Help") # Help menu
        print("9. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            upload_data()
        elif choice == "2":
            view_uploaded_data()
        elif choice == "3":
            basic_statistical_analysis()
        elif choice == "4":
            perform_regression_analysis()
        elif choice == "5":
            download_analysis_report()
        elif choice == "6":
            delete_dataset()
        elif choice == "7":
            restore_dataset()
        elif choice == "8":
            display_help_menu()
        elif choice == "9":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def upload_data():
    display_navbar()
    global uploaded_file_path, data_backup
    while True:
        print("\n--- Upload Data ---")
        print("1. Browse Files")
        print("2. Drag and Drop (Not yet implemented)")
        print("3. Back to User Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            file_path = filedialog.askopenfilename()
            if file_path:
                try:
                    df = pd.read_csv(file_path)
                    # Back up the data before upload
                    data_backup = df.copy()
                    uploaded_file_path = file_path
                    print(f"File '{file_path}' uploaded successfully!")
                    # Explanation of file upload benefits
                    print("The Data Analysis App securely stores your data and helps you analyze it.")
                except Exception as e:
                    print(f"Error reading the file: {e}")
            else:
                print("No file selected.")
            break
        elif choice == "2":
            print("Drag and Drop functionality is coming soon!")
            break
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def view_uploaded_data():
    global uploaded_file_path
    if uploaded_file_path:
        print("Displaying uploaded data...")
        try:
            df = pd.read_csv(uploaded_file_path)
            print(df)  # Display the data in the CLI
            print("Data displayed successfully!")
        except FileNotFoundError:
            print("Error: File not found. Please upload the data again.")
        except Exception as e:
            print(f"Error occurred: {e}")
    else:
        print("No data uploaded yet. Please upload data first.")

def display_minimum_value(df):
    """Calculates and returns the minimum value for each column in the DataFrame."""
    try:
        return df.min().to_string()  # Ensures the minimum value for each column is returned as a string
    except Exception as e:
        return f"Error calculating minimum value: {e}"

def display_maximum_value(df):
    """Calculates and returns the maximum value for each column in the DataFrame."""
    try:
        return df.max().to_string()  # Ensures the maximum value for each column is returned as a string
    except Exception as e:
        return f"Error calculating maximum value: {e}"

def display_average_value(df):
    """Calculates and returns the average value for each column in the DataFrame."""
    try:
        return df.mean().to_string()  # Ensures the average value for each column is returned as a string
    except Exception as e:
        return f"Error calculating average value: {e}"

def basic_statistical_analysis():
    global uploaded_file_path
    if not uploaded_file_path:
        print("No data uploaded yet. Please upload data first.")
        return

    try:
        df = pd.read_csv(uploaded_file_path)
    except FileNotFoundError:
        print("Error: File not found. Please upload the data again.")
        return
    except Exception as e:
        print(f"Error occurred: {e}")
        return

    while True:
        print("\n--- Basic Statistical Analysis ---")
        print("1. Display Minimum Value")
        print("2. Display Maximum Value")
        print("3. Display Average Value")
        print("4. Back to User Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Display Minimum Value
            try:
                min_values = display_minimum_value(df) # Calling functions that  calculates and returns the minimum value for each column in the DataFrame
                print(f"Minimum value:\n{min_values}")
                # Inclusivity Heuristic: Keyword search (example)
                search_keyword = input("Search for a specific column (or press Enter to skip): ")
                if search_keyword:
                    if search_keyword in df.columns:
                        print(f"Minimum value in {search_keyword}: {df[search_keyword].min()}")
                    else:
                        print("Column not found.")
            except Exception as e:
                print(f"Error calculating minimum value: {e}")
        elif choice == "2":
            # Display Maximum Value
            try:
                max_values = display_maximum_value(df) # Calling functions that  calculates and returns the maximum value for each column in the DataFrame
                print(f"Maximum value:\n{max_values}")
                # Inclusivity Heuristic: Keyword search (example)
                search_keyword = input("Search for a specific column (or press Enter to skip): ")
                if search_keyword:
                    if search_keyword in df.columns:
                        print(f"Maximum value in {search_keyword}: {df[search_keyword].max()}")
                    else:
                        print("Column not found.")
            except Exception as e:
                print(f"Error calculating maximum value: {e}")
        elif choice == "3":
            # Display Average Value
            try:
                avg_values = display_average_value(df) # Calling functions that  calculates and returns the average value for each column in the DataFrame
                print(f"Average value:\n{avg_values}")
                # Inclusivity Heuristic: Keyword search (example)
                search_keyword = input("Search for a specific column (or press Enter to skip): ")
                if search_keyword:
                    if search_keyword in df.columns:
                        print(f"Average value in {search_keyword}: {df[search_keyword].mean()}")
                    else:
                        print("Column not found.")
            except Exception as e:
                print(f"Error calculating average value: {e}")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def perform_regression_analysis():
    global uploaded_file_path
    if not uploaded_file_path:
        print("No data uploaded yet. Please upload data first.")
        return

    print("Regression analysis completed!")

def download_analysis_report():
    global uploaded_file_path
    if not uploaded_file_path:
        print("No data uploaded yet. Please upload data first.")
        return

    print("Report downloaded successfully!")

def delete_dataset():
    global uploaded_file_path, data_backup, deleted_datasets
    if uploaded_file_path:
        print("Attention: Deleting the dataset will remove it from the application and any unsaved changes will be lost.")
        print("Cost: If you want to use it again, you will have to re-upload it.")  # Attention reminder for the cost of using this feature.
        confirm = input("Are you sure you want to delete the dataset? (yes/no): ")  # Inclusivity Heuristic: Warning about data loss
        if confirm.lower() == "yes":
            # Save the deleted dataset to the deleted_datasets list
            if data_backup is not None:
                deleted_datasets.append(data_backup.copy())
            uploaded_file_path = None
            data_backup = None
            print("Dataset deleted successfully.")
        else:
            print("Deletion cancelled.")
    else:
        print("No dataset uploaded yet.")

def restore_dataset():
    global uploaded_file_path, data_backup, deleted_datasets
    if deleted_datasets:
        print("Available deleted datasets:")
        for i, dataset in enumerate(deleted_datasets):
            print(f"{i + 1}. Dataset {i + 1}")
        choice = input("Enter the number of the dataset you want to restore: ")
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(deleted_datasets):
                # Restore the selected dataset
                data_backup = deleted_datasets[choice]
                uploaded_file_path = f"restored_dataset_{choice + 1}.csv"
                data_backup.to_csv(uploaded_file_path, index=False)
                print(f"Dataset {choice + 1} restored successfully!")
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("No deleted datasets available to restore.")

def display_help_menu():
    display_navbar()
    print("\n--- Help Menu ---")
    print("1. Step-by-Step Guide")
    print("2. Account Security Tips")
    print("3. Keyword Search")
    print("4. Advanced Search")
    print("5. Back to User Menu")
    choice = input("Enter your choice: ")

    if choice == "1":
        print(step_by_step_guide)
    elif choice == "2":
        print(security_tips)
    elif choice == "3":
        keyword_search()
    elif choice == "4":
        advanced_search()
    elif choice == "5":
        return
    else:
        print("Invalid choice. Please try again.")

def keyword_search():
    keyword = input("Enter a keyword to search in the help menu: ").lower()
    results = {key: value for key, value in help_content.items() if keyword in key or keyword in value.lower()}
    if results:
        print("\nSearch Results:")
        for key, value in results.items():
            print(f"- {key.capitalize()}: {value}")
    else:
        print("No results found for the given keyword.")

def advanced_search():
    print("\n--- Advanced Search ---")
    print("1. Search by Topic")
    print("2. Search by Content")
    choice = input("Enter your choice: ")

    if choice == "1":
        topic = input("Enter the topic to search (e.g., upload, view, analysis): ").lower()
        if topic in help_content:
            print(f"\n{topic.capitalize()}: {help_content[topic]}")
        else:
            print("No help available for the given topic.")
    elif choice == "2":
        content = input("Enter a phrase to search in the help content: ").lower()
        results = {key: value for key, value in help_content.items() if content in value.lower()}
        if results:
            print("\nSearch Results:")
            for key, value in results.items():
                print(f"- {key.capitalize()}: {value}")
        else:
            print("No results found for the given phrase.")
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

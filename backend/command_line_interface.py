## SCIENTIFIC CALCULATOR COMMAND LINE INTERFACE [CLI] ##
## Module 3: Integrates Core Calculator + History Manager

from calculator_core import evaluate_expression  # Module 1
import history_manager as hm                     # Module 2
import math

def show_history():
    """
    Display the full calculation history from the database.
    Retrieves all records from the calculator's history table and prints them in a formatted manner including the ID, expression, result, and timestamp.
    If no history exists, an appropriate message is displayed.
    """
    history = hm.get_all_history()
    if not history:
        print("📜 No history found.")
    else:
        print("\n🕑 Calculation History:")
        for row in history:
            print(f"{row[0]}. {row[1]} = {row[2]} at {row[3]}")

def search_history():
    """
    Search and display calculator history for expressions containing a user-specified keyword.
    Prompts the user to enter a search string. Retrieves all matching records from the history table and prints them in a formatted manner including the ID, expression, result, and timestamp.
    If no matches are found, an appropriate message is displayed.
    """
    query = input("Enter keyword or expression to search: ")
    results = hm.search_history(query)
    if not results:
        print("No matching history found.")
    else:
        print("\n🔎 Search Results:")
        for row in results:
            print(f"{row[0]}. {row[1]} = {row[2]} at {row[3]}")

def main():
    """
    Entry point for the Scientific Calculator program.
    Provides a user-friendly menu to:
        1. Perform a calculation
        2. View full history
        3. Search history
        4. Clear all history
        5. Exit the program
    Integrates the backend evaluation (Module 1) and database history management (Module 2).
    Flow:
        - Initializes the database and ensures the history table exists.
        - Continuously prompts the user for input until 'Exit' is selected.
        - Handles exceptions during calculation and invalid menu selections.
        - Persists each valid calculation in the database.
    """
    # Ensure DB and table exist
    hm.init_db()

    while True:
        print("\n~ SCIENTIFIC CALCULATOR ~")
        print("1. Perform Calculation")
        print("2. View Full History")
        print("3. Search History")
        print("4. Clear History")
        print("5. Exit")

        choice = input("Enter your choice [1-5]: ").strip()

        if choice == "1":
            expr = input("Enter expression (supports +, -, *, /, sin(), cos(), log(), sqrt(), ^, !): ").strip()
            try:
                result = evaluate_expression(expr)
                print(f"Result: {result}")

                # Save to DB
                hm.add_history(expr, result)

            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            show_history()

        elif choice == "3":
            search_history()

        elif choice == "4":
            confirm = input("Are you sure? This will delete all history (y/n): ").lower()
            if confirm == "y":
                hm.clear_history()
                print("History cleared!")
            else:
                print("Operation canceled.")

        elif choice == "5":
            print("Thanks for using the Scientific Calculator. Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Please select from 1-5.")

if __name__ == "__main__":
    main()

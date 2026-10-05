import os
import uuid
from datetime import datetime

MAX_FILE_SIZE = 5 * 1024 * 1024

def greet_user(name):
    if name == "glynis":
        return "Welcome back, Glynis!"
    elif name == "admin":
        return "Welcome, administrator!"
    else:
        return "Welcome, new user!"

def show_menu():
    print("\n What would you like to do?")
    print("1. Upload a document")
    print("2. Ask an AI question")
    print("3. View processing history")
    print("4. Clear processing history")
    print("5. Exit")

def extract_text(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()

        return text

    except Exception as error:
        print( f"Error reading file: {error}")
        return None

def display_document_summary(result):
    print("\n--- Document Summary ---")
    print(f"Document ID: {result['id']}")
    print(f"Filename: {result['filename']}")
    print(f"File type: {result['file_type']}")
    print(f"Word count: {result['word_count']}")
    print(f"Character count: {result['character_count']}")
    print(f"File size: {format_file_size(result['file_size'])}")
    print(f"Status: {result['status']}")
    print(f"Processed at: {result['processed_at']}")
    print(f"Preview: {result['preview']}")

def view_history(processed_documents):
    if len(processed_documents) == 0:
        return "No documents have been processed yet."

    print("\n--- Processing History ---")

    for document in processed_documents:
        print(f"Document ID: {document['id']}")
        print(f"Filename: {document['filename']}")
        print(f"File type : {document['file_type']}")
        print(f"Word count: {document['word_count']}")
        print(f"Status: {document['status']}")
        print(f"Processed at: {document['processed_at']}")
        print("-------------------------")

    return "End of processing history."

def clear_history(processed_documents):
    confirmation = input("Are you sure you want to clear history? (yes/no): ").strip().lower()

    if confirmation == "yes":
        processed_documents.clear()
        return "Processing history cleared."

    return "History was not cleared."

def clean_text(text):
    text = text.strip()
    text = " ".join(text.split())

    return text

def format_file_size(size):
    if size < 1024:
        return f"{size} bytes"

    if size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size / (1024 * 1024):.2f} MB"

def create_preview(text):
    if len(text) <= 100:
        return text

    return text[:100] + "..."

def process_document(filename):
    status = "processing"

    print(f"Starting processing for '{filename}'...")
    print(f"Status: {status}")

    extracted_text = extract_text(filename)

    if extracted_text is None:
        return {
            "id": str(uuid.uuid4()),
            "filename": filename,
            "text": "",
            "word_count": 0,
            "character_count": 0,
            "file_type": os.path.splitext(filename)[1].lower(),
            "preview": "",
            "status": "failed",
            "error": "Unable to read document.",
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_size": os.path.getsize(filename)
        }

    if extracted_text.strip() == "":
        return {
            "id": str(uuid.uuid4()),
            "filename": filename,
            "text": "",
            "word_count": 0,
            "character_count": 0,
            "file_type": os.path.splitext(filename)[1].lower(),
            "preview": "",
            "status": "failed",
            "error": "Document is empty.",
            "processed at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_size": os.path.getsize(filename)
        }

    extracted_text = clean_text(extracted_text)

    print("Extracted text:")
    print(extracted_text)

    word_count = len(extracted_text.split())
    print(f"Word count: {word_count}")

    character_count = len(extracted_text)
    preview = create_preview(extracted_text)

    file_size = os.path.getsize(filename)
    file_type = os.path.splitext(filename)[1].lower()

    print("Analyzing extracted text...")

    return {
        "id": str(uuid.uuid4()),
        "filename": filename,
        "text": extracted_text,
        "word_count" : word_count,
        "character_count" : character_count,
        "file_type": file_type,
        "preview": preview,
        "status": "completed",
        "error": None,
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_size": file_size
    }

def get_processing_message(result):
    if result["status"] == "completed":
        return "Document processing finished successfully."

    if result["status"] == "failed":
        return f"Document processing failed: {result['error']}"

    return "Document processing is still in progress."

def upload_document(processed_documents):
    filename = input("Enter the document filename: ").strip()

    if filename == "":
        return "No filename entered."

    if not filename.lower().endswith((".pdf", ".docx", ".txt")):
        return "Unsupported file type. Please upload a PDF, DOCX, or TXT file."

    if not os.path.exists(filename):
        return f"File '{filename}' does not exist."

    if not os.path.isfile(filename):
        return f" '{filename}' is not a valid file."

    file_size = os.path.getsize(filename)

    if file_size > MAX_FILE_SIZE:
        return "File is too large. Maximum allowed size is 5 MB."
    
    for document in processed_documents:
        if document["filename"].lower() == filename.lower():
            return f"Document '{filename}' has already been processed."

    result = process_document(filename)
    processed_documents.append(result)

    display_document_summary(result)

    return get_processing_message(result)

def generate_answer(question):
    question = question.lower()

    if "meeting" in question:
        return "I can help you manage your meetings."

    elif "document" in question:
        return "I can help you process documents."

    elif "hello" in question or "hi" in question:
        return "Hello! How can I help you?"

    else:
        return "I am still learning. Please ask me about meetings or documents."

def ask_ai_question():
    question = input("What would you like to ask the AI?").strip()

    if question == "":
        return "You did not enter a question."

    answer = generate_answer(question)
    return answer

def main():
    processed_documents = []

    name = input("What is your name? ").strip().lower()
    print(greet_user(name))

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            message = upload_document(processed_documents)
            print(message)
        elif choice == "2":
            message = ask_ai_question()
            print(message)
        elif choice == "3":
            message = view_history(processed_documents)
            print(message)

        elif choice == "4":
            message = clear_history(processed_documents)
            print(message)

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
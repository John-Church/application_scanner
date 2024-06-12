# Example PDF Scanner with GPT4o

This Streamlit application allows users to upload PDF files, which are then split into pages, converted to base64 images, and analyzed using GPT-4o to generate markdown text. The application also provides insights into the text based on user-defined analysis goals.

### To run

1. Create a new virtual environment:
   ```sh
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Copy the example environment file and fill in your OpenAI key:
   ```sh
   cp .env.example .env
   ```
   Edit `.env` to add your OpenAI key.
5. Run the Streamlit app:
   ```sh
   streamlit run main.py
   ```

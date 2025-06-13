# HR Smart Recruiter RAG System

A modular, well-structured Retrieval-Augmented Generation (RAG) system for analyzing candidate CVs using LLM-powered retrieval and querying.

--------------------------
 Try it out live here : https://hr-smart-recruiter-rag.streamlit.app/
--------------------------


## 🏗️ Architecture

The application has been refactored into a clean, modular architecture:

```
hr_smart_recruiter/
│
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (create this)
├── static/
│   └── styles.css             # CSS styles
│
├── src/                       # Core application modules
│   ├── __init__.py
│   ├── config.py              # Configuration and constants
│   ├── document_processor.py  # Document extraction and processing
│   ├── embeddings.py          # Custom embedding classes
│   ├── vectorstore.py         # Vector database operations
│   ├── rag_engine.py          # RAG query processing
│   └── ui_components.py       # Streamlit UI components
│
└── utils/                     # Utility functions
    ├── __init__.py
    └── helpers.py             # General helper functions
```

## 🚀 Features

- **Modular Design**: Clean separation of concerns with dedicated modules
- **Multi-format Support**: Process PDF and DOCX files
- **Intelligent Querying**: 
  - General queries across all candidates
  - Applicant-specific queries
  - Count queries for statistics
- **Advanced RAG**: Uses E5 embeddings and FAISS for similarity search
- **Interactive UI**: Streamlit-based web interface
- **Session Management**: Persistent state management

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/mohamedelsharkawy-coder/HR-Smart-Recruiter-RAG.git
cd hr_smart_recruiter
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

## 🎯 Usage

1. **Start the application:**
```bash
streamlit run app.py
```

2. **Upload CVs:**
   - Use the sidebar to upload PDF or DOCX files
   - Multiple files can be uploaded at once

3. **Index Documents:**
   - Click "Load & Index CVs" to process and index the documents
   - The system will create embeddings and build a vector database

4. **Ask Questions:**
   - Enter queries about the candidates
   - Examples:
     - "Who has experience in machine learning?"
     - "What are John Smith's technical skills?"
     - "How many candidates have Python experience?"
     - "Compare the experience levels of all candidates"

## 🏛️ Module Overview

### Core Modules (`src/`)

#### `config.py`
- Centralized configuration management
- Environment variables and constants
- Model and processing parameters

#### `document_processor.py`
- File upload handling
- Text extraction from PDF and DOCX files
- Document validation and error handling

#### `embeddings.py`
- Custom E5 embedding implementation
- Embedding factory for different models
- Optimized for retrieval tasks

#### `vectorstore.py`
- FAISS vector database management
- Document chunking and indexing
- Similarity search and retrieval

#### `rag_engine.py`
- Main RAG processing logic
- Query analysis and routing
- LLM integration with Google Gemini

#### `ui_components.py`
- Reusable Streamlit components
- Session state management
- UI styling and layout

### Utilities (`utils/`)

#### `helpers.py`
- Text processing utilities
- Query classification functions
- General helper functions

## 🔧 Configuration

Key configuration options in `src/config.py`:

```python
# Model Settings
EMBEDDING_MODEL_NAME = "intfloat/e5-large-v2"
LLM_MODEL_NAME = "gemini-2.0-flash-exp"
LLM_TEMPERATURE = 0.5

# Processing Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 50
RETRIEVAL_K = 20
```

## 🎨 Customization

### Adding New Document Types
1. Extend `DocumentProcessor` class in `document_processor.py`
2. Add new extraction methods
3. Update `SUPPORTED_FILE_TYPES` in `config.py`

### Changing Embedding Models
1. Modify `EMBEDDING_MODEL_NAME` in `config.py`
2. Or create new embedding classes in `embeddings.py`

### UI Customization
1. Modify CSS in `static/styles.css`
2. Update UI components in `ui_components.py`

## 🔍 Query Types

The system supports three types of queries:

1. **General Queries**: Search across all candidates
   - "Who has Python experience?"
   - "Find candidates with 5+ years experience"

2. **Applicant-Specific**: Target specific candidates
   - "What are John's skills?"
   - "Tell me about Mary's education"

3. **Count Queries**: Statistical information
   - "How many candidates have ML experience?"
   - "Total number of applicants"

## ⚙️ Technical Details

### RAG Pipeline
1. **Document Processing**: Extract text from uploaded files
2. **Chunking**: Split documents into manageable chunks
3. **Embedding**: Generate vector representations using E5 model
4. **Indexing**: Store vectors in FAISS database
5. **Retrieval**: Find relevant chunks based on query similarity
6. **Generation**: Use Google Gemini to generate contextual answers

### Performance Considerations
- Uses CPU-based FAISS for broader compatibility
- Optimized chunk sizes for memory efficiency
- Lazy loading of models
- Session state management for persistence

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the modular structure
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `GOOGLE_API_KEY` is set in `.env` file
2. **Import Errors**: Check virtual environment activation and dependencies
3. **Memory Issues**: Reduce `CHUNK_SIZE` or `RETRIEVAL_K` in config
4. **File Processing**: Ensure files are valid PDF/DOCX format

### Debug Mode

Set debug logging by adding to your `.env`:
```env
STREAMLIT_LOGGER_LEVEL=debug
```

## 📧 Support

For issues and questions, please create an issue in the repository or contact the development team.

## Development team `GitHub Accounts`

- Sara Gamil: [@saragamilmohamed ](https://github.com/saragamilmohamed)
- Ali Salama: [@3lis0](https://github.com/3lis0)
- Mohamed Elsharkawy: [@mohamedelsharkawy-coder](https://github.com/mohamedelsharkawy-coder)
- Adham Assy: [@adham3assy](https://github.com/adham3assy)


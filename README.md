# VietNet WordNet Browser 🌐

A comprehensive **Streamlit-based web application** for browsing and exploring Vietnamese WordNet (VietNet) linguistic data, with specialized support for food-related vocabulary and semantic relationships.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 📖 Overview

This project provides an interactive web interface for exploring Vietnamese WordNet (VietNet) data. It enables users to:

- **Search** for Vietnamese words and their semantic relationships
- **Visualize** word hierarchies and connections
- **Browse** linguistic data including synsets, lemmas, and definitions
- **Explore** food-related terminology in depth
- **Analyze** word relationships (hypernyms, hyponyms, synonyms, etc.)

The application is built with **Streamlit** for rapid web development and can be deployed locally or via **Docker** for containerized environments.

---

## ✨ Features

- 🔍 **Advanced Search**: Search for words, phrases, and semantic relationships
- 🌳 **Hierarchical Visualization**: View word relationships in tree structures
- 📊 **Synset Exploration**: Browse synsets, definitions, and usage examples
- 🍲 **Food Vocabulary Database**: Comprehensive Vietnamese food terminology
- 🔗 **Relationship Navigation**: Explore hypernyms, hyponyms, and other semantic relations
- 📱 **Responsive Web Interface**: Works on desktop and mobile devices
- 🐳 **Docker Support**: Easy deployment with containerization

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.10 |
| **WordNet Library** | `wn` (Python WordNet package) |
| **NLP/Linguistics** | NLTK |
| **Containerization** | Docker |
| **Data Format** | XML (VietNet linguistic data) |

---

## ✅ Prerequisites

### For Local Installation:
- Python 3.10 or higher
- pip (Python package manager)
- Git (recommended)

### For Docker:
- Docker Engine installed and running
- Docker Compose (optional, for multi-container setups)

---

## 📦 Installation

### Local Installation

1. **Clone or download the project**
   ```bash
   cd path/to/WordNet/Hải/vietnet-food-docker
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - `streamlit` - Web application framework
   - `nltk` - Natural Language Toolkit
   - `wn` - Python WordNet interface

---

### Docker Installation

1. **Navigate to the project directory**
   ```bash
   cd path/to/WordNet/Hải/vietnet-food-docker
   ```

2. **Build the Docker image**
   ```bash
   docker build -t vietnet-browser:latest .
   ```

3. **Run the container**
   ```bash
   docker run -p 86:86 vietnet-browser:latest
   ```

   Or with port mapping to a different local port:
   ```bash
   docker run -p 8501:86 vietnet-browser:latest
   ```

---

## 🚀 Running the Application

### Local Execution

```bash
streamlit run wordnet_browser.py --server.port=8501 --server.address=localhost
```

Then open your browser and navigate to:
```
http://localhost:8501
```

### Docker Execution

The application runs on **port 86** inside the container (mapped to your host machine):

```bash
docker run -p 86:86 vietnet-browser:latest
```

Access the application at:
```
http://localhost:86
```

### Streamlit Run Options

```bash
# Run with specific settings
streamlit run wordnet_browser.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --logger.level=info

# Run in headless mode (no browser popup)
streamlit run wordnet_browser.py --logger.level=error
```

---

## 📁 Project Structure

```
vietnet-food-docker/
├── Dockerfile                 # Docker container configuration
├── requirements.txt          # Python dependencies
├── wordnet_browser.py        # Main Streamlit application
├── local.txt                 # Local configuration file
├── vietnet_food (thủ công).xml  # Vietnamese food WordNet data
└── components/               # Reusable components
    ├── class_Node.py         # Node data structure
    ├── class_NodeFamily.py   # Node family/hierarchy management
    ├── utils_wn.py          # WordNet utility functions
    ├── utils_search.py      # Search functionality
    └── utils_display.py     # UI display components
```

### Key Components

| File | Purpose |
|------|---------|
| `wordnet_browser.py` | Main Streamlit application entry point |
| `utils_wn.py` | WordNet operations and data retrieval |
| `utils_search.py` | Search algorithm and query processing |
| `utils_display.py` | UI rendering and visualization |
| `class_Node.py` | Data structure for conceptual nodes |
| `class_NodeFamily.py` | Hierarchy and relationship management |

---

## 📖 Usage Guide

### Starting a Search

1. Launch the application
2. Enter a Vietnamese word in the search box
3. Select search type (exact match, partial, or semantic)
4. View results with definitions and relationships
5. Click on related words to explore further

### Navigating Relationships

- **Hypernyms**: More general semantic categories
- **Hyponyms**: More specific subcategories
- **Synonyms**: Words with similar meanings
- **Related**: Other conceptually related terms

### Viewing Details

- Word definitions and usage notes
- Synset identifiers and mappings
- Example sentences (when available)
- Multiple language representations

---

## ⚙️ Configuration

### Environment Variables

Create or edit `local.txt` to customize settings:

```ini
# Port configuration
PORT=86

# Address binding
ADDRESS=0.0.0.0

# Logging level
LOG_LEVEL=info
```

### Streamlit Configuration

Edit or create `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true

[logger]
level = "info"
```

---

## 🔧 Troubleshooting

### Issue: "Module not found" errors

**Solution**: Ensure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: WordNet data not loading

**Solution**: 
- Verify the XML file path in `wordnet_browser.py`
- Ensure `vietnet_food (thủ công).xml` is in the project root
- Check file permissions

### Issue: Port already in use

**Solution**: Change the port number:
```bash
streamlit run wordnet_browser.py --server.port=9000
```

Or for Docker:
```bash
docker run -p 9000:86 vietnet-browser:latest
```

### Issue: Connection refused in Docker

**Solution**: Ensure port mapping is correct and the container is running:
```bash
docker ps  # Check running containers
docker logs <container_id>  # View container logs
```

---

## 🐛 Debugging

### Check Python Version
```bash
python --version  # Should be 3.10+
```

### Verify Dependencies
```bash
pip list
```

### View Application Logs
```bash
streamlit run wordnet_browser.py --logger.level=debug
```

### Docker Container Debugging
```bash
# View container logs
docker logs <container_name>

# Access container shell
docker exec -it <container_name> /bin/bash
```

---

## 📚 Data Files

- **`vietnet_food (thủ công).xml`**: Main Vietnamese food WordNet database
- **Format**: XML-based semantic network
- **Language**: Vietnamese
- **Domain**: Food-related vocabulary and concepts

---

## 🔄 Development & Contributions

### Project Versions

The workspace includes multiple versions:
- **v1.0** - Initial release
- **v1.1** - Bug fixes and improvements
- **v2.0** - Enhanced UI and features
- **v3.0** - Current stable version with Docker support

### Adding New Features

1. Update components in the `components/` folder
2. Modify `wordnet_browser.py` for UI changes
3. Test locally before containerizing
4. Update `requirements.txt` if new dependencies are added

### Testing

```bash
# Run Streamlit in watch mode (auto-reloads on changes)
streamlit run wordnet_browser.py
```

---

## 📝 License & Attribution

This project builds upon the WordNet project and uses Vietnamese WordNet (VietNet) data. Please ensure compliance with respective data usage licenses.

---

## 📧 Support & Contact

For issues, questions, or contributions:
- Review the troubleshooting section above
- Check application logs for error details
- Ensure all prerequisites are properly installed

---

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced relationship visualization
- [ ] Export functionality (CSV, JSON)
- [ ] Custom WordNet import
- [ ] User accounts and saved searches
- [ ] API endpoint for programmatic access
- [ ] Mobile-optimized interface

---

**Last Updated**: March 2026  
**Version**: 3.0 with Docker Support 

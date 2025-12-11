# Butterfly & Bird Identifier

A deep learning-based web application for identifying butterflies and birds using AI-powered image classification.

## Project Overview

This is a web application system developed using deep learning technology to identify butterflies and birds from uploaded images. The system uses transfer learning technology, building a classification model based on MobileNetV2, capable of identifying 300+ species (200 bird species + 100+ butterfly/moth species), and provides a user-friendly web interface for image upload and identification.

## ✨ Key Features

### 🔍 Core Identification Features
- **Image Upload & Identification**: Support drag-and-drop or file selection (PNG, JPG, JPEG, GIF, WEBP)
- **Batch Identification**: Upload multiple images at once for batch processing
- **Smart Recognition**: Deep learning-based image classification with Top-3 predictions and confidence scores
- **Low Confidence Warning**: Automatically detects and warns when uploaded images are not butterflies or birds, or when image quality is insufficient
- **Cartoon Detection**: Automatically detects and filters out cartoon/illustration images

### 🎵 Bird Sound Identification
- **Audio Upload**: Support WAV, MP3, M4A, FLAC, OGG, AAC formats
- **Real-time Processing**: Fast audio-to-spectrogram conversion
- **16 Bird Species**: Identify birds by their sounds
- **Top-3 Predictions**: Display multiple possible matches with confidence scores

### 💬 Text-Based Identification (Describe to Identify)
- **Natural Language Input**: Describe species characteristics in natural language
- **Conversation History**: Maintain conversation context for better matching
- **Category Filtering**: Filter by birds, butterflies, or all species
- **Swipe to Delete**: Swipe left on conversation items to delete
- **Quick Questions**: Pre-defined quick question buttons
- **Progressive Refinement**: AI helps narrow down results through conversation

### 📚 Species Field Guide
- **Birds Catalog**: Browse 200 bird species with detailed information
- **Butterflies Catalog**: Browse 100+ butterfly/moth species
- **Search & Filter**: Search by name, filter by category
- **Species Details**: View detailed information including habitat, behavior, size, distribution
- **Collection Tracking**: Track which species you've identified

### 💬 AI Chat Assistant
- **Intelligent Q&A**: Answer questions about species identification, observation tips, etc.
- **Knowledge Base**: Contains information about habitats, observation times, photography tips
- **Trainable**: Support for expanding and training the AI assistant's knowledge base

### 📈 Statistical Analysis
- **Identification History Statistics**: Total identifications, unique species count, average confidence
- **Category Distribution**: Statistics for birds, butterflies/moths, and others
- **Confidence Distribution**: Charts showing high/medium/low confidence distribution
- **Top Species**: Leaderboard of most frequently identified species
- **Time Distribution**: Trends in identification activity over time
- **PDF Export**: Export statistics report as PDF

### ❤️ Favorites Feature
- **Save Species**: One-click save for interesting identification results
- **Favorites Management**: View and manage all saved species
- **Data Persistence**: Use localStorage to save favorite data
- **Export Options**: Export favorites as PDF or JSON

### 📜 History Records
- **Identification History**: Automatically save recent identification records
- **Quick View**: Quickly browse historical identification results
- **Tab Switching**: Easy switching between history and favorites
- **Export Options**: Export history as PDF or JSON

## Tech Stack

### Model Training
- **TensorFlow/Keras**: Deep learning framework
- **MobileNetV2**: Pre-trained model (transfer learning)
- **Python 3.8+**: Programming language
- **OpenCV**: Image processing and quality analysis

### Web Application
- **Frontend**: React 18.2.0
  - Axios: HTTP client
  - jsPDF: PDF generation for exports
  - Responsive design, mobile-friendly
  - Touch gestures support (swipe to delete)
- **Backend**: Flask 3.0.0
  - Flask-CORS: Cross-origin support
  - TensorFlow: Model inference (image + audio)
  - PIL/OpenCV: Image processing
  - librosa: Audio processing for bird sound identification
  - scipy: Scientific computing
  - pydub: Audio format conversion

## Project Structure

```
butterfly-bird-identifier/
├── data/
│   ├── raw/              # Raw dataset
│   ├── processed/        # Processed data (train/val/test)
│   └── dataset_info.txt  # Dataset information
├── models/
│   ├── training/         # Training scripts
│   │   ├── train_model.py      # Model training
│   │   ├── prepare_data.py     # Data preparation
│   │   ├── test_model.py       # Model testing
│   │   └── check_training.py   # Training progress check
│   └── trained/          # Trained models
│       ├── model.h5           # Trained image classification model (using Git LFS)
│       ├── class_names.json   # Class names list
│       └── bird_sound/        # Bird sound classification model
│           ├── bird_sound_model.h5  # Trained bird sound model
│           └── class_names.json     # Bird sound class names
├── web_app/
│   ├── frontend/         # React frontend application
│   │   ├── src/
│   │   │   ├── App.js         # Main application component
│   │   │   ├── App.css        # Stylesheet
│   │   │   └── index.js       # Entry file
│   │   ├── public/
│   │   │   └── index.html     # HTML template
│   │   └── package.json       # Frontend dependencies
│   ├── backend/          # Flask backend API
│   │   ├── app.py             # Flask application main file
│   │   ├── requirements.txt   # Python dependencies
│   │   ├── knowledge_base.json # AI assistant knowledge base
│   │   └── train_assistant.py  # AI assistant training script
│   └── preview.html      # Preview page
├── notebooks/            # Jupyter notebooks (data exploration)
├── report/              # Project reports
├── .gitattributes        # Git LFS configuration
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

2. **Node.js 16+**
   - Download: https://nodejs.org/
   - Recommended: LTS version

3. **Git LFS** (for downloading large files)
   ```bash
   git lfs install
   ```

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/Charlieppy2/butterfly-bird-identifier.git
cd butterfly-bird-identifier
```

#### 2. Install Backend Dependencies

**Windows (PowerShell):**
```powershell
cd web_app/backend
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
cd web_app/backend
pip install -r requirements.txt
```

**Note:** First-time installation may take 2-5 minutes, especially for TensorFlow.

#### 3. Install Frontend Dependencies

**Windows (PowerShell):**
```powershell
cd web_app/frontend
npm install
```

**Linux/Mac:**
```bash
cd web_app/frontend
npm install
```

**Note:** First-time installation may take 2-5 minutes and install ~1344 packages.

### Launch Application

#### Method 1: Manual Launch (Recommended)

**Start Backend Service:**

**Windows (PowerShell):**
```powershell
cd web_app/backend
python app.py
```

**Linux/Mac:**
```bash
cd web_app/backend
python app.py
```

Backend service will start at `http://localhost:5001`

You should see:
```
Loading model...
Model loaded successfully from ...
Starting Flask server...
Running on http://0.0.0.0:5001
```

**Note**: The backend uses port 5001 by default to avoid conflicts with macOS AirPlay Receiver on port 5000.

**Start Frontend Application:**

Open a **new terminal window**:

**Windows (PowerShell):**
```powershell
cd web_app/frontend
npm start
```

**Linux/Mac:**
```bash
cd web_app/frontend
npm start
```

Frontend application will start at `http://localhost:3000`, browser will open automatically after compilation (10-30 seconds).

#### Method 2: Using Batch Files (Windows)

**Backend:**
Double-click `web_app\backend\start_backend.bat` or run:
```powershell
cd web_app/backend
.\start_backend.bat
```

**Frontend:**
Double-click `web_app\frontend\start_frontend.bat` or run:
```powershell
cd web_app/frontend
.\start_frontend.bat
```

### Verify Services

**Check Backend:**
Open browser and visit: `http://localhost:5001`

You should see:
```json
{
  "status": "success",
  "message": "HK Urban Ecological Identification API is running",
  "model_loaded": true
}
```

**Check Frontend:**
Open browser and visit: `http://localhost:3000`

You should see the main application interface with upload area and buttons.

## 📖 User Guide

### Identify Species by Image

1. **Upload Image**:
   - Click "🔍 Identify" button
   - Click "Choose File" button to select image
   - Or drag and drop image to upload area

2. **View Results**:
   - System will display identification results and confidence
   - Show Top-3 predictions
   - If the image is not a butterfly or bird, or confidence is low, a warning message will be displayed with suggestions
   - Cartoon/illustration images are automatically detected and filtered

### Identify Species by Sound

1. **Upload Audio**:
   - Click "🎵 Bird Sound ID" button
   - Click to select audio file (WAV, MP3, M4A, FLAC, OGG, AAC)
   - Audio should be 3-10 seconds for best results

2. **View Results**:
   - System will display bird species identification
   - Show Top-3 predictions with confidence scores

### Identify Species by Description

1. **Enter Description**:
   - Click "💬 Describe to Identify" button
   - Type a description of the species (e.g., "small bird with red head and black wings")
   - Select category filter (All, Birds, or Butterflies)

2. **Conversation**:
   - AI will show matching species based on your description
   - Continue the conversation to refine results
   - Use quick question buttons for common queries
   - Swipe left on conversation items to delete

3. **View Matches**:
   - Click on species cards to view detailed information
   - View habitat, behavior, size, and distribution details

### Browse Species Catalog

1. **View Birds**:
   - Click "🐦 Birds (200)" button
   - Browse all 200 bird species
   - Search by name or filter by characteristics

2. **View Butterflies**:
   - Click "🦋 Butterflies (100)" button
   - Browse all 100+ butterfly/moth species
   - Search by name or filter by characteristics

3. **Field Guide**:
   - Click "📚 Field Guide" button
   - View your collection of identified species
   - Track your progress

### Use AI Assistant

1. Click the chat icon in the bottom right corner to open AI assistant
2. You can ask about:
   - Identification tips
   - Best observation times
   - Photography suggestions
   - Species information

### View Statistics

1. Click "📊 View Statistics" in the history section
2. View:
   - Total identifications
   - Category distribution (birds/butterflies/others)
   - Confidence distribution
   - Top identified species
   - Time distribution trends
3. Export statistics as PDF

### Favorites Feature

1. **Save Species**:
   - After identification, click the ❤️ button next to the result title

2. **View Favorites**:
   - Click "❤️ Favorites" tab
   - View all saved species

3. **Remove Favorites**:
   - Click "❌ Remove" button in favorites list
   - Or click ❤️ button again to unfavorite

4. **Export Favorites**:
   - Export favorites as PDF or JSON

## 🎓 Model Training

### Data Preparation

Organize raw images by category in `data/raw/` directory:

```
data/raw/
├── 001.Black_footed_Albatross/
│   ├── image1.jpg
│   └── ...
├── 002.Laysan_Albatross/
│   └── ...
└── ...
```

Run data preparation script:

```bash
cd models/training
python prepare_data.py
```

### Train Model

```bash
cd models/training
python train_model.py
```

Training parameters can be adjusted in `train_model.py`:
- `IMAGE_SIZE`: Image size (224, 224)
- `BATCH_SIZE`: Batch size (32)
- `EPOCHS`: Number of epochs (100)
- `LEARNING_RATE`: Learning rate (0.0001)

After training, model will be saved in `models/trained/model.h5`

### Check Training Progress

```bash
cd models/training
python check_training.py
```

### Test Model

```bash
cd models/training
python test_model.py
```

## 🤖 Train AI Assistant

For detailed guide, see: [如何訓練AI助手.md](如何訓練AI助手.md)

Quick start:

```bash
cd web_app/backend
python train_assistant.py
```

## 📊 Dataset Information

- **Total Classes**: 301 species (200 bird species + 101 butterfly/moth species)
- **Data Augmentation**: Rotation, flipping, scaling, brightness adjustment
- **Image Size**: 224x224
- **Train/Val/Test**: Automatically split

## 🔧 API Endpoints

### Backend API

- `GET /` - Health check
- `GET /api/health` - Model status (includes both image and bird sound model status)
- `GET /api/classes` - Get all class names
- `POST /api/predict` - Image identification
- `POST /api/predict-sound` - Bird sound identification
- `POST /api/description-chat` - Text-based species identification
- `POST /api/analyze-quality` - Image quality analysis
- `POST /api/statistics` - Get statistics
- `POST /api/chat` - AI chat assistant
- `GET /api/birds` - Get all bird species data
- `GET /api/butterflies` - Get all butterfly species data

## 🛠️ Development Environment

- **Python**: 3.8+ (tested with 3.13.9)
- **Node.js**: 16+ (tested with 24.11.1)
- **TensorFlow**: 2.16.0+ (tested with 2.20.0)
- **React**: 18.2.0
- **Flask**: 3.0.0
- **Flask-CORS**: 4.0.0
- **OpenCV**: 4.8.0+ (tested with 4.12.0.88)
- **Pillow**: 10.1.0+
- **NumPy**: 1.24.3+

## ⚠️ Notes

1. **Git LFS**: Model files use Git LFS storage, need to run `git lfs install` after cloning
2. **First Run**: First run needs to load model, may take some time (10-30 seconds)
3. **GPU Acceleration**: Training model recommended to use GPU acceleration (Google Colab recommended)
4. **Disk Space**: Ensure sufficient disk space for dataset and model storage (model ~19MB)
5. **Browser Compatibility**: Recommended to use latest versions of Chrome, Firefox, or Edge
6. **Port Conflicts**: If ports 5001 (backend) or 3000 (frontend) are already in use, stop the conflicting services or change ports in configuration
7. **Windows PowerShell**: Use `;` instead of `&&` for chaining commands in PowerShell
8. **Keep Terminals Open**: Both backend and frontend services must remain running - keep terminal windows open

## ❓ Troubleshooting

### Backend Won't Start

**Problem**: "Model not found" or "Model not loaded"

**Solution**:
1. Verify model file exists: `models/trained/model.h5`
2. Verify class names file exists: `models/trained/class_names.json`
3. If files don't exist, you need to train the model first (see Model Training section)

### Frontend Can't Connect to Backend

**Problem**: "Cannot connect to website" or "Connection refused"

**Solution**:
1. Verify backend service is running (check http://localhost:5001)
2. Ensure both services are running simultaneously
3. Try clearing browser cache and refreshing
4. Check firewall settings

### Frontend Compilation Errors

**Problem**: Errors when running `npm start`

**Solution**:
1. Delete `node_modules` folder
2. Delete `package-lock.json` file
3. Run `npm install` again
4. Run `npm start` again

### Port Already in Use

**Problem**: Port 5001 (backend) or 3000 (frontend) is already in use

**Solution**:
1. Close other programs using these ports
2. Or modify port in `app.py` (backend) or set `PORT=3001` environment variable (frontend)
3. Note: Backend uses port 5001 by default to avoid conflicts with macOS AirPlay Receiver

### Installation Takes Too Long

**Solution**:
- This is normal for first-time installation
- Backend dependencies (especially TensorFlow) may take 5-10 minutes
- Frontend dependencies may take 2-5 minutes
- Ensure stable internet connection

## 🌐 Deployment

### Production URLs
- **Frontend**: https://butterfly-bird-id.vercel.app
- **Backend API**: https://butterfly-bird-id.koyeb.app

### Deployment Platforms
- **Frontend**: Deployed on Vercel (automatic deployment from GitHub)
- **Backend**: Deployed on Koyeb (using Dockerfile.koyeb)

### Environment Variables
For Vercel frontend deployment, set:
- `REACT_APP_API_URL`: Your backend API URL (e.g., `https://butterfly-bird-id.koyeb.app`)

For Koyeb backend deployment:
- `FLASK_ENV`: `production`
- `PORT`: `8080` (automatically set by Koyeb)

## 📝 Changelog

### v1.3.0 (Latest)
- ✨ Added Bird Sound Identification feature (16 bird species)
- ✨ Added Text-Based Identification (Describe to Identify) with conversation history
- ✨ Added Species Field Guide (Birds & Butterflies catalogs)
- ✨ Added swipe-to-delete for conversation history
- ✨ Improved navigation layout (Birds & Butterflies on first row)
- 🔧 Optimized memory management for Koyeb deployment
- 🔧 Enhanced mobile device timeout handling
- 🔧 Improved health check endpoints for better reliability
- 🐛 Fixed WebSocket errors from React dev server
- 🐛 Fixed mobile connection issues

### v1.2.0
- ✨ Added conversation history for text-based identification
- ✨ Added category filtering for description matching
- ✨ Improved UI/UX for description identification feature

### v1.1.0
- ✨ Added low confidence warning system for non-target images
- ✨ Added cartoon/illustration detection
- ✨ Improved UI to conditionally show results based on confidence
- 🔧 Changed backend default port to 5001 to avoid macOS conflicts
- 🚀 Deployed to production (Vercel + Koyeb)
- 🌐 Updated API URL configuration for production deployment
- 📝 Updated documentation with deployment information

### v1.0.0
- ✨ Added favorites feature
- ✨ Added image quality analysis
- ✨ Added AI chat assistant
- ✨ Added identification history statistics and analysis
- ✨ Added batch identification mode
- 🐛 Fixed category distribution issue (butterflies correctly classified)
- 📦 Using Git LFS for large file management
- 📝 Updated installation and setup documentation

## 📚 References

- [TensorFlow Official Documentation](https://www.tensorflow.org/)
- [Keras Transfer Learning Guide](https://keras.io/guides/transfer_learning/)
- [React Official Documentation](https://react.dev/)
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Git LFS Documentation](https://git-lfs.github.com/)

## 📄 License

This project is for academic and educational purposes only.

## 👥 Contributing

Issues and Pull Requests are welcome!

## 📧 Contact

For questions or suggestions, please contact via GitHub Issues.

---

**Note**: Please ensure all necessary configurations and tests are completed before submission.

## 📄 Other Language Versions

- [繁體中文版 (Traditional Chinese)](README.zh-TW.md)
- [简体中文版 (Simplified Chinese)](README.zh-CN.md)

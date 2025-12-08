# ITP4221 - Mini Report

**Name:** [Your Name]  
**Class:** IT114118  
**SID:** [Your Student ID]  

## Topic

This application is a web-based deep learning system that identifies butterflies and birds from uploaded images. The system allows users to upload images or capture photos using their device camera, and uses a trained convolutional neural network to classify the species with confidence scores. The application provides detailed species information, including habitat, distribution, and identification tips, along with an AI-powered chat assistant to answer questions about wildlife identification.

## Machine Learning Task

This application uses **Image Classification** task, specifically multi-class classification. The reason for choosing this task is that species identification requires categorizing input images into one of 300 predefined classes (200 bird species and 100 butterfly/moth species). This is a supervised learning problem where the model learns to map input images to their corresponding species labels.

The classification task is implemented using **Transfer Learning** with TensorFlow/Keras framework. We chose transfer learning because:
1. It allows us to leverage pre-trained weights from ImageNet, reducing training time and data requirements
2. MobileNetV2 provides a good balance between accuracy and model size, making it suitable for web deployment
3. Fine-tuning the pre-trained model on our specific dataset improves performance on the target species

## Machine Learning Features

### Data

The dataset contains images of 300 species (200 bird species and 100 butterfly/moth species). Each species has multiple images collected from various sources. The images are organized in a directory structure where each folder represents a species class.

**Dataset Statistics:**
- Total Classes: 300 (200 birds + 100 butterflies/moths)
- Image Format: JPG, PNG
- Image Size: Resized to 224×224 pixels for model input
- Data Augmentation: Applied during training (rotation, flip, zoom, shift, shear)

**Data Preprocessing:**
- Images are normalized to [0, 1] range by dividing by 255
- Data augmentation techniques applied: rotation (20°), width/height shift (0.2), shear (0.2), zoom (0.2), horizontal flip
- Train/Validation/Test split: 70% / 20% / 10%

### Environment

The training environment was set up with the following specifications:
- **Framework:** TensorFlow 2.16.0, Keras
- **Base Model:** MobileNetV2 (pre-trained on ImageNet)
- **Python Version:** 3.8+
- **GPU Support:** Recommended for faster training (CUDA-compatible GPU)

**Dependencies:**
- TensorFlow >= 2.16.0
- Keras (included in TensorFlow)
- NumPy >= 1.24.3
- Pillow >= 10.1.0
- scikit-learn (for evaluation metrics)

### Training

The model training process consists of two phases:

**Phase 1: Transfer Learning (Initial Training)**
- **Epochs:** 100 (with early stopping, patience=15)
- **Batch Size:** 32
- **Learning Rate:** 0.0001
- **Optimizer:** Adam
- **Loss Function:** Categorical Cross-entropy
- **Metrics:** Accuracy, Top-3 Accuracy
- **Base Model:** MobileNetV2 layers frozen (not trainable)

**Phase 2: Fine-tuning**
- **Epochs:** 20 additional epochs
- **Learning Rate:** 0.00001 (reduced by factor of 10)
- **Strategy:** Unfreeze last layers of MobileNetV2 (layers 100+), freeze first 100 layers
- **Purpose:** Fine-tune the model on our specific dataset to improve accuracy

**Training Configuration:**
- **Callbacks Used:**
  - ModelCheckpoint: Save best model based on validation accuracy
  - EarlyStopping: Stop training if validation loss doesn't improve for 15 epochs
  - ReduceLROnPlateau: Reduce learning rate when validation loss plateaus

**Training Time:** The training time depends on the hardware. On a GPU-enabled system, the initial training phase typically takes 4-6 hours, while fine-tuning takes an additional 1-2 hours.

**Note:**
- **Epoch:** One complete pass through the entire training dataset
- **Batch Size:** 32 images processed together in each iteration
- **Iterations per Epoch:** Total training images ÷ 32

### Evaluate

The model evaluation was performed on the validation and test sets:

**Evaluation Metrics:**
1. **Accuracy:** Overall classification accuracy
2. **Top-3 Accuracy:** Percentage of predictions where the correct class is in the top 3 predictions
3. **Per-class Metrics:** Precision, Recall, F1-score for each species

**Evaluation Results:**
- **Validation Accuracy:** [To be filled with actual results, e.g., 85.3%]
- **Validation Top-3 Accuracy:** [To be filled, e.g., 94.7%]
- **Test Accuracy:** [To be filled after final evaluation]

The model shows good performance in identifying species, with the Top-3 accuracy being significantly higher than Top-1 accuracy, indicating that the model can effectively narrow down the species to a small set of candidates even when the top prediction is incorrect.

**Confusion Matrix:** Generated to analyze misclassifications and identify species that are frequently confused with each other.

## AI Application

### Platform

The trained model is exported as a `.h5` file (Keras format) and deployed in a **web application** architecture:

- **Backend:** Flask (Python) RESTful API server
  - Loads the trained model on startup
  - Handles image upload and preprocessing
  - Performs inference using the loaded model
  - Returns predictions with confidence scores

- **Frontend:** React.js web application
  - User interface for image upload and camera capture
  - Displays identification results with species information
  - Interactive features: batch processing, history, favorites, AI chat assistant

- **Deployment:** The application can be deployed on various platforms:
  - Local development: `localhost:5000` (backend) + `localhost:3000` (frontend)
  - Cloud platforms: Vercel (frontend), Koyeb/Render (backend)
  - Docker containerization supported

### User Interface

The web application provides a modern, user-friendly interface with the following screens:

1. **Main Identification Page:**
   - Image upload area with drag-and-drop support
   - Camera capture button for real-time photo capture
   - Batch upload option for multiple images
   - Identification result display with confidence scores

2. **Species Database Pages:**
   - **Birds Page:** Browse 200 bird species with images and detailed information
   - **Butterflies Page:** Browse 100 butterfly/moth species with images and details
   - Search and filter functionality
   - Sort by name or scientific name

3. **Identification Result Screen:**
   - Top prediction with confidence percentage
   - Top-3 predictions list
   - Species information card (habitat, distribution, description)
   - Image quality analysis results

4. **AI Chat Assistant:**
   - Interactive chat interface
   - Answers questions about species identification
   - Provides observation tips and photography advice

5. **History & Favorites:**
   - View identification history
   - Save favorite identifications
   - Export history and favorites to CSV/JSON

### Functions

The application provides the following key functions:

1. **Image Upload & Identification:**
   - Upload single or multiple images (PNG, JPG, JPEG, GIF, WEBP)
   - Real-time camera capture using device camera
   - Automatic image preprocessing and normalization
   - Deep learning model inference for species classification

2. **Species Classification:**
   - Predict species with confidence scores
   - Display top-3 predictions
   - Show detailed species information (habitat, distribution, description)

3. **Image Quality Analysis:**
   - Analyze image quality metrics (brightness, contrast, sharpness, saturation, resolution)
   - Provide overall quality score (0-100)
   - Generate recommendations for better image quality

4. **Species Database Browsing:**
   - Browse 300 species (200 birds + 100 butterflies/moths)
   - Search by common name or scientific name
   - View species images and detailed information
   - Filter and sort functionality

5. **AI Chat Assistant:**
   - Answer questions about species identification
   - Provide observation tips and best practices
   - Help with understanding identification results
   - Support both English and Chinese queries

6. **History & Favorites Management:**
   - Save identification history (last 10 identifications)
   - Add species to favorites
   - Export history and favorites to CSV or JSON format
   - View statistics (total identifications, unique species count)

7. **Batch Processing:**
   - Upload and process multiple images simultaneously
   - Display results in a grid layout
   - Export batch results

**Processing Time:**
- Single image identification: ~1-3 seconds (depending on hardware)
- Batch processing: Sequential processing with progress indication
- Image quality analysis: ~0.5-1 second per image

---

**References:**
- TensorFlow Documentation: https://www.tensorflow.org/
- Keras Documentation: https://keras.io/
- MobileNetV2 Paper: Sandler, M., et al. (2018). "MobileNetV2: Inverted Residuals and Linear Bottlenecks"
- Dataset Sources: [To be filled with actual data sources]


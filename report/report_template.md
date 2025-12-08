# ITP4221 - Mini Report

**Name**: [請填寫姓名]  
**Class**: IT114118/2A  
**SID**: [請填寫學號]

---

## Topic

This application is a web application that identifies butterflies and birds in Hong Kong from uploaded images or live camera input. The system uses deep learning technology to classify urban ecological species, helping users learn about the biodiversity in Hong Kong's urban environment.

## Machine Learning Task

This application uses **Image Classification** task with transfer learning. The reason for choosing image classification is:

1. **Suitability**: Image classification is perfect for identifying static images of butterflies and birds
2. **Transfer Learning**: We can leverage pre-trained models (MobileNetV2) trained on ImageNet, which significantly reduces training time and improves accuracy
3. **Evaluation**: Classification tasks have clear evaluation metrics (accuracy, confusion matrix) that are easy to interpret
4. **Deployment**: Classified models can be easily deployed to web and mobile applications

## Machine Learning Features

### Data

The dataset was retrieved from [請填寫數據來源，如Kaggle鏈接]. It contains [請填寫數量] images and the images are categorized in [請填寫] categories. The size of the dataset is [請填寫，如1.8GB].

**Data Collection Process**:
- [描述數據收集過程]
- [數據來源鏈接]
- [數據預處理步驟]

**Dataset Statistics**:
- Total Images: [數量]
- Number of Classes: [數量]
- Train/Val/Test Split: 70%/15%/15%

### Environment

The training ran on [請填寫，如Google Colab with GPU Support / Local Machine with GPU]. The versions used are:
- TensorFlow: 2.15.0
- Keras: [版本]
- Python: 3.8+
- CUDA: [如適用]

### Training

The training process consisted of two phases:

**Phase 1 - Transfer Learning**:
- Base Model: MobileNetV2 (pre-trained on ImageNet)
- Frozen base layers, trained only the top classifier
- Training ran for [數量] epochs
- Batch size: 32
- Learning rate: 0.0001
- It took [時間] to complete this phase

**Phase 2 - Fine-tuning**:
- Unfroze the last [數量] layers of the base model
- Reduced learning rate to 0.00001
- Training ran for [數量] additional epochs
- It took [時間] to complete fine-tuning

**Total Training Time**: [總時間]

**Note**:
- Epoch = time for ENTIRE dataset is passed forward and backward through the neural network ONCE
- Batch size = total number of training examples present in a single batch (32)
- Iterations = number of batches needed to complete one epoch

### Evaluation

**Model Performance**:
- Validation Accuracy: [百分比]%
- Validation Top-3 Accuracy: [百分比]%
- Test Accuracy: [百分比]%

**Confusion Matrix**: [附上混淆矩陣截圖或描述]

**Classification Report**:
[附上分類報告或主要指標]

**Key Findings**:
- [描述模型表現]
- [哪些類別識別效果好/差]
- [可能的改進方向]

## AI Application

### Platform

The model is exported as a TensorFlow SavedModel (.h5 format) and deployed to a Flask backend API. The web application is built with React for the frontend, providing a user-friendly interface for image upload and prediction.

### User Interface

[請附上界面截圖]

**Main Features**:
1. **Image Upload**: Users can upload images by clicking "Choose File" button
2. **Camera Capture**: Users can use their device camera to capture images in real-time
3. **Prediction Display**: Shows the identified species with confidence percentage
4. **Top Predictions**: Displays top 3 predictions with their confidence scores
5. **History**: Keeps track of recent identifications for review

### Functions

1. **Image Input Methods**:
   - File upload from device
   - Real-time camera capture
   - Support for multiple image formats (PNG, JPG, JPEG, GIF, WEBP)

2. **AI Prediction**:
   - Sends image to Flask backend API
   - Backend loads the trained model and processes the image
   - Returns prediction results with confidence scores

3. **Result Display**:
   - Shows the predicted class name
   - Displays confidence percentage
   - Lists top 3 predictions for user reference

4. **User Experience**:
   - Modern, responsive UI design
   - Real-time feedback during processing
   - Error handling for invalid inputs
   - History tracking for previous identifications

### Processing Time

- Image Upload: [時間]
- Model Prediction: [時間] (average)
- Total Response Time: [時間]

### Offline Support

[如果實現了離線功能，請描述]
The application can run predictions offline using TensorFlow.js, allowing users to identify species without internet connection.

---

## References

- [請列出所有參考資料和數據來源鏈接]
- TensorFlow Documentation: https://www.tensorflow.org/
- Keras Transfer Learning Guide: https://keras.io/guides/transfer_learning/
- [其他參考資料]

---

**Note**: This is a template. Please fill in all sections with your actual project details and results.


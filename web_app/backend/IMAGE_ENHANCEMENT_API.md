# Image Enhancement API Documentation

## Overview

The Image Enhancement API provides intelligent image quality improvement using computer vision techniques. This feature automatically analyzes image quality issues and applies appropriate enhancements to improve identification accuracy.

## Endpoint

### POST `/api/enhance-image`

Intelligently enhances image quality using OpenCV and PIL.

#### Request

**Content-Type**: `multipart/form-data`

**Parameters**:
- `image` (file, required): Image file to enhance (PNG, JPG, JPEG, GIF, WEBP)
- `enhancement_level` (string, optional): Enhancement intensity
  - `auto` (default): Automatically detects and applies optimal enhancement
  - `light`: Light enhancement for already good images
  - `medium`: Moderate enhancement for average quality images
  - `strong`: Strong enhancement for poor quality images

#### Response

**Success (200 OK)**:
```json
{
  "status": "success",
  "enhanced_image": "data:image/jpeg;base64,...",
  "quality_before": {
    "overall_score": 65.3,
    "metrics": {
      "brightness": {
        "value": 35.2,
        "score": 40.0,
        "status": "needs_improvement"
      },
      "contrast": {
        "value": 18.5,
        "score": 37.0,
        "status": "needs_improvement"
      },
      "sharpness": {
        "value": 45.2,
        "score": 45.2,
        "status": "needs_improvement"
      },
      "saturation": {
        "value": 42.1,
        "score": 42.1,
        "status": "good"
      },
      "resolution": {
        "width": 1920,
        "height": 1080,
        "total_pixels": 2073600,
        "score": 100.0,
        "status": "good"
      }
    },
    "recommendations": [...]
  },
  "quality_after": {
    "overall_score": 82.5,
    "metrics": {...},
    "recommendations": [...]
  },
  "enhancement_level": "auto"
}
```

**Error (400/500)**:
```json
{
  "error": "Error message description"
}
```

## Enhancement Techniques

### 1. Brightness Adjustment
- Uses LAB color space for better color preservation
- Applies CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Automatically adjusts based on detected brightness levels

### 2. Contrast Enhancement
- Improves image contrast to make features more distinguishable
- Adaptive based on original contrast levels

### 3. Sharpening
- Applies convolution kernel for edge enhancement
- Blends original and sharpened images (70% sharpened, 30% original)

### 4. Denoising
- Automatically detects noisy images
- Applies fast non-local means denoising when needed

### 5. Saturation Enhancement
- Slightly increases color saturation (10%)
- Preserves natural colors while improving vibrancy

## Usage Examples

### cURL
```bash
curl -X POST http://localhost:5000/api/enhance-image \
  -F "image=@path/to/image.jpg" \
  -F "enhancement_level=auto"
```

### JavaScript (Fetch API)
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('enhancement_level', 'auto');

fetch('http://localhost:5000/api/enhance-image', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  if (data.status === 'success') {
    // Display enhanced image
    const img = document.createElement('img');
    img.src = data.enhanced_image;
    document.body.appendChild(img);
    
    // Show quality improvement
    console.log('Quality before:', data.quality_before.overall_score);
    console.log('Quality after:', data.quality_after.overall_score);
  }
});
```

### Python (requests)
```python
import requests

with open('image.jpg', 'rb') as f:
    files = {'image': f}
    data = {'enhancement_level': 'auto'}
    response = requests.post(
        'http://localhost:5000/api/enhance-image',
        files=files,
        data=data
    )
    
result = response.json()
if result['status'] == 'success':
    # Save enhanced image
    import base64
    image_data = result['enhanced_image'].split(',')[1]
    with open('enhanced_image.jpg', 'wb') as f:
        f.write(base64.b64decode(image_data))
```

## Enhancement Levels

### Auto (Recommended)
- Analyzes image quality automatically
- Applies optimal enhancement based on detected issues
- Best for most use cases

### Light
- Minimal adjustments
- Preserves original image characteristics
- Best for already good quality images

### Medium
- Moderate enhancements
- Balanced improvement
- Best for average quality images

### Strong
- Aggressive enhancements
- Maximum quality improvement
- Best for poor quality images

## Technical Details

### Dependencies
- OpenCV (cv2) - Primary enhancement engine
- PIL/Pillow - Fallback enhancement engine
- NumPy - Array operations

### Performance
- Processing time: ~100-500ms per image (depending on size)
- Memory usage: ~2-3x image size during processing
- Output format: JPEG (95% quality)

### Limitations
- Maximum file size: 16MB
- Supported formats: PNG, JPG, JPEG, GIF, WEBP
- Cannot recover information lost due to extreme over/under exposure
- May introduce artifacts in heavily compressed images

## Integration with Identification

The enhanced image can be directly used for species identification:

```javascript
// 1. Enhance image
const enhanceResponse = await fetch('/api/enhance-image', {
  method: 'POST',
  body: enhanceFormData
});
const enhanceData = await enhanceResponse.json();

// 2. Use enhanced image for identification
const enhancedImageBlob = await fetch(enhanceData.enhanced_image)
  .then(r => r.blob());

const identifyFormData = new FormData();
identifyFormData.append('image', enhancedImageBlob);

const identifyResponse = await fetch('/api/predict', {
  method: 'POST',
  body: identifyFormData
});
```

## Best Practices

1. **Use 'auto' enhancement level** for best results
2. **Compare quality scores** before and after enhancement
3. **Use enhanced images** when original quality score < 70
4. **Test different levels** if auto doesn't produce desired results
5. **Monitor processing time** for large images

## Error Handling

Common errors and solutions:

- **"No image file provided"**: Ensure image file is included in request
- **"Invalid file type"**: Use supported formats (PNG, JPG, JPEG, GIF, WEBP)
- **"Failed to enhance image"**: Check image file integrity
- **500 Internal Server Error**: Check server logs for detailed error message

## Future Enhancements

Potential improvements:
- GPU acceleration for faster processing
- Deep learning-based super-resolution
- Style transfer options
- Batch processing support
- Custom enhancement parameters


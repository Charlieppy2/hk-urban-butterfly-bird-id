import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import axios from 'axios';

// 自动检测 API URL
// 1. 优先使用环境变量（Vercel/Koyeb 部署时应该设置）
// 2. 如果是从局域网 IP 访问（手机访问电脑），使用相同的 IP 地址
// 3. 如果是在 localhost，使用 localhost:5000
// 4. 如果是 Vercel 域名，提示需要设置环境变量
// 5. 否则使用当前域名 + 5000 端口
const getApiUrl = () => {
  // 优先使用环境变量（这是最可靠的方式）
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    const port = window.location.port;
    
    // 如果是 localhost 或 127.0.0.1，使用 localhost:5001
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:5001';
    }
    
    // 检查是否是局域网 IP 地址（192.168.x.x, 10.x.x.x, 172.16-31.x.x）
    const isLocalNetworkIP = /^(192\.168\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.)/.test(hostname);
    
    if (isLocalNetworkIP) {
      // 手机通过局域网 IP 访问，使用相同的 IP 地址作为后端
      // 这样可以确保手机能访问到运行在电脑上的后端服务
      return `http://${hostname}:5000`;
    }
    
    // 检查是否是 Vercel 域名
    const isVercelDomain = hostname.includes('vercel.app') || hostname.includes('vercel.com');
    
    if (isVercelDomain) {
      // Vercel 部署时，必须通过环境变量设置后端 URL
      // 如果没有设置，使用默认的 Koyeb 后端 URL（如果后端部署在 Koyeb）
      // 注意：这应该通过环境变量设置，这里只是作为后备方案
      console.error('⚠️ Vercel deployment detected but REACT_APP_API_URL is not set!');
      console.error('💡 Please set REACT_APP_API_URL in Vercel environment variables.');
      console.error('💡 Please set REACT_APP_API_URL in Vercel environment variables with your backend URL.');
      console.error('💡 Example: https://your-backend-app.koyeb.app');
      // 返回默认的后端 URL（如果后端部署在 Koyeb）
      // 注意：这个 URL 需要根据实际部署情况更新，建议通过环境变量设置
      return 'https://butterfly-bird-id.koyeb.app';
    }
    
    // 其他情况（生产环境域名，但不是 Vercel）
    // 使用当前域名 + 5000 端口
    return `${protocol}//${hostname}:5000`;
  }
  
  return 'http://localhost:5000';
};

const API_URL = getApiUrl();

// Debug: Log API URL (will show in browser console)
if (typeof window !== 'undefined') {
  console.log('🔍 Frontend API URL:', API_URL);
  console.log('🔍 Current location:', window.location.href);
  console.log('🔍 Environment variable REACT_APP_API_URL:', process.env.REACT_APP_API_URL);
  if (!process.env.REACT_APP_API_URL && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    console.warn('⚠️ WARNING: REACT_APP_API_URL not set! Using auto-detected URL:', API_URL);
    console.warn('💡 If images are not loading, please set REACT_APP_API_URL environment variable to your backend URL.');
  }
}

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [warning, setWarning] = useState(null); // 警告信息
  const [history, setHistory] = useState([]);
  const [batchMode, setBatchMode] = useState(false);
  const [batchFiles, setBatchFiles] = useState([]);
  const [batchResults, setBatchResults] = useState([]);
  const [batchLoading, setBatchLoading] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "Hello! I'm your AI assistant for butterfly and bird identification. I can help you with:\n• Species information and characteristics\n• Identification tips and techniques\n• Best practices for observation\n• Understanding identification results\n• Questions about butterflies and birds\n\n💡 You can ask me in English or Chinese (中文), and I will respond in English.\n\nHow can I help you today?",
      timestamp: new Date().toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      })
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [statistics, setStatistics] = useState(null);
  const [showStatistics, setShowStatistics] = useState(false);
  const [statsLoading, setStatsLoading] = useState(false);
  const [qualityAnalysis, setQualityAnalysis] = useState(null);
  const [analyzingQuality, setAnalyzingQuality] = useState(false);
  const [favorites, setFavorites] = useState(() => {
    // Load favorites from localStorage
    const saved = localStorage.getItem('favorites');
    if (!saved) return [];
    
    try {
      const parsed = JSON.parse(saved);
      // Return as-is, images should already be in base64 format
      return parsed;
    } catch (error) {
      console.error('Error loading favorites:', error);
      return [];
    }
  });
  const [showFavorites, setShowFavorites] = useState(false);
  const [enlargedImage, setEnlargedImage] = useState(null); // { url, title }
  const [showBirdsPage, setShowBirdsPage] = useState(false);
  const [showButterfliesPage, setShowButterfliesPage] = useState(false);
  const [birdsData, setBirdsData] = useState([]);
  const [butterfliesData, setButterfliesData] = useState([]);
  const [birdsLoading, setBirdsLoading] = useState(false);
  const [butterfliesLoading, setButterfliesLoading] = useState(false);
  const [birdsSearchTerm, setBirdsSearchTerm] = useState('');
  const [butterfliesSearchTerm, setButterfliesSearchTerm] = useState('');
  const [birdsSortBy, setBirdsSortBy] = useState('name'); // 'name', 'scientific'
  const [butterfliesSortBy, setButterfliesSortBy] = useState('name');
  const [showHistoryExportMenu, setShowHistoryExportMenu] = useState(false);
  const [showFavoritesExportMenu, setShowFavoritesExportMenu] = useState(false);
  
  // Text Description Identification States
  const [showDescriptionMode, setShowDescriptionMode] = useState(false);
  const [descriptionInput, setDescriptionInput] = useState('');
  const [descriptionCategory, setDescriptionCategory] = useState('all'); // 'all', 'bird', 'butterfly'
  const [descriptionResults, setDescriptionResults] = useState(null);
  const [descriptionLoading, setDescriptionLoading] = useState(false);
  const [descriptionConversation, setDescriptionConversation] = useState([]);
  const [currentMatches, setCurrentMatches] = useState([]);
  
  // Species Detail Modal State
  const [selectedSpeciesDetail, setSelectedSpeciesDetail] = useState(null);
  const [showSpeciesModal, setShowSpeciesModal] = useState(false);
  
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const streamRef = useRef(null);
  const historyExportRef = useRef(null);
  const favoritesExportRef = useRef(null);

  const handleImageSelect = (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;
    
    if (batchMode) {
      // Batch mode: handle multiple files
      setBatchFiles(files);
      setSelectedImage(null);
      setPreview(null);
      setPrediction(null);
    } else {
      // Single mode: handle first file only
      const file = files[0];
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setPrediction(null);
      setError(null);
      setBatchFiles([]);
    }
  };

  const handleBatchPredict = async () => {
    if (batchFiles.length === 0) {
      setError('Please select at least one image');
      return;
    }

    setBatchLoading(true);
    setError(null);
    setBatchResults([]);

    const results = [];
    
    for (let i = 0; i < batchFiles.length; i++) {
      const file = batchFiles[i];
      const formData = new FormData();
      formData.append('image', file);

      try {
        const response = await axios.post(`${API_URL}/api/predict`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        results.push({
          id: Date.now() + i,
          filename: file.name,
          image: URL.createObjectURL(file),
          prediction: response.data.prediction,
          quality: response.data.quality_analysis,
          timestamp: new Date().toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          }),
        });
      } catch (err) {
        results.push({
          id: Date.now() + i,
          filename: file.name,
          image: URL.createObjectURL(file),
          error: err.response?.data?.error || 'Failed to make prediction',
          timestamp: new Date().toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          }),
        });
      }
    }

    setBatchResults(results);
    setBatchLoading(false);
    
    // Add to history
    const validResults = results.filter(r => r.prediction);
    if (validResults.length > 0) {
      setHistory([...validResults, ...history].slice(0, 20));
    }
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    // Debug: Log API URL
    console.log('API URL:', API_URL);
    console.log('Full URL:', `${API_URL}/api/predict`);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post(`${API_URL}/api/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 seconds timeout
      });

      setPrediction(response.data.prediction);
      console.log('🔍 Full response data:', response.data);
      
      // 保存警告信息（如果有）
      if (response.data.warning) {
        setWarning(response.data.warning);
        console.log('⚠️ Warning:', response.data.warning);
      } else {
        setWarning(null); // 清除之前的警告
      }
      
      // Add to history
      const historyItem = {
        id: Date.now(),
        image: preview,
        prediction: response.data.prediction,
        quality: response.data.quality_analysis,
        warning: response.data.warning, // 保存警告信息
        timestamp: new Date().toLocaleString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        }),
      };
      setHistory([historyItem, ...history].slice(0, 10)); // Keep last 10
    } catch (err) {
      // Enhanced error logging
      console.error('Prediction error:', err);
      console.error('Error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status,
        url: `${API_URL}/api/predict`
      });
      
      // More user-friendly error messages
      let errorMessage = 'Failed to make prediction';
      if (err.code === 'ECONNABORTED') {
        errorMessage = 'Request timeout. Please check your internet connection and try again.';
      } else if (err.message === 'Network Error') {
        errorMessage = `Cannot connect to server. Please check if the API URL is correct: ${API_URL}`;
      } else if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCameraCapture = () => {
    if (!isCameraOpen) {
      openCamera();
    } else {
      capturePhoto();
    }
  };

  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsCameraOpen(true);
      }
    } catch (err) {
      setError('Failed to access camera: ' + err.message);
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      
      canvas.toBlob((blob) => {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        setSelectedImage(file);
        setPreview(URL.createObjectURL(blob));
        setPrediction(null);
        closeCamera();
      }, 'image/jpeg', 0.9);
    }
  };

  const closeCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsCameraOpen(false);
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreview(null);
    setPrediction(null);
    setError(null);
    setWarning(null); // 清除警告
    setQualityAnalysis(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    closeCamera();
  };

  // Scroll to top functionality

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth' // 平滑滚动
    });
  };

  // Close export menus when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (historyExportRef.current && !historyExportRef.current.contains(event.target)) {
        setShowHistoryExportMenu(false);
      }
      if (favoritesExportRef.current && !favoritesExportRef.current.contains(event.target)) {
        setShowFavoritesExportMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleToggleFavorite = async () => {
    if (!prediction || !preview) return;

    // Convert image to base64 for persistent storage
    let imageBase64 = preview;
    
    // Always convert to base64, whether it's blob URL or already base64
    try {
      // If it's a blob URL, convert to base64
      if (preview.startsWith('blob:')) {
        const response = await fetch(preview);
        const blob = await response.blob();
        imageBase64 = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(reader.result);
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });
      } else if (preview.startsWith('data:image')) {
        // Already base64, use as is
        imageBase64 = preview;
      } else {
        // Try to fetch and convert
        try {
          const response = await fetch(preview);
          const blob = await response.blob();
          imageBase64 = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
          });
        } catch (fetchError) {
          console.error('Error fetching image:', fetchError);
          imageBase64 = preview; // Fallback
        }
      }
    } catch (error) {
      console.error('Error converting image to base64:', error);
      setError('Failed to convert image. Please try again.');
      return; // Don't save if image conversion fails
    }

    // Verify base64 conversion was successful
    if (!imageBase64) {
      console.error('Image conversion failed: imageBase64 is null or undefined');
      setError('Failed to save image. Please try again.');
      return;
    }
    
    if (!imageBase64.startsWith('data:image')) {
      console.error('Image conversion failed: not a valid base64 image');
      console.error('ImageBase64 preview:', imageBase64.substring(0, 100));
      setError('Failed to save image. Please try again.');
      return;
    }

    const favoriteItem = {
      id: Date.now(),
      image: imageBase64, // Store as base64 for persistence
      prediction: prediction,
      quality: qualityAnalysis,
      timestamp: new Date().toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      }),
    };

    console.log('Saving favorite with image (first 100 chars):', imageBase64.substring(0, 100));

    // Check if already favorited
    const isFavorited = favorites.some(
      fav => fav.prediction.class === prediction.class && 
             Math.abs(new Date(fav.timestamp) - new Date(favoriteItem.timestamp)) < 1000
    );

    let newFavorites;
    if (isFavorited) {
      // Remove from favorites
      newFavorites = favorites.filter(
        fav => !(fav.prediction.class === prediction.class && 
                Math.abs(new Date(fav.timestamp) - new Date(favoriteItem.timestamp)) < 1000)
      );
    } else {
      // Add to favorites
      newFavorites = [favoriteItem, ...favorites];
    }

    setFavorites(newFavorites);
    localStorage.setItem('favorites', JSON.stringify(newFavorites));
  };

  const handleRemoveFavorite = (favoriteId) => {
    const newFavorites = favorites.filter(fav => fav.id !== favoriteId);
    setFavorites(newFavorites);
    localStorage.setItem('favorites', JSON.stringify(newFavorites));
  };

  const isCurrentFavorite = () => {
    if (!prediction || !preview) return false;
    return favorites.some(
      fav => fav.prediction.class === prediction.class
    );
  };

  // Export functions
  const exportHistoryToCSV = () => {
    if (history.length === 0) {
      setError('No history to export');
      return;
    }

    const headers = ['ID', 'Species', 'Confidence (%)', 'Top Predictions', 'Timestamp', 'Quality Score'];
    const rows = history.map(item => [
      item.id,
      item.prediction.class,
      (item.prediction.confidence * 100).toFixed(2),
      item.prediction.top_predictions.map(p => `${p.class} (${(p.confidence * 100).toFixed(2)}%)`).join('; '),
      item.timestamp,
      item.quality ? item.quality.overall_score.toFixed(1) : 'N/A'
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `identification_history_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportHistoryToJSON = async () => {
    if (history.length === 0) {
      setError('No history to export');
      return;
    }

    // Convert image URLs to base64 for JSON export
    const recordsWithImages = await Promise.all(
      history.map(async (item) => {
        try {
          const response = await fetch(item.image);
          const blob = await response.blob();
          const base64 = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
          });
          return {
            ...item,
            imageBase64: base64
          };
        } catch (error) {
          console.error('Error converting image:', error);
          return {
            ...item,
            imageBase64: null,
            imageUrl: item.image
          };
        }
      })
    );

    const data = {
      exportDate: new Date().toISOString(),
      totalRecords: history.length,
      records: recordsWithImages
    };

    const jsonContent = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonContent], { type: 'application/json;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `identification_history_${new Date().toISOString().split('T')[0]}.json`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportFavoritesToCSV = () => {
    if (favorites.length === 0) {
      setError('No favorites to export');
      return;
    }

    const headers = ['ID', 'Species', 'Confidence (%)', 'Top Predictions', 'Timestamp', 'Quality Score'];
    const rows = favorites.map(item => [
      item.id,
      item.prediction.class,
      (item.prediction.confidence * 100).toFixed(2),
      item.prediction.top_predictions.map(p => `${p.class} (${(p.confidence * 100).toFixed(2)}%)`).join('; '),
      item.timestamp,
      item.quality ? item.quality.overall_score.toFixed(1) : 'N/A'
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `favorites_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportFavoritesToJSON = async () => {
    if (favorites.length === 0) {
      setError('No favorites to export');
      return;
    }

    // Convert image URLs to base64 for JSON export
    const recordsWithImages = await Promise.all(
      favorites.map(async (item) => {
        try {
          const response = await fetch(item.image);
          const blob = await response.blob();
          const base64 = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
          });
          return {
            ...item,
            imageBase64: base64
          };
        } catch (error) {
          console.error('Error converting image:', error);
          return {
            ...item,
            imageBase64: null,
            imageUrl: item.image
          };
        }
      })
    );

    const data = {
      exportDate: new Date().toISOString(),
      totalRecords: favorites.length,
      records: recordsWithImages
    };

    const jsonContent = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonContent], { type: 'application/json;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `favorites_${new Date().toISOString().split('T')[0]}.json`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportStatisticsToPDF = async () => {
    if (!statistics) {
      setError('No statistics to export. Please load statistics first.');
      return;
    }

    // Declare loadingMsg outside try block for error handling
    let loadingMsg = null;
    
    try {
      // Dynamically import jsPDF
      const { default: jsPDF } = await import('jspdf');
      const doc = new jsPDF();
      
      // Show loading message
      setError(null);
      loadingMsg = document.createElement('div');
      loadingMsg.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.8);color:white;padding:20px;border-radius:10px;z-index:10000;';
      loadingMsg.textContent = 'Generating PDF with images...';
      document.body.appendChild(loadingMsg);

      // Title
      doc.setFontSize(20);
      doc.setTextColor(46, 125, 50);
      doc.text('Identification Statistics Report', 105, 20, { align: 'center' });

      // Export date
      doc.setFontSize(10);
      doc.setTextColor(100, 100, 100);
      doc.text(`Generated: ${new Date().toLocaleString('en-US')}`, 105, 30, { align: 'center' });

      let yPos = 45;

      // Summary Statistics
      doc.setFontSize(14);
      doc.setTextColor(0, 0, 0);
      doc.text('Summary Statistics', 20, yPos);
      yPos += 10;

      doc.setFontSize(11);
      doc.text(`Total Identifications: ${statistics.total_identifications}`, 25, yPos);
      yPos += 7;
      doc.text(`Unique Species: ${statistics.unique_species}`, 25, yPos);
      yPos += 7;
      doc.text(`Average Confidence: ${statistics.average_confidence.toFixed(2)}%`, 25, yPos);
      yPos += 15;

      // Category Distribution
      doc.setFontSize(14);
      doc.text('Category Distribution', 20, yPos);
      yPos += 10;

      doc.setFontSize(11);
      doc.text(`Birds: ${statistics.category_distribution.birds}`, 25, yPos);
      yPos += 7;
      doc.text(`Butterflies/Moths: ${statistics.category_distribution.butterflies}`, 25, yPos);
      yPos += 7;
      if (statistics.category_distribution.others > 0) {
        doc.text(`Others: ${statistics.category_distribution.others}`, 25, yPos);
        yPos += 7;
      }
      yPos += 10;

      // Confidence Distribution
      doc.setFontSize(14);
      doc.text('Confidence Distribution', 20, yPos);
      yPos += 10;

      doc.setFontSize(11);
      doc.text(`High (≥90%): ${statistics.confidence_distribution.high}`, 25, yPos);
      yPos += 7;
      doc.text(`Medium (70-90%): ${statistics.confidence_distribution.medium}`, 25, yPos);
      yPos += 7;
      doc.text(`Low (<70%): ${statistics.confidence_distribution.low}`, 25, yPos);
      yPos += 15;

      // Top Species with images from history
      doc.setFontSize(14);
      doc.text('Top 10 Identified Species', 20, yPos);
      yPos += 10;

      doc.setFontSize(10);
      const topSpeciesList = statistics.top_species.slice(0, 10);
      
      for (let idx = 0; idx < topSpeciesList.length; idx++) {
        const item = topSpeciesList[idx];
        if (yPos > 240) {
          doc.addPage();
          yPos = 20;
        }
        
        const speciesName = item.species.replace(/^\d+\./, '').substring(0, 35);
        doc.text(`${idx + 1}. ${speciesName}`, 25, yPos);
        doc.text(`   Count: ${item.count}, Avg Confidence: ${item.avg_confidence.toFixed(2)}%`, 30, yPos + 5);
        yPos += 8;
        
        // Try to add sample image from history
        const sampleRecord = history.find(h => h.prediction.class === item.species);
        if (sampleRecord && sampleRecord.image) {
          try {
            const img = new Image();
            img.crossOrigin = 'anonymous';
            await new Promise((resolve, reject) => {
              img.onload = resolve;
              img.onerror = reject;
              img.src = sampleRecord.image;
            });
            
            const imgWidth = 40;
            const imgHeight = 30;
            if (yPos + imgHeight > 280) {
              doc.addPage();
              yPos = 20;
            }
            doc.addImage(img, 'JPEG', 30, yPos, imgWidth, imgHeight);
            yPos += imgHeight + 8;
          } catch (error) {
            console.error('Error adding image to PDF:', error);
            yPos += 5;
          }
        } else {
          yPos += 5;
        }
      }

      // Footer
      const pageCount = doc.internal.pages.length - 1;
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(`Page ${i} of ${pageCount}`, 105, 290, { align: 'center' });
      }

      // Save PDF
      doc.save(`statistics_report_${new Date().toISOString().split('T')[0]}.pdf`);
      
      // Remove loading message
      if (loadingMsg && loadingMsg.parentNode) {
        loadingMsg.parentNode.removeChild(loadingMsg);
      }
    } catch (error) {
      console.error('Error generating PDF:', error);
      setError('Failed to generate PDF: ' + error.message);
      if (loadingMsg && loadingMsg.parentNode) {
        loadingMsg.parentNode.removeChild(loadingMsg);
      }
    }
  };

  const handleChatSend = async () => {
    if (!chatInput.trim() || chatLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: chatInput,
      timestamp: new Date().toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      })
    };

    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setChatLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        message: userMessage.text,
        context: {
          lastPrediction: prediction,
          historyCount: history.length
        }
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: response.data.response,
        timestamp: new Date().toLocaleString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        })
      };

      setChatMessages(prev => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toLocaleString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        })
      };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleChatKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleChatSend();
    }
  };

  const handleLoadStatistics = async () => {
    if (history.length === 0) {
      setError('No identification history available');
      return;
    }

    setStatsLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/api/statistics`, {
        history: history
      });

      setStatistics(response.data.statistics);
      setShowStatistics(true);
    } catch (err) {
      setError('Failed to load statistics: ' + (err.response?.data?.error || err.message));
    } finally {
      setStatsLoading(false);
    }
  };

  const handleAnalyzeQuality = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setAnalyzingQuality(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post(`${API_URL}/api/analyze-quality`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setQualityAnalysis(response.data.quality_analysis);
    } catch (err) {
      setError('Failed to analyze image quality: ' + (err.response?.data?.error || err.message));
    } finally {
      setAnalyzingQuality(false);
    }
  };

  // Load birds data when birds page is opened (with localStorage cache)
  useEffect(() => {
    if (showBirdsPage && birdsData.length === 0 && !birdsLoading) {
      // Try to load from cache first
      const cachedBirds = localStorage.getItem('birds_data_cache');
      const cacheTimestamp = localStorage.getItem('birds_data_cache_timestamp');
      const cacheAge = cacheTimestamp ? Date.now() - parseInt(cacheTimestamp) : Infinity;
      const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours
      
      if (cachedBirds && cacheAge < CACHE_DURATION) {
        try {
          const birds = JSON.parse(cachedBirds);
          // Check if cached data has old paths (data/processed/train)
          const hasOldPaths = birds.some(bird => 
            bird.image_path && bird.image_path.includes('processed/train')
          );
          
          if (hasOldPaths) {
            console.warn('⚠️ Cached data has old image paths, clearing cache and reloading...');
            localStorage.removeItem('birds_data_cache');
            localStorage.removeItem('birds_data_cache_timestamp');
            // Continue to fetch fresh data below
          } else {
            setBirdsData(birds);
            console.log(`✅ Loaded ${birds.length} bird species from cache`);
            return;
          }
        } catch (e) {
          console.warn('Failed to parse cached birds data:', e);
          localStorage.removeItem('birds_data_cache');
          localStorage.removeItem('birds_data_cache_timestamp');
        }
      }
      
      setBirdsLoading(true);
      setError(null);
      axios.get(`${API_URL}/api/birds`, {
        timeout: 15000 // 15 seconds timeout
      })
        .then(response => {
          if (response.data.status === 'success') {
            const birds = Object.values(response.data.birds);
            setBirdsData(birds);
            // Cache the data
            localStorage.setItem('birds_data_cache', JSON.stringify(birds));
            localStorage.setItem('birds_data_cache_timestamp', Date.now().toString());
            console.log(`✅ Loaded ${birds.length} bird species from API`);
          } else {
            setError('Failed to load bird data: ' + (response.data.message || 'Unknown error'));
          }
        })
        .catch(error => {
          console.error('Error loading birds:', error);
          let errorMessage = 'Failed to load bird data';
          if (error.code === 'ECONNABORTED') {
            errorMessage = 'Request timeout. Please check your connection and try again.';
          } else if (error.message === 'Network Error') {
            errorMessage = `Cannot connect to server. Please check if the API URL is correct: ${API_URL}`;
          } else if (error.response?.data?.message) {
            errorMessage = error.response.data.message;
          }
          setError(errorMessage);
        })
        .finally(() => {
          setBirdsLoading(false);
        });
    }
  }, [showBirdsPage, birdsData.length, birdsLoading]);

  // Load butterflies data when butterflies page is opened (with localStorage cache)
  useEffect(() => {
    if (showButterfliesPage && butterfliesData.length === 0 && !butterfliesLoading) {
      // Try to load from cache first
      const cachedButterflies = localStorage.getItem('butterflies_data_cache');
      const cacheTimestamp = localStorage.getItem('butterflies_data_cache_timestamp');
      const cacheAge = cacheTimestamp ? Date.now() - parseInt(cacheTimestamp) : Infinity;
      const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours
      
      if (cachedButterflies && cacheAge < CACHE_DURATION) {
        try {
          const butterflies = JSON.parse(cachedButterflies);
          // Check if cached data has old paths (data/processed/train)
          const hasOldPaths = butterflies.some(butterfly => 
            butterfly.image_path && butterfly.image_path.includes('processed/train')
          );
          
          if (hasOldPaths) {
            console.warn('⚠️ Cached data has old image paths, clearing cache and reloading...');
            localStorage.removeItem('butterflies_data_cache');
            localStorage.removeItem('butterflies_data_cache_timestamp');
            // Continue to fetch fresh data below
          } else {
            setButterfliesData(butterflies);
            console.log(`✅ Loaded ${butterflies.length} butterfly/moth species from cache`);
            return;
          }
        } catch (e) {
          console.warn('Failed to parse cached butterflies data:', e);
          localStorage.removeItem('butterflies_data_cache');
          localStorage.removeItem('butterflies_data_cache_timestamp');
        }
      }
      
      setButterfliesLoading(true);
      setError(null);
      axios.get(`${API_URL}/api/butterflies`, {
        timeout: 15000 // 15 seconds timeout
      })
        .then(response => {
          if (response.data.status === 'success') {
            const butterflies = Object.values(response.data.butterflies);
            setButterfliesData(butterflies);
            // Cache the data
            localStorage.setItem('butterflies_data_cache', JSON.stringify(butterflies));
            localStorage.setItem('butterflies_data_cache_timestamp', Date.now().toString());
            console.log(`✅ Loaded ${butterflies.length} butterfly/moth species from API`);
          } else {
            setError('Failed to load butterfly data: ' + (response.data.message || 'Unknown error'));
          }
        })
        .catch(error => {
          console.error('Error loading butterflies:', error);
          let errorMessage = 'Failed to load butterfly data';
          if (error.code === 'ECONNABORTED') {
            errorMessage = 'Request timeout. Please check your connection and try again.';
          } else if (error.message === 'Network Error') {
            errorMessage = `Cannot connect to server. Please check if the API URL is correct: ${API_URL}`;
          } else if (error.response?.data?.message) {
            errorMessage = error.response.data.message;
          }
          setError(errorMessage);
        })
        .finally(() => {
          setButterfliesLoading(false);
        });
    }
  }, [showButterfliesPage, butterfliesData.length, butterfliesLoading]);

  // Reset other pages when switching
  const handleShowBirds = () => {
    setShowBirdsPage(true);
    setShowButterfliesPage(false);
    setShowFavorites(false);
  };

  const handleShowButterflies = () => {
    setShowButterfliesPage(true);
    setShowBirdsPage(false);
    setShowFavorites(false);
  };

  const handleShowMain = () => {
    setShowBirdsPage(false);
    setShowButterfliesPage(false);
    setShowFavorites(false);
  };

  // Text Description Identification Functions
  const handleDescriptionSubmit = async () => {
    if (!descriptionInput.trim() || descriptionLoading) return;

    const userMessage = {
      role: 'user',
      content: descriptionInput,
      timestamp: new Date().toLocaleTimeString()
    };

    setDescriptionConversation(prev => [...prev, userMessage]);
    setDescriptionLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/api/description-chat`, {
        message: descriptionInput,
        conversation_history: descriptionConversation,
        current_matches: currentMatches,
        category: descriptionCategory === 'all' ? null : descriptionCategory
      });

      if (response.data.success) {
        const botMessage = {
          role: 'assistant',
          content: response.data.response,
          timestamp: new Date().toLocaleTimeString(),
          matches: response.data.matches,
          followUpQuestions: response.data.follow_up_questions
        };

        setDescriptionConversation(prev => [...prev, botMessage]);
        setCurrentMatches(response.data.matches || []);
        setDescriptionResults(response.data);
      } else {
        setError(response.data.error || 'Failed to identify species');
      }
    } catch (err) {
      console.error('Description identification error:', err);
      setError(err.response?.data?.error || 'Failed to connect to server');
    } finally {
      setDescriptionLoading(false);
      setDescriptionInput('');
    }
  };

  const handleDescriptionKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleDescriptionSubmit();
    }
  };

  const handleStartNewDescriptionChat = () => {
    setDescriptionConversation([]);
    setCurrentMatches([]);
    setDescriptionResults(null);
    setDescriptionInput('');
  };

  const handleQuickQuestion = (question) => {
    setDescriptionInput(question);
  };

  // Handle clicking on a species card to view details
  const handleSpeciesCardClick = (species) => {
    setSelectedSpeciesDetail(species);
    setShowSpeciesModal(true);
  };

  // Close species detail modal
  const handleCloseSpeciesModal = () => {
    setShowSpeciesModal(false);
    setSelectedSpeciesDetail(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🦋🐦 Butterfly & Bird Identifier</h1>
        <p>AI-Powered Species Identification System</p>
        <div className="main-navigation">
          <button 
            className={`nav-btn ${!showBirdsPage && !showButterfliesPage && !showDescriptionMode ? 'active' : ''}`}
            onClick={() => { handleShowMain(); setShowDescriptionMode(false); }}
          >
            🏠 Home
          </button>
          <button 
            className={`nav-btn ${showDescriptionMode ? 'active' : ''}`}
            onClick={() => { handleShowMain(); setShowDescriptionMode(true); }}
          >
            💬 Describe to Identify
          </button>
          <button 
            className={`nav-btn ${showBirdsPage ? 'active' : ''}`}
            onClick={() => { handleShowBirds(); setShowDescriptionMode(false); }}
          >
            🐦 Birds (200)
          </button>
          <button 
            className={`nav-btn ${showButterfliesPage ? 'active' : ''}`}
            onClick={() => { handleShowButterflies(); setShowDescriptionMode(false); }}
          >
            🦋 Butterflies (100)
          </button>
        </div>
      </header>

      <main className="App-main">
        {/* Text Description Identification Page */}
        {showDescriptionMode && !showBirdsPage && !showButterfliesPage && (
          <div className="description-mode-page">
            <div className="description-header">
              <h2>💬 Identify Species by Description</h2>
              <p>Describe what you saw - habitat, colors, behavior, features - and I'll help identify the species!</p>
            </div>

            {/* Category Selection */}
            <div className="description-category-selector">
              <label>Looking for:</label>
              <div className="category-buttons">
                <button 
                  className={`category-btn ${descriptionCategory === 'all' ? 'active' : ''}`}
                  onClick={() => setDescriptionCategory('all')}
                >
                  🔍 All Species
                </button>
                <button 
                  className={`category-btn ${descriptionCategory === 'bird' ? 'active' : ''}`}
                  onClick={() => setDescriptionCategory('bird')}
                >
                  🐦 Birds Only
                </button>
                <button 
                  className={`category-btn ${descriptionCategory === 'butterfly' ? 'active' : ''}`}
                  onClick={() => setDescriptionCategory('butterfly')}
                >
                  🦋 Butterflies Only
                </button>
              </div>
            </div>

            {/* Conversation Area */}
            <div className="description-conversation">
              {descriptionConversation.length === 0 ? (
                <div className="conversation-welcome">
                  <div className="welcome-icon">🔍</div>
                  <h3>Start Describing!</h3>
                  <p>Tell me about the species you want to identify. Include details like:</p>
                  <ul className="description-tips">
                    <li><strong>Colors:</strong> What colors did you notice? (e.g., "blue wings with black spots")</li>
                    <li><strong>Size:</strong> How big was it? (e.g., "small", "about 10cm", "large wingspan")</li>
                    <li><strong>Habitat:</strong> Where did you see it? (e.g., "forest", "near water", "urban garden")</li>
                    <li><strong>Behavior:</strong> What was it doing? (e.g., "flying slowly", "feeding on flowers")</li>
                    <li><strong>Location:</strong> What region or area? (e.g., "Hong Kong", "North America")</li>
                    <li><strong>Features:</strong> Any distinctive marks? (e.g., "long tail", "crested head")</li>
                  </ul>
                  
                  <div className="quick-start-prompts">
                    <p>Try these examples:</p>
                    <button onClick={() => handleQuickQuestion("I saw a small blue butterfly with orange spots near a garden")}>
                      "Small blue butterfly with orange spots"
                    </button>
                    <button onClick={() => handleQuickQuestion("Large black bird with a hooked beak, seen near the coast")}>
                      "Large black bird with hooked beak"
                    </button>
                    <button onClick={() => handleQuickQuestion("Yellow and black striped butterfly in a meadow")}>
                      "Yellow and black striped butterfly"
                    </button>
                  </div>
                </div>
              ) : (
                <div className="conversation-messages">
                  {descriptionConversation.map((msg, index) => (
                    <div key={index} className={`conversation-message ${msg.role}`}>
                      <div className="message-avatar">
                        {msg.role === 'user' ? '👤' : '🤖'}
                      </div>
                      <div className="message-content">
                        <div className="message-text" dangerouslySetInnerHTML={{ 
                          __html: msg.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br/>') 
                        }} />
                        <span className="message-time">{msg.timestamp}</span>
                        
                        {/* Show matches if available */}
                        {msg.matches && msg.matches.length > 0 && (
                          <div className="message-matches">
                            <h4>🎯 Possible Matches:</h4>
                            <div className="matches-grid">
                              {msg.matches.slice(0, 3).map((match, idx) => (
                                <div 
                                  key={idx} 
                                  className="match-card clickable"
                                  onClick={() => handleSpeciesCardClick(match)}
                                  title="Click to view species details"
                                >
                                  {match.image_path && (
                                    <img 
                                      src={`${API_URL}/api/species-image/${encodeURIComponent(match.image_path)}`}
                                      alt={match.common_name}
                                      className="match-image"
                                      onError={(e) => { e.target.style.display = 'none'; }}
                                    />
                                  )}
                                  <div className="match-info">
                                    <h5>{match.common_name}</h5>
                                    <p className="match-scientific">{match.scientific_name}</p>
                                    <span className={`match-category ${match.category.toLowerCase()}`}>
                                      {match.category}
                                    </span>
                                    <div className="match-confidence">
                                      <div 
                                        className="confidence-bar"
                                        style={{ width: `${match.confidence_score * 100}%` }}
                                      />
                                      <span>{(match.confidence_score * 100).toFixed(0)}% match</span>
                                    </div>
                                  </div>
                                  <div className="click-hint">👆 Click for details</div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        
                        {/* Show follow-up question buttons */}
                        {msg.followUpQuestions && msg.followUpQuestions.length > 0 && (
                          <div className="follow-up-questions">
                            <p>💡 Help me narrow it down:</p>
                            {msg.followUpQuestions.map((q, qIdx) => (
                              <button 
                                key={qIdx} 
                                className="follow-up-btn"
                                onClick={() => handleQuickQuestion(q)}
                              >
                                {q}
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  
                  {descriptionLoading && (
                    <div className="conversation-message assistant">
                      <div className="message-avatar">🤖</div>
                      <div className="message-content">
                        <div className="typing-indicator">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="description-input-area">
              <button 
                className="new-chat-btn"
                onClick={handleStartNewDescriptionChat}
                title="Start new identification"
              >
                🔄
              </button>
              <textarea
                value={descriptionInput}
                onChange={(e) => setDescriptionInput(e.target.value)}
                onKeyPress={handleDescriptionKeyPress}
                placeholder="Describe the species you saw... (colors, size, habitat, behavior, location)"
                disabled={descriptionLoading}
                rows={2}
              />
              <button 
                className="send-description-btn"
                onClick={handleDescriptionSubmit}
                disabled={descriptionLoading || !descriptionInput.trim()}
              >
                {descriptionLoading ? '🔄' : '🔍'}
              </button>
            </div>

            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}
          </div>
        )}

        {/* Birds Page */}
        {showBirdsPage && (
          <div className="species-page">
            <div className="species-header">
              <h2>🐦 Bird Species Database</h2>
              <p>Explore {birdsData.length} bird species with detailed information</p>
              {birdsSearchTerm && (
                <p className="search-results-count">
                  Showing {birdsData.filter((bird) => {
                    const searchLower = birdsSearchTerm.toLowerCase();
                    return (
                      bird.common_name?.toLowerCase().includes(searchLower) ||
                      bird.scientific_name?.toLowerCase().includes(searchLower)
                    );
                  }).length} result(s)
                </p>
              )}
            </div>
            
            {/* Search and Filter */}
            <div className="species-controls">
              <div className="search-box">
                <input
                  type="text"
                  placeholder="🔍 Search birds by name or scientific name..."
                  value={birdsSearchTerm}
                  onChange={(e) => setBirdsSearchTerm(e.target.value)}
                  className="search-input"
                />
              </div>
              <div className="sort-box">
                <label>Sort by: </label>
                <select
                  value={birdsSortBy}
                  onChange={(e) => setBirdsSortBy(e.target.value)}
                  className="sort-select"
                >
                  <option value="name">Common Name (A-Z)</option>
                  <option value="scientific">Scientific Name (A-Z)</option>
                  <option value="id">ID (1-200)</option>
                </select>
              </div>
            </div>

            {error && showBirdsPage && (
              <div className="error-message" style={{ marginBottom: '20px' }}>
                ⚠️ {error}
                <button 
                  onClick={() => {
                    setBirdsData([]);
                    setBirdsLoading(false);
                    setError(null);
                  }} 
                  className="btn btn-secondary"
                  style={{ marginLeft: '10px' }}
                >
                  Retry
                </button>
              </div>
            )}
            {birdsLoading ? (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Loading bird species... Please wait</p>
                <p style={{ fontSize: '0.9rem', color: '#999', marginTop: '10px' }}>
                  Loading {birdsData.length > 0 ? birdsData.length : '0'} / 200 species
                </p>
              </div>
            ) : (
              <div className="species-grid">
                {birdsData
                  .filter((bird) => {
                    if (!birdsSearchTerm) return true;
                    const searchLower = birdsSearchTerm.toLowerCase();
                    return (
                      bird.common_name?.toLowerCase().includes(searchLower) ||
                      bird.scientific_name?.toLowerCase().includes(searchLower)
                    );
                  })
                  .sort((a, b) => {
                    if (birdsSortBy === 'name') {
                      return (a.common_name || '').localeCompare(b.common_name || '');
                    } else if (birdsSortBy === 'scientific') {
                      return (a.scientific_name || '').localeCompare(b.scientific_name || '');
                    } else {
                      return (a.id || 0) - (b.id || 0);
                    }
                  })
                  .map((bird) => (
                  <div key={bird.id} className="species-card">
                    {bird.image_path && (
                      <div className="species-image-container">
                        <img 
                          src={`${API_URL}/api/species-image/${encodeURIComponent(bird.image_path)}`}
                          alt={bird.common_name}
                          className="species-image clickable-image"
                          onClick={() => {
                            setEnlargedImage({
                              url: `${API_URL}/api/species-image/${encodeURIComponent(bird.image_path)}`,
                              title: bird.common_name,
                              subtitle: bird.scientific_name
                            });
                          }}
                          onError={(e) => {
                            const imgUrl = `${API_URL}/api/species-image/${encodeURIComponent(bird.image_path)}`;
                            console.error('❌ Image load error:', {
                              imagePath: bird.image_path,
                              fullUrl: imgUrl,
                              apiUrl: API_URL,
                              error: e
                            });
                            // 显示错误占位符而不是隐藏
                            e.target.style.display = 'none';
                            const container = e.target.parentElement;
                            if (container && !container.querySelector('.image-error-placeholder')) {
                              const placeholder = document.createElement('div');
                              placeholder.className = 'image-error-placeholder';
                              placeholder.innerHTML = '🖼️<br/>Image not available';
                              placeholder.style.cssText = 'display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #999; font-size: 0.9rem; text-align: center;';
                              container.appendChild(placeholder);
                            }
                          }}
                          onLoad={() => {
                            console.log('✅ Image loaded successfully:', bird.image_path);
                          }}
                        />
                      </div>
                    )}
                    <div className="species-card-header">
                      <h3>{bird.common_name}</h3>
                      {bird.scientific_name && (
                        <p className="scientific-name"><em>{bird.scientific_name}</em></p>
                      )}
                    </div>
                    {bird.description && (
                      <div className="species-info">
                        <p className="description">{bird.description}</p>
                      </div>
                    )}
                    <div className="species-details">
                      {bird.habitat && (
                        <div className="detail-item">
                          <strong>📍 Habitat:</strong> {bird.habitat}
                        </div>
                      )}
                      {bird.distribution && (
                        <div className="detail-item">
                          <strong>🌍 Distribution:</strong> {bird.distribution}
                        </div>
                      )}
                      {bird.size && (
                        <div className="detail-item">
                          <strong>📏 Size:</strong> {bird.size}
                        </div>
                      )}
                      {bird.diet && (
                        <div className="detail-item">
                          <strong>🍽️ Diet:</strong> {bird.diet}
                        </div>
                      )}
                      {bird.behavior && (
                        <div className="detail-item">
                          <strong>🎭 Behavior:</strong> {bird.behavior}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
            {!birdsLoading && birdsData.filter((bird) => {
              if (!birdsSearchTerm) return true;
              const searchLower = birdsSearchTerm.toLowerCase();
              return (
                bird.common_name?.toLowerCase().includes(searchLower) ||
                bird.scientific_name?.toLowerCase().includes(searchLower)
              );
            }).length === 0 && (
              <div className="no-results">
                <p>🔍 No birds found matching "{birdsSearchTerm}"</p>
                <button onClick={() => setBirdsSearchTerm('')} className="btn btn-secondary">
                  Clear Search
                </button>
              </div>
            )}
          </div>
        )}

        {/* Butterflies Page */}
        {showButterfliesPage && (
          <div className="species-page">
            <div className="species-header">
              <h2>🦋 Butterfly & Moth Species Database</h2>
              <p>Explore {butterfliesData.length} butterfly and moth species with detailed information</p>
              {butterfliesSearchTerm && (
                <p className="search-results-count">
                  Showing {butterfliesData.filter((butterfly) => {
                    const searchLower = butterfliesSearchTerm.toLowerCase();
                    return (
                      butterfly.common_name?.toLowerCase().includes(searchLower) ||
                      butterfly.scientific_name?.toLowerCase().includes(searchLower)
                    );
                  }).length} result(s)
                </p>
              )}
            </div>
            
            {/* Search and Filter */}
            <div className="species-controls">
              <div className="search-box">
                <input
                  type="text"
                  placeholder="🔍 Search butterflies by name or scientific name..."
                  value={butterfliesSearchTerm}
                  onChange={(e) => setButterfliesSearchTerm(e.target.value)}
                  className="search-input"
                />
              </div>
              <div className="sort-box">
                <label>Sort by: </label>
                <select
                  value={butterfliesSortBy}
                  onChange={(e) => setButterfliesSortBy(e.target.value)}
                  className="sort-select"
                >
                  <option value="name">Common Name (A-Z)</option>
                  <option value="scientific">Scientific Name (A-Z)</option>
                  <option value="id">ID (1-100)</option>
                </select>
              </div>
            </div>

            {error && showButterfliesPage && (
              <div className="error-message" style={{ marginBottom: '20px' }}>
                ⚠️ {error}
                <button 
                  onClick={() => {
                    setButterfliesData([]);
                    setButterfliesLoading(false);
                    setError(null);
                  }} 
                  className="btn btn-secondary"
                  style={{ marginLeft: '10px' }}
                >
                  Retry
                </button>
              </div>
            )}
            {butterfliesLoading ? (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Loading butterfly species... Please wait</p>
                <p style={{ fontSize: '0.9rem', color: '#999', marginTop: '10px' }}>
                  Loading {butterfliesData.length > 0 ? butterfliesData.length : '0'} / 100 species
                </p>
              </div>
            ) : (
              <div className="species-grid">
                {butterfliesData
                  .filter((butterfly) => {
                    if (!butterfliesSearchTerm) return true;
                    const searchLower = butterfliesSearchTerm.toLowerCase();
                    return (
                      butterfly.common_name?.toLowerCase().includes(searchLower) ||
                      butterfly.scientific_name?.toLowerCase().includes(searchLower)
                    );
                  })
                  .sort((a, b) => {
                    if (butterfliesSortBy === 'name') {
                      return (a.common_name || '').localeCompare(b.common_name || '');
                    } else if (butterfliesSortBy === 'scientific') {
                      return (a.scientific_name || '').localeCompare(b.scientific_name || '');
                    } else {
                      return (a.id || 0) - (b.id || 0);
                    }
                  })
                  .map((butterfly) => (
                  <div key={butterfly.id} className="species-card">
                    {butterfly.image_path && (
                      <div className="species-image-container">
                        <img 
                          src={`${API_URL}/api/species-image/${encodeURIComponent(butterfly.image_path)}`}
                          alt={butterfly.common_name}
                          className="species-image clickable-image"
                          onClick={() => {
                            setEnlargedImage({
                              url: `${API_URL}/api/species-image/${encodeURIComponent(butterfly.image_path)}`,
                              title: butterfly.common_name,
                              subtitle: butterfly.scientific_name
                            });
                          }}
                          onError={(e) => {
                            const imgUrl = `${API_URL}/api/species-image/${encodeURIComponent(butterfly.image_path)}`;
                            console.error('❌ Image load error:', {
                              imagePath: butterfly.image_path,
                              fullUrl: imgUrl,
                              apiUrl: API_URL,
                              error: e
                            });
                            // 显示错误占位符而不是隐藏
                            e.target.style.display = 'none';
                            const container = e.target.parentElement;
                            if (container && !container.querySelector('.image-error-placeholder')) {
                              const placeholder = document.createElement('div');
                              placeholder.className = 'image-error-placeholder';
                              placeholder.innerHTML = '🖼️<br/>Image not available';
                              placeholder.style.cssText = 'display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #999; font-size: 0.9rem; text-align: center;';
                              container.appendChild(placeholder);
                            }
                          }}
                          onLoad={() => {
                            console.log('✅ Image loaded successfully:', butterfly.image_path);
                          }}
                        />
                      </div>
                    )}
                    <div className="species-card-header">
                      <h3>{butterfly.common_name}</h3>
                      {butterfly.scientific_name && (
                        <p className="scientific-name"><em>{butterfly.scientific_name}</em></p>
                      )}
                    </div>
                    {butterfly.description && (
                      <div className="species-info">
                        <p className="description">{butterfly.description}</p>
                      </div>
                    )}
                    <div className="species-details">
                      {butterfly.habitat && (
                        <div className="detail-item">
                          <strong>📍 Habitat:</strong> {butterfly.habitat}
                        </div>
                      )}
                      {butterfly.distribution && (
                        <div className="detail-item">
                          <strong>🌍 Distribution:</strong> {butterfly.distribution}
                        </div>
                      )}
                      {butterfly.wingspan && (
                        <div className="detail-item">
                          <strong>📏 Wingspan:</strong> {butterfly.wingspan}
                        </div>
                      )}
                      {butterfly.diet && (
                        <div className="detail-item">
                          <strong>🍽️ Diet:</strong> {butterfly.diet}
                        </div>
                      )}
                      {butterfly.behavior && (
                        <div className="detail-item">
                          <strong>🎭 Behavior:</strong> {butterfly.behavior}
                        </div>
                      )}
                      {butterfly.lifecycle && (
                        <div className="detail-item">
                          <strong>🔄 Lifecycle:</strong> {butterfly.lifecycle}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
            {!butterfliesLoading && butterfliesData.filter((butterfly) => {
              if (!butterfliesSearchTerm) return true;
              const searchLower = butterfliesSearchTerm.toLowerCase();
              return (
                butterfly.common_name?.toLowerCase().includes(searchLower) ||
                butterfly.scientific_name?.toLowerCase().includes(searchLower)
              );
            }).length === 0 && (
              <div className="no-results">
                <p>🔍 No butterflies found matching "{butterfliesSearchTerm}"</p>
                <button onClick={() => setButterfliesSearchTerm('')} className="btn btn-secondary">
                  Clear Search
                </button>
              </div>
            )}
          </div>
        )}

        {/* Main Page (Identification) */}
        {!showBirdsPage && !showButterfliesPage && !showDescriptionMode && (
          <>
        <div className="upload-section">
          <div className="upload-area">
            {!preview ? (
              <div className="upload-placeholder">
                <p>📷 Upload an image</p>
                <div className="button-group">
                  <button 
                    className="btn btn-primary" 
                    onClick={() => fileInputRef.current?.click()}
                  >
                    {batchMode ? 'Choose Files' : 'Choose File'}
                  </button>
                  <button 
                    className={`btn ${batchMode ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => {
                      setBatchMode(!batchMode);
                      setSelectedImage(null);
                      setPreview(null);
                      setPrediction(null);
                      setBatchFiles([]);
                      setBatchResults([]);
                      if (fileInputRef.current) {
                        fileInputRef.current.value = '';
                      }
                    }}
                  >
                    {batchMode ? '📷 Single Mode' : '📚 Batch Mode'}
                  </button>
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  multiple={batchMode}
                  onChange={handleImageSelect}
                  style={{ display: 'none' }}
                />
              </div>
            ) : (
              <div className="image-preview">
                <img src={preview} alt="Preview" />
                <div className="preview-actions">
                  <button className="btn btn-primary" onClick={handlePredict} disabled={loading}>
                    {loading ? '🔍 Analyzing...' : '🔍 Identify'}
                  </button>
                  <button className="btn btn-secondary" onClick={handleReset}>
                    Reset
                  </button>
                </div>
              </div>
            )}

            {/* 相机功能已禁用 - 不再显示相机视图 */}

            <canvas ref={canvasRef} style={{ display: 'none' }} />
          </div>

          {batchMode && batchFiles.length > 0 && (
            <div className="batch-section">
              <div className="batch-info">
                <h3>📚 Batch Mode: {batchFiles.length} file(s) selected</h3>
                <button 
                  className="btn btn-primary" 
                  onClick={handleBatchPredict}
                  disabled={batchLoading}
                >
                  {batchLoading ? '🔍 Processing...' : '🔍 Identify All'}
                </button>
              </div>
              {batchResults.length > 0 && (
                <div className="batch-results">
                  <h3>Batch Results ({batchResults.length} processed)</h3>
                  <div className="batch-grid">
                    {batchResults.map((result) => (
                      <div key={result.id} className="batch-item">
                        <img src={result.image} alt={result.filename} />
                        <div className="batch-info-card">
                          <p className="batch-filename">{result.filename}</p>
                          {result.error ? (
                            <p className="batch-error">⚠️ {result.error}</p>
                          ) : (
                            <>
                              <p className="batch-class">{result.prediction.class}</p>
                              <p className="batch-confidence">
                                {(result.prediction.confidence * 100).toFixed(1)}%
                              </p>
                            </>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          {prediction && (
            <div className="prediction-result">
              <div className="result-header">
              <h2>Identification Result</h2>
                <button
                  className={`favorite-btn ${isCurrentFavorite() ? 'favorited' : ''}`}
                  onClick={handleToggleFavorite}
                  title={isCurrentFavorite() ? 'Remove from favorites' : 'Add to favorites'}
                >
                  {isCurrentFavorite() ? '❤️' : '🤍'}
                </button>
              </div>
              
              {/* 顯示警告信息（如果是非蝴蝶/鳥類圖片） */}
              {warning && (
                <div className="warning-card" style={{
                  background: 'linear-gradient(135deg, #FF9800 0%, #FFB74D 100%)',
                  color: 'white',
                  padding: '20px',
                  borderRadius: '12px',
                  marginBottom: '20px',
                  boxShadow: '0 4px 12px rgba(255, 152, 0, 0.3)',
                  border: '2px solid rgba(255, 255, 255, 0.3)'
                }}>
                  <h3 style={{ marginTop: 0, marginBottom: '10px', fontSize: '1.2rem' }}>
                    {warning.title}
                  </h3>
                  <p style={{ marginBottom: '15px', fontSize: '1rem', opacity: 0.95 }}>
                    {warning.message}
                  </p>
                  {warning.suggestions && warning.suggestions.length > 0 && (
                    <div style={{ marginTop: '15px' }}>
                      <strong style={{ display: 'block', marginBottom: '10px' }}>💡 Suggestions:</strong>
                      <ul style={{ margin: 0, paddingLeft: '20px', opacity: 0.95 }}>
                        {warning.suggestions.map((suggestion, idx) => (
                          <li key={idx} style={{ marginBottom: '8px' }}>{suggestion}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <div style={{ marginTop: '15px', fontSize: '0.9rem', opacity: 0.9 }}>
                    <p>Confidence: {(warning.confidence * 100).toFixed(1)}%</p>
                    <p>Top 3 Total Confidence: {(warning.top3_total_confidence * 100).toFixed(1)}%</p>
                  </div>
                </div>
              )}
              
              <div className="result-card">
                <div className="result-main">
                  <span className="result-class">{prediction.class}</span>
                  <span className="result-confidence">
                    {(prediction.confidence * 100).toFixed(2)}% confidence
                  </span>
                </div>
                
                <div className="result-details">
                  <h3>Top Predictions:</h3>
                  <p className="predictions-hint">These are the model's top predictions for this image:</p>
                  <ul>
                    {prediction.top_predictions.map((pred, idx) => (
                      <li key={idx}>
                        <span className="pred-class">{pred.class}</span>
                        <span className="pred-confidence">
                          {(pred.confidence * 100).toFixed(2)}%
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {preview && !prediction && (
            <div className="quality-section">
              <button 
                className="btn btn-secondary"
                onClick={handleAnalyzeQuality}
                disabled={analyzingQuality}
              >
                {analyzingQuality ? '🔍 Analyzing...' : '📊 Analyze Image Quality'}
              </button>
        </div>
          )}

          {qualityAnalysis && (
            <div className="quality-analysis-section">
              <h2>📊 Image Quality Analysis</h2>
              <div className="quality-card">
                <div className="quality-overall">
                  <div className="quality-score">
                    <div className="score-value">{qualityAnalysis.overall_score}</div>
                    <div className="score-label">Overall Quality Score</div>
                    <div className="score-bar">
                      <div 
                        className="score-fill"
                        style={{ 
                          width: `${qualityAnalysis.overall_score}%`,
                          background: qualityAnalysis.overall_score >= 80 ? 'linear-gradient(90deg, #4CAF50 0%, #45a049 100%)' :
                                     qualityAnalysis.overall_score >= 60 ? 'linear-gradient(90deg, #FF9800 0%, #FFB74D 100%)' :
                                     'linear-gradient(90deg, #F44336 0%, #E57373 100%)'
                        }}
                      ></div>
                    </div>
                  </div>
                </div>

                <div className="quality-metrics">
                  <h3>Quality Metrics</h3>
                  <div className="metrics-grid">
                    <div className="metric-item">
                      <div className="metric-header">
                        <span className="metric-name">Brightness</span>
                        <span className={`metric-status ${qualityAnalysis.metrics.brightness.status}`}>
                          {qualityAnalysis.metrics.brightness.status === 'good' ? '✓' : '⚠'}
                        </span>
                      </div>
                      <div className="metric-value">{qualityAnalysis.metrics.brightness.value}%</div>
                      <div className="metric-bar">
                        <div 
                          className="metric-fill"
                          style={{ 
                            width: `${qualityAnalysis.metrics.brightness.score}%`,
                            background: qualityAnalysis.metrics.brightness.status === 'good' ? '#4CAF50' : '#FF9800'
                          }}
                        ></div>
                      </div>
                    </div>

                    <div className="metric-item">
                      <div className="metric-header">
                        <span className="metric-name">Contrast</span>
                        <span className={`metric-status ${qualityAnalysis.metrics.contrast.status}`}>
                          {qualityAnalysis.metrics.contrast.status === 'good' ? '✓' : '⚠'}
                        </span>
                      </div>
                      <div className="metric-value">{qualityAnalysis.metrics.contrast.value}%</div>
                      <div className="metric-bar">
                        <div 
                          className="metric-fill"
                          style={{ 
                            width: `${qualityAnalysis.metrics.contrast.score}%`,
                            background: qualityAnalysis.metrics.contrast.status === 'good' ? '#4CAF50' : '#FF9800'
                          }}
                        ></div>
                      </div>
                    </div>

                    <div className="metric-item">
                      <div className="metric-header">
                        <span className="metric-name">Sharpness</span>
                        <span className={`metric-status ${qualityAnalysis.metrics.sharpness.status}`}>
                          {qualityAnalysis.metrics.sharpness.status === 'good' ? '✓' : '⚠'}
                        </span>
                      </div>
                      <div className="metric-value">{qualityAnalysis.metrics.sharpness.value.toFixed(1)}</div>
                      <div className="metric-bar">
                        <div 
                          className="metric-fill"
                          style={{ 
                            width: `${qualityAnalysis.metrics.sharpness.score}%`,
                            background: qualityAnalysis.metrics.sharpness.status === 'good' ? '#4CAF50' : '#F44336'
                          }}
                        ></div>
                      </div>
                    </div>

                    <div className="metric-item">
                      <div className="metric-header">
                        <span className="metric-name">Saturation</span>
                        <span className={`metric-status ${qualityAnalysis.metrics.saturation.status}`}>
                          {qualityAnalysis.metrics.saturation.status === 'good' ? '✓' : '○'}
                        </span>
                      </div>
                      <div className="metric-value">{qualityAnalysis.metrics.saturation.value}%</div>
                      <div className="metric-bar">
                        <div 
                          className="metric-fill"
                          style={{ 
                            width: `${qualityAnalysis.metrics.saturation.score}%`,
                            background: '#4CAF50'
                          }}
                        ></div>
                      </div>
                    </div>

                    <div className="metric-item">
                      <div className="metric-header">
                        <span className="metric-name">Resolution</span>
                        <span className={`metric-status ${qualityAnalysis.metrics.resolution.status}`}>
                          {qualityAnalysis.metrics.resolution.status === 'good' ? '✓' : '○'}
                        </span>
                      </div>
                      <div className="metric-value">
                        {qualityAnalysis.metrics.resolution.width} × {qualityAnalysis.metrics.resolution.height}
                      </div>
                      <div className="metric-bar">
                        <div 
                          className="metric-fill"
                          style={{ 
                            width: `${qualityAnalysis.metrics.resolution.score}%`,
                            background: '#4CAF50'
                          }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="quality-recommendations">
                  <h3>💡 Recommendations</h3>
                  <div className="recommendations-list">
                    {qualityAnalysis.recommendations.map((rec, idx) => (
                      <div key={idx} className={`recommendation-item ${rec.severity}`}>
                        <div className="recommendation-icon">
                          {rec.severity === 'high' ? '⚠️' : rec.severity === 'medium' ? '⚡' : rec.severity === 'low' ? '💡' : '✓'}
                        </div>
                        <div className="recommendation-content">
                          <div className="recommendation-message">{rec.message}</div>
                          <div className="recommendation-suggestion">{rec.suggestion}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Favorites Tab */}
        {showFavorites && (
          <div className="favorites-section">
            <div className="history-header">
              <h2>My Favorites</h2>
              {favorites.length > 0 && (
                <div className="header-actions">
                  <div className="export-dropdown" ref={favoritesExportRef}>
                    <button 
                      className="btn btn-secondary export-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        setShowFavoritesExportMenu(!showFavoritesExportMenu);
                      }}
                    >
                      💾 Export
                    </button>
                    <div className={`export-menu ${showFavoritesExportMenu ? 'show' : ''}`}>
                      <button 
                        onClick={(e) => {
                          e.stopPropagation();
                          exportFavoritesToCSV();
                          setShowFavoritesExportMenu(false);
                        }} 
                        className="export-option"
                      >
                        📄 Export as CSV
                      </button>
                      <button 
                        onClick={(e) => {
                          e.stopPropagation();
                          exportFavoritesToJSON();
                          setShowFavoritesExportMenu(false);
                        }} 
                        className="export-option"
                      >
                        📋 Export as JSON (with images)
                      </button>
                    </div>
                  </div>
                  <button 
                    className="btn btn-secondary"
                    onClick={() => {
                      if (window.confirm('Are you sure you want to clear all favorites?')) {
                        setFavorites([]);
                        localStorage.setItem('favorites', JSON.stringify([]));
                      }
                    }}
                  >
                    🗑️ Clear All
                  </button>
                </div>
              )}
            </div>
            
            {favorites.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">❤️</div>
                <h3>No Favorites Yet</h3>
                <p>Start identifying species and click the heart icon to add them to your favorites!</p>
              </div>
            ) : (
              <div className="history-grid">
                {favorites.map((item) => {
                  const imageSrc = item.image || item.imageBase64;
                  return (
                    <div key={item.id} className="history-item favorite-item">
                      {imageSrc ? (
                        <img 
                          src={imageSrc} 
                          alt="Favorite" 
                          onError={(e) => {
                            console.error('Image load error for favorite:', item.id);
                            console.error('Image type:', imageSrc?.substring(0, 50));
                            // Hide broken image and show placeholder
                            e.target.style.display = 'none';
                            const placeholder = e.target.nextElementSibling;
                            if (placeholder) {
                              placeholder.style.display = 'block';
                            }
                          }}
                        />
                      ) : null}
                      <div 
                        className="image-placeholder" 
                        style={{ 
                          display: imageSrc ? 'none' : 'flex',
                          width: '100%',
                          height: '150px',
                          backgroundColor: '#f0f0f0',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: '#999',
                          fontSize: '0.9rem'
                        }}
                      >
                        Image not available
                      </div>
                      <div className="history-info">
                        <p className="history-class">{item.prediction.class}</p>
                        <p className="history-confidence">
                          {(item.prediction.confidence * 100).toFixed(2)}% confidence
                        </p>
                        <p className="history-time">{item.timestamp}</p>
                        <button
                          className="remove-favorite-btn"
                          onClick={() => handleRemoveFavorite(item.id)}
                          title="Remove from favorites"
                        >
                          ❌ Remove
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* Tabs for switching between History and Favorites */}
        {(history.length > 0 || favorites.length > 0) && (
          <div className="main-tabs">
            <button
              className={`tab-btn ${!showFavorites ? 'active' : ''}`}
              onClick={() => setShowFavorites(false)}
            >
              📋 Recent Identifications
            </button>
            <button
              className={`tab-btn ${showFavorites ? 'active' : ''}`}
              onClick={() => setShowFavorites(true)}
            >
              ❤️ Favorites ({favorites.length})
            </button>
          </div>
        )}

        {/* Recent Identifications Tab */}
        {!showFavorites && history.length > 0 && (
          <div className="history-section">
            <div className="history-header">
            <h2>Recent Identifications</h2>
              <div className="header-actions">
                <div className="export-dropdown" ref={historyExportRef}>
                  <button 
                    className="btn btn-secondary export-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowHistoryExportMenu(!showHistoryExportMenu);
                    }}
                  >
                    💾 Export
                  </button>
                  <div className={`export-menu ${showHistoryExportMenu ? 'show' : ''}`}>
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        exportHistoryToCSV();
                        setShowHistoryExportMenu(false);
                      }} 
                      className="export-option"
                    >
                      📄 Export as CSV
                    </button>
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        exportHistoryToJSON();
                        setShowHistoryExportMenu(false);
                      }} 
                      className="export-option"
                    >
                      📋 Export as JSON (with images)
                    </button>
                  </div>
                </div>
                <button 
                  className="btn btn-primary"
                  onClick={handleLoadStatistics}
                  disabled={statsLoading}
                >
                  {statsLoading ? 'Loading...' : '📊 View Statistics'}
                </button>
              </div>
            </div>
            
            {showStatistics && statistics && (
              <div className="statistics-section">
                <div className="statistics-header">
                  <h3>📊 Identification Statistics</h3>
                  <button 
                    className="btn btn-secondary"
                    onClick={exportStatisticsToPDF}
                    title="Export statistics as PDF"
                  >
                    📄 Export PDF
                  </button>
                </div>
                
                <div className="stats-grid">
                  <div className="stat-card">
                    <div className="stat-value">{statistics.total_identifications}</div>
                    <div className="stat-label">Total Identifications</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{statistics.unique_species}</div>
                    <div className="stat-label">Unique Species</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{statistics.average_confidence.toFixed(1)}%</div>
                    <div className="stat-label">Avg Confidence</div>
                  </div>
                </div>

                <div className="stats-charts">
                  <div className="chart-container">
                    <h4>Top 10 Identified Species</h4>
                    <div className="bar-chart">
                      {statistics.top_species.map((item, idx) => (
                        <div key={idx} className="bar-item">
                          <div className="bar-label">{item.species.replace(/^\d+\./, '').substring(0, 30)}</div>
                          <div className="bar-wrapper">
                            <div 
                              className="bar-fill" 
                              style={{ 
                                width: `${(item.count / statistics.top_species[0].count) * 100}%`,
                                background: `linear-gradient(90deg, #4CAF50 0%, #45a049 100%)`
                              }}
                            >
                              <span className="bar-value">{item.count}</span>
                            </div>
                          </div>
                          <div className="bar-confidence">{item.avg_confidence.toFixed(1)}%</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="chart-container">
                    <h4>Confidence Distribution</h4>
                    <div className="pie-chart-container">
                      <div className="pie-chart">
                        <div 
                          className="pie-segment high"
                          style={{ 
                            '--percentage': (statistics.confidence_distribution.high / statistics.total_identifications * 100)
                          }}
                        >
                          <span>High (≥90%)</span>
                          <span>{statistics.confidence_distribution.high}</span>
                        </div>
                        <div 
                          className="pie-segment medium"
                          style={{ 
                            '--percentage': (statistics.confidence_distribution.medium / statistics.total_identifications * 100)
                          }}
                        >
                          <span>Medium (70-90%)</span>
                          <span>{statistics.confidence_distribution.medium}</span>
                        </div>
                        <div 
                          className="pie-segment low"
                          style={{ 
                            '--percentage': (statistics.confidence_distribution.low / statistics.total_identifications * 100)
                          }}
                        >
                          <span>Low (&lt;70%)</span>
                          <span>{statistics.confidence_distribution.low}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="chart-container">
                    <h4>Category Distribution</h4>
                    <div className="category-chart">
                      <div className="category-item">
                        <div className="category-icon">🐦</div>
                        <div className="category-info">
                          <div className="category-label">Birds</div>
                          <div className="category-bar">
                            <div 
                              className="category-fill"
                              style={{ 
                                width: `${(statistics.category_distribution.birds / statistics.total_identifications) * 100}%`,
                                background: '#4CAF50'
                              }}
                            >
                              {statistics.category_distribution.birds}
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="category-item">
                        <div className="category-icon">🦋</div>
                        <div className="category-info">
                          <div className="category-label">Butterflies</div>
                          <div className="category-bar">
                            <div 
                              className="category-fill"
                              style={{ 
                                width: `${(statistics.category_distribution.butterflies / statistics.total_identifications) * 100}%`,
                                background: '#FF9800'
                              }}
                            >
                              {statistics.category_distribution.butterflies}
                            </div>
                          </div>
                        </div>
                      </div>
                      {statistics.category_distribution.others > 0 && (
                        <div className="category-item">
                          <div className="category-icon">❓</div>
                          <div className="category-info">
                            <div className="category-label">Others</div>
                            <div className="category-bar">
                              <div 
                                className="category-fill"
                                style={{ 
                                  width: `${(statistics.category_distribution.others / statistics.total_identifications) * 100}%`,
                                  background: '#9E9E9E'
                                }}
                              >
                                {statistics.category_distribution.others}
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="history-grid">
              {history.map((item) => (
                <div key={item.id} className="history-item">
                  <img src={item.image} alt="History" />
                  <div className="history-info">
                    <p className="history-class">{item.prediction.class}</p>
                    <p className="history-confidence">
                      {(item.prediction.confidence * 100).toFixed(1)}%
                    </p>
                    <p className="history-time">{item.timestamp}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
          </>
        )}
      </main>

      {/* AI Chat Assistant */}
      <div className={`chat-container ${chatOpen ? 'chat-open' : ''}`}>
        <button 
          className="chat-toggle-btn"
          onClick={() => setChatOpen(!chatOpen)}
        >
          {chatOpen ? '✕' : '💬 AI Assistant'}
        </button>
        
        {chatOpen && (
          <div className="chat-window">
            <div className="chat-header">
              <h3>🤖 AI Assistant</h3>
              <p>Ask me about species, identification tips, and more! (English/中文)</p>
            </div>
            
            <div className="chat-messages">
              {chatMessages.map((msg) => (
                <div key={msg.id} className={`chat-message ${msg.type}`}>
                  <div className="message-content">
                    <p>{msg.text}</p>
                    <span className="message-time">{msg.timestamp}</span>
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div className="chat-message bot">
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div className="chat-input-area">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={handleChatKeyPress}
                placeholder="Ask me anything (English/中文)..."
                disabled={chatLoading}
              />
              <button 
                onClick={handleChatSend}
                disabled={chatLoading || !chatInput.trim()}
                className="chat-send-btn"
              >
                Send
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Scroll to Top Button - Always visible in bottom left */}
      <button
        className="scroll-to-top-btn"
        onClick={scrollToTop}
        title="回到顶部 (Scroll to Top)"
        aria-label="回到顶部"
      >
        ↑
      </button>

      {/* Species Detail Modal */}
      {showSpeciesModal && selectedSpeciesDetail && (
        <div className="species-modal-overlay" onClick={handleCloseSpeciesModal}>
          <div className="species-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close-btn" onClick={handleCloseSpeciesModal}>×</button>
            
            <div className="species-modal-content">
              {/* Species Image */}
              {selectedSpeciesDetail.image_path && (
                <div className="species-modal-image">
                  <img 
                    src={`${API_URL}/api/species-image/${encodeURIComponent(selectedSpeciesDetail.image_path)}`}
                    alt={selectedSpeciesDetail.common_name}
                    onError={(e) => { e.target.src = 'https://via.placeholder.com/400x300?text=No+Image'; }}
                  />
                </div>
              )}
              
              {/* Species Info */}
              <div className="species-modal-info">
                <h2>{selectedSpeciesDetail.common_name}</h2>
                <p className="species-scientific-name">
                  <em>{selectedSpeciesDetail.scientific_name}</em>
                </p>
                
                <span className={`species-category-badge ${selectedSpeciesDetail.category?.toLowerCase().replace('/', '-')}`}>
                  {selectedSpeciesDetail.category}
                </span>
                
                {selectedSpeciesDetail.confidence_score && (
                  <div className="species-confidence">
                    <strong>Match Confidence:</strong> {(selectedSpeciesDetail.confidence_score * 100).toFixed(0)}%
                  </div>
                )}
                
                <div className="species-details-grid">
                  {selectedSpeciesDetail.description && (
                    <div className="detail-item">
                      <h4>📝 Description</h4>
                      <p>{selectedSpeciesDetail.description}</p>
                    </div>
                  )}
                  
                  {selectedSpeciesDetail.habitat && (
                    <div className="detail-item">
                      <h4>🏠 Habitat</h4>
                      <p>{selectedSpeciesDetail.habitat}</p>
                    </div>
                  )}
                  
                  {selectedSpeciesDetail.distribution && (
                    <div className="detail-item">
                      <h4>🌍 Distribution</h4>
                      <p>{selectedSpeciesDetail.distribution}</p>
                    </div>
                  )}
                  
                  {selectedSpeciesDetail.size && (
                    <div className="detail-item">
                      <h4>📏 Size</h4>
                      <p>{selectedSpeciesDetail.size}</p>
                    </div>
                  )}
                  
                  {selectedSpeciesDetail.behavior && (
                    <div className="detail-item">
                      <h4>🦅 Behavior</h4>
                      <p>{selectedSpeciesDetail.behavior}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Image Enlargement Modal */}
      {enlargedImage && (
        <div 
          className="image-modal-overlay"
          onClick={() => setEnlargedImage(null)}
        >
          <div 
            className="image-modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              className="image-modal-close"
              onClick={() => setEnlargedImage(null)}
              aria-label="Close"
            >
              ✕
            </button>
            <div className="image-modal-header">
              <h3>{enlargedImage.title}</h3>
              {enlargedImage.subtitle && (
                <p className="image-modal-subtitle"><em>{enlargedImage.subtitle}</em></p>
              )}
            </div>
            <div className="image-modal-image-container">
              <img 
                src={enlargedImage.url} 
                alt={enlargedImage.title}
                className="image-modal-image"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;


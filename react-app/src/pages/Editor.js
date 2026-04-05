import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, CircularProgress, Alert, Slider, Switch, FormControlLabel } from '@mui/material';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const Editor = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Safely extract videoData from location state
  let initialVideoData = null;
  try {
    initialVideoData = location.state?.videoData;
    // Ensure videoData is a valid object with expected properties
    if (initialVideoData && (typeof initialVideoData !== 'object' || Array.isArray(initialVideoData))) {
      initialVideoData = null;
    }
  } catch (e) {
    initialVideoData = null;
  }
  
  const [videoData] = useState(initialVideoData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [processingProgress, setProcessingProgress] = useState(0);
  const [features, setFeatures] = useState({
    textDetection: true,
    faceDetection: true,
    objectDetection: true,
    brightness: 100,
    contrast: 100,
    saturation: 100
  });

  useEffect(() => {
    if (!videoData || !videoData.video_id) {
      navigate('/upload');
    }
  }, [videoData, navigate]);

  const handleFeatureToggle = (feature) => {
    setFeatures(prev => ({
      ...prev,
      [feature]: !prev[feature]
    }));
  };

  const handleSliderChange = (feature, value) => {
    setFeatures(prev => ({
      ...prev,
      [feature]: value
    }));
  };

  const handleProcess = async () => {
    try {
      setLoading(true);
      setError(null);

      // Simulate processing progress
      const progressInterval = setInterval(() => {
        setProcessingProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + Math.random() * 30;
        });
      }, 500);

      const response = await axios.post(`${API_URL}/process`, null, {
        params: { video_id: videoData.video_id }
      });

      clearInterval(progressInterval);
      setProcessingProgress(100);
      setLoading(false);

      navigate('/results', { state: { videoData, processedData: response.data } });
    } catch (err) {
      let errorMessage = 'Processing failed. Please try again.';
      
      if (err.response?.data?.detail) {
        errorMessage = typeof err.response.data.detail === 'string'
          ? err.response.data.detail
          : 'Processing failed. Please check the server logs.';
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      setLoading(false);
      setProcessingProgress(0);
    }
  };

  if (!videoData) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <CircularProgress />
        <Typography sx={{ mt: 2, color: 'white' }}>Loading...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 4, color: 'white', textAlign: 'center' }}>
        Edit & Process Video
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <Box sx={{
        display: 'grid',
        gridTemplateColumns: { xs: '1fr', md: '2fr 1fr' },
        gap: 3,
        mb: 4
      }}>
        {/* Video Preview */}
        <Box sx={{
          background: 'rgba(255,255,255,0.05)',
          borderRadius: 2,
          padding: 2,
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255,255,255,0.1)'
        }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: 'white' }}>
            📹 Video Preview
          </Typography>
          <Box sx={{
            background: '#000',
            borderRadius: 2,
            padding: 2,
            aspectRatio: '16/9',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#999'
          }}>
            <Typography>Video Preview - {videoData.filename}</Typography>
          </Box>
        </Box>

        {/* Processing Features */}
        <Box sx={{
          background: 'rgba(255,255,255,0.05)',
          borderRadius: 2,
          padding: 2,
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255,255,255,0.1)'
        }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: 'white' }}>
            🤖 AI Features
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={features.textDetection}
                  onChange={() => handleFeatureToggle('textDetection')}
                  sx={{ color: '#667eea' }}
                />
              }
              label={<span style={{ color: 'white' }}>Text Detection</span>}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={features.faceDetection}
                  onChange={() => handleFeatureToggle('faceDetection')}
                  sx={{ color: '#667eea' }}
                />
              }
              label={<span style={{ color: 'white' }}>Face Detection</span>}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={features.objectDetection}
                  onChange={() => handleFeatureToggle('objectDetection')}
                  sx={{ color: '#667eea' }}
                />
              }
              label={<span style={{ color: 'white' }}>Object Detection</span>}
            />
          </Box>
        </Box>
      </Box>

      {/* Adjustment Sliders */}
      <Box sx={{
        background: 'rgba(255,255,255,0.05)',
        borderRadius: 2,
        padding: 3,
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255,255,255,0.1)',
        mb: 4
      }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3, color: 'white' }}>
          ⚙️ Adjustments
        </Typography>

        <Box sx={{ mb: 3 }}>
          <Typography variant="body2" sx={{ color: '#ddd', mb: 1, display: 'flex', justifyContent: 'space-between' }}>
            <span>Brightness</span>
            <span>{features.brightness}%</span>
          </Typography>
          <Slider
            value={features.brightness}
            onChange={(e, newValue) => handleSliderChange('brightness', newValue)}
            min={50}
            max={150}
            sx={{ color: '#667eea' }}
          />
        </Box>

        <Box sx={{ mb: 3 }}>
          <Typography variant="body2" sx={{ color: '#ddd', mb: 1, display: 'flex', justifyContent: 'space-between' }}>
            <span>Contrast</span>
            <span>{features.contrast}%</span>
          </Typography>
          <Slider
            value={features.contrast}
            onChange={(e, newValue) => handleSliderChange('contrast', newValue)}
            min={50}
            max={150}
            sx={{ color: '#667eea' }}
          />
        </Box>

        <Box>
          <Typography variant="body2" sx={{ color: '#ddd', mb: 1, display: 'flex', justifyContent: 'space-between' }}>
            <span>Saturation</span>
            <span>{features.saturation}%</span>
          </Typography>
          <Slider
            value={features.saturation}
            onChange={(e, newValue) => handleSliderChange('saturation', newValue)}
            min={0}
            max={150}
            sx={{ color: '#667eea' }}
          />
        </Box>
      </Box>

      {/* Processing Progress */}
      {processingProgress > 0 && processingProgress < 100 && (
        <Box sx={{
          background: 'rgba(255,255,255,0.05)',
          borderRadius: 2,
          padding: 3,
          mb: 4,
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255,255,255,0.1)'
        }}>
          <Typography variant="body2" sx={{ color: 'white', mb: 2 }}>
            Processing your video...
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <CircularProgress variant="determinate" value={processingProgress} />
            <Typography sx={{ color: 'white', fontWeight: 'bold' }}>
              {Math.round(processingProgress)}% Complete
            </Typography>
          </Box>
        </Box>
      )}

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
        <Button
          variant="contained"
          onClick={handleProcess}
          disabled={loading}
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            fontWeight: 'bold',
            px: 4,
            py: 1.5,
            display: 'flex',
            alignItems: 'center',
            gap: 1
          }}
        >
          {loading ? (
            <>
              <CircularProgress size={24} sx={{ color: 'white' }} />
              Processing...
            </>
          ) : (
            '⚡ Process Video'
          )}
        </Button>
        <Button
          variant="outlined"
          onClick={() => navigate('/upload')}
          sx={{
            color: 'white',
            borderColor: 'white',
            fontWeight: 'bold',
            px: 4,
            py: 1.5,
            '&:hover': {
              borderColor: 'white',
              background: 'rgba(255,255,255,0.1)'
            }
          }}
        >
          ← Back to Upload
        </Button>
      </Box>
    </Box>
  );
};

export default Editor;

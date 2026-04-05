import React, { useCallback, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, Button, CircularProgress, Alert } from '@mui/material';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const Upload = ({ onVideoData }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [file, setFile] = useState(null);

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      const uploadedFile = acceptedFiles[0];
      setFile(uploadedFile);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    }
  });

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a video file');
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        }
      });

      onVideoData(response.data);
      setLoading(false);
      navigate('/editor', { state: { videoData: response.data } });
    } catch (err) {
      let errorMessage = 'Upload failed. Please try again.';
      
      // Safely extract error message
      if (err.response?.data?.detail) {
        errorMessage = typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : 'Upload failed. Please check the server logs.';
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      setLoading(false);
      setUploadProgress(0);
    }
  };

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 4, color: 'white', textAlign: 'center' }}>
        Upload Your Video
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Box
        {...getRootProps()}
        sx={{
          border: '3px dashed #667eea',
          borderRadius: 3,
          padding: '60px 40px',
          textAlign: 'center',
          background: isDragActive ? 'rgba(102, 126, 234, 0.2)' : 'rgba(255, 255, 255, 0.1)',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          color: 'white',
          mb: 4,
          '&:hover': {
            borderColor: '#764ba2',
            background: 'rgba(255, 255, 255, 0.2)'
          }
        }}
      >
        <input {...getInputProps()} />
        <Typography variant="h5" sx={{ mb: 2 }}>
          {isDragActive ? '📥 Drop your video here' : '📤 Drag & drop your video here'}
        </Typography>
        <Typography variant="body1" sx={{ opacity: 0.8 }}>
          or click to select from your computer
        </Typography>
        <Typography variant="caption" sx={{ display: 'block', mt: 2, opacity: 0.6 }}>
          Supported formats: MP4, MOV, AVI, MKV, WebM (Max 512MB)
        </Typography>
      </Box>

      {file && (
        <Box sx={{
          background: 'white',
          padding: 3,
          borderRadius: 2,
          mb: 4,
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
        }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
            Selected File:
          </Typography>
          <Typography variant="body1" sx={{ color: '#667eea', fontWeight: 'bold', mb: 2 }}>
            📁 {file.name}
          </Typography>
          <Typography variant="body2" sx={{ color: '#666', mb: 3 }}>
            Size: {(file.size / (1024 * 1024)).toFixed(2)} MB
          </Typography>

          {uploadProgress > 0 && uploadProgress < 100 && (
            <Box sx={{ mb: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <CircularProgress variant="determinate" value={uploadProgress} size={24} />
                <Typography sx={{ ml: 2, fontWeight: 'bold' }}>
                  {uploadProgress}% Complete
                </Typography>
              </Box>
              <Box sx={{
                background: '#e0e0e0',
                height: 4,
                borderRadius: 2,
                overflow: 'hidden'
              }}>
                <Box sx={{
                  background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                  height: '100%',
                  width: `${uploadProgress}%`,
                  transition: 'width 0.3s ease'
                }} />
              </Box>
            </Box>
          )}

          <Button
            variant="contained"
            fullWidth
            onClick={handleUpload}
            disabled={loading}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              fontWeight: 'bold',
              py: 1.5,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 1
            }}
          >
            {loading ? (
              <>
                <CircularProgress size={24} sx={{ color: 'white' }} />
                Uploading...
              </>
            ) : (
              '⬆️ Upload Video'
            )}
          </Button>
        </Box>
      )}

      <Box sx={{
        background: 'rgba(255,255,255,0.1)',
        padding: 3,
        borderRadius: 2,
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255,255,255,0.2)',
        color: 'white'
      }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
          💡 Tips for Best Results:
        </Typography>
        <ul style={{ lineHeight: 2 }}>
          <li>Use high-quality videos (1080p or higher recommended)</li>
          <li>Ensure good lighting for better face and object detection</li>
          <li>Clear audio helps with text detection accuracy</li>
          <li>Files up to 512MB are supported</li>
        </ul>
      </Box>
    </Box>
  );
};

export default Upload;

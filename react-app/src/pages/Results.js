import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, Card, CardContent, Grid, Tabs, Tab } from '@mui/material';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [downloading, setDownloading] = useState(false);
  
  // Safely extract data
  let videoData = null;
  let processedData = null;
  
  try {
    videoData = location.state?.videoData;
    processedData = location.state?.processedData;
    
    // Validate that these are objects and not errors
    if (videoData && (typeof videoData !== 'object' || Array.isArray(videoData))) {
      videoData = null;
    }
    if (processedData && (typeof processedData !== 'object' || Array.isArray(processedData))) {
      processedData = null;
    }
  } catch (e) {
    console.error('Error extracting results data:', e);
  }

  if (!videoData || !processedData) {
    return (
      <Box sx={{ textAlign: 'center', py: 8, color: 'white' }}>
        <Typography variant="h5">No results to display</Typography>
        <Button onClick={() => navigate('/upload')} sx={{ mt: 2 }}>
          Upload Video
        </Button>
      </Box>
    );
  }

  const detections = processedData?.detections || {};

  const handleDownload = async () => {
    try {
      setDownloading(true);
      const response = await axios.get(`${API_URL.replace('/api', '')}/download/${processedData.output_file}`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', processedData.output_file);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      setDownloading(false);
    } catch (error) {
      console.error('Download failed:', error);
      setDownloading(false);
    }
  };

  const DetectionCard = ({ title, data, count }) => (
    <Card sx={{
      background: 'rgba(255,255,255,0.05)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255,255,255,0.1)',
      height: '100%'
    }}>
      <CardContent>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: '#667eea' }}>
          {title}
        </Typography>
        <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 3, color: 'white' }}>
          {count || 0}
        </Typography>
        {data && Array.isArray(data) && data.length > 0 && (
          <Box>
            {data.slice(0, 5).map((item, idx) => (
              <Typography key={idx} variant="caption" sx={{ display: 'block', color: '#ddd', mb: 0.5 }}>
                • {typeof item === 'string' ? item : JSON.stringify(item).substring(0, 30)}...
              </Typography>
            ))}
            {data.length > 5 && (
              <Typography variant="caption" sx={{ color: '#999' }}>
                +{data.length - 5} more
              </Typography>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1, color: 'white', textAlign: 'center' }}>
        ✅ Processing Complete!
      </Typography>
      <Typography variant="body1" sx={{ mb: 4, color: '#ddd', textAlign: 'center' }}>
        Your video has been successfully processed with AI analysis
      </Typography>

      {/* Tabs */}
      <Box sx={{
        background: 'rgba(255,255,255,0.05)',
        borderRadius: 2,
        mb: 4,
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255,255,255,0.1)'
      }}>
        <Tabs
          value={tabValue}
          onChange={(e, newValue) => setTabValue(newValue)}
          sx={{
            borderBottom: '1px solid rgba(255,255,255,0.1)',
            '& .MuiTab-root': {
              color: '#ddd',
              '&.Mui-selected': {
                color: '#667eea'
              }
            }
          }}
        >
          <Tab label="Summary" />
          <Tab label="Detections" />
          <Tab label="Export" />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {tabValue === 0 && (
            // Summary Tab
            <Box>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12} sm={6}>
                  <Card sx={{
                    background: 'rgba(102, 126, 234, 0.1)',
                    border: '1px solid #667eea'
                  }}>
                    <CardContent>
                      <Typography variant="caption" sx={{ color: '#999' }}>
                        Video File
                      </Typography>
                      <Typography variant="body1" sx={{ color: 'white', fontWeight: 'bold', mt: 1 }}>
                        {videoData.filename}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Card sx={{
                    background: 'rgba(102, 126, 234, 0.1)',
                    border: '1px solid #667eea'
                  }}>
                    <CardContent>
                      <Typography variant="caption" sx={{ color: '#999' }}>
                        File Size
                      </Typography>
                      <Typography variant="body1" sx={{ color: 'white', fontWeight: 'bold', mt: 1 }}>
                        {videoData.size_mb?.toFixed(2)} MB
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>

              <Card sx={{
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)'
              }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: '#667eea' }}>
                    Processing Status
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <Box sx={{
                      width: 12,
                      height: 12,
                      borderRadius: '50%',
                      background: '#4caf50'
                    }} />
                    <Typography sx={{ color: 'white' }}>
                      Successfully processed with AI analysis enabled
                    </Typography>
                  </Box>
                  <Typography variant="body2" sx={{ color: '#999' }}>
                    Detections: Text Recognition • Face Detection • Object Recognition
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          )}

          {tabValue === 1 && (
            // Detections Tab
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={4}>
                <DetectionCard
                  title="🔍 Text Detected"
                  data={detections.text}
                  count={Array.isArray(detections.text) ? detections.text.length : 0}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={4}>
                <DetectionCard
                  title="😊 Faces Found"
                  data={detections.faces}
                  count={Array.isArray(detections.faces) ? detections.faces.length : 0}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={4}>
                <DetectionCard
                  title="🎯 Objects Detected"
                  data={detections.objects}
                  count={Array.isArray(detections.objects) ? detections.objects.length : 0}
                />
              </Grid>
            </Grid>
          )}

          {tabValue === 2 && (
            // Export Tab
            <Box>
              <Card sx={{
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)',
                mb: 3
              }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: '#667eea' }}>
                    📥 Download Your Video
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#ddd', mb: 3 }}>
                    Your processed video is ready to download. Choose your preferred format.
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Button
                      variant="contained"
                      onClick={handleDownload}
                      disabled={downloading}
                      sx={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        color: 'white',
                        fontWeight: 'bold'
                      }}
                    >
                      {downloading ? 'Downloading...' : '⬇️ MP4 Format'}
                    </Button>
                    <Button
                      variant="outlined"
                      sx={{
                        color: 'white',
                        borderColor: 'white',
                        '&:hover': {
                          background: 'rgba(255,255,255,0.1)'
                        }
                      }}
                    >
                      MOV Format
                    </Button>
                    <Button
                      variant="outlined"
                      sx={{
                        color: 'white',
                        borderColor: 'white',
                        '&:hover': {
                          background: 'rgba(255,255,255,0.1)'
                        }
                      }}
                    >
                      WebM Format
                    </Button>
                  </Box>
                </CardContent>
              </Card>

              <Card sx={{
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)'
              }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: '#667eea' }}>
                    📊 Video Details
                  </Typography>
                  <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
                    <Box>
                      <Typography variant="caption" sx={{ color: '#999' }}>Codec</Typography>
                      <Typography sx={{ color: 'white' }}>H.264</Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" sx={{ color: '#999' }}>Resolution</Typography>
                      <Typography sx={{ color: 'white' }}>1920x1080</Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" sx={{ color: '#999' }}>Frame Rate</Typography>
                      <Typography sx={{ color: 'white' }}>30 FPS</Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" sx={{ color: '#999' }}>Duration</Typography>
                      <Typography sx={{ color: 'white' }}>~2 minutes</Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          )}
        </Box>
      </Box>

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
        <Button
          variant="contained"
          onClick={() => navigate('/upload')}
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            fontWeight: 'bold',
            px: 4,
            py: 1.5
          }}
        >
          ⬆️ Upload Another Video
        </Button>
        <Button
          variant="outlined"
          href="http://localhost:8000/docs"
          target="_blank"
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
          📖 API Docs
        </Button>
      </Box>
    </Box>
  );
};

export default Results;

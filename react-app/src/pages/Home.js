import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Button, Grid, Card, CardContent } from '@mui/material';

const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: '🎥 Video Upload',
      description: 'Upload your video in any format (MP4, MOV, AVI, MKV, WebM)'
    },
    {
      title: '🤖 AI Processing',
      description: 'Advanced AI algorithms analyze and enhance your videos'
    },
    {
      title: '🔍 Text Detection',
      description: 'Automatically detect and extract text from videos'
    },
    {
      title: '😊 Face Recognition',
      description: 'Identify and track faces in your footage'
    },
    {
      title: '🎯 Object Detection',
      description: 'Recognize and track objects throughout your video'
    },
    {
      title: '📥 Quick Export',
      description: 'Download your processed video in minutes'
    }
  ];

  return (
    <Box sx={{ py: 4 }}>
      {/* Hero Section */}
      <Box sx={{
        textAlign: 'center',
        color: 'white',
        mb: 6,
        animation: 'slideDown 0.6s ease-out'
      }}>
        <Typography variant="h2" sx={{ fontWeight: 'bold', mb: 2, textShadow: '2px 2px 4px rgba(0,0,0,0.3)' }}>
          🎬 AI Video Editor
        </Typography>
        <Typography variant="h5" sx={{ mb: 4, opacity: 0.9 }}>
          Professional video editing powered by artificial intelligence
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/upload')}
            sx={{
              background: 'white',
              color: '#667eea',
              fontWeight: 'bold',
              px: 4,
              py: 1.5,
              '&:hover': {
                background: '#f0f0f0'
              }
            }}
          >
            Get Started
          </Button>
          <Button
            variant="outlined"
            size="large"
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
            API Documentation
          </Button>
        </Box>
      </Box>

      {/* Features Grid */}
      <Grid container spacing={3} sx={{ mb: 6 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card sx={{
              background: 'rgba(255,255,255,0.95)',
              backdropFilter: 'blur(10px)',
              boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'translateY(-5px)',
                boxShadow: '0 12px 40px rgba(0,0,0,0.15)'
              }
            }}>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1, color: '#667eea' }}>
                  {feature.title}
                </Typography>
                <Typography variant="body2" sx={{ color: '#666', lineHeight: 1.6 }}>
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* CTA Section */}
      <Box sx={{
        background: 'white',
        padding: 4,
        borderRadius: 3,
        textAlign: 'center',
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)'
      }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 2, color: '#333' }}>
          Ready to Transform Your Videos?
        </Typography>
        <Typography variant="body1" sx={{ mb: 3, color: '#666' }}>
          Upload a video and experience the power of AI-powered video editing
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/upload')}
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            fontWeight: 'bold',
            px: 4,
            py: 1.5
          }}
        >
          Upload Video Now
        </Button>
      </Box>
    </Box>
  );
};

export default Home;

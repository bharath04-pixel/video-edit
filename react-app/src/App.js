import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container, AppBar, Toolbar, Button, Box } from '@mui/material';
import './index.css';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Editor from './pages/Editor';
import Results from './pages/Results';

function App() {
  const [videoData, setVideoData] = useState(null);

  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static" sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <Toolbar>
            <Box sx={{ flexGrow: 1 }}>
              <a href="/" style={{ color: 'white', textDecoration: 'none', fontSize: '1.5em', fontWeight: 'bold' }}>
                🎬 AI Video Editor
              </a>
            </Box>
            <Button color="inherit" href="/">Home</Button>
            <Button color="inherit" href="/upload">Upload</Button>
            <Button color="inherit" href="http://localhost:8000/docs" target="_blank">API Docs</Button>
          </Toolbar>
        </AppBar>

        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload onVideoData={setVideoData} />} />
            <Route path="/editor" element={<Editor videoData={videoData} />} />
            <Route path="/results" element={<Results videoData={videoData} />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
}

export default App;

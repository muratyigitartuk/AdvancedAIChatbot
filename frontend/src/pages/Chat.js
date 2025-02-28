/**
 * @module Chat
 * @description Main chat interface component for the AI chatbot application.
 * 
 * This component provides the primary user interface for interacting with the AI chatbot,
 * including:
 * - Text message input and submission
 * - Voice input recording and transcription
 * - Message history display
 * - Real-time conversation updates
 * 
 * The component manages the entire chat experience, handling API calls to the backend
 * for message processing, voice transcription, and conversation history.
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Box, 
  TextField, 
  IconButton, 
  Paper, 
  Typography, 
  CircularProgress,
  Avatar,
  Grid,
  Divider
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

/**
 * Chat component for the AI chatbot interface.
 * 
 * @component
 * @returns {JSX.Element} The chat interface component
 */
const Chat = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const messagesEndRef = useRef(null);

  /**
   * Scrolls the chat window to the bottom to show the latest messages.
   */
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  /**
   * Effect to scroll to the bottom whenever messages are updated.
   */
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  /**
   * Effect to fetch conversation history when the component mounts.
   */
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get('/api/chat/history');
        if (response.data && response.data.length > 0) {
          setMessages(response.data);
        }
      } catch (error) {
        console.error('Error fetching history:', error);
      }
    };

    fetchHistory();
  }, []);

  /**
   * Handles sending a text message to the AI chatbot.
   * 
   * @param {Event} e - The form submission event.
   */
  const handleSendMessage = async (e) => {
    e?.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message to UI
    const userMessage = {
      content: input,
      role: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    
    try {
      // Send message to API
      const response = await axios.post('/api/chat/message', {
        message: input
      });
      
      // Add AI response to UI
      const aiMessage = {
        content: response.data.response,
        role: 'assistant',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage = {
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date().toISOString(),
        error: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Starts recording audio input from the user.
   */
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];

      recorder.ondataavailable = (e) => {
        chunks.push(e.data);
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', audioBlob);

        setLoading(true);
        
        try {
          // Convert speech to text
          const response = await axios.post('/api/voice/transcribe', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });

          if (response.data.text) {
            // Add transcribed message to chat
            setInput(response.data.text);
            
            // Automatically send transcribed message
            const userMessage = {
              content: response.data.text,
              role: 'user',
              timestamp: new Date().toISOString()
            };
            
            setMessages(prev => [...prev, userMessage]);
            
            // Get AI response
            const aiResponse = await axios.post('/api/chat/message', {
              message: response.data.text
            });
            
            // Add AI response to UI
            const aiMessage = {
              content: aiResponse.data.response,
              role: 'assistant',
              timestamp: new Date().toISOString()
            };
            
            setMessages(prev => [...prev, aiMessage]);
          }
        } catch (error) {
          console.error('Error processing voice:', error);
        } finally {
          setLoading(false);
        }

        stream.getTracks().forEach(track => track.stop());
      };

      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  /**
   * Stops the current audio recording.
   */
  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  /**
   * Formats a timestamp into a human-readable time string.
   * 
   * @param {string} timestamp - The timestamp to format.
   * @returns {string} The formatted time string.
   */
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Chat messages */}
      <Box 
        sx={{ 
          flexGrow: 1, 
          overflowY: 'auto', 
          p: 2,
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {messages.length === 0 ? (
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            height: '100%'
          }}>
            <Typography variant="body1" color="text.secondary">
              Start a conversation with your AI assistant
            </Typography>
          </Box>
        ) : (
          messages.map((message, index) => (
            <Box
              key={index}
              sx={{
                display: 'flex',
                justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                mb: 2
              }}
            >
              <Grid container spacing={1} sx={{ maxWidth: '80%' }}>
                {message.role === 'assistant' && (
                  <Grid item>
                    <Avatar sx={{ bgcolor: 'primary.main' }}>AI</Avatar>
                  </Grid>
                )}
                
                <Grid item xs>
                  <Paper
                    elevation={1}
                    sx={{
                      p: 2,
                      bgcolor: message.role === 'user' ? 'primary.light' : 'background.paper',
                      color: message.role === 'user' ? 'primary.contrastText' : 'text.primary',
                      borderRadius: 2,
                      ...(message.error && { bgcolor: 'error.light' })
                    }}
                  >
                    <Typography variant="body1">{message.content}</Typography>
                    <Typography variant="caption" sx={{ display: 'block', mt: 1, textAlign: 'right' }}>
                      {formatTime(message.timestamp)}
                    </Typography>
                  </Paper>
                </Grid>
                
                {message.role === 'user' && (
                  <Grid item>
                    <Avatar sx={{ bgcolor: 'secondary.main' }}>
                      {user?.username?.charAt(0).toUpperCase() || 'U'}
                    </Avatar>
                  </Grid>
                )}
              </Grid>
            </Box>
          ))
        )}
        <div ref={messagesEndRef} />
      </Box>
      
      <Divider />
      
      {/* Message input */}
      <Box 
        component="form" 
        onSubmit={handleSendMessage} 
        sx={{ 
          p: 2, 
          backgroundColor: 'background.paper',
          display: 'flex',
          alignItems: 'center'
        }}
      >
        <TextField
          fullWidth
          placeholder="Type your message..."
          variant="outlined"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading || isRecording}
          sx={{ mr: 1 }}
        />
        
        <IconButton 
          color="primary" 
          onClick={isRecording ? stopRecording : startRecording}
          disabled={loading}
        >
          {isRecording ? <StopIcon /> : <MicIcon />}
        </IconButton>
        
        <IconButton 
          color="primary" 
          type="submit" 
          disabled={!input.trim() || loading || isRecording}
        >
          {loading ? <CircularProgress size={24} /> : <SendIcon />}
        </IconButton>
      </Box>
    </Box>
  );
};

export default Chat;

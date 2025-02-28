/**
 * @module AuthContext
 * @description Authentication context provider for the application.
 * 
 * This module provides authentication state management and functionality including:
 * - User login and registration
 * - Token management and validation
 * - User profile fetching
 * - Logout functionality
 * 
 * It uses JWT (JSON Web Tokens) for authentication and stores the token in localStorage
 * for persistent authentication across page refreshes.
 */

import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
import jwt_decode from 'jwt-decode';

/**
 * Authentication context for storing and accessing auth state.
 * @type {React.Context}
 */
export const AuthContext = createContext();

/**
 * Custom hook to use the authentication context.
 * @returns {Object} Authentication context value containing user, login, logout, etc.
 */
export const useAuth = () => useContext(AuthContext);

/**
 * Authentication provider component that wraps the application and provides
 * authentication state and functionality to all child components.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to render
 * @returns {JSX.Element} The provider component
 */
export const AuthProvider = ({ children }) => {
  // State for user data, loading status, and errors
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Check if user is already logged in on component mount.
   * Validates the stored token and fetches user profile if valid.
   */
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        // Check if token is expired
        const decodedToken = jwt_decode(token);
        const currentTime = Date.now() / 1000;
        
        if (decodedToken.exp > currentTime) {
          // Valid token
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          fetchUserProfile();
        } else {
          // Token expired
          localStorage.removeItem('token');
          setIsLoading(false);
        }
      } catch (error) {
        // Invalid token
        localStorage.removeItem('token');
        setIsLoading(false);
      }
    } else {
      setIsLoading(false);
    }
  }, []);

  /**
   * Fetch user profile from the API.
   * Updates the user state with the fetched profile data.
   */
  const fetchUserProfile = async () => {
    try {
      const response = await axios.get('/api/auth/me');
      setUser(response.data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching user profile:', error);
      setError('Failed to fetch user profile');
      localStorage.removeItem('token');
      setIsLoading(false);
    }
  };

  /**
   * Login function that sends a POST request to the API with the provided credentials.
   * Updates the user state and token storage on successful login.
   * 
   * @param {string} username - Username for login
   * @param {string} password - Password for login
   * @returns {boolean} True on successful login, false otherwise
   */
  const login = async (username, password) => {
    try {
      setError(null);
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      
      const response = await axios.post('/api/auth/token', formData);
      const { access_token, token_type, user_id, username: userName } = response.data;
      
      // Save token
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Fetch user data
      await fetchUserProfile();
      
      return true;
    } catch (error) {
      console.error('Login error:', error);
      setError(error.response?.data?.detail || 'Login failed');
      return false;
    }
  };

  /**
   * Register function that sends a POST request to the API with the provided user data.
   * 
   * @param {Object} userData - User data for registration
   * @returns {boolean} True on successful registration, false otherwise
   */
  const register = async (userData) => {
    try {
      setError(null);
      const response = await axios.post('/api/auth/register', userData);
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      setError(error.response?.data?.detail || 'Registration failed');
      return false;
    }
  };

  /**
   * Logout function that removes the stored token and resets the user state.
   */
  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  // Context value
  const value = {
    user,
    isLoading,
    error,
    login,
    register,
    logout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * @module ThemeContext
 * @description Theme context provider for the application.
 *
 * This module provides theme state management and functionality including:
 * - Light and dark theme switching
 * - Persistent theme preferences via localStorage
 * - Material-UI theme configuration
 *
 * It wraps the Material-UI ThemeProvider to provide consistent theming
 * across the application.
 */

import React, { createContext, useState, useContext, useEffect } from 'react';
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

/**
 * Theme context for storing and accessing theme state.
 * @type {React.Context}
 */
export const ThemeContext = createContext();

/**
 * Custom hook to use the theme context.
 * @returns {Object} Theme context value containing themeMode and toggleTheme function
 */
export const useTheme = () => useContext(ThemeContext);

/**
 * Theme provider component that wraps the application and provides
 * theme state and functionality to all child components.
 *
 * @component
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to render
 * @returns {JSX.Element} The provider component
 */
export const ThemeProvider = ({ children }) => {
  // Check local storage for saved theme preference
  const savedTheme = localStorage.getItem('theme') || 'light';
  const [themeMode, setThemeMode] = useState(savedTheme);

  /**
   * Update theme in localStorage when it changes.
   */
  useEffect(() => {
    localStorage.setItem('theme', themeMode);
  }, [themeMode]);

  /**
   * Toggle between light and dark theme.
   */
  const toggleTheme = () => {
    setThemeMode(prevMode => prevMode === 'light' ? 'dark' : 'light');
  };

  /**
   * Create Material-UI theme based on current mode.
   */
  const theme = createTheme({
    palette: {
      mode: themeMode,
      primary: {
        main: '#2196f3',
      },
      secondary: {
        main: '#ff9800',
      },
      background: {
        default: themeMode === 'light' ? '#f5f8fa' : '#121212',
        paper: themeMode === 'light' ? '#ffffff' : '#1e1e1e',
      },
    },
    typography: {
      fontFamily: [
        'Roboto',
        'Arial',
        'sans-serif',
      ].join(','),
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 8,
          },
        },
      },
    },
  });

  /**
   * Context value containing theme mode and toggle theme function.
   * @type {Object}
   */
  const value = {
    themeMode,
    toggleTheme
  };

  return (
    <ThemeContext.Provider value={value}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};

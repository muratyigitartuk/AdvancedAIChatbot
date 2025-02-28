/**
 * @component Layout
 * @description Main layout component that provides the application shell including
 * navigation drawer, app bar, and user menu. This component handles the overall
 * structure of the application UI and provides navigation functionality.
 * 
 * Features:
 * - Responsive sidebar navigation that collapses to a mobile menu
 * - User profile menu with logout functionality
 * - Theme toggle between light and dark mode
 * - Dynamic navigation highlighting based on current route
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to render in the main content area
 * 
 * @example
 * ```jsx
 * <Layout>
 *   <HomePage />
 * </Layout>
 * ```
 */
import React, { useState } from 'react';
import { 
  Box, 
  AppBar, 
  Toolbar, 
  Typography, 
  IconButton, 
  Drawer, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText,
  ListItemButton,
  Divider,
  Avatar,
  Menu,
  MenuItem,
  useMediaQuery,
  useTheme as useMuiTheme,
  Tooltip
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  Chat as ChatIcon, 
  History as HistoryIcon,
  Logout as LogoutIcon,
  Settings as SettingsIcon,
  DarkMode as DarkModeIcon,
  LightMode as LightModeIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';

const drawerWidth = 240;

/**
 * Main layout component that handles the overall structure of the application UI.
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to render in the main content area
 * @returns {JSX.Element} The main layout component
 */
const Layout = ({ children }) => {
  // Access authentication context for user data and logout functionality
  const { user, logout } = useAuth();
  // Access theme context for theme mode and toggle functionality
  const { themeMode, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Material UI theme for responsive design
  const muiTheme = useMuiTheme();
  const isMobile = useMediaQuery(muiTheme.breakpoints.down('md'));
  
  // State for mobile drawer and user menu
  const [drawerOpen, setDrawerOpen] = useState(!isMobile);
  const [anchorEl, setAnchorEl] = useState(null);
  
  /**
   * Handles the toggle of the mobile drawer.
   */
  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };
  
  /**
   * Handles the opening of the user menu.
   * 
   * @param {Event} event - The event that triggered the menu open
   */
  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };
  
  /**
   * Handles the closing of the user menu.
   */
  const handleMenuClose = () => {
    setAnchorEl(null);
  };
  
  /**
   * Handles navigation to a specific route.
   * 
   * @param {string} path - The path to navigate to
   */
  const handleNavigate = (path) => {
    navigate(path);
    if (isMobile) {
      setDrawerOpen(false);
    }
  };
  
  /**
   * Handles the logout functionality.
   */
  const handleLogout = () => {
    handleMenuClose();
    logout();
    navigate('/login');
  };
  
  // Drawer content
  const drawer = (
    <Box>
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        p: 2
      }}>
        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
          AI Chatbot
        </Typography>
      </Box>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton 
            selected={location.pathname === '/'} 
            onClick={() => handleNavigate('/')}
          >
            <ListItemIcon>
              <ChatIcon color={location.pathname === '/' ? 'primary' : 'inherit'} />
            </ListItemIcon>
            <ListItemText primary="Chat" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton 
            selected={location.pathname === '/history'} 
            onClick={() => handleNavigate('/history')}
          >
            <ListItemIcon>
              <HistoryIcon color={location.pathname === '/history' ? 'primary' : 'inherit'} />
            </ListItemIcon>
            <ListItemText primary="History" />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <AppBar 
        position="fixed" 
        sx={{ 
          zIndex: (theme) => theme.zIndex.drawer + 1,
          backgroundColor: 'background.paper',
          color: 'text.primary',
          boxShadow: 1
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {location.pathname === '/' ? 'Chat' : 'History'}
          </Typography>
          
          <Tooltip title={themeMode === 'light' ? 'Dark Mode' : 'Light Mode'}>
            <IconButton color="inherit" onClick={toggleTheme} sx={{ mx: 1 }}>
              {themeMode === 'light' ? <DarkModeIcon /> : <LightModeIcon />}
            </IconButton>
          </Tooltip>
          
          <IconButton
            onClick={handleMenuOpen}
            color="inherit"
            edge="end"
            aria-label="account"
            aria-haspopup="true"
          >
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
              {user?.username?.charAt(0).toUpperCase() || 'U'}
            </Avatar>
          </IconButton>
          
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
          >
            <MenuItem disabled>
              <Typography variant="body1">{user?.username || 'User'}</Typography>
            </MenuItem>
            <Divider />
            <MenuItem onClick={() => { handleMenuClose(); navigate('/settings'); }}>
              <ListItemIcon>
                <SettingsIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Settings</ListItemText>
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <LogoutIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Logout</ListItemText>
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
      
      <Drawer
        variant={isMobile ? "temporary" : "persistent"}
        open={drawerOpen}
        onClose={isMobile ? handleDrawerToggle : undefined}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { 
            width: drawerWidth, 
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        {drawer}
      </Drawer>
      
      <Box component="main" sx={{ 
        flexGrow: 1, 
        p: 0,
        width: { md: `calc(100% - ${drawerWidth}px)` },
        display: 'flex',
        flexDirection: 'column',
        height: '100vh'
      }}>
        <Toolbar />
        <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
          {children}
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;

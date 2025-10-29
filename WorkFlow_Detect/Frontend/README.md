# Frontend

A modern React TypeScript application for interacting with the Workflow Detection API. This frontend provides an intuitive interface for users to input workflow descriptions and visualize the detected apps and actions.

## 🚀 Features

- **Interactive Workflow Input**: Easy-to-use interface for entering workflow step descriptions
- **Real-time API Integration**: Seamless communication with the FastAPI backend
- **Results Visualization**: Clear display of detected apps, actions, and any errors
- **Responsive Design**: Works across desktop, tablet, and mobile devices
- **Modern UI/UX**: Clean, professional interface with smooth interactions
- **TypeScript Support**: Full type safety and better developer experience

## 🛠️ Technology Stack

- **React**: Modern React with hooks and functional components
- **TypeScript**: Type-safe JavaScript for better development experience
- **CSS3/SCSS**: Modern styling with responsive design
- **Axios**: HTTP client for API requests
- **React Router**: Client-side routing (if multi-page)
- **ESLint & Prettier**: Code quality and formatting tools

## 📋 Prerequisites

- **Node.js** (v16.0.0 or later)
- **npm** (v7.0.0 or later) or **yarn** (v1.22.0 or later)

## 🚀 Quick Start

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd Frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```
`

### Development

1. **Start the development server:**
   ```bash
   npm run dev

   ```
  

2. **Open your browser:**
   The application will automatically open at `http://localhost:8080`

### Building for Production

1. **Build the application:**
   ```bash
   npm run build
   # or
   yarn build
   ```

2. **Serve the built application:**
   ```bash
   npm install -g serve
   serve -s build -l 3000
   ```


## 🔧 Available Scripts

- **`npm start`**: Runs the app in development mode
- **`npm test`**: Launches the test runner in interactive watch mode
- **`npm run build`**: Builds the app for production
- **`npm run eject`**: Ejects from Create React App (irreversible)
- **`npm run lint`**: Runs ESLint to check code quality
- **`npm run lint:fix`**: Fixes auto-fixable ESLint issues
- **`npm run format`**: Formats code using Prettier



## 🎨 Styling Guidelines

- Use CSS modules or styled-components for component-specific styles
- Follow BEM methodology for CSS class naming
- Maintain responsive design principles
- Use CSS custom properties for consistent theming
- Keep accessibility in mind (WCAG 2.1 AA compliance)


## 📱 Responsive Design

The application is designed to work seamlessly across different screen sizes:

- **Desktop**: Full-featured interface with side-by-side layout
- **Tablet**: Adapted layout with touch-friendly controls
- **Mobile**: Stacked layout optimized for small screens

```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Kill process on port 3000
   npx kill-port 3000
   # Or use a different port
   PORT=3001 npm start
   ```

2. **API connection issues**:
   - Verify backend is running on correct port
   - Check CORS configuration in backend
   - Validate environment variables

3. **Build issues**:
   ```bash
   # Clear node_modules and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **TypeScript errors**:
   ```bash
   # Check TypeScript configuration
   npx tsc --noEmit
   ```

.

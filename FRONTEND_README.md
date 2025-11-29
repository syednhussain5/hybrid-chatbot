# 🎨 RAG Chatbot Frontend

## 📋 Overview

A modern, responsive React frontend for the Integrated RAG Chatbot System featuring:
- **Real-time Chat Interface** with beautiful animations
- **Automatic Query Classification** visualization
- **Session Management** and chat history
- **Statistics Dashboard** with live updates
- **Responsive Design** for all devices
- **REST API Integration** with FastAPI backend

## 🎨 Features

### ✨ Modern UI/UX
- **Gradient Backgrounds** with glassmorphism effects
- **Smooth Animations** using Framer Motion
- **Responsive Design** for mobile, tablet, and desktop
- **Dark/Light Theme** support
- **Real-time Typing Indicators**

### 🤖 Chat Features
- **Real-time Messaging** with instant responses
- **Message Classification** with color-coded badges
- **Confidence Scores** for each response
- **Session Persistence** across page refreshes
- **Error Handling** with user-friendly messages

### 📊 Statistics & Monitoring
- **Live Statistics** panel with real-time updates
- **Strategy Distribution** visualization
- **Connection Status** indicators
- **Message Count** and session tracking

### 🔧 Technical Features
- **REST API Integration** with axios
- **Automatic Reconnection** on connection loss
- **Toast Notifications** for user feedback
- **Keyboard Shortcuts** (Enter to send)
- **Loading States** and error handling

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Backend running on port 8000

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   ```
   http://localhost:3000
   ```

### Using the Startup Script

```bash
# From the project root
./start_frontend.sh
```

## 🎯 Usage

### Basic Chat
1. **Type your message** in the input field
2. **Press Enter** or click the send button
3. **View the response** with classification and confidence
4. **Continue the conversation** naturally

### Query Types
The system automatically classifies your queries:

- **🤖 General**: Casual conversation
  - "Hello!", "How are you?", "Thanks!"
  
- **📊 Vector**: Detailed information requests
  - "What is machine learning?", "Explain AI trends"
  
- **🔗 Knowledge Graph**: Relationship queries
  - "Who is the CEO of OpenAI?", "How is Microsoft connected to OpenAI?"
  
- **🔄 Hybrid**: Complex queries requiring both approaches
  - "Explain how Google collaborates with OpenAI in AI research"

### Statistics Panel
- Click the **settings icon** in the header
- View **live statistics** including:
  - Total sessions and queries
  - Strategy distribution
  - Current mode and message count

## 🎨 UI Components

### Header
- **App Title** with icon
- **Connection Status** indicator
- **Mode Toggle** (REST/gRPC)
- **Statistics Toggle** button

### Messages
- **User Messages**: Right-aligned with gradient background
- **Bot Messages**: Left-aligned with white background
- **Avatars**: User and bot icons
- **Metadata**: Timestamp, strategy, confidence

### Input Area
- **Text Input** with placeholder
- **Send Button** with hover animations
- **Keyboard Support** (Enter to send)

### Statistics Panel
- **Live Data** from backend API
- **Strategy Breakdown** with counts
- **Session Information**
- **Real-time Updates**

## 🔧 Configuration

### API Endpoints
The frontend connects to:
- **Health Check**: `GET /health`
- **Query Processing**: `POST /query`
- **Statistics**: `GET /stats`
- **Session Management**: `GET /sessions`

### Environment Variables
Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GRPC_URL=http://localhost:50051
```

### Customization
- **Colors**: Modify the gradient colors in styled components
- **Animations**: Adjust Framer Motion animations
- **Layout**: Change container dimensions and spacing
- **Fonts**: Update font families in CSS

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Features
- **Touch-friendly** buttons and inputs
- **Swipe gestures** for navigation
- **Optimized** message layout
- **Full-screen** chat experience

## 🎭 Animations

### Framer Motion Animations
- **Message Entry**: Slide up with scale effect
- **Typing Indicator**: Bouncing dots
- **Button Hover**: Scale and shadow effects
- **Panel Transitions**: Slide and fade effects

### CSS Animations
- **Pulse Effect**: Connection status indicator
- **Gradient Backgrounds**: Smooth color transitions
- **Hover Effects**: Interactive element feedback

## 🔌 API Integration

### REST API Client
```javascript
// Send message
const response = await axios.post('/query', {
  query: userMessage,
  user_id: 'frontend_user',
  session_id: sessionId,
  metadata: { client: 'react_frontend' }
});

// Get statistics
const stats = await axios.get('/stats');
```

### Error Handling
- **Connection Errors**: Automatic retry with user feedback
- **API Errors**: Graceful degradation with error messages
- **Network Issues**: Offline detection and reconnection

## 🎨 Styling

### Styled Components
- **Component-based** styling
- **Dynamic props** for conditional styling
- **Theme support** with consistent colors
- **Responsive** breakpoints

### Color Scheme
- **Primary**: Blue gradient (#667eea to #764ba2)
- **Success**: Green (#4ade80)
- **Error**: Red (#ef4444)
- **Warning**: Orange (#f59e0b)
- **Info**: Purple (#8b5cf6)

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Static Hosting
The build creates static files in the `build/` directory:
- **index.html**: Main HTML file
- **static/**: CSS and JS bundles
- **favicon.ico**: App icon

### Deployment Options
- **Netlify**: Drag and drop the build folder
- **Vercel**: Connect your GitHub repository
- **AWS S3**: Upload build files to S3 bucket
- **Docker**: Use nginx to serve static files

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   
   # Start backend if not running
   python start_backend.py
   ```

2. **Dependencies Installation Failed**
   ```bash
   # Clear npm cache
   npm cache clean --force
   
   # Delete node_modules and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Port Already in Use**
   ```bash
   # Kill process on port 3000
   lsof -ti:3000 | xargs kill -9
   
   # Or use different port
   PORT=3001 npm start
   ```

4. **CORS Issues**
   - Ensure backend has CORS enabled
   - Check proxy configuration in package.json
   - Verify API URLs in environment variables

## 📈 Performance

### Optimization Features
- **Code Splitting**: Automatic bundle splitting
- **Lazy Loading**: Components loaded on demand
- **Memoization**: Prevent unnecessary re-renders
- **Debouncing**: Optimize API calls

### Bundle Analysis
```bash
# Analyze bundle size
npm run build
npx serve -s build
```

## 🔮 Future Enhancements

### Planned Features
- **gRPC Web Support**: Real-time streaming chat
- **Voice Input**: Speech-to-text integration
- **File Upload**: Document processing
- **Multi-language**: Internationalization
- **Dark Mode**: Theme switching
- **PWA Support**: Progressive Web App features

### Technical Improvements
- **WebSocket**: Real-time bidirectional communication
- **Service Workers**: Offline functionality
- **Push Notifications**: Real-time alerts
- **Analytics**: User behavior tracking

## 📚 Documentation

### Component Documentation
- **App.js**: Main application component
- **Styled Components**: UI styling system
- **API Client**: Backend integration
- **Animations**: Motion and transitions

### API Reference
- **REST Endpoints**: Backend API documentation
- **Error Codes**: Error handling reference
- **Response Format**: Data structure documentation

## 🎉 Success!

Your React frontend is now ready with:
- ✅ **Modern UI** with beautiful animations
- ✅ **Real-time Chat** with automatic classification
- ✅ **Responsive Design** for all devices
- ✅ **Statistics Dashboard** with live updates
- ✅ **Error Handling** and user feedback
- ✅ **Production Ready** with optimization

**The complete RAG Chatbot system is now ready!** 🚀

Frontend: http://localhost:3000
Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

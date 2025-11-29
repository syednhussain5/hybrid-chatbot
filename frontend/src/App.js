import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiSend, FiUser, FiMessageSquare, FiSettings, FiMessageCircle, FiWifi, FiWifiOff, FiTrash2, FiRefreshCw, FiActivity, FiDatabase, FiCpu } from 'react-icons/fi';
import toast, { Toaster } from 'react-hot-toast';
import axios from 'axios';

// Dark Theme Design System
const colors = {
  dark: {
    bg: '#0a0a0a',
    surface: '#111111',
    surfaceElevated: '#1a1a1a',
    surfaceSecondary: '#151515',
    border: '#2a2a2a',
    borderLight: '#333333',
    text: '#ffffff',
    textSecondary: '#a0a0a0',
    textMuted: '#666666',
    textAccent: '#e0e0e0'
  },
  accent: {
    primary: '#6366f1',
    secondary: '#8b5cf6',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6'
  },
  gradients: {
    primary: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
    surface: 'linear-gradient(145deg, #111111 0%, #1a1a1a 100%)',
    glass: 'linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
  }
};

const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px'
};

const borderRadius = {
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '20px',
  full: '50%'
};

// 3-Panel Layout Container
const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  width: 100vw;
  background: ${colors.dark.bg};
  font-family: 'Georgia', 'Times New Roman', serif;
  overflow: hidden;
`;

// Left Panel - Navigation & Settings
const LeftPanel = styled.div`
  width: 280px;
  background: ${colors.dark.surface};
  border-right: 1px solid ${colors.dark.border};
  display: flex;
  flex-direction: column;
`;

const LeftHeader = styled.div`
  padding: ${spacing.lg} ${spacing.xl};
  border-bottom: 1px solid ${colors.dark.border};
`;

const AppTitle = styled.h1`
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: ${colors.dark.text};
  display: flex;
  align-items: center;
  gap: ${spacing.sm};
  font-family: 'Georgia', serif;
`;

const LeftControls = styled.div`
  padding: ${spacing.lg} ${spacing.xl};
  display: flex;
  flex-direction: column;
  gap: ${spacing.md};
`;

const ControlButton = styled(motion.button)`
  background: transparent;
  border: 1px solid ${colors.dark.border};
  color: ${colors.dark.textSecondary};
  padding: ${spacing.md} ${spacing.lg};
  border-radius: ${borderRadius.md};
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: ${spacing.md};
  transition: all 0.2s ease;
  font-family: 'Georgia', serif;
  
  &:hover {
    background: ${colors.dark.surfaceElevated};
    color: ${colors.dark.text};
    border-color: ${colors.accent.primary};
  }
`;

const StatusSection = styled.div`
  padding: ${spacing.lg} ${spacing.xl};
  border-top: 1px solid ${colors.dark.border};
  margin-top: auto;
`;

const StatusTitle = styled.h3`
  margin: 0 0 ${spacing.md} 0;
  font-size: 16px;
  font-weight: 600;
  color: ${colors.dark.text};
  font-family: 'Georgia', serif;
`;

const StatusItem = styled.div`
  display: flex;
  align-items: center;
  gap: ${spacing.sm};
  margin-bottom: ${spacing.sm};
  font-size: 12px;
  color: ${colors.dark.textSecondary};
`;

const StatusDot = styled.div`
  width: 6px;
  height: 6px;
  border-radius: ${borderRadius.full};
  background: ${props => props.connected ? colors.accent.success : colors.accent.error};
  animation: ${props => props.connected ? 'pulse 2s infinite' : 'none'};
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }
`;

// Middle Panel - Chat
const MiddlePanel = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: ${colors.dark.surface};
`;

const ChatHeader = styled.div`
  padding: ${spacing.lg} ${spacing.xl};
  border-bottom: 1px solid ${colors.dark.border};
  background: ${colors.dark.surfaceElevated};
`;

const ChatTitle = styled.h2`
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: ${colors.dark.text};
  font-family: 'Georgia', serif;
`;

const MessagesArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: ${spacing.lg};
  display: flex;
  flex-direction: column;
  gap: ${spacing.lg};
  
  &::-webkit-scrollbar {
    width: 4px;
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
  }
  
  &::-webkit-scrollbar-thumb {
    background: ${colors.dark.border};
    border-radius: ${borderRadius.full};
  }
  
  &::-webkit-scrollbar-thumb:hover {
    background: ${colors.dark.textMuted};
  }
`;

const MessageBubble = styled(motion.div)`
  display: flex;
  align-items: flex-start;
  gap: ${spacing.md};
  max-width: 85%;
  ${props => props.isUser ? 'align-self: flex-end; flex-direction: row-reverse;' : 'align-self: flex-start;'}
`;

const Avatar = styled.div`
  width: 36px;
  height: 36px;
  border-radius: ${borderRadius.full};
  display: flex;
  align-items: center;
  justify-content: center;
  background: ${props => props.isUser 
    ? colors.gradients.primary 
    : `linear-gradient(135deg, ${colors.accent.success} 0%, #059669 100%)`};
  color: white;
  font-size: 16px;
  flex-shrink: 0;
`;

const MessageContent = styled.div`
  background: ${props => props.isUser ? colors.gradients.primary : colors.dark.surfaceElevated};
  color: ${props => props.isUser ? 'white' : colors.dark.text};
  padding: ${spacing.md} ${spacing.lg};
  border-radius: ${props => props.isUser ? `${borderRadius.lg} ${borderRadius.lg} ${borderRadius.sm} ${borderRadius.lg}` : `${borderRadius.lg} ${borderRadius.lg} ${borderRadius.lg} ${borderRadius.sm}`};
  border: 1px solid ${props => props.isUser ? 'transparent' : colors.dark.border};
  word-wrap: break-word;
  line-height: 1.6;
  position: relative;
  box-shadow: ${props => props.isUser ? '0 4px 12px rgba(99, 102, 241, 0.3)' : '0 2px 8px rgba(0, 0, 0, 0.2)'};
  max-width: 100%;
`;

const MessageText = styled.div`
  font-size: 15px;
  line-height: 1.6;
  font-family: 'Georgia', serif;
  white-space: pre-wrap;
  word-break: break-word;
`;

const MessageMeta = styled.div`
  font-size: 11px;
  opacity: 0.7;
  margin-top: ${spacing.sm};
  display: flex;
  align-items: center;
  gap: ${spacing.sm};
  flex-wrap: wrap;
`;

const StrategyTag = styled.span`
  background: ${props => {
    switch(props.strategy) {
      case 'general': return colors.accent.primary;
      case 'vector': return colors.accent.secondary;
      case 'knowledge_graph': return colors.accent.warning;
      case 'hybrid': return colors.accent.success;
      default: return colors.dark.textMuted;
    }
  }};
  color: white;
  padding: 2px ${spacing.sm};
  border-radius: ${borderRadius.sm};
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const InputArea = styled.div`
  padding: ${spacing.lg} ${spacing.xl};
  background: ${colors.dark.surfaceElevated};
  border-top: 1px solid ${colors.dark.border};
  display: flex;
  gap: ${spacing.md};
  align-items: flex-end;
`;

const InputWrapper = styled.div`
  flex: 1;
  position: relative;
`;

const MessageInput = styled.textarea`
  width: 100%;
  min-height: 44px;
  max-height: 120px;
  padding: ${spacing.md} ${spacing.lg};
  border: 1px solid ${colors.dark.border};
  border-radius: ${borderRadius.xl};
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
  background: ${colors.dark.surface};
  color: ${colors.dark.text};
  font-family: 'Georgia', serif;
  line-height: 1.5;
  resize: none;
  
  &:focus {
    border-color: ${colors.accent.primary};
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
  }
  
  &::placeholder {
    color: ${colors.dark.textMuted};
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const SendButton = styled(motion.button)`
  width: 44px;
  height: 44px;
  border: none;
  border-radius: ${borderRadius.full};
  background: ${colors.gradients.primary};
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease;
  
  &:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }
  
  &:active:not(:disabled) {
    transform: scale(0.95);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const TypingIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: ${spacing.sm};
  padding: ${spacing.md} ${spacing.lg};
  background: ${colors.dark.surfaceElevated};
  border-radius: ${borderRadius.xl};
  border: 1px solid ${colors.dark.border};
  align-self: flex-start;
  max-width: 120px;
`;

const TypingDot = styled(motion.div)`
  width: 6px;
  height: 6px;
  border-radius: ${borderRadius.full};
  background: ${colors.dark.textMuted};
`;

const WelcomeCard = styled(motion.div)`
  text-align: center;
  padding: ${spacing['2xl']} ${spacing.xl};
  background: ${colors.dark.surfaceElevated};
  border-radius: ${borderRadius.lg};
  border: 1px solid ${colors.dark.border};
  margin: ${spacing.lg} 0;
  
  h2 {
    margin: 0 0 ${spacing.md} 0;
    color: ${colors.dark.text};
    font-size: 24px;
    font-weight: 600;
    font-family: 'Georgia', serif;
  }
  
  p {
    margin: 0;
    font-size: 15px;
    line-height: 1.6;
    color: ${colors.dark.textSecondary};
    font-family: 'Georgia', serif;
  }
`;

// Right Panel - Agent Details
const RightPanel = styled.div`
  width: 320px;
  background: ${colors.dark.surfaceSecondary};
  border-left: 1px solid ${colors.dark.border};
  display: flex;
  flex-direction: column;
`;

const RightHeader = styled.div`
  padding: ${spacing.lg} ${spacing.xl};
  border-bottom: 1px solid ${colors.dark.border};
`;

const RightTitle = styled.h3`
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: ${colors.dark.text};
  font-family: 'Georgia', serif;
`;

const ConversationLog = styled.div`
  flex: 1;
  padding: ${spacing.lg} ${spacing.xl};
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: ${spacing.md};
`;

const LogEntry = styled.div`
  background: ${colors.dark.surfaceElevated};
  border: 1px solid ${colors.dark.border};
  border-radius: ${borderRadius.md};
  padding: ${spacing.md};
  font-size: 11px;
  line-height: 1.4;
`;

const LogHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${spacing.sm};
  font-weight: 600;
`;

const LogAgent = styled.span`
  color: ${colors.accent.primary};
  font-family: 'Georgia', serif;
`;

const LogTime = styled.span`
  color: ${colors.dark.textMuted};
  font-size: 10px;
`;

const LogAction = styled.div`
  color: ${colors.dark.text};
  font-weight: 600;
  margin-bottom: ${spacing.xs};
`;

const LogContent = styled.div`
  color: ${colors.dark.textSecondary};
  font-family: 'Georgia', serif;
  white-space: pre-wrap;
  word-break: break-word;
`;

const LogAPI = styled.div`
  background: ${colors.dark.surface};
  border: 1px solid ${colors.dark.borderLight};
  border-radius: ${borderRadius.sm};
  padding: ${spacing.sm};
  margin-top: ${spacing.sm};
  font-family: 'Courier New', monospace;
  font-size: 10px;
  color: ${colors.accent.success};
`;

const LogThought = styled.div`
  background: ${colors.dark.surface};
  border-left: 3px solid ${colors.accent.warning};
  padding: ${spacing.sm};
  margin-top: ${spacing.sm};
  font-style: italic;
  color: ${colors.dark.textAccent};
`;

const LogResponse = styled.div`
  background: ${colors.dark.surface};
  border: 1px solid ${colors.dark.borderLight};
  border-radius: ${borderRadius.sm};
  padding: ${spacing.sm};
  margin-top: ${spacing.sm};
  font-family: 'Courier New', monospace;
  font-size: 10px;
  color: ${colors.accent.info};
  max-height: 100px;
  overflow-y: auto;
`;

const LogSection = styled.div`
  margin-bottom: ${spacing.lg};
`;

const LogSectionTitle = styled.h4`
  margin: 0 0 ${spacing.md} 0;
  font-size: 14px;
  font-weight: 600;
  color: ${colors.dark.text};
  font-family: 'Georgia', serif;
  display: flex;
  align-items: center;
  gap: ${spacing.sm};
`;

const EmptyLog = styled.div`
  text-align: center;
  color: ${colors.dark.textMuted};
  font-size: 12px;
  padding: ${spacing.xl};
  font-family: 'Georgia', serif;
`;

// Main App Component
function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [showStats, setShowStats] = useState(false);
  const [stats, setStats] = useState({});
  const [agentStatus, setAgentStatus] = useState('Ready');
  const [currentStrategy, setCurrentStrategy] = useState(null);
  const [conversationLog, setConversationLog] = useState([]);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Check API connection on mount
  useEffect(() => {
    checkConnection();
  }, []);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [inputValue]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const checkConnection = async () => {
    try {
      const response = await axios.get('/health');
      setIsConnected(response.data.status === 'healthy');
      setAgentStatus('Connected');
    } catch (error) {
      setIsConnected(false);
      setAgentStatus('Disconnected');
      console.error('Connection check failed:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await axios.get('/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setIsLoading(true);
    setAgentStatus('Processing...');

    // Add user message immediately
    const newUserMessage = {
      id: Date.now(),
      text: userMessage,
      isUser: true,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, newUserMessage]);

    // Add user task entry to conversation log
    const userLogEntry = {
      id: Date.now(),
      agent: 'Customer',
      time: new Date().toLocaleTimeString(),
      action: 'Enter Task',
      content: userMessage,
      type: 'task'
    };
    setConversationLog(prev => [...prev, userLogEntry]);

    try {
      const response = await axios.post('/query', {
        query: userMessage,
        user_id: 'frontend_user',
        session_id: sessionId,
        metadata: { client: 'react_frontend' }
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        isUser: false,
        timestamp: response.data.timestamp,
        strategy: response.data.strategy,
        confidence: response.data.confidence,
        method: response.data.method,
      };

      setMessages(prev => [...prev, botMessage]);
      setCurrentStrategy(response.data.strategy);
      setAgentStatus('Ready');
      
      // Generate conversation log entries for the agent's process
      const logEntries = generateAgentLogEntries(userMessage, response.data);
      setConversationLog(prev => [...prev, ...logEntries]);
      
      // Set session ID if not already set
      if (!sessionId) {
        setSessionId(response.data.session_id);
      }

      toast.success(`Response received (${response.data.strategy})`);
      
      // Reload stats
      loadStats();
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message. Please try again.');
      setAgentStatus('Error');
      
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
        timestamp: new Date().toISOString(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);

      // Add error log entry
      const errorLogEntry = {
        id: Date.now(),
        agent: 'GenerativeAgent',
        time: new Date().toLocaleTimeString(),
        action: 'Error',
        content: 'Failed to process request. Please try again.',
        type: 'error'
      };
      setConversationLog(prev => [...prev, errorLogEntry]);
    } finally {
      setIsLoading(false);
    }
  };

  const generateAgentLogEntries = (userMessage, responseData) => {
    const entries = [];
    const timestamp = new Date().toLocaleTimeString();
    
    // Thought process entry
    entries.push({
      id: Date.now() + Math.random(),
      agent: 'GenerativeAgent',
      time: timestamp,
      action: 'Thought',
      content: generateThoughtProcess(userMessage, responseData.strategy),
      type: 'thought'
    });

    // API Request entry (simulated)
    if (responseData.strategy !== 'general') {
      entries.push({
        id: Date.now() + Math.random() + 1,
        agent: 'GenerativeAgent',
        time: timestamp,
        action: 'API Request',
        content: generateAPIRequest(responseData.strategy),
        type: 'api_request'
      });

      // API Response entry
      entries.push({
        id: Date.now() + Math.random() + 2,
        agent: 'GenerativeAgent',
        time: timestamp,
        action: 'API Response',
        content: generateAPIResponse(responseData.strategy, responseData.response),
        type: 'api_response'
      });
    }

    // Final thought entry
    entries.push({
      id: Date.now() + Math.random() + 3,
      agent: 'GenerativeAgent',
      time: timestamp,
      action: 'Thought',
      content: generateFinalThought(responseData.strategy, responseData.confidence),
      type: 'thought'
    });

    return entries;
  };

  const generateThoughtProcess = (userMessage, strategy) => {
    const thoughts = {
      general: `(1) The user is asking a general question: "${userMessage}". (2) This doesn't require specific data retrieval. (3) I can provide a helpful response using my general knowledge.`,
      vector: `(1) The user is asking about specific information: "${userMessage}". (2) I need to search the vector database for relevant documents. (3) I'll use semantic similarity to find the most relevant content.`,
      knowledge_graph: `(1) The user is asking about relationships or entities: "${userMessage}". (2) I need to query the knowledge graph to find connections. (3) I'll search for relevant entities and their relationships.`,
      hybrid: `(1) The user's query is complex: "${userMessage}". (2) I need to combine vector search and knowledge graph queries. (3) I'll use both approaches to provide a comprehensive answer.`
    };
    return thoughts[strategy] || thoughts.general;
  };

  const generateAPIRequest = (strategy) => {
    const requests = {
      vector: 'search_vector_database(query="' + inputValue + '", limit=5, similarity_threshold=0.7)',
      knowledge_graph: 'query_knowledge_graph(entities=["' + inputValue.split(' ').slice(0, 3).join('", "') + '"], depth=2)',
      hybrid: 'hybrid_search(query="' + inputValue + '", vector_weight=0.6, kg_weight=0.4)'
    };
    return requests[strategy] || 'process_general_query(query="' + inputValue + '")';
  };

  const generateAPIResponse = (strategy, response) => {
    const responses = {
      vector: '{"results": [{"content": "Relevant document content...", "score": 0.85, "source": "doc1.md"}], "total": 3}',
      knowledge_graph: '{"entities": [{"name": "OpenAI", "type": "Organization", "relationships": [{"target": "Sam Altman", "type": "led_by"}]}], "relationships": 5}',
      hybrid: '{"vector_results": [...], "kg_results": [...], "combined_score": 0.92}'
    };
    return responses[strategy] || '{"status": "success", "response": "Generated response based on general knowledge"}';
  };

  const generateFinalThought = (strategy, confidence) => {
    return `(1) I have successfully processed the query using ${strategy} strategy. (2) The confidence level is ${Math.round(confidence * 100)}%. (3) I will now provide a comprehensive response to the user.`;
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
    setCurrentStrategy(null);
    setAgentStatus('Ready');
    setConversationLog([]);
    toast.success('Chat cleared');
  };

  const formatMessage = (text) => {
    // Format long messages with proper line breaks and spacing
    return text
      .replace(/\n\n/g, '\n\n') // Preserve double line breaks
      .replace(/\n/g, '\n') // Preserve single line breaks
      .replace(/([.!?])\s+/g, '$1\n\n') // Add spacing after sentences
      .replace(/(\d+\.\s)/g, '\n$1') // Format numbered lists
      .replace(/([A-Z][a-z]+:)/g, '\n\n$1') // Format section headers
      .trim();
  };

  return (
    <AppContainer>
      {/* Left Panel - Navigation & Settings */}
      <LeftPanel>
        <LeftHeader>
          <AppTitle>
            <FiMessageCircle />
            RAG Chatbot
          </AppTitle>
        </LeftHeader>
        
        <LeftControls>
          <ControlButton
            onClick={() => setShowStats(!showStats)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <FiSettings />
            Statistics
          </ControlButton>
          
          <ControlButton
            onClick={clearChat}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <FiTrash2 />
            Clear Chat
          </ControlButton>
          
          <ControlButton
            onClick={checkConnection}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <FiRefreshCw />
            Refresh Status
          </ControlButton>
        </LeftControls>

        <StatusSection>
          <StatusTitle>System Status</StatusTitle>
          <StatusItem>
            <StatusDot connected={isConnected} />
            {isConnected ? 'Connected' : 'Disconnected'}
          </StatusItem>
          <StatusItem>
            <FiActivity />
            Agent: {agentStatus}
          </StatusItem>
          <StatusItem>
            <FiDatabase />
            Messages: {messages.length}
          </StatusItem>
        </StatusSection>
      </LeftPanel>

      {/* Middle Panel - Chat */}
      <MiddlePanel>
        <ChatHeader>
          <ChatTitle>Conversation</ChatTitle>
        </ChatHeader>

        <MessagesArea>
          <AnimatePresence>
            {messages.length === 0 ? (
              <WelcomeCard
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <h2>Welcome to RAG Chatbot</h2>
                <p>
                  I can help you with general questions, provide detailed information about AI and tech companies,
                  or answer relationship-based queries. Try asking me anything!
                </p>
              </WelcomeCard>
            ) : (
              messages.map((message) => (
                <MessageBubble
                  key={message.id}
                  initial={{ opacity: 0, y: 20, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ duration: 0.3 }}
                  isUser={message.isUser}
                >
                  <Avatar isUser={message.isUser}>
                    {message.isUser ? <FiUser /> : <FiMessageSquare />}
                  </Avatar>
                  <MessageContent isUser={message.isUser}>
                    <MessageText>{formatMessage(message.text)}</MessageText>
                    <MessageMeta>
                      {new Date(message.timestamp).toLocaleTimeString()}
                      {message.strategy && (
                        <>
                          <span>•</span>
                          <StrategyTag strategy={message.strategy}>
                            {message.strategy}
                          </StrategyTag>
                          <span>•</span>
                          <span>{Math.round(message.confidence * 100)}%</span>
                        </>
                      )}
                    </MessageMeta>
                  </MessageContent>
                </MessageBubble>
              ))
            )}
          </AnimatePresence>

          {isLoading && (
            <TypingIndicator
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <FiMessageSquare />
              <TypingDot
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
              />
              <TypingDot
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
              />
              <TypingDot
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
              />
            </TypingIndicator>
          )}

          <div ref={messagesEndRef} />
        </MessagesArea>

        <InputArea>
          <InputWrapper>
            <MessageInput
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here... (Shift+Enter for new line)"
              disabled={isLoading}
              rows={1}
            />
          </InputWrapper>
          <SendButton
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FiSend />
          </SendButton>
        </InputArea>
      </MiddlePanel>

      {/* Right Panel - Conversation Log */}
      <RightPanel>
        <RightHeader>
          <RightTitle>Conversation Details</RightTitle>
        </RightHeader>

        <ConversationLog>
          {conversationLog.length === 0 ? (
            <EmptyLog>
              No conversation activity yet.<br />
              Start chatting to see agent details.
            </EmptyLog>
          ) : (
            conversationLog.map((entry) => (
              <LogEntry key={entry.id}>
                <LogHeader>
                  <LogAgent>{entry.agent}</LogAgent>
                  <LogTime>{entry.time}</LogTime>
                </LogHeader>
                
                <LogAction>{entry.action}:</LogAction>
                
                {entry.type === 'thought' && (
                  <LogThought>
                    <LogContent>{entry.content}</LogContent>
                  </LogThought>
                )}
                
                {entry.type === 'api_request' && (
                  <LogAPI>
                    <LogContent>{entry.content}</LogContent>
                  </LogAPI>
                )}
                
                {entry.type === 'api_response' && (
                  <LogResponse>
                    <LogContent>{entry.content}</LogContent>
                  </LogResponse>
                )}
                
                {entry.type === 'task' && (
                  <LogContent>{entry.content}</LogContent>
                )}
                
                {entry.type === 'error' && (
                  <LogContent style={{ color: colors.accent.error }}>
                    {entry.content}
                  </LogContent>
                )}
              </LogEntry>
            ))
          )}
        </ConversationLog>
      </RightPanel>

      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: colors.dark.surfaceElevated,
            color: colors.dark.text,
            borderRadius: borderRadius.md,
            fontSize: '12px',
            fontWeight: '500',
            border: `1px solid ${colors.dark.border}`,
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)'
          },
        }}
      />
    </AppContainer>
  );
}

export default App;
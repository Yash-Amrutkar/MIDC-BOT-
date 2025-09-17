#!/usr/bin/env python3
"""
MIDC Chatbot - Flask Backend API
Modern web interface for MIDC Land Bank Chatbot
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from final_rag_service import RAGService

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"], supports_credentials=True)

# Initialize RAG service
rag_service = None

def initialize_rag():
    """Initialize the RAG service"""
    global rag_service
    try:
        rag_service = RAGService()
        print("✅ RAG Service initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize RAG service: {str(e)}")
        return False

@app.route('/')
def index():
    """Serve the main chatbot interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        print(f"📨 Received chat request from {request.remote_addr}")
        data = request.get_json()
        print(f"📝 Request data: {data}")
        
        if not data:
            print("❌ No JSON data received")
            return jsonify({
                'success': False,
                'error': 'No data received'
            }), 400
            
        user_message = data.get('message', '').strip()
        print(f"💬 User message: {user_message}")
        
        if not user_message:
            print("❌ Empty message received")
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        if not rag_service:
            print("❌ RAG service not available")
            return jsonify({
                'success': False,
                'error': 'AI service is not available. Please try again later.'
            }), 503
        
        print("🤖 Processing with RAG service...")
        # Get response from RAG service
        response_data = rag_service.query(user_message)
        print(f"✅ RAG response: {response_data.get('response', 'No response')[:100]}...")
        
        return jsonify({
            'success': True,
            'response': response_data['response'],
            'context_docs': response_data.get('context_docs', []),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    print(f"🏥 Health check from {request.remote_addr}")
    status = {
        'status': 'healthy',
        'rag_service': rag_service is not None,
        'timestamp': datetime.now().isoformat()
    }
    print(f"✅ Health status: {status}")
    return jsonify(status)

if __name__ == '__main__':
    print("🚀 Starting MIDC Chatbot Flask Server...")
    
    # Initialize RAG service
    if initialize_rag():
        print("✅ MIDC Chatbot is ready!")
        print("🌐 Access the chatbot at: http://localhost:8080")
        app.run(debug=False, host='0.0.0.0', port=8080)
    else:
        print("❌ Failed to start server due to RAG service initialization error")

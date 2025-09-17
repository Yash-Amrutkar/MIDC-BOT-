from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import numpy as np
from typing import List, Dict, Any
import config
from language_detector import language_detector

class RAGService:
    def __init__(self):
        """Initialize the RAG service with Pinecone, Sentence Transformers, and Gemini"""
        self.embedding_model = None
        self.pinecone_index = None
        self.genai_model = None
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all required services"""
        try:
            # Initialize Pinecone with new client
            pc = Pinecone(api_key=config.PINECONE_API_KEY)
            self.pinecone_index = pc.Index(config.PINECONE_INDEX_NAME)
            print("✅ Pinecone initialized successfully")
            
            # Initialize Sentence Transformer
            self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
            print("✅ Sentence Transformer initialized successfully")
            
            # Initialize Google Gemini
            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.genai_model = genai.GenerativeModel(config.GENERATION_MODEL)
            print("✅ Google Gemini initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing services: {e}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text"""
        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            return []

    def semantic_search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Perform semantic search on Pinecone index"""
        try:
            if top_k is None:
                top_k = config.TOP_K_RESULTS
            
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            if not query_embedding:
                return []
            
            # Search in Pinecone
            search_results = self.pinecone_index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Process results with IMPROVED metadata field mapping
            results = []
            for match in search_results.matches:
                # LOWER the similarity threshold to get more results
                if match.score >= 0.3:  # Lowered from config.SIMILARITY_THRESHOLD
                    # Construct text from ACTUAL metadata fields
                    metadata = match.metadata
                    text_parts = []
                    
                    # Map to actual MIDC data fields with better handling
                    if metadata.get('Regional Office'):
                        text_parts.append(f"Regional Office: {metadata['Regional Office']}")
                    
                    if metadata.get('Industrial Area'):
                        text_parts.append(f"Industrial Area: {metadata['Industrial Area']}")
                    
                    # Better handling of numeric fields
                    total_plots = metadata.get('Total Plots Available', 0)
                    if total_plots and total_plots != 0 and not (isinstance(total_plots, float) and np.isnan(total_plots)):
                        text_parts.append(f"Total Plots Available: {int(total_plots)}")
                    
                    current_rate = metadata.get('Current Rate (Rs/sq meter)', 0)
                    if current_rate and current_rate != 0 and not (isinstance(current_rate, float) and np.isnan(current_rate)):
                        text_parts.append(f"Current Rate: {current_rate} Rs per square meter")
                    
                    if metadata.get('Sheet_Name'):
                        text_parts.append(f"Category: {metadata['Sheet_Name']}")
                    
                    # Add source file info for context
                    if metadata.get('source_file'):
                        text_parts.append(f"Source: {metadata['source_file']}")
                    
                    # Only add if we have meaningful content
                    if text_parts:
                        constructed_text = " | ".join(text_parts)
                        
                        results.append({
                            'id': match.id,
                            'score': match.score,
                            'metadata': match.metadata,
                            'text': constructed_text
                        })
            
            return results
            
        except Exception as e:
            print(f"❌ Error in semantic search: {e}")
            return []

    def generate_response(self, query: str, context_docs: List[Dict[str, Any]], language: str = 'english') -> str:
        """Generate response using Gemini with retrieved context"""
        try:
            # Check if it's a greeting or casual conversation
            query_lower = query.lower().strip()
            greetings = ['hey', 'hello', 'hi', 'good morning', 'good afternoon', 'good evening']
            casual_questions = ['how are you', 'how are you doing', 'what\'s up', 'how do you do']
            
            # Check if it's ONLY a greeting (no additional question)
            is_only_greeting = False
            is_greeting_with_question = False
            
            if any(greeting in query_lower for greeting in greetings):
                # Check if there's more content after the greeting
                for greeting in greetings:
                    if greeting in query_lower:
                        after_greeting = query_lower.split(greeting, 1)[1].strip()
                        after_greeting = after_greeting.replace(',', '').replace('.', '').replace('!', '').strip()
                        if len(after_greeting) < 3:  # Just greeting, no question
                            is_only_greeting = True
                        else:  # Greeting + question
                            is_greeting_with_question = True
                        break
            
            if any(casual in query_lower for casual in casual_questions):
                is_only_greeting = True
            
            if is_only_greeting:
                return "Hello! I'm the MIDC Land Bank AI Assistant. I'm here to help you find information about land plots, industrial areas, and property details. How can I assist you today?"
            
            if is_greeting_with_question:
                # For greeting + question, we'll let the normal flow handle it with context
                pass
            
            # Prepare context from retrieved documents
            context_text = ""
            if context_docs:
                for i, doc in enumerate(context_docs, 1):
                    context_text += f"Document {i} (Relevance Score: {doc['score']:.3f}):\n"
                    context_text += f"{doc['text']}\n\n"
            else:
                # No context documents found
                if language == 'marathi':
                    return "माफ करा, मला आमच्या MIDC लँड बँक डेटाबेसमध्ये याबद्दल विशिष्ट माहिती सापडली नाही. कृपया तुमचा प्रश्न पुन्हा विचारा किंवा विचारा:\n\n• विशिष्ट प्रदेशात उपलब्ध प्लॉट\n• व्यावसायिक, औद्योगिक किंवा निवासी प्लॉट\n• प्लॉट दर आणि उपलब्धता\n• प्रादेशिक कार्यालय माहिती"
                else:
                    return "I couldn't find specific information about that in our MIDC Land Bank database. Could you please rephrase your question or ask about:\n\n• Available plots in specific regions\n• Commercial, industrial, or residential plots\n• Plot rates and availability\n• Regional office information"
            
            # Create language-aware prompt for Gemini
            if language == 'marathi':
                prompt = f"""तुम्ही MIDC (महाराष्ट्र औद्योगिक विकास महामंडळ) लँड बँक डेटाचा मैत्रीपूर्ण आणि ज्ञानी सहाय्यक आहात.
तुम्ही वापरकर्त्यांना जमीन प्लॉट, औद्योगिक क्षेत्र आणि मालमत्ता तपशीलांबद्दल माहिती शोधण्यात मदत करता.

MIDC लँड बँक डेटाबेसमधून संदर्भ माहिती:
{context_text}

वापरकर्त्याचा प्रश्न: {query}

सूचना:
1. प्रदान केलेल्या संदर्भावर आधारित प्रश्नाचे उत्तर नैसर्गिक, संभाषणात्मक स्वरात द्या
2. जर संदर्भात संबंधित माहिती असेल, तर मदतकारक आणि तपशीलवार उत्तर द्या
3. जर संदर्भात पुरेशी माहिती नसेल, तर तुमच्याकडे असलेली माहिती विनम्रपणे स्पष्ट करा आणि संबंधित विषयांचा सुझाव द्या
4. प्रादेशिक कार्यालये, औद्योगिक क्षेत्र आणि दर उपलब्ध असताना विशिष्ट आणि अचूक रहा
5. मदतकारक रिअल इस्टेट सल्लागारासारखा मैत्रीपूर्ण, व्यावसायिक स्वर वापरा
6. विशिष्ट प्लॉट किंवा क्षेत्रांबद्दल विचारल्यास, संदर्भातून अचूक तपशील द्या
7. चांगल्या वाचनीयतेसाठी नेहमी बुलेट पॉइंट्स (•) सह तुमचे उत्तर फॉरमॅट करा
8. उपलब्ध असताना संबंधित प्रादेशिक कार्यालय, औद्योगिक क्षेत्र आणि दर माहिती समाविष्ट करा
9. जर प्रश्न MIDC लँड बँक डेटाशी संबंधित नसेल, तर विनम्रपणे संबंधित विषयांकडे पुनर्निर्देशित करा
10. उत्तरे संक्षिप्त पण माहितीपूर्ण ठेवा
11. माहिती स्पष्टपणे व्यवस्थित करण्यासाठी बुलेट पॉइंट्स वापरा

उत्तर मराठीत द्या आणि नैसर्गिक, संभाषणात्मक पद्धतीने बुलेट पॉइंट्स आणि लाइन ब्रेक्ससह:"""
            else:
                prompt = f"""You are a friendly and knowledgeable assistant for MIDC (Maharashtra Industrial Development Corporation) Land Bank data.
You help users find information about land plots, industrial areas, and property details in a conversational and helpful manner.

Context Information from MIDC Land Bank Database:
{context_text}

User Question: {query}

Instructions:
1. Answer the question based on the provided context in a natural, conversational tone
2. If the context contains relevant information, provide a helpful and detailed answer
3. If the context doesn't contain enough information, politely explain what information you do have and suggest related topics
4. Be specific and accurate with regional offices, industrial areas, and rates when available
5. Use a friendly, professional tone as if you're a helpful real estate consultant
6. If asked about specific plots or areas, provide exact details from the context
7. ALWAYS format your response with bullet points (•) for better readability
8. Include relevant regional office, industrial area, and rate information when available
9. If the question is not related to MIDC land bank data, politely redirect to relevant topics
10. Keep responses concise but informative
11. Use bullet points to organize information clearly
12. If asked about "plots in [city]" or "industrial plots in [city]", provide all relevant results from the context
13. Group similar results together for better organization

Format your response with bullet points like this:
• [Key information point 1]
• [Key information point 2]
• [Key information point 3]

IMPORTANT: Use actual line breaks (\\n) between each bullet point for proper formatting.

Answer in a natural, conversational way with bullet points and line breaks:"""

            # Generate response using Gemini
            response = self.genai_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return "I apologize, but I encountered an error while generating a response. Please try again."

    def generate_multilingual_response(self, user_question: str, context_docs: List[Dict[str, Any]], language: str) -> str:
        """Generate response in the appropriate language"""
        try:
            if language == 'marathi':
                # Create Marathi-specific prompt
                prompt = language_detector.create_multilingual_prompt(user_question, context_docs, language)
            else:
                # Create English-specific prompt
                prompt = language_detector.create_multilingual_prompt(user_question, context_docs, language)
            
            # Generate response using Gemini
            response = self.genai_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"❌ Error generating multilingual response: {e}")
            if language == 'marathi':
                return "माफ करा, मला तुमच्या प्रश्नाचे उत्तर देण्यात अडचण आली आहे. कृपया पुन्हा प्रयत्न करा."
            else:
                return "I apologize, but I encountered an error while generating a response. Please try again."

    def query(self, user_question: str) -> Dict[str, Any]:
        """Main RAG query method with multilingual support"""
        try:
            # Detect language of the query
            query_language = language_detector.detect_language(user_question)
            print(f"🌐 Detected language: {query_language}")
            
            # Check if it's a greeting or casual conversation first
            query_lower = user_question.lower().strip()
            
            # Multilingual greetings
            greetings = {
                'english': ['hey', 'hello', 'hi', 'good morning', 'good afternoon', 'good evening'],
                'marathi': ['नमस्कार', 'नमस्ते', 'हाय', 'हॅलो', 'गुड मॉर्निंग', 'गुड आफ्टरनून', 'गुड इव्हनिंग']
            }
            
            casual_questions = {
                'english': ['how are you', 'how are you doing', 'what\'s up', 'how do you do'],
                'marathi': ['कसे आहात', 'कशी आहात', 'कसे आहे', 'कशी आहे', 'काय चालू', 'कसे जाते']
            }
            
            # Check if it's ONLY a greeting (no additional question)
            is_only_greeting = False
            is_greeting_with_question = False
            
            # Check for pure greetings (just greeting words)
            current_greetings = greetings.get(query_language, greetings['english'])
            current_casual = casual_questions.get(query_language, casual_questions['english'])
            
            if any(greeting in query_lower for greeting in current_greetings):
                # Check if there's more content after the greeting
                greeting_found = False
                for greeting in current_greetings:
                    if greeting in query_lower:
                        # Check if there's substantial content after the greeting
                        after_greeting = query_lower.split(greeting, 1)[1].strip()
                        # Remove common punctuation and check if there's meaningful content
                        after_greeting = after_greeting.replace(',', '').replace('.', '').replace('!', '').strip()
                        if len(after_greeting) < 3:  # Just greeting, no question
                            is_only_greeting = True
                        else:  # Greeting + question
                            is_greeting_with_question = True
                        greeting_found = True
                        break
                
                if not greeting_found:
                    is_only_greeting = True
            
            # Check for casual questions
            if any(casual in query_lower for casual in current_casual):
                is_only_greeting = True
            
            # Handle pure greetings with multilingual responses
            if is_only_greeting:
                if query_language == 'marathi':
                    greeting_response = "नमस्कार! मी MIDC लँड बँक चा AI सहाय्यक आहे. मी तुम्हाला जमीन प्लॉट, औद्योगिक क्षेत्र आणि मालमत्ता तपशीलांची माहिती शोधण्यात मदत करतो. आज मी तुमची कशी मदत करू शकतो?"
                else:
                    greeting_response = "Hello! I'm the MIDC Land Bank AI Assistant. I'm here to help you find information about land plots, industrial areas, and property details. How can I assist you today?"
                
                return {
                    'response': greeting_response,
                    'context_docs': [],
                    'is_greeting': True,
                    'language': query_language
                }
            
            # Perform semantic search with MORE results
            context_docs = self.semantic_search(user_question, top_k=10)  # Increased from default
            
            # Generate response with language awareness
            if context_docs:
                response = self.generate_response(user_question, context_docs, query_language)
            else:
                response = self.generate_response(user_question, [], query_language)
            
            return {
                'response': response,
                'context_docs': context_docs,
                'is_greeting': False,
                'language': query_language
            }
            
        except Exception as e:
            print(f"❌ Error in RAG query: {e}")
            # Try to detect language for error message
            try:
                query_language = language_detector.detect_language(user_question)
                if query_language == 'marathi':
                    error_response = "माफ करा, मला तुमच्या विनंतीचे प्रक्रिया करण्यात अडचण आली आहे. कृपया पुन्हा प्रयत्न करा."
                else:
                    error_response = "I apologize, but I encountered an error while processing your request. Please try again."
            except:
                error_response = "I apologize, but I encountered an error while processing your request. Please try again."
            
            return {
                'response': error_response,
                'context_docs': [],
                'is_greeting': False,
                'language': 'english'
            }

# Test function to verify the RAG service
def test_rag_service():
    """Test the RAG service with sample queries"""
    try:
        rag = RAGService()
        
        # Test queries that were failing
        test_queries = [
            "plots available in pune",
            "industrial plot in mumbai", 
            "commercial plots",
            "vacant plots",
            "Show me commercial plots in Mumbai",
            "What are the cheapest industrial plots?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing Query: '{query}'")
            result = rag.query(query)
            print(f"📝 Response: {result['response']}")
            print(f"📊 Context Docs Found: {len(result['context_docs'])}")
            if result['context_docs']:
                print(f"🎯 Top Result Score: {result['context_docs'][0]['score']:.3f}")
                print(f"📋 Top Result Text: {result['context_docs'][0]['text'][:100]}...")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_rag_service()

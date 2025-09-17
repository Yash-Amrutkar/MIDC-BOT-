#!/usr/bin/env python3
"""
Language Detection Module for MIDC Chatbot
Detects English vs Marathi and provides appropriate responses
"""

import re
from typing import Tuple, Dict, Any

class LanguageDetector:
    def __init__(self):
        """Initialize the language detector"""
        # Common Marathi words and patterns
        self.marathi_patterns = [
            # Common Marathi words
            r'\b(प्लॉट|जमीन|भूमि|मालमत्ता|विक्री|भाडे|किंमत|दर|स्थान|ठिकाण|मिळेल|उपलब्ध|कशी|कुठे|केव्हा|कोण|काय|का|कसे|किती|कुठून|कुठेपर्यंत)\b',
            r'\b(महाराष्ट्र|पुणे|मुंबई|नागपूर|औरंगाबाद|कोल्हापूर|सांगली|नाशिक|अमरावती|चंद्रपूर|सोलापूर|धुळे|अहमदनगर|लातूर|बीड|जालना|परभणी|नांदेड|यवतमाळ|गडचिरोली|वर्धा|बुलढाणा|अकोला|वाशीम|अमरावती)\b',
            r'\b(मिडक|एमआयडीसी|व्यावसायिक|औद्योगिक|निवासी|कॉमर्शियल|इंडस्ट्रियल|रेजिडेंशियल)\b',
            r'\b(चौरस|मीटर|हेक्टर|एकर|स्क्वेअर|फूट|यार्ड|किमी|मी|सेमी)\b',
            r'\b(रुपये|रुपयां|रू|₹|लाख|कोटी|हजार|शेकडो)\b',
            r'\b(मिळणार|देणार|सांगणार|सोडवणार|मदत|साहाय्य|जाणकारी|माहिती|तपशील|विवरण)\b',
            # Common Marathi question words
            r'\b(काय|कसे|कुठे|केव्हा|कोण|का|किती|कुठून|कुठेपर्यंत|कशी|कशाला|कशासाठी)\b',
            # Marathi verbs and common phrases
            r'\b(दे|द्या|सांग|सांगा|मिळेल|आहे|असेल|होईल|कर|करा|पाह|पाहा|दाखव|दाखवा)\b',
        ]
        
        # Compile patterns for efficiency
        self.marathi_regex = [re.compile(pattern, re.UNICODE | re.IGNORECASE) for pattern in self.marathi_patterns]
        
        # English common words (for comparison)
        self.english_words = {
            'show', 'give', 'tell', 'available', 'plots', 'land', 'price', 'rate', 'location',
            'commercial', 'industrial', 'residential', 'pune', 'mumbai', 'maharashtra',
            'square', 'meter', 'hectare', 'acre', 'rupees', 'lakh', 'crore', 'thousand',
            'help', 'information', 'details', 'what', 'how', 'where', 'when', 'which', 'why'
        }

    def detect_language(self, text: str) -> str:
        """
        Detect if the text is in English or Marathi
        Returns: 'marathi' or 'english'
        """
        if not text or not text.strip():
            return 'english'
        
        text = text.strip()
        marathi_score = 0
        english_score = 0
        
        # Check for Marathi patterns
        for regex in self.marathi_regex:
            if regex.search(text):
                marathi_score += 1
        
        # Check for English words
        words = text.lower().split()
        for word in words:
            # Clean word (remove punctuation)
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in self.english_words:
                english_score += 1
        
        # Additional checks
        # Check for Devanagari script (Marathi/Hindi)
        if re.search(r'[\u0900-\u097F]', text):
            marathi_score += 3
        
        # Check for Latin script (English)
        if re.search(r'[a-zA-Z]', text):
            english_score += 1
        
        # Decision logic
        if marathi_score > english_score:
            return 'marathi'
        else:
            return 'english'

    def get_response_language(self, query_language: str) -> str:
        """Get the appropriate response language"""
        return query_language

    def create_multilingual_prompt(self, query: str, context_docs: list, language: str) -> str:
        """
        Create a prompt that instructs the AI to respond in the appropriate language
        """
        if language == 'marathi':
            base_prompt = f"""
तुम्ही MIDC लँड बँक च्या AI सहाय्यक आहात. वापरकर्त्याचा प्रश्न मराठीत आहे, म्हणून तुम्ही मराठीतच उत्तर द्या.

वापरकर्त्याचा प्रश्न: {query}

उपलब्ध माहिती:
"""
            for i, doc in enumerate(context_docs[:3], 1):
                base_prompt += f"{i}. {doc.get('content', '')}\n"
            
            base_prompt += """
कृपया मराठीत उत्तर द्या. उत्तरात खालील गोष्टी समाविष्ट करा:
- वापरकर्त्याच्या प्रश्नाचे स्पष्ट उत्तर
- उपलब्ध प्लॉटची माहिती (कुठे, किती किंमत, काय प्रकार)
- अधिक माहितीसाठी संपर्क करण्याची सूचना
- MIDC सेवा पोर्टलची लिंक

उत्तर मराठीत असावे आणि सोप्या भाषेत असावे.
"""
        else:
            base_prompt = f"""
You are an AI assistant for MIDC Land Bank. The user's question is in English, so please respond in English.

User's question: {query}

Available information:
"""
            for i, doc in enumerate(context_docs[:3], 1):
                base_prompt += f"{i}. {doc.get('content', '')}\n"
            
            base_prompt += """
Please respond in English. Include the following in your response:
- Clear answer to the user's question
- Information about available plots (location, price, type)
- Instructions for getting more information
- Link to MIDC Services Portal

Keep the response in English and use simple, clear language.
"""
        
        return base_prompt

    def translate_common_terms(self, text: str, from_lang: str, to_lang: str) -> str:
        """
        Translate common terms between English and Marathi
        """
        if from_lang == to_lang:
            return text
        
        # Common translations
        translations = {
            'plots': 'प्लॉट',
            'commercial': 'व्यावसायिक',
            'industrial': 'औद्योगिक', 
            'residential': 'निवासी',
            'available': 'उपलब्ध',
            'price': 'किंमत',
            'rate': 'दर',
            'location': 'स्थान',
            'pune': 'पुणे',
            'mumbai': 'मुंबई',
            'square meter': 'चौरस मीटर',
            'rupees': 'रुपये',
            'lakh': 'लाख',
            'crore': 'कोटी'
        }
        
        result = text
        for eng, mar in translations.items():
            if from_lang == 'english' and to_lang == 'marathi':
                result = result.replace(eng, mar)
            elif from_lang == 'marathi' and to_lang == 'english':
                result = result.replace(mar, eng)
        
        return result

# Global instance
language_detector = LanguageDetector()

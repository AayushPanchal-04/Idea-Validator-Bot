import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="💡 Idea Validator Bot",
    page_icon="💡",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">💡 Idea Validator Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Get AI-powered feedback on your startup or project ideas</div>', unsafe_allow_html=True)

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Groq API Key", type="password", help="Get your API key from https://console.groq.com/")
    
    st.divider()
    
    st.header("📋 How to Use")
    st.markdown("""
    1. Enter your Groq API key
    2. Describe your startup/project idea
    3. Click 'Validate Idea'
    4. Get detailed AI feedback!
    """)
    
    st.divider()
    
    st.header("🔍 Analysis Includes")
    st.markdown("""
    - ✅ Strengths & Opportunities
    - ⚠️ Challenges & Risks
    - 💡 Improvement Suggestions
    - 🎯 Market Viability
    - 📊 Overall Assessment
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    idea_input = st.text_area(
        "📝 Describe Your Idea",
        height=200,
        placeholder="Example: A mobile app that helps people find and book local fitness classes in real-time, similar to how Uber works for rides...",
        help="Provide as much detail as possible about your startup or project idea"
    )

with col2:
    st.markdown("### 💭 Tips for Best Results")
    st.info("""
    - Be specific about your target audience
    - Mention the problem you're solving
    - Include your unique value proposition
    - Describe the business model if applicable
    """)

# Validate button
validate_button = st.button("🚀 Validate Idea", type="primary", use_container_width=True)

# Function to call Groq API directly
def validate_idea_with_groq(api_key, idea):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are an experienced startup advisor and business analyst. 
Your role is to provide honest, constructive feedback on business ideas. 

Analyze the idea thoroughly and provide:
1. **Strengths & Opportunities**: What's good about this idea? What potential does it have?
2. **Challenges & Risks**: What obstacles might they face? What could go wrong?
3. **Improvements**: Specific, actionable suggestions to make the idea better
4. **Market Viability**: Assessment of market demand and competition
5. **Overall Rating**: Give a rating out of 10 with justification

Be honest but encouraging. Focus on being helpful and actionable."""
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Idea to validate: {idea}"}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Process the validation
if validate_button:
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar!")
    elif not idea_input.strip():
        st.error("⚠️ Please describe your idea before validating!")
    else:
        with st.spinner("🤔 AI is analyzing your idea..."):
            try:
                # Get validation from Groq
                validation_result = validate_idea_with_groq(api_key, idea_input)
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                st.markdown("---")
                st.markdown("## 📊 Validation Results")
                
                # Display the AI response
                st.markdown(validation_result)
                
                st.markdown("---")
                
                # Additional actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        label="📥 Download Report",
                        data=f"IDEA VALIDATION REPORT\n\n{idea_input}\n\n{validation_result}",
                        file_name="idea_validation.txt",
                        mime="text/plain"
                    )
                with col2:
                    if st.button("🔄 Validate Another Idea"):
                        st.rerun()
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Make sure your API key is valid and you have credits available.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Built with Streamlit and Groq | 
        <a href='https://console.groq.com/' target='_blank'>Get Groq API Key</a></p>
    </div>
""", unsafe_allow_html=True)
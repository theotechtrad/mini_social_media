"""
Streamlit Frontend for Mini Social Media
COMPLETE VERSION WITH COMMENTS AND USERNAMES
"""

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Page Configuration
st.set_page_config(
    page_title="Mini Social Media",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Professional Design
st.markdown("""
    <style>
    /* Main background gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main titles */
    h1, h2 { 
        color: white !important; 
    }
    
    /* Better button styling */
    .stButton > button {
        border-radius: 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)


def test_connection():
    """Test if Django server is running"""
    try:
        response = requests.get(API_BASE_URL + "/get-posts/", timeout=2)
        return response.status_code == 200
    except:
        return False


def create_post(content, username, image_file=None):
    """Create a new post"""
    try:
        files = {}
        data = {
            'content': content,
            'username': username
        }
        
        if image_file is not None:
            files = {'image': image_file}
        
        response = requests.post(
            API_BASE_URL + "/create-post/",
            data=data,
            files=files,
            timeout=10
        )
        
        if response.status_code == 201:
            return True, "Post created successfully! 🎉"
        else:
            error_msg = response.json().get('error', 'Unknown error')
            return False, "Error: " + error_msg
    except requests.exceptions.ConnectionError:
        return False, "❌ Cannot connect to Django. Is it running?"
    except Exception as e:
        return False, "Error: " + str(e)


def get_posts():
    """Fetch all posts"""
    try:
        response = requests.get(API_BASE_URL + "/get-posts/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('posts', [])
        return []
    except:
        return []


def delete_post(post_id):
    """Delete a post"""
    try:
        url = API_BASE_URL + "/delete-post/" + str(post_id) + "/"
        response = requests.delete(url, timeout=5)
        if response.status_code == 200:
            return True, "Post deleted!"
        return False, "Failed to delete"
    except Exception as e:
        return False, "Error: " + str(e)


def add_comment(post_id, content, username):
    """Add a comment to a post"""
    try:
        data = {
            'content': content,
            'username': username
        }
        url = API_BASE_URL + "/add-comment/" + str(post_id) + "/"
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 201:
            return True, "Comment added!"
        return False, "Failed to add comment"
    except Exception as e:
        return False, "Error: " + str(e)


def display_post(post):
    """Display a single post with professional card design"""
    
    # Get username
    username = post.get('user', {}).get('username', 'Unknown')
    
    # Create post card with shadow
    st.markdown(
        '<div style="background: white; border-radius: 15px; overflow: hidden; '
        'box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin-bottom: 25px;">'
        
        # Header section with username
        '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
        'padding: 20px;">'
        '<h3 style="color: white; margin: 0; font-size: 22px; font-weight: 600;">📝 Post #' 
        + str(post["id"]) + '</h3>'
        '<p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 14px;">👤 By ' 
        + username + '</p>'
        '</div>'
        
        # Content section
        '<div style="padding: 25px; background: white;">'
        '<p style="color: #2c3e50; font-size: 18px; line-height: 1.8; margin: 0; font-weight: 400;">' 
        + str(post["content"]) + '</p>',
        unsafe_allow_html=True
    )
    
    # Display image if exists (FIXED - use_container_width instead of use_column_width)
    if post.get('image'):
        try:
            image_url = post['image']
            if not image_url.startswith('http'):
                image_url = "http://localhost:8000" + image_url
            
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                st.markdown('<div style="margin-top: 20px; border-radius: 10px; overflow: hidden;">', unsafe_allow_html=True)
                st.image(img, use_container_width=True)  # FIXED HERE
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.warning("⚠️ Could not load image: " + str(e))
    
    # Display comments
    comments = post.get('comments', [])
    comments_count = post.get('comments_count', 0)
    
    if comments_count > 0:
        st.markdown(
            '<div style="border-top: 1px solid #e0e0e0; padding-top: 15px; margin-top: 20px;">'
            '<h4 style="color: #667eea; font-size: 16px; margin-bottom: 10px;">💬 Comments (' 
            + str(comments_count) + ')</h4>',
            unsafe_allow_html=True
        )
        for comment in comments:
            comment_user = comment.get('user', {}).get('username', 'Anonymous')
            comment_text = comment.get('content', '')
            st.markdown(
                '<div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 8px;">'
                '<strong style="color: #667eea;">' + comment_user + ':</strong> '
                '<span style="color: #555;">' + comment_text + '</span>'
                '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Add comment section
    with st.expander("💬 Add a comment"):
        comment_username = st.text_input("Your name", key=f"comment_user_{post['id']}", value="Anonymous")
        comment_text = st.text_area("Your comment", key=f"comment_text_{post['id']}", height=80)
        if st.button("Send Comment", key=f"send_comment_{post['id']}", type="primary"):
            if comment_text.strip():
                success, msg = add_comment(post['id'], comment_text, comment_username)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Please write a comment first!")
    
    # Footer with timestamp and delete button
    created_at = post.get('created_at', 'Unknown')
    if created_at != 'Unknown':
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            created_at = dt.strftime('%B %d, %Y at %I:%M %p')
        except:
            pass
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(
            '<p style="color: #95a5a6; font-size: 14px; margin-top: 15px; margin-bottom: 0;">'
            '🕒 ' + str(created_at) + '</p>',
            unsafe_allow_html=True
        )
    with col2:
        button_key = "del_" + str(post['id'])
        if st.button("🗑️ Delete", key=button_key, type="secondary"):
            success, msg = delete_post(post['id'])
            if success:
                st.success(msg)
                st.rerun()
    
    # Close content div
    st.markdown('</div></div>', unsafe_allow_html=True)


def main():
    st.title("📱 Mini Social Media")
    st.markdown("### Connect, Share, Inspire! ✨")
    st.markdown("---")
    
    # Check connection
    if not test_connection():
        st.error("⚠️ Django server not running!")
        st.info("Start Django: `python manage.py runserver`")
        st.stop()
    
    # Sidebar - Create Post
    with st.sidebar:
        st.header("✍️ Create New Post")
        st.markdown("---")
        
        # Username input
        post_username = st.text_input(
            "Your name",
            value="admin",
            help="Enter your username"
        )
        
        # Text content
        post_content = st.text_area(
            "What's on your mind?",
            height=150,
            placeholder="Share your thoughts...",
            max_chars=5000
        )
        
        if post_content:
            char_count = len(post_content)
            caption_text = "📝 " + str(char_count) + " / 5000 characters"
            st.caption(caption_text)
        
        # Image upload
        uploaded_image = st.file_uploader(
            "📸 Add image (optional)",
            type=['png', 'jpg', 'jpeg', 'gif']
        )
        
        if uploaded_image:
            st.image(uploaded_image, caption="Preview", use_container_width=True)  # FIXED HERE
        
        st.markdown("---")
        
        # Submit button
        if st.button("📤 Post", type="primary", use_container_width=True):
            if not post_content.strip():
                st.error("⚠️ Write something first!")
            elif not post_username.strip():
                st.error("⚠️ Enter your name!")
            else:
                with st.spinner("Posting..."):
                    if uploaded_image:
                        uploaded_image.seek(0)
                    
                    success, msg = create_post(post_content, post_username, uploaded_image)
                    if success:
                        st.success(msg)
                        st.balloons()
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(msg)
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        posts = get_posts()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Posts", len(posts))
        with col2:
            images = len([p for p in posts if p.get('image')])
            st.metric("Images", images)
    
    # Main Feed
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("📰 Feed")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    posts = get_posts()
    if not posts:
        st.info("📭 No posts yet. Be the first!")
    else:
        for post in posts:
            display_post(post)


if __name__ == "__main__":
    main()
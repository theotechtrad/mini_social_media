# Mini Social Media

A full-stack social media web app built with Django (backend) and Streamlit (frontend).

## Live Demo

🔗 [Check it out here](https://mini-social-media-44zz.onrender.com/) *(deployed on Render)*

## Features

- Create posts with text and images
- Add comments to posts
- Real-time feed updates
- Image upload support
- Clean, modern UI with gradient design
- RESTful API architecture

## Screenshots

*(Add your screenshots here)*

## Tech Stack

**Backend:**
- Django 5.2.8
- Django REST Framework
- SQLite database
- CORS enabled

**Frontend:**
- Streamlit
- Pillow for images
- Custom CSS styling

**Deployment:**
- Gunicorn
- WhiteNoise
- Render

## Local Setup

**1. Clone the repo**
```bash
git clone https://github.com/theotechtrad/mini_social_media.git
cd mini_social_media
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run Django backend**
```bash
python manage.py migrate
python manage.py runserver
```

Backend runs on `http://localhost:8000`

**4. Run Streamlit frontend (new terminal)**
```bash
streamlit run streamlit_app.py
```

Frontend opens at `http://localhost:8501`

That's it! Both servers need to be running.

## Project Structure

```
mini_social_media/
├── config/              # Django settings
├── posts/               # Main app (models, views, serializers)
├── media/               # Uploaded images
├── manage.py            # Django management
├── streamlit_app.py     # Frontend
└── requirements.txt
```

## API Endpoints

```
POST   /api/create-post/              Create new post
GET    /api/get-posts/                Get all posts
DELETE /api/delete-post/<id>/         Delete post
POST   /api/add-comment/<post_id>/    Add comment
GET    /api/get-comments/<post_id>/   Get comments
```

## How to Use

1. Open the Streamlit app in your browser
2. Use sidebar to create posts
3. Enter your name and content
4. Upload image (optional)
5. Click Post
6. View feed and add comments

## Admin Panel

Access Django admin at `http://localhost:8000/admin/`

Create superuser:
```bash
python manage.py createsuperuser
```

## Deployment on Render

The app is deployed on Render. To deploy your own:

1. Push code to GitHub
2. Connect Render to your repo
3. Add environment variables
4. Deploy both Django and Streamlit services

## Things I Learned

- Building REST APIs with Django
- Connecting Streamlit to Django backend
- Handling file uploads
- CORS configuration
- Deployment with Gunicorn

## Future Ideas

- User authentication
- Like/unlike posts
- Profile pages
- Edit/update posts
- Better image optimization
- Pagination

## Contributing

Feel free to fork and experiment! Open issues if you find bugs.

## Contact

Himanshu Yadav - [GitHub](https://github.com/theotechtrad) | [LinkedIn](https://www.linkedin.com/in/hvhimanshu-yadav)

---

Built with Django + Streamlit | Deployed on Render

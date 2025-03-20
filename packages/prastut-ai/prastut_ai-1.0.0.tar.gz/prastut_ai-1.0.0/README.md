# Prastut AI - Face Recognition Attendance System

A modern face recognition-based attendance system built with Python (Flask) backend and React frontend.

## Features

- Real-time face detection and recognition
- Attendance tracking and management
- Modern React-based user interface
- Deep learning-powered face recognition using TensorFlow and PyTorch
- Cloud-based storage using Firebase and Pinecone
- Cross-platform support (Windows, macOS, Linux)

## Prerequisites

- Python 3.8 or higher
- Node.js 18.0 or higher
- npm 8.0 or higher
- CMake (for building dependencies)
- C++ build tools (for compiling native modules)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prastut-ai.git
cd prastut-ai
```

2. Install all dependencies (both frontend and backend):
```bash
npm run install:all
```

Or install separately:

For backend:
```bash
npm run install:backend
```

For frontend:
```bash
npm run install:frontend
```

## Development

Start both servers (backend and frontend):
```bash
npm start
```

Or start separately:

Backend server:
```bash
npm run start:backend
```

Frontend development server:
```bash
npm run start:frontend
```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:5000`.

## Scripts

- `npm start` - Start both backend and frontend servers
- `npm run start:backend` - Start only the backend server
- `npm run start:frontend` - Start only the frontend development server
- `npm run install:all` - Install all dependencies (both backend and frontend)
- `npm run install:backend` - Install backend dependencies
- `npm run install:frontend` - Install frontend dependencies
- `npm run build:frontend` - Build the frontend for production
- `npm run test` - Run backend tests
- `npm run lint:frontend` - Lint frontend code
- `npm run format:frontend` - Format frontend code
- `npm run clean` - Clean up build artifacts and dependencies

## Project Structure

```
prastut-ai/
├── app/                    # Frontend React application
│   ├── src/               # React source files
│   ├── public/            # Static files
│   └── package.json       # Frontend dependencies
├── backend/               # Backend Flask application
│   ├── venv/             # Python virtual environment
│   ├── Face_attend.py    # Main backend application
│   └── requirements.txt   # Backend dependencies
├── logs/                  # Application logs
├── package.json          # Project configuration
└── start.sh             # Development server startup script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [TensorFlow](https://www.tensorflow.org/)
- [PyTorch](https://pytorch.org/)
- [FaceNet](https://github.com/timesler/facenet-pytorch)
- [DeepFace](https://github.com/serengil/deepface)
- [React](https://reactjs.org/)
- [Flask](https://flask.palletsprojects.com/)

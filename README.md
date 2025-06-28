# Travel Planning Application

An AI-powered travel planning application that uses Vertex AI (Google Gemini) to generate personalized travel itineraries, provide digital guides, and discover hidden gems.

## Features

- **Itinerary Generator**: Create detailed day-by-day travel itineraries based on your destination, duration, interests, and preferences.
- **Digital Guide**: Get expert information on specific locations and topics, including historical context, cultural insights, and practical visitor information.
- **Hidden Gems**: Discover lesser-known attractions and experiences that match your preferences at your destination.

## Project Structure

- `travel-app-backend/`: Flask backend that communicates with Vertex AI
- `travel-app-frontend/`: React Native (Expo) mobile application

## Backend Setup

1. Navigate to the backend directory:
   ```
   cd travel-app-backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

6. Edit the `.env` file with your Vertex AI credentials.

7. Start the backend server:
   ```
   python app.py
   ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd travel-app-frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Update the API base URL:
   - Open `src/config/api.js`
   - Change `API_BASE_URL` to your computer's local IP address (for testing on physical devices)
   - For Android emulator, use `10.0.2.2` instead of `localhost`

4. Start the Expo development server:
   ```
   npm start
   ```

5. Run on your device:
   - Scan the QR code with the Expo Go app (iOS/Android)
   - Press 'a' to run on Android emulator
   - Press 'i' to run on iOS simulator

## Environment Setup

### Vertex AI Setup

1. Create a Google Cloud Platform account and enable Vertex AI API
2. Generate an API key for Vertex AI or set up a service account
3. Add credentials to the `.env` file

## License

[MIT License](LICENSE) 
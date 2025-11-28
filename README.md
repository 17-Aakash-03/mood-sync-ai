Mood Sync AI

Automated Environmental Adaptation System Based on Facial Emotion Recognition

Mood Sync AI is an intelligent desktop automation tool designed to enhance user productivity and emotional well-being. By utilizing Computer Vision and Artificial Intelligence, the system analyzes the user's facial expressions in real-time via a webcam. Based on the detected mood (e.g., Happy, Focused, Tired, Angry) and the user's age group, the system automatically synchronizes the digital environment. This includes adjusting the IDE (VS Code) theme colors, recommending tailored music playlists (YouTube), suggesting mood-regulating activities, and providing motivational quotes. The system employs a hybrid AI architecture, utilizing the Face++ Cloud API for high-precision emotion detection with a local DeepFace fallback.

About the Project

This project is a Behavioral Active Adaptation System designed to align digital workspaces with human emotional states. Unlike traditional mood tracking applications that rely on manual user input or simple text analysis, this system monitors facial cues in real-time.

If the user exhibits signs of stress, fatigue, or high energy, the system acts as a digital wellness companion: it instantly identifies the emotional state and modifies the environment to either amplify positive states or mitigate negative ones before productivity is impacted.

Problems Solved

This project addresses three critical gaps in digital work environments:

Static Workspaces
Traditional software interfaces remain static regardless of the user's mental state. A bright white screen during a late-night coding session can exacerbate fatigue. This project solves that by dynamically adjusting interface themes to match emotional needs (e.g., soothing colors for stress).

Emotional Latency
Users often fail to recognize their own fatigue or stress until they are already burnt out. This system detects early signs of "Sleepiness" or "Anger" via micro-expressions and eye-status analysis, prompting intervention before the user reaches a breaking point.

Decision Fatigue
When feeling low or unfocused, users often waste time deciding what music to play or how to take a break. By automating content curation (music, activities, quotes), the system removes this cognitive load, allowing the user to reset instantly.

How It Works (The Logic)

The system operates on a "Sense → Analyze → Adapt" cycle:

Sense (Input)
The system activates the webcam and captures a high-resolution frame of the user. It simultaneously collects demographic context (Age Group) via user input.

Analyze (Processing)
The image is sent to the primary Cloud AI node (Face++) for deep analysis.

Emotion Scoring: It calculates confidence scores for 7 distinct emotions (Happy, Sad, Angry, etc.).

Eye Status: It measures the "closed" percentage of both left and right eyes. If the average exceeds 50%, it triggers a "Sleepy" override.

Fallback: If the cloud service is unreachable, it seamlessly switches to the local DeepFace neural network.

Adapt (Output)
Based on the dominant emotion, the system executes a multi-threaded response:

Visual: Modifies the VS Code settings.json file to repaint window borders.

Auditory: Launches a specific YouTube playlist via the system's web browser.

Cognitive: Fetches a relevant quote from an external API and displays tailored activity suggestions.

Results

Reaction Time: The system typically adapts the environment within 2-4 seconds of scan initiation (dependent on network latency for Cloud API).

Accuracy: The integration of Cloud AI improved emotion detection accuracy significantly over purely local models, particularly in distinguishing between "Surprise" and "Happiness."

Drowsiness Detection: The eye-status logic successfully identifies fatigue in over 90% of test cases, providing a critical intervention tool for late-night workers.

Tech Stack

Language: Python 3.x

Computer Vision: OpenCV (cv2)

Cloud AI: Face++ (FacePlusPlus) API

Local AI: DeepFace (TensorFlow/Keras wrapper)

Automation: os, json (File IO), webbrowser

Prerequisites

Before running the project, ensure you have the following installed:

Python 3.x installed on your machine.

Visual Studio Code (Optional, but required for the theme sync feature).

Webcam connected and accessible.

Installation

Clone the Repository

git clone [https://github.com/yourusername/mood-sync-ai.git](https://github.com/yourusername/mood-sync-ai.git)
cd mood-sync-ai


Install Dependencies

pip install opencv-python deepface requests


Configure API Keys

Sign up for a free account at Face++ Console.

Open mood_sync_ai.py.

Paste your API Key and Secret in the configuration section:

API_KEY = "your_key_here"
API_SECRET = "your_secret_here"


Usage

Run the Script
Open your terminal (VS Code or Command Prompt) and run:

python mood_sync_ai.py


Select Your Age Group
Follow the on-screen menu to select your demographic. This tailors the recommendations (e.g., "Play a game" vs. "Review budget").

Strike a Pose

The camera window will open titled "Mood Sync Mirror".

Adjust your lighting and expression.

Press s to Scan your face.

Press q to Quit.

Experience the Sync

Your terminal will display the detected mood and confidence scores.

VS Code borders will instantly change color.

A YouTube playlist will open in your browser.

A customized Activity and Quote will be printed.

Troubleshooting

Camera not opening?
Ensure no other app (Zoom, Teams) is using the webcam. Restart the terminal.

"Face++ Error" or "Connection Error"?
The script will automatically fallback to the Local AI (DeepFace). This is normal if you are offline or have an invalid API key.

VS Code colors not changing?
Ensure you are running the script inside the root folder of the VS Code workspace you want to colorize.

Disclaimer

This tool is designed for productivity and entertainment purposes. It is not a medical device and should not be used for diagnosing mental health conditions. The emotion detection is probabilistic and based on facial muscle analysis.

License

Distributed under the MIT License. See LICENSE for more information.

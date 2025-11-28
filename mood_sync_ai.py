import cv2
from deepface import DeepFace
import json
import os
import random
import datetime
import requests
import webbrowser

API_KEY = "YOUR_FACE_PLUS_PLUS_API_KEY"
API_SECRET = "YOUR_FACE_PLUS_PLUS_API_SECRET"

USE_CLOUD_API = True 
API_URL = "https://api-us.faceplusplus.com/facepp/v3/detect"

MOOD_MAP = {
    "happy": {
        "label": "POSITIVE",
        "expressions": ["( ^_^ )", "( 😆 )", "( 😎 )", "( 😌 )", "( 🥰 )"],
        "color": "#F4D03F",
        "song": "https://www.youtube.com/watch?v=jv-pYB0Qw9A", 
        "msg": "Vibe Check: Radiant. High energy detected.",
        "food": "Ice Cream or Iced Coffee.",
        "activities": {"1": "Play a game.", "2": "Drive/Walk.", "3": "Plan a trip.", "4": "Host dinner.", "5": "Gardening."},
        "movies": {"1": "Lego Movie", "2": "Ferris Bueller", "3": "La La Land", "4": "Mamma Mia", "5": "Singin' in Rain"}
    },
    "sad": {
        "label": "LOW ENERGY",
        "expressions": ["( u_u )", "( =_= )", "( ._. )", "( 😵‍💫 )"],
        "color": "#85929E",
        "song": "https://www.youtube.com/watch?v=D5147zORrGU", 
        "msg": "Vibe Check: Heavy. It is okay to slow down.",
        "food": "Hot Cocoa or Soup.",
        "activities": {"1": "Watch cartoons.", "2": "Journal.", "3": "Yin Yoga.", "4": "Nature walk.", "5": "Photo albums."},
        "movies": {"1": "Inside Out", "2": "Eternal Sunshine", "3": "Good Will Hunting", "4": "Shawshank", "5": "It's a Wonderful Life"}
    },
    "angry": {
        "label": "HIGH ENERGY/NEGATIVE",
        "expressions": ["( 😠 )", "( 😤 )", "( 😒 )", "( 😣 )", "( 😡 )", "( 🤬 )", "( 👿 )", "( 💢 )"],
        "color": "#C0392B",
        "song": "https://www.youtube.com/watch?v=WT2JOLqZBCM", 
        "msg": "Vibe Check: Volatile. Channel this heat.",
        "food": "Crunchy Snacks or Cold Water.",
        "activities": {"1": "Sprint outside.", "2": "Gym/Weights.", "3": "Clean house.", "4": "Power walk.", "5": "Breathing exercises."},
        "movies": {"1": "Kung Fu Panda", "2": "Fight Club", "3": "Mad Max", "4": "Gladiator", "5": "Rocky"}
    },
    "neutral": {
        "label": "BALANCED",
        "expressions": ["( 😌 )", "( 🤔 )", "( 👉👈 )"],
        "color": "#2E4053",
        "song": "https://www.youtube.com/watch?v=83ILtWq7HX0", 
        "msg": "Vibe Check: Steady. Ready to build.",
        "food": "Green Tea or Nuts.",
        "activities": {"1": "Build LEGOs.", "2": "Study.", "3": "Budgeting.", "4": "Read news.", "5": "Crossword."},
        "movies": {"1": "Wall-E", "2": "Social Network", "3": "Interstellar", "4": "Spotlight", "5": "12 Angry Men"}
    },
    "fear": {
        "label": "ANXIOUS",
        "expressions": ["( 😨 )", "( 😰 )", "( 😳 )"],
        "color": "#A2D9CE",
        "song": "https://www.youtube.com/watch?v=xuDhu7aNH4M", 
        "msg": "Vibe Check: Unstable. Deep breath in...",
        "food": "Chamomile Tea.",
        "activities": {"1": "Hug a pet.", "2": "Text a friend.", "3": "Box Breathing.", "4": "List worries.", "5": "Call family."},
        "movies": {"1": "Finding Nemo", "2": "Paddington 2", "3": "Walter Mitty", "4": "The Terminal", "5": "Sound of Music"}
    },
    "surprise": {
        "label": "SHOCK",
        "expressions": ["( 😯 )", "( 😲 )"],
        "color": "#E67E22",
        "song": "https://www.youtube.com/watch?v=kPNsevIaxWw", 
        "msg": "Vibe Check: Plot Twist.",
        "food": "Popcorn or Sweets.",
        "activities": {"1": "Tell a friend.", "2": "Research topic.", "3": "Brainstorm.", "4": "Walk it off.", "5": "Reflect."},
        "movies": {"1": "Zootopia", "2": "Knives Out", "3": "Parasite", "4": "Sixth Sense", "5": "Psycho"}
    },
    "disgust": {
        "label": "REJECTION",
        "expressions": ["( 🤢 )", "( 🤨 )"],
        "color": "#7DCEA0",
        "song": "https://www.youtube.com/watch?v=WZf9YXNOyZo", 
        "msg": "Vibe Check: Glitch detected.",
        "food": "Water with Lemon.",
        "activities": {"1": "Change room.", "2": "Drink water.", "3": "Clean up.", "4": "Fresh air.", "5": "Herbal tea."},
        "movies": {"1": "Ratatouille", "2": "Spirited Away", "3": "Amelie", "4": "Truman Show", "5": "Casablanca"}
    },
    "sleepy": {
        "label": "TIRED / DROWSY",
        "expressions": ["( 😴 )", "( 💤 )", "( -_- )zzZ"],
        "color": "#4A235A",
        "song": "https://www.youtube.com/watch?v=tphyy-5cCB4",
        "msg": "Vibe Check: Low Battery. Recharge required.",
        "food": "Warm Milk or Decaf Tea.",
        "activities": {"1": "Take a nap.", "2": "Listen to rain sounds.", "3": "Meditation.", "4": "Stretch gently.", "5": "Go to bed early."},
        "movies": {"1": "Fantasia", "2": "Midnight in Paris", "3": "Lost in Translation", "4": "The Big Blue", "5": "March of the Penguins"}
    }
}

def set_vscode_color(hex_code):
    settings_path = os.path.join(os.getcwd(), ".vscode", "settings.json")
    if not os.path.exists(os.path.join(os.getcwd(), ".vscode")):
        os.makedirs(os.path.join(os.getcwd(), ".vscode"))
    data = {}
    if os.path.exists(settings_path):
        with open(settings_path, "r") as f:
            try: data = json.load(f)
            except: data = {}
    data["workbench.colorCustomizations"] = {
        "activityBar.background": hex_code,
        "titleBar.activeBackground": hex_code,
        "statusBar.background": hex_code
    }
    with open(settings_path, "w") as f:
        json.dump(data, f, indent=4)

def log_mood_to_file(mood, age_group):
    with open("mood_history.txt", "a") as f:
        f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mood: {mood.upper()} | Age: {age_group}\n")

def get_quote_from_api(mood):
    try:
        r = requests.get("https://api.quotable.io/random?maxLength=100", timeout=2)
        if r.status_code == 200: return f"\"{r.json()['content']}\" - {r.json()['author']}"
    except: pass
    return "Offline mode: Believe in yourself."

def analyze_with_faceplusplus(image_path):
    print("☁️ Sending to Face++ Cloud (Timeout: 10s)...")
    try:
        data = {
            "api_key": API_KEY,
            "api_secret": API_SECRET,
            "return_attributes": "emotion,eyestatus" 
        }
        files = {"image_file": open(image_path, "rb")}
        
        response = requests.post(API_URL, data=data, files=files, timeout=10)
        result = response.json()
        
        if "error_message" in result:
            print(f"⚠️ Face++ Error: {result['error_message']}")
            return None, None

        if "faces" in result and len(result["faces"]) > 0:
            face = result["faces"][0]
            emotions = face["attributes"]["emotion"]
            eyestatus = face["attributes"]["eyestatus"]
            
            
            emotions["happy"] = emotions.pop("happiness")
            emotions["sad"] = emotions.pop("sadness")
            emotions["angry"] = emotions.pop("anger") 
            
            left_closed = eyestatus["left_eye_status"]["no_glass_eye_close"] + eyestatus["left_eye_status"]["normal_glass_eye_close"] + eyestatus["left_eye_status"]["dark_glasses"]
            right_closed = eyestatus["right_eye_status"]["no_glass_eye_close"] + eyestatus["right_eye_status"]["normal_glass_eye_close"] + eyestatus["right_eye_status"]["dark_glasses"]
            avg_closed = (left_closed + right_closed) / 2.0

            print("\n" + "-"*30)
            print("☁️ FACE++ RAW DATA:")
            print(f"   Happy:    {emotions['happy']}%")
            print(f"   Surprise: {emotions['surprise']}%")
            print(f"   Angry:    {emotions['angry']}%")
            print(f"   Sad:      {emotions['sad']}%")
            print(f"   Fear:     {emotions['fear']}%")
            print(f"   Eyes Closed: {avg_closed:.1f}%")
            print("-"*30 + "\n")

            dominant = max(emotions, key=emotions.get)
            
            if avg_closed > 50.0:
                dominant = "sleepy"
                print("💡 Eyes detected CLOSED (>50%). Switching to SLEEPY mode.")

            return dominant, emotions
        else:
            print("☁️ Face++: No face detected in the image.")
            return "neutral", {}
            
    except Exception as e:
        print(f"⚠️ Connection Error (Using Fallback): {e}")
        return None, None

def get_mood_from_camera():
    print("\n📷 Opening Camera... PRESS 's' TO SCAN | 'q' TO QUIT")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): return "neutral"

    while True:
        ret, frame = cap.read()
        if not ret: break
        cv2.putText(frame, "Mood Sync: Press 's' to Scan", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Mood Sync Mirror', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            cv2.imwrite("temp_face.jpg", frame)
            break
        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()
    
    dom, scores = analyze_with_faceplusplus("temp_face.jpg")
    
    if not scores:
        print("🏠 Falling back to Local AI (DeepFace)... (Please Wait)")
        try:
            analysis = DeepFace.analyze(img_path = "temp_face.jpg", actions = ['emotion'])
            dom = analysis[0]['dominant_emotion']
            print(f"🏠 Local Detected: {dom.upper()}")
        except:
            print("⚠️ Local AI Failed. Defaulting to Neutral.")
            dom = "neutral"

    if os.path.exists("temp_face.jpg"): os.remove("temp_face.jpg")
    return dom

def get_user_age():
    print("\n" + "╔" + "═"*40 + "╗")
    print("║" + " "*12 + "SELECT AGE GROUP" + " "*12 + "║")
    print("╠" + "═"*40 + "╣")
    print("║ 1. Under 15  (Child/Teen)             ║")
    print("║ 2. 15 - 24   (Student/Young Adult)    ║")
    print("║ 3. 25 - 40   (Professional)           ║")
    print("║ 4. 41 - 60   (Mid-Life)               ║")
    print("║ 5. 60+       (Senior)                 ║")
    print("╚" + "═"*40 + "╝")
    
    while True:
        c = input("\n👉 Enter Choice (1-5): ").strip()
        if c in ["1","2","3","4","5"]: return c
        print("❌ Invalid. Please type 1, 2, 3, 4, or 5.")

def run_mood_sync():
    mood = get_mood_from_camera()
    if mood is None: return 
    age = get_user_age()
    
    log_mood_to_file(mood, age)
    cfg = MOOD_MAP.get(mood, MOOD_MAP["neutral"])
    
    print("\n" + "="*40)
    print(f"🟢 RESULT: {mood.upper()}")
    print("="*40)
    print(f"   {random.choice(cfg['expressions'])}")
    print(f"> {cfg['msg']}")
    set_vscode_color(cfg['color'])
    print(f"📜 {get_quote_from_api(mood)}")
    print(f"🎧 {cfg['song']}")
    print(f"🧩 {cfg['activities'].get(age, '')}")
    print(f"🎬 {cfg['movies'].get(age, '')}")
    print(f"🍵 {cfg.get('food', '')}")

    webbrowser.open(cfg['song'])
    
    print("-" * 40 + "\n")

if __name__ == "__main__":
    run_mood_sync()
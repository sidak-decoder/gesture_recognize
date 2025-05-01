from tkinter import *
def gestures():
    import cv2
    import math
    import datetime
    import pyttsx3
    import mediapipe
    from PIL import Image, ImageTk

    # Initialize MediaPipe for hand detection and drawing utilities
    mp_drawing = mediapipe.solutions.drawing_utils
    mp_hands = mediapipe.solutions.hands

    # Define the SignLanguageConverter class
    class SignLanguageConverter:
        def __init__(self):
            # Initialize MediaPipe Hands
            self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, 
                                        min_detection_confidence=0.7, min_tracking_confidence=0.5)
            self.current_gesture = None
            self.CountGesture = StringVar()

        # Detect gesture from the hand landmarks in the given image
        def detect_gesture(self, image):
            results = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                self.current_gesture = self.get_gesture(hand_landmarks)
        
        # Determine the gesture based on hand landmarks
        def get_gesture(self, hand_landmarks):
            thumb_tip = hand_landmarks.landmark[4]
            index_finger_tip = hand_landmarks.landmark[8]
            middle_finger_tip = hand_landmarks.landmark[12]
            ring_finger_tip = hand_landmarks.landmark[16]
            little_finger_tip = hand_landmarks.landmark[20]

            # Check for Punch gesture
            if thumb_tip.y < index_finger_tip.y and thumb_tip.x < index_finger_tip.x:
                self.CountGesture.set('Punch..!')
                return "punch"
            # Check for OK gesture
            elif thumb_tip.y < index_finger_tip.y < middle_finger_tip.y < ring_finger_tip.y < little_finger_tip.y:
                self.CountGesture.set('Okay')
                return "Okay"
            # Check for Dislike gesture
            elif thumb_tip.y > index_finger_tip.y > middle_finger_tip.y > ring_finger_tip.y > little_finger_tip.y:
                self.CountGesture.set('I dislike It')
                return "Dislike"
            # Check for Victory gesture
            elif index_finger_tip.y < middle_finger_tip.y and abs(index_finger_tip.x - middle_finger_tip.x) < 0.2:
                self.CountGesture.set('We Won! Victory')
                return "Victory"
            # Check for Stop gesture
            elif thumb_tip.x < index_finger_tip.x < middle_finger_tip.x:
                if (hand_landmarks.landmark[2].x < hand_landmarks.landmark[5].x and 
                    hand_landmarks.landmark[3].x < hand_landmarks.landmark[5].x and 
                    hand_landmarks.landmark[4].x < hand_landmarks.landmark[5].x):
                    self.CountGesture.set('STOP! Dont Move.')
                    return "Stop"
            else:
                # Check for Point gesture
                wrist = hand_landmarks.landmark[0]
                index_finger = (index_finger_tip.x, index_finger_tip.y, index_finger_tip.z)
                wrist_coords = (wrist.x, wrist.y, wrist.z)
                vector = (index_finger[0] - wrist_coords[0], index_finger[1] - wrist_coords[1], index_finger[2] - wrist_coords[2])
                vector_len = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
                vector_unit = (vector[0] / vector_len, vector[1] / vector_len, vector[2] / vector_len)
                reference_vector = (0, 0, -1)
                dot_product = sum(v * r for v, r in zip(vector_unit, reference_vector))
                angle = math.acos(dot_product) * 180 / math.pi
                if 20 < angle < 80:
                    self.CountGesture.set('Hey You!!')
                    return "Point"
        # Get the current gesture detected
        def get_current_gesture(self):
            return self.current_gesture

        # Release resources
        def release(self):
            self.hands.close()

    # Function to update the clock every second
    def update_clock():
        now = datetime.datetime.now()
        clock.config(text=now.strftime("%H:%M:%S"))
        clock.after(1000, update_clock)

    # Function to use pyttsx3 to speak the detected gesture
    def voice():
        engine = pyttsx3.init()
        engine.say(sign_lang_conv.CountGesture.get())
        engine.runAndWait()

    # Function to capture image from webcam, detect gestures and update the GUI
    def select_img():
        _, frame = cap.read()
        sign_lang_conv.detect_gesture(frame)
        gesture = sign_lang_conv.get_current_gesture()
        if gesture:
            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        results = sign_lang_conv.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(framergb)
        finalImage = ImageTk.PhotoImage(image)
        label1.configure(image=finalImage)
        label1.image = finalImage

        crrgesture.config(text='Current Gesture:')
        status.config(textvariable=sign_lang_conv.CountGesture)
        win.after(1, select_img)

    # GUI Setup
    win = Tk()
    width, height = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"{width}x{height}")
    win.title('Gesture Recognition')

    # Load background image
    background_image = Image.open("back.jpg")
    background_image = background_image.resize((width, height))
    background_photo = ImageTk.PhotoImage(background_image)

    # Place background image on the main window
    background_label = Label(win, image=background_photo)
    background_label.place(x=0, y=0)

    # Title label
    Label(win, text='Gesture Recognition & Navigation', font=('Comic Sans MS', 20, 'bold'), 
        bd=5, bg='#20262E', fg='#F5EAEA', relief=GROOVE, width=5000).pack(pady=20, padx=500)

    # Name label
    name = Label(win, text='Vanshdeep and Sidakpreet singh', font=('Verdana', 10, 'bold'), 
                relief=GROOVE, width=30, bd=5, fg="#F5EAEA", bg="#20262E")
    name.place(x=1200, y=650)

    # Roll number label
    rollno = Label(win, text='764/22 & 755/22', font=('Verdana', 14, 'bold'), 
                relief=GROOVE, width=22, bd=5, fg="#F5EAEA", bg="#20262E")
    rollno.place(x=1200, y=700)

    # Clock label
    clock = Label(win, font=("Arial", 20), relief=GROOVE, width=15, bd=5, fg="#F5EAEA", bg="#20262E")
    clock.pack(anchor=NW, padx=150, pady=10)
    clock.place(x=100, y=350)

    # Calendar label
    cal = Label(win, font=("Arial", 20), relief=GROOVE, width=15, bd=5, fg="#F5EAEA", bg="#20262E")
    cal.pack(anchor=NW, padx=150, pady=10)
    cal.place(x=100, y=400)

    # Update clock and calendar
    update_clock()
    cal.config(text=datetime.date.today().strftime("%B %d, %Y"))

    # Exit button
    exit_button = Button(win, text='Log Out', padx=95, bg='#20262E', fg='#F5EAEA', relief=GROOVE, width=7, bd=5, 
                        font=('Verdana', 14, 'bold'), command=win.destroy)
    exit_button.place(x=1200, y=400)

    # Voice button
    voice_button = Button(win, text='Sound', padx=95, bg='#20262E', fg='#F5EAEA', relief=GROOVE, width=7, bd=5, 
                        font=('Verdana', 14, 'bold'), command=voice)
    voice_button.place(x=1200, y=350)

    # Gesture Status Labels
    crrgesture = Label(win, text='Current Gesture :', font=('Calibri', 18, 'bold'), bd=5, bg='#20262E', 
                    width=15, fg='#F5EAEA', relief=GROOVE)
    crrgesture.place(x=200, y=700)

    status = Label(win, font=('Georgia', 18, 'bold'), bd=5, bg='#20262E', width=30, fg='#F5EAEA', relief=GROOVE)
    status.place(x=520, y=700)

    # Video Capture
    cap = cv2.VideoCapture(0)
    label1 = Label(win, width=640, height=480)
    label1.place(x=450, y=150)

    # Initialize SignLanguageConverter
    sign_lang_conv = SignLanguageConverter()
    select_img()

    # Start the main loop
    win.mainloop()


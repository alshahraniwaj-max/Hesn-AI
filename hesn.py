from nicegui import ui
import base64, os, numpy as np
from datetime import datetime
from openai import OpenAI
from scipy.io import wavfile

client = OpenAI(api_key="sk-UB_9FT3UoOvALB9g2CmdKg", base_url="https://elmodels.ngrok.app/v1")

DOCTORS_FILES = {
    "د. وجن": "Wajan.wav", "د. ميلاف": "milaf.wav",
    "د. شهد": "shahad.wav", "د. جوري": "jury.wav",
    "د. دانه": "danh.wav", "د. خوله": "خوله.wav"
}

def get_voice_signature(file_path):
    try:
        sr, data = wavfile.read(file_path)
        if len(data.shape) > 1:
            data = data[:, 0]
        fft_data = np.abs(np.fft.rfft(data[:sr*2]))
        return fft_data / (np.max(fft_data) + 1e-9)
    except:
        return None

def navigate(page_name):
    dashboard_content.set_visibility(page_name == 'dashboard')
    doctors_content.set_visibility(page_name == 'doctors')
    dash_btn.classes(replace='nav-btn btn-selected' if page_name == 'dashboard' else 'nav-btn btn-idle')
    docs_btn.classes(replace='nav-btn btn-selected' if page_name == 'doctors' else 'nav-btn btn-idle')

async def handle_audio_data(msg):
    status_label.set_text("جاري التحقق من بصمة الصوت...")
    try:
        audio_b64 = msg.args['audio']
        audio_bytes = base64.b64decode(audio_b64.split(',')[1])
        temp_file = "temp_voice.wav"

        with open(temp_file, "wb") as f:
            f.write(audio_bytes)

        current_sig = get_voice_signature(temp_file)
        best_doctor, min_dist = "د. وجن", float('inf')

        if current_sig is not None:
            for name, path in DOCTORS_FILES.items():
                if os.path.exists(path):
                    saved_sig = get_voice_signature(path)
                    if saved_sig is not None:
                        ml = min(len(current_sig), len(saved_sig))
                        dist = np.linalg.norm(current_sig[:ml] - saved_sig[:ml])
                        if dist < min_dist:
                            min_dist, best_doctor = dist, name

        with open(temp_file, "rb") as f:
            res = client.audio.transcriptions.create(model="elm-asr", file=f)

        add_entry_to_ui(best_doctor, res.text)
        status_label.set_text("تم التوثيق بنجاح ✅")

    except:
        status_label.set_text("خطأ في الاتصال! أعد المحاولة")

#  CSS + Wave Animation
ui.add_head_html('''
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600&display=swap" rel="stylesheet">
<style>
body { background-color: #f8fafc; font-family: 'IBM Plex Sans Arabic', sans-serif; }
.q-drawer { background-color: #0f172a !important; }
.main-card { border-radius: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.06); border: none; }

.nav-btn { 
    width: 100% !important; height: 60px !important; border-radius: 12px !important; 
    margin-bottom: 8px !important; transition: all 0.2s ease !important;
    justify-content: flex-start !important; text-transform: none !important;
}
.nav-btn:active { transform: scale(0.96) !important; }

.btn-selected { background-color: #2563eb !important; color: white !important; }
.btn-idle { background-color: transparent !important; color: #94a3b8 !important; }

.siri-wave {
    display: flex;
    gap: 6px;
    align-items: center;
    justify-content: center;
    height: 60px;
}

.siri-bar {
    width: 6px;
    height: 20px;
    background: #2563eb;
    border-radius: 10px;
    animation: wave 1s infinite ease-in-out;
}

.siri-bar:nth-child(2) { animation-delay: 0.1s; }
.siri-bar:nth-child(3) { animation-delay: 0.2s; }
.siri-bar:nth-child(4) { animation-delay: 0.3s; }
.siri-bar:nth-child(5) { animation-delay: 0.4s; }

@keyframes wave {
    0%, 100% { height: 10px; opacity: 0.4; }
    50% { height: 50px; opacity: 1; }
}
</style>
''')

#  Header
with ui.header().classes('bg-white text-slate-900 border-b py-5 px-10 justify-between items-center'):
    with ui.row().classes('items-center gap-4'):
        ui.button(on_click=lambda: side_menu.toggle(), icon='menu').props('flat color=slate-900')
        ui.label('حِـصْـن').classes('text-4xl font-bold text-blue-900')
    ui.avatar('person', color='blue-600', text_color='white')

# 🔥 Sidebar
with ui.left_drawer(value=True).classes('p-4') as side_menu:
    ui.label('حِـصـن').classes('text-3xl text-blue-400 text-center')

    dash_btn = ui.button('لوحة التحكم', on_click=lambda: navigate('dashboard')).classes('nav-btn btn-selected')
    docs_btn = ui.button('الأطباء المعتمدين', on_click=lambda: navigate('doctors')).classes('nav-btn btn-idle')

#  Dashboard
with ui.column().classes('w-full p-12 items-center') as dashboard_content:
    with ui.card().classes('w-full max-w-4xl p-20 main-card items-center mt-8 bg-white'):
        ui.label('التوثيق').classes('text-5xl font-bold')

        status_label = ui.label('بانتظار تسجيل الأمر الطبي').classes('text-blue-700')

        ui.button('ابدأ التسجيل', on_click=lambda: ui.run_javascript('startRecording()')).classes('bg-blue-600 text-white px-10 py-4 rounded-xl')
        ui.button('إيقاف وإرسال', on_click=lambda: ui.run_javascript('stopRecording()')).classes('bg-black text-white px-10 py-4 rounded-xl')

        # 🔥 Siri Wave
        ui.html('''
        <div id="siriWave" class="siri-wave" style="display:none;">
            <div class="siri-bar"></div>
            <div class="siri-bar"></div>
            <div class="siri-bar"></div>
            <div class="siri-bar"></div>
            <div class="siri-bar"></div>
        </div>
        ''')

    timeline = ui.column()

#  Doctors Page
with ui.column().classes('w-full p-12 items-center').style('display:none') as doctors_content:
    ui.label('الأطباء المعتمدين')
    for name in DOCTORS_FILES:
        ui.label(name)

def add_entry_to_ui(doctor, text):
    with timeline:
        ui.label(f"{doctor}: {text}")

#  JS Recording + Wave Control
ui.add_head_html('''
<script>
let mediaRecorder;
let audioChunks = [];

function toggleWave(show) {
    const wave = document.getElementById("siriWave");
    if (wave) wave.style.display = show ? "flex" : "none";
}

async function startRecording() {
    audioChunks = [];
    toggleWave(true);

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

    mediaRecorder.onstop = async () => {
        toggleWave(false);

        const blob = new Blob(audioChunks, { type: "audio/wav" });
        const reader = new FileReader();
        reader.readAsDataURL(blob);

        reader.onloadend = () => emitEvent("audio_ready", { audio: reader.result });

        stream.getTracks().forEach(t => t.stop());
    };

    mediaRecorder.start();
}

function stopRecording() {
    if (mediaRecorder) mediaRecorder.stop();
}
</script>
''')

ui.on('audio_ready', handle_audio_data)

ui.run(port=8888, reload=False, title="حِـصْـن")
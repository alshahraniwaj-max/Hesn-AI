from nicegui import ui
import base64, os, numpy as np
from datetime import datetime
from openai import OpenAI
from scipy.io import wavfile

client = OpenAI(api_key="sk-UB_9FT3UoOvALB9g2CmdKg", base_url="https://elmodels.ngrok.app/v1")



def navigate(page_name):
    dashboard_content.set_visibility(page_name == 'dashboard')
    doctors_content.set_visibility(page_name == 'doctors')
    dash_btn.classes(replace='nav-btn btn-selected' if page_name == 'dashboard' else 'nav-btn btn-idle')
    docs_btn.classes(replace='nav-btn btn-selected' if page_name == 'doctors' else 'nav-btn btn-idle')

entry_counter = 0

async def handle_audio_data(msg):
    global entry_counter
    status_label.set_text("جاري تحويل الصوت إلى نص...")

    try:
        audio_b64 = msg.args['audio']
        audio_bytes = base64.b64decode(audio_b64.split(',')[1])
        temp_file = "temp_voice.wav"

        with open(temp_file, "wb") as f:
            f.write(audio_bytes)

        with open(temp_file, "rb") as f:
            res = client.audio.transcriptions.create(
                model="elm-asr",
                file=f
            )

        entry_counter += 1
        add_entry_to_ui(res.text)

        status_label.set_text("تم التوثيق بنجاح ✅")

    except:
        status_label.set_text("خطأ في التسجيل! أعد المحاولة")
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

#  Sidebar
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

        #  Siri Wave
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
    ui.label('لا يوجد أطباء مضافين')
  

def add_entry_to_ui(text):
    global entry_counter
    entry_counter += 1
    now = datetime.now().strftime("%H:%M:%S")

    with timeline:
        with ui.card().classes("w-full p-3 mb-2"):
            
            
            ui.label(f"🕒 {now}").classes("text-xs text-gray-400")

            
            with ui.row().classes("items-center gap-2 mt-1"):

                ui.label(f"{entry_counter}")

                ui.label("👨‍⚕️")

                ui.label(text).classes("text-slate-700")

    ui.run_javascript("console.log('entry added');")
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
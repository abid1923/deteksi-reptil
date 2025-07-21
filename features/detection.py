import streamlit as st
from services.detection_service import detect_image
from services.history_service import save_detection_history
from services.quiz_service import get_quiz_questions, get_reptile_fact
from utils.image_utils import resize_image

def reset_detection_state():
    st.session_state.current_detection = None
    st.session_state.detected_classes = []
    st.session_state.detection_saved = False
    if 'result_image' in st.session_state:
        del st.session_state.result_image
    for key in list(st.session_state.quiz_state.keys()):
        st.session_state.quiz_state[key]['started'] = False
        st.session_state.quiz_state[key]['completed'] = False
        st.session_state.quiz_state[key]['score'] = 0
        st.session_state.quiz_state[key]['answers'] = {}

def init_quiz_state(class_name):
    if class_name not in st.session_state.quiz_state:
        questions = get_quiz_questions(class_name)
        if questions:
            st.session_state.quiz_state[class_name] = {
                'questions': questions,
                'current_question': 0,
                'score': 0,
                'answered': False,
                'started': False,
                'completed': False,
                'answers': {}
            }
    elif 'answers' not in st.session_state.quiz_state[class_name]:
        st.session_state.quiz_state[class_name]['answers'] = {}

def show_detection_page():
    st.write("## 📸 Deteksi Gambar Reptil")
    uploaded_file = st.file_uploader("Upload gambar reptil", type=['jpg', 'jpeg', 'png'], on_change=reset_detection_state)

    if uploaded_file is not None:
        image = resize_image(uploaded_file)
        st.image(image, caption="Gambar yang diupload", use_container_width=True)

        conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Deteksi"):
                with st.spinner("Sedang mendeteksi..."):
                    result_image, detected_classes = detect_image(uploaded_file, conf_threshold)

                    if result_image is None:
                        st.warning("⚠️ Gambar tidak terdeteksi sebagai reptil")
                        save_detection_history(st.session_state.username, "Tidak terdeteksi", 0.0)
                        return

                    st.session_state.detected_classes = detected_classes
                    st.session_state.current_detection = True
                    st.session_state.result_image = result_image

        if st.session_state.current_detection and st.session_state.detected_classes:
            st.image(st.session_state.result_image, caption="Hasil Deteksi", use_container_width=True)
            st.write("### Hasil Deteksi:")

            if 'detection_saved' not in st.session_state or not st.session_state.detection_saved:
                for label, conf in st.session_state.detected_classes:
                    save_detection_history(st.session_state.username, label, conf)
                st.session_state.detection_saved = True

            for label, conf in st.session_state.detected_classes:
                st.write(f"- {label} (Confidence: {conf:.2f})")

            seen_labels = set()
            for idx, (label, conf) in enumerate(st.session_state.detected_classes):
                if label in seen_labels:
                    continue
                seen_labels.add(label)

                st.write("#### Fakta Menarik:")
                fact = get_reptile_fact(label)
                st.info(fact)

                init_quiz_state(label)
                if label in st.session_state.quiz_state:
                    quiz_state = st.session_state.quiz_state[label]
                    questions = quiz_state['questions']

                    if not quiz_state['started']:
                        if st.button("Mulai Kuis", key=f"start_quiz_{label}_{idx}"):
                            quiz_state['started'] = True
                            st.rerun()

                    if quiz_state['started'] and not quiz_state['completed']:
                        st.write("#### Kuis:")
                        for i, q in enumerate(questions):
                            st.write(f"\n**Pertanyaan {i+1}:** {q['soal']}")

                            options = [q.get('opsi_a'), q.get('opsi_b'), q.get('opsi_c')]
                            options = [opt for opt in options if opt]

                            if options:
                                radio_key = f"quiz_{label}_{i}_{idx}"
                                answer = st.radio("Pilih jawaban:", options, index=None, key=radio_key)

                                if answer:
                                    if answer == q['opsi_a']:
                                        quiz_state['answers'][i] = 'A'
                                    elif answer == q['opsi_b']:
                                        quiz_state['answers'][i] = 'B'
                                    elif answer == q['opsi_c']:
                                        quiz_state['answers'][i] = 'C'
                            else:
                                st.warning("Tidak ada opsi jawaban tersedia untuk pertanyaan ini.")

                        col1, col2 = st.columns([2, 1])
                        with col1:
                            if st.button("Submit Jawaban", key=f"submit_all_{label}_{idx}"):
                                unanswered = [i+1 for i in range(len(questions)) if i not in quiz_state['answers']]
                                if unanswered:
                                    st.warning(f"Mohon jawab pertanyaan {', '.join(map(str, unanswered))} terlebih dahulu.")
                                else:
                                    score = 0
                                    for i, q in enumerate(questions):
                                        user_answer = quiz_state['answers'].get(i)
                                        correct_answer = str(q['jawaban_benar']).strip().upper()
                                        if user_answer == correct_answer:
                                            score += 1
                                            st.write(f"✅ Pertanyaan {i+1}: Benar!")
                                        else:
                                            st.write(f"❌ Pertanyaan {i+1}: Salah")
                                            correct_option = q.get(f"opsi_{correct_answer.lower()}")
                                            st.write(f"Jawaban yang benar adalah: {correct_option}")

                                    quiz_state['score'] = score
                                    quiz_state['completed'] = True
                                    st.success(f"Kuis selesai! Skor Anda: {score}/{len(questions)}")
                                    st.rerun()

                        with col2:
                            if st.button("Kembali ke Deteksi", key=f"back_to_detection_{label}_{idx}"):
                                st.session_state.current_detection = None
                                st.rerun()

                    elif quiz_state['completed']:
                        st.success(f"Kuis selesai! Skor Anda: {quiz_state['score']}/{len(questions)}")
                        if st.button("Mulai Kuis Baru", key=f"restart_quiz_{label}_{idx}"):
                            st.session_state.quiz_state[label] = {
                                'questions': questions,
                                'current_question': 0,
                                'score': 0,
                                'answered': False,
                                'started': True,
                                'completed': False,
                                'answers': {}
                            }
                            st.rerun()
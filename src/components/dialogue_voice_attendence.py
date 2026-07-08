import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import  pandas as pd
from src.components.attendence_results_dialogue import show_attendance_result
@st.dialog("Voice Attendence")

def voice_attendance_dialogue(selected_subject_id):
    st.write("Record audio of students sayng I am Present")

    audio_data=None
    audio_data=st.audio_input("Record Classroom Audio")
    if st.button("Analyze Audio",type="primary",width="stretch"):
       with  st.spinner("Analyzing the audio"):
            enroll_response=supabase.table("subject_students").select("*,students(*)").eq("subject_id",selected_subject_id).execute()
            enroll_students=enroll_response.data
            if not enroll_students:
                st.warning('No students enrolled in this course')
                return
            candidate_dict={
                s["students"]["student_id"]:s["students"]["voice_embeddings"]
                for s in enroll_students if s["students"].get("voice_embeddings")
            }
            if not candidate_dict:
                st.error("No enrolled students have voice emebedding")
                return
            audio_bytes=audio_data.read()
            detected_sore=process_bulk_audio(audio_bytes,candidate_dict)

            results, attendence_to_logs  = [], []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


            for node in enroll_students:
                student = node['students']
                scores=detected_sore.get(student["student_id"],0.0)
                is_present=bool(scores>0) 

                results.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "Score": scores if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendence_to_logs.append({
                    "timestamp": current_timestamp,
                    'student_id': student['student_id'],
                    "subject_id":selected_subject_id,
                    'is_present': bool(is_present)
                })
            st.session_state.voice_attendance_results=(pd.DataFrame(results),attendence_to_logs)
    if st.session_state.get("voice_attendance_results"):
        st.divider()
        df_results,logs=st.session_state.voice_attendance_results
        show_attendance_result(df_results,logs)

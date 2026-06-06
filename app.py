import os
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip

async def generate_voiceover(text, output_audio_path):
    import edge_tts
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)
    print("✓ AI Voiceover successfully created.")

def create_final_video(video_path, audio_path, output_path):
    print("✓ Video processing started...")
    
    # Audio aur Video clips load karein
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # Agar video lambi hai, toh audio ke mutabiq cut karein
    if video_clip.duration > audio_clip.duration:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    # Audio ko direct video par lagayein (Abhi hum simple bina subtitle layer ke test kar rahe hain taake error pakra jaye)
    final_clip = video_clip.set_audio(audio_clip)
    
    print("⏳ Final video render ho rahi hai...")
    final_clip.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac",
        fps=24,
        threads=4
    )
    print(f"🏆 SUCCESS: Video Ready -> {output_path}")

async def main():
    story_text = "I automated my entire job using Python. My boss thinks I work 8 hours a day, but I only work 5 minutes. Should I tell him?"
    
    bg_video = "background.mp4" 
    temp_audio = "voiceover.mp3"
    final_video = "final_output.mp4"
    
    if not os.path.exists(bg_video):
        print(f"❌ Error: '{bg_video}' file nahi mili.")
        return

    await generate_voiceover(story_text, temp_audio)
    create_final_video(bg_video, temp_audio, final_video)
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

if __name__ == "__main__":
    asyncio.run(main())

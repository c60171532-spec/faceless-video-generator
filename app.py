import os
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# 1. Free Voiceover Generator
async def generate_voiceover(text, output_audio_path):
    import edge_tts
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)
    print("✓ AI Voiceover successfully created.")

# 2. Main Video Processing System with Subtitles
def create_final_video(video_path, audio_path, output_path, story_text):
    print("✓ Video processing started...")
    
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # Video ko audio ke mutabiq cut karein
    if video_clip.duration > audio_clip.duration:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    # Subtitles (Captions) Layer Banana
    # Hum text ko screen ke center mien dikhayenge
    try:
        # Simple subtitle text layer (Font aur size aap change kar sakte hain)
        txt_clip = TextClip(
            story_text, 
            fontsize=40, 
            color='white', 
            font='Arial-Bold',
            method='caption',
            size=(video_clip.w - 100, None)
        )
        # Subtitle ko video ke center mien set karna aur uski duration fix karna
        txt_clip = txt_clip.set_position('center').set_duration(audio_clip.duration)
        
        # Video aur Subtitles ko aapas mien overlay (merge) karna
        final_video_layer = CompositeVideoClip([video_clip, txt_clip])
    except Exception as e:
        print(f"⚠️ Subtitle Font Warning: {e}. Subtitles ke bina video ban rahi hai.")
        final_video_layer = video_clip

    # Audio attach karein
    final_clip = final_video_layer.set_audio(audio_clip)
    
    # Render (Save) Video
    print("⏳ Final video render ho rahi hai, thoda sabar karein...")
    final_clip.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac",
        fps=24,
        threads=4
    )
    print(f"🏆 SUCCESS: Aap ki video ready hai -> {output_path}")

async def main():
    # Aap is text ko apni marzi se badal sakte hain jo video mien bolna hai
    story_text = "I automated my entire job using Python. My boss thinks I work 8 hours a day, but I only work 5 minutes. Should I tell him?"
    
    bg_video = "background.mp4" 
    temp_audio = "voiceover.mp3"
    final_video = "final_output.mp4"
    
    if not os.path.exists(bg_video):
        print(f"❌ Error: '{bg_video}' file nahi mili. Pehle apni background video upload karein.")
        return

    await generate_voiceover(story_text, temp_audio)
    create_final_video(bg_video, temp_audio, final_video, story_text)
    
    # Temporary audio file delete karna
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

if __name__ == "__main__":
    asyncio.run(main())

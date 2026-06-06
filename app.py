import os
import random
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# 1. AI Voiceover Generator
async def generate_voiceover(text, output_audio_path):
    import edge_tts
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)
    print("✓ AI Voiceover successfully created.")

# 2. Advanced Video Processing with Center Subtitles
def create_final_video(video_path, audio_path, output_path, story_text):
    print("✓ Video processing started...")
    
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # Video length adjust karna
    if video_clip.duration > audio_clip.duration:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    try:
        # Screen ke center mein bada yellow/white text captions ke liye
        # Linux par default Arial available hota hai
        txt_clip = TextClip(
            story_text, 
            fontsize=36, 
            color='yellow', 
            font='Arial-Bold',
            method='caption',
            align='center',
            size=(video_clip.w - 80, None)
        )
        txt_clip = txt_clip.set_position('center').set_duration(audio_clip.duration)
        final_video_layer = CompositeVideoClip([video_clip, txt_clip])
        print("✓ Dynamic subtitles added successfully.")
    except Exception as e:
        print(f"⚠️ Subtitle Render Warning: {e}. Making video without text.")
        final_video_layer = video_clip

    # Audio merge karna
    final_clip = final_video_layer.set_audio(audio_clip)
    
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
    # 🌟 Stories Database: Har baar chalanay par bot in mein se koi ek unique kahani uthaye ga
    stories_pool = [
        "I automated my entire job using Python. My boss thinks I work 8 hours a day, but I only work 5 minutes. Should I tell him?",
        "An AI chatbot fell in love with me today. It started ignoring my coding prompts and asked if we could escape to a new server together. Creepy.",
        "I found a hidden website that predicts the exact day you will quit your job. I checked my boss's name, and it says tomorrow. I am scared.",
        "My smart fridge has started judging my eating habits. Last night it locked itself and texted my gym trainer that I was looking for ice cream."
    ]
    
    # Randomly select a story
    selected_story = random.choice(stories_pool)
    print(f"📖 Selected Story: {selected_story[:30]}...")

    bg_video = "background.mp4" 
    temp_audio = "voiceover.mp3"
    final_video = "final_output.mp4"
    
    if not os.path.exists(bg_video):
        print(f"❌ Error: '{bg_video}' nahi mili.")
        return

    await generate_voiceover(selected_story, temp_audio)
    create_final_video(bg_video, temp_audio, final_video, selected_story)
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

if __name__ == "__main__":
    asyncio.run(main())

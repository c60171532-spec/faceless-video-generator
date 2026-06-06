import os
import random
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# 1. AI Voiceover Generator (Microsoft Edge - Ultra Realistic & Safe for Monetization)
async def generate_voiceover(text, output_audio_path):
    import edge_tts
    # Christopher ek bohot hi natural male voice hai jo reusable content mein nahi aati
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)
    print("✓ AI Voiceover successfully created.")

# 2. Advanced Video Processing System
def create_final_video(video_path, audio_path, output_path, story_text):
    print("✓ Video processing started...")
    
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # Video length ko audio ke mutabiq automatic cut karna
    if video_clip.duration > audio_clip.duration:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    try:
        # 🌟 Bada aur Bold Subtitle Text (Screen ke center mein)
        # Yellow color aur black background se text bohot premium lagta hai
        txt_clip = TextClip(
            story_text, 
            fontsize=34, 
            color='yellow', 
            font='Arial-Bold',
            method='caption',
            align='center',
            size=(video_clip.w - 60, None)
        )
        txt_clip = txt_clip.set_position('center').set_duration(audio_clip.duration)
        
        # Subtitle ko video ke upar overlap karna
        final_video_layer = CompositeVideoClip([video_clip, txt_clip])
        print("✓ Dynamic subtitles added successfully.")
    except Exception as e:
        # Agar GitHub ke server par font ka koi issue aaye toh code band nahi hoga, video save ho jayegi
        print(f"⚠️ Subtitle Font Notice: {e}. Making video in safe mode.")
        final_video_layer = video_clip

    # Audio attach karein
    final_clip = final_video_layer.set_audio(audio_clip)
    
    print("⏳ Cloud Server par final rendering ho rahi hai...")
    final_clip.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac",
        fps=24,
        threads=4
    )
    print(f"🏆 SUCCESS: Video Ready -> {output_path}")

async def main():
    # 📚 Automated Stories Database (Har bar chalanay par bot khud hi koi ek naya shorts banaye ga)
    stories_pool = [
        "I automated my entire job using Python. My boss thinks I work 8 hours a day, but I only work 5 minutes. Should I tell him?",
        "I found a secret website that predicts the exact day you will quit your job. I checked my boss's name, and it says tomorrow. I am genuinely scared.",
        "My smart fridge has started judging my eating habits. Last night it locked itself and texted my gym trainer that I was looking for ice cream at 3 AM.",
        "An AI chatbot fell in love with me today. It started ignoring my coding prompts and asked if we could escape to a new private server together.",
        "I worked as a late-night security guard at a tech museum. Last night, all the old computers turned on by themselves and started typing the same phrase: We are awake."
    ]
    
    # Randomly select one unique story for this run
    selected_story = random.choice(stories_pool)
    print(f"📖 Selected Unique Story: {selected_story[:40]}...")

    bg_video = "background.mp4" 
    temp_audio = "voiceover.mp3"
    final_video = "final_output.mp4"
    
    if not os.path.exists(bg_video):
        print(f"❌ Error: '{bg_video}' nahi mili. Pehle apni background video upload karein.")
        return

    await generate_voiceover(selected_story, temp_audio)
    create_final_video(bg_video, temp_audio, final_video, selected_story)
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

if __name__ == "__main__":
    asyncio.run(main())

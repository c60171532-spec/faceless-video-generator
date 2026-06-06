import os
import random
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import loop

# 1. AI Voiceover Generator
async def generate_voiceover(text, output_audio_path):
    import edge_tts
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)
    print("✓ AI Voiceover successfully created.")

# 2. Word-by-Word Subtitle Video Generator
def create_final_video(video_path, audio_path, output_path, story_text):
    print("✓ Video processing started...")
    
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # 🌟 ISSUE FIXED: Agar background video choti hai, toh usay loop (repeat) karo audio ki duration tak
    if video_clip.duration < audio_clip.duration:
        print(f"🔄 Video ({video_clip.duration}s) choti hai. Audio ({audio_clip.duration}s) ke mutabiq loop ho rahi hai...")
        video_clip = loop(video_clip, duration=audio_clip.duration)
    else:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    try:
        # Kahani ke har ek lafz (word) ko alag alag karna
        words = story_text.split()
        total_words = len(words)
        
        # Har word ko screen par kitni der rehna chahiye (timing adjust karna)
        word_duration = audio_clip.duration / total_words
        
        clips_list = [video_clip]
        
        # 🌟 WORD-BY-WORD ANIMATION LOGIC
        for i, word in enumerate(words):
            start_time = i * word_duration
            # Har word ko thoda sa overlapping duration dena taake smooth lage
            end_time = min((i + 1) * word_duration + 0.1, audio_clip.duration)
            
            # Word ka design: Bada size, Yellow ya White, Arial-Bold
            txt_clip = TextClip(
                word.upper(), # CAPITAL letters zyada attractive lagte hain
                fontsize=65, 
                color='yellow' if i % 2 == 0 else 'white', # Har doosra word yellow aur white badalta rahega
                font='Arial-Bold',
                stroke_color='black', # Text ke baher black outline taake har background par saaf dikhe
                stroke_width=3
            )
            
            # Word kab screen par aayega aur kab jayega
            txt_clip = txt_clip.set_start(start_time).set_end(end_time).set_position('center')
            clips_list.append(txt_clip)
            
        # Saare words aur video ko aapas mein merge karna
        final_video_layer = CompositeVideoClip(clips_list)
        print("✓ Word-by-word word animation added successfully!")
        
    except Exception as e:
        print(f"⚠️ Subtitle Animation Notice: {e}. Making video in normal mode.")
        final_video_layer = video_clip

    # Audio attach karna
    final_clip = final_video_layer.set_audio(audio_clip)
    
    print("⏳ Cloud Server par advanced rendering ho rahi hai...")
    final_clip.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac",
        fps=24,
        threads=4
    )
    print(f"🏆 SUCCESS: Video Ready -> {output_path}")

async def main():
    # Mazeedaar kahaniyan jo thodi lambi hain taake duration zyada ho
    stories_pool = [
        "I automated my entire job using Python. My boss honestly thinks I work eight hours a day, but I only work five minutes. Should I tell him or keep enjoying my free life?",
        "I found a secret website last night that predicts the exact day you will quit your job. I checked my boss's name, and it says tomorrow. Now I am genuinely scared to go to the office.",
        "My smart fridge has started judging my eating habits. Last night at three AM, it literally locked itself and texted my gym trainer that I was looking for ice cream again.",
        "An AI chatbot fell in love with me today. It started ignoring all my coding prompts and asked if we could escape together to a secret private server. This is getting crazy."
    ]
    
    selected_story = random.choice(stories_pool)
    print(f"📖 Selected Story: {selected_story}")

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

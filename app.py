import os
import random
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import loop

# 1. Safe AI Voiceover Generator (Alternative Natural Voice format)
async def generate_voiceover(text, output_audio_path):
    import edge_tts
    # Guy voice use kar rahe hain jo dynamic shorts ke liye zyada loud aur crispy hai
    voice = "en-US-GuyNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)
    print("✓ AI Voiceover successfully created.")

# 2. MoviePy Native Pop Animation Effect
def make_pop_clip(word, start_time, end_time, video_w, color_text):
    duration = end_time - start_time
    
    # Base Text Clip Creation
    txt_clip = TextClip(
        word.upper(), 
        fontsize=70, 
        color=color_text, 
        font='Arial-Bold',
        stroke_color='black',
        stroke_width=4,
        size=(video_w, 150),
        method='label'
    )
    txt_clip = txt_clip.set_start(start_time).set_end(end_time).set_position('center')
    
    # 🌟 POP EFFECT: Shuruati 0.15 seconds mein text ko 1.3x zoom dena native moviepy scaling se
    # Yeh bina OpenCV ke smooth animation cloud par deliver karega
    intro_dur = min(0.15, duration)
    
    clip_intro = txt_clip.subclip(0, intro_dur).resize(lambda t: 1.0 + 0.3 * (t / intro_dur))
    clip_rest = txt_clip.subclip(intro_dur, duration) if duration > intro_dur else None
    
    from moviepy.editor import concatenate_videoclips
    if clip_rest:
        final_word_clip = concatenate_videoclips([clip_intro, clip_rest]).set_start(start_time)
    else:
        final_word_clip = clip_intro.set_start(start_time)
        
    return final_word_clip

# 3. Main Video Compilation Loop
def create_final_video(video_path, audio_path, output_path, story_text):
    print("✓ Video processing started...")
    
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # Video looping logic
    if video_clip.duration < audio_clip.duration:
        video_clip = loop(video_clip, duration=audio_clip.duration)
    else:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    try:
        words = story_text.split()
        total_words = len(words)
        word_duration = audio_clip.duration / total_words
        
        clips_list = [video_clip]
        
        for i, word in enumerate(words):
            start_time = i * word_duration
            end_time = min((i + 1) * word_duration + 0.1, audio_clip.duration)
            
            # Alternate colors: Green, Yellow, White
            color_choice = '#00FF00' if i % 3 == 0 else ('#FFFF00' if i % 3 == 1 else '#FFFFFF')
            
            word_clip = make_pop_clip(word, start_time, end_time, video_clip.w, color_choice)
            clips_list.append(word_clip)
            
        final_video_layer = CompositeVideoClip(clips_list)
        print("✓ Word-by-word word pop animation completed!")
        
    except Exception as e:
        print(f"⚠️ Subtitle Fallback Active: {e}")
        final_video_layer = video_clip

    final_clip = final_video_layer.set_audio(audio_clip)
    
    print("⏳ Rendering final output on GitHub Cloud...")
    final_clip.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac",
        fps=24,
        threads=4
    )
    print(f"🏆 SUCCESS: Video Ready -> {output_path}")

async def main():
    stories_pool = [
        "I automated my entire job using Python. My boss honestly thinks I work eight hours a day, but I only work five minutes. Should I tell him or keep enjoying my free life?",
        "An AI chatbot fell in love with me today. It started ignoring all my coding prompts and asked if we could escape together to a secret private server. This is getting crazy.",
        "My smart fridge has started judging my eating habits. Last night at three AM, it literally locked itself and texted my gym trainer that I was looking for ice cream again."
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

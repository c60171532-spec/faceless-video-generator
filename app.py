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

# 2. Advanced Animation Logic (Text Zoom/Pop In)
def zoom_in_effect(clip, duration, max_scale=1.3):
    """Har word screen par aate hi halka sa bada ho kar zoom-in effect dega"""
    def filter(get_frame, t):
        # Shuruati 0.15 seconds mein text bada hoga, fir normal size par text rukega
        if t < 0.15:
            scale = 1.0 + (max_scale - 1.0) * (t / 0.15)
        elif t < 0.30:
            scale = max_scale - (max_scale - 1.0) * ((t - 0.15) / 0.15)
        else:
            scale = 1.0
        
        frame = get_frame(t)
        # MoviePy image resize logic safely handles zoom frames without crashing
        import cv2
        h, w = frame.shape[:2]
        new_w, new_h = int(w * scale), int(h * scale)
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        # Center crop matrix back to original canvas size
        start_x = (new_w - w) // 2
        start_y = (new_h - h) // 2
        return resized[start_y:start_y+h, start_x:start_x+w]
        
    return clip.fl(filter)

# 3. Word-by-Word Dynamic Subtitle Video Generator
def create_final_video(video_path, audio_path, output_path, story_text):
    print("✓ Video processing started...")
    
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # 🔄 FIXED DURATION: Video ko background mein loop karo jab tak audio chal rahi hai
    if video_clip.duration < audio_clip.duration:
        print(f"🔄 Video loop ho rahi hai: {video_clip.duration}s -> {audio_clip.duration}s")
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
            end_time = min((i + 1) * word_duration + 0.15, audio_clip.duration)
            clip_len = end_time - start_time
            
            # Text Design Customization
            # Har word capital letter mein popup hoga
            txt_clip = TextClip(
                word.upper(), 
                fontsize=75, 
                color='#00FF00' if i % 3 == 0 else ('#FFFF00' if i % 3 == 1 else '#FFFFFF'), # Green, Yellow, White colors switch honge
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=4,
                size=(video_clip.w, 150),
                method='label'
            )
            
            txt_clip = txt_clip.set_start(start_time).set_end(end_time).set_position('center')
            
            # Apply pop/zoom animation effect to individual word clip
            try:
                txt_clip = zoom_in_effect(txt_clip, clip_len)
            except Exception as anim_err:
                print(f"Animation fallback active: {anim_err}")
                
            clips_list.append(txt_clip)
            
        final_video_layer = CompositeVideoClip(clips_list)
        print("✓ Advanced word animation added successfully!")
        
    except Exception as e:
        print(f"⚠️ Subtitle Notice: {e}. Safe mode layer active.")
        final_video_layer = video_clip

    # Merge background audio
    final_clip = final_video_layer.set_audio(audio_clip)
    
    print("⏳ Cloud Server par rendering process active hai...")
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
        "An AI chatbot fell in love with me today. It started ignoring all my coding prompts and asked if we could escape together to a secret private server. This is getting crazy.",
        "I automated my entire job using Python. My boss honestly thinks I work eight hours a day, but I only work five minutes. Should I tell him or keep enjoying my free life?",
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

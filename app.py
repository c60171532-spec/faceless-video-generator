import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import loop
from gtts import gTTS

# 1. 100% Guaranteed Stable Voiceover Generator (Using Google TTS)
def generate_voiceover(text, output_audio_path):
    print("⏳ AI Voiceover generation started...")
    tts = gTTS(text=text, lang='en', tld='com', slow=False)
    tts.save(output_audio_path)
    print("✓ AI Voiceover successfully created with Google TTS.")

# 2. Word-by-Word Word Highlight Generator
def create_final_video(video_path, audio_path, output_path, story_text):
    print("✓ Video processing started...")
    
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # Video loop fix logic
    if video_clip.duration < audio_clip.duration:
        print(f"🔄 Video loop active: {video_clip.duration}s -> {audio_clip.duration}s")
        video_clip = loop(video_clip, duration=audio_clip.duration)
    else:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    try:
        words = story_text.split()
        total_words = len(words)
        word_duration = audio_clip.duration / total_words
        
        clips_list = [video_clip]
        
        # Word-by-word active timing loop
        for i, word in enumerate(words):
            start_time = i * word_duration
            end_time = min((i + 1) * word_duration + 0.1, audio_clip.duration)
            
            # Clean and clean color switching (Yellow and White combo)
            word_color = '#FFFF00' if i % 2 == 0 else '#FFFFFF'
            
            txt_clip = TextClip(
                word.upper(), 
                fontsize=75, 
                color=word_color, 
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=4,
                size=(video_clip.w, 160),
                method='label'
            )
            txt_clip = txt_clip.set_start(start_time).set_end(end_time).set_position('center')
            clips_list.append(txt_clip)
            
        final_video_layer = CompositeVideoClip(clips_list)
        print("✓ Word-by-word layout created safely.")
        
    except Exception as e:
        print(f"⚠️ Subtitle notice: {e}")
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

def main():
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

    generate_voiceover(selected_story, temp_audio)
    create_final_video(bg_video, temp_audio, final_video, selected_story)
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

if __name__ == "__main__":
    main()

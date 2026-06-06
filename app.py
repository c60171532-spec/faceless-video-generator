import os
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip

# 1. Free Ultra-Realistic Voiceover Function (Microsoft Edge API)
async def generate_voiceover(text, output_audio_path):
    import edge_tts
    # 'en-US-ChristopherNeural' ek bohot pyari male voice hai jo free hai
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)
    print("✓ Voiceover tayyar ho gaya.")

# 2. Video aur Audio ko jorne ka function
def merge_video_audio(video_path, audio_path, output_path):
    print("✓ Video process ho rahi hai...")
    
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)
    
    # Agar background video lambi hai, toh usay audio ke size ka cut karein
    if video_clip.duration > audio_clip.duration:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    # Audio ko video par lagayein
    final_clip = video_clip.set_audio(audio_clip)
    
    # Final video save karein
    final_clip.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac",
        threads=4
    )
    print(f"✓ Mubarak ho! Aap ki video ready hai: {output_path}")

async def main():
    # Input text jo video mein bolna hai (Aap isay badal sakte hain)
    story_text = "I automated my entire job using Python. My boss thinks I work 8 hours a day, but I only work 5 minutes. Should I tell him?"
    
    bg_video = "background.mp4" # Yeh file aapke computer wale folder mein honi chahiye
    temp_audio = "voiceover.mp3"
    final_video = "final_output.mp4"
    
    if not os.path.exists(bg_video):
        print(f"Error: Pehle ek short video '{bg_video}' naam se is folder mein rakhein.")
        return

    await generate_voiceover(story_text, temp_audio)
    merge_video_audio(bg_video, temp_audio, final_video)
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

if __name__ == "__main__":
    asyncio.run(main())

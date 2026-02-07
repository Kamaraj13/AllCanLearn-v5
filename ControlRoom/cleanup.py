# cleanup.py

import os
import json
import glob
from datetime import datetime, timedelta

def cleanup_old_audio_files():
    """Delete audio files older than 3 days (72 hours)"""
    try:
        tts_dir = "tts_output"
        episodes_file = "episodes.json"
        episodes_data_dir = "episodes_data"
        
        if not os.path.exists(tts_dir):
            print(" TTS output directory does not exist")
            return
        
        # Calculate cutoff time (3 days ago)
        cutoff_time = datetime.now() - timedelta(hours=72)
        cutoff_timestamp = int(cutoff_time.timestamp() * 1000)
        
        print(f" Starting cleanup - deleting files older than {cutoff_time}")
        
        # Clean up audio files
        deleted_files = 0
        for file_path in glob.glob(os.path.join(tts_dir, "*.mp3")) + glob.glob(os.path.join(tts_dir, "*.aiff")) + glob.glob(os.path.join(tts_dir, "*.wav")):
            try:
                # Extract timestamp from filename
                filename = os.path.basename(file_path)
                timestamp_str = filename.split('.')[0]
                
                if timestamp_str.isdigit():
                    file_timestamp = int(timestamp_str)
                    if file_timestamp < cutoff_timestamp:
                        os.remove(file_path)
                        deleted_files += 1
                        print(f"  Deleted old audio file: {filename}")
            except Exception as e:
                print(f" Error processing {file_path}: {e}")
        
        # Clean up old episodes from episodes.json
        if os.path.exists(episodes_file):
            try:
                with open(episodes_file, 'r') as f:
                    episodes = json.load(f)
                
                original_count = len(episodes)
                episodes_to_keep = {}
                
                for episode_id, episode_data in episodes.items():
                    try:
                        episode_timestamp = int(episode_id)
                        if episode_timestamp >= cutoff_timestamp:
                            episodes_to_keep[episode_id] = episode_data
                        else:
                            print(f"  Deleted old episode: {episode_data.get('topic', 'Unknown')}")
                    except (ValueError, TypeError):
                        # Keep episodes with non-numeric IDs
                        episodes_to_keep[episode_id] = episode_data
                
                with open(episodes_file, 'w') as f:
                    json.dump(episodes_to_keep, f, indent=2)
                
                deleted_episodes = original_count - len(episodes_to_keep)
                print(f" Cleaned up {deleted_episodes} old episodes from episodes.json")
                
            except Exception as e:
                print(f" Error cleaning episodes.json: {e}")
        
        # Clean up old episode data files
        if os.path.exists(episodes_data_dir):
            try:
                deleted_data_files = 0
                for file_path in glob.glob(os.path.join(episodes_data_dir, "*.json")):
                    try:
                        filename = os.path.basename(file_path)
                        timestamp_str = filename.split('.')[0]
                        
                        if timestamp_str.isdigit():
                            file_timestamp = int(timestamp_str)
                            if file_timestamp < cutoff_timestamp:
                                os.remove(file_path)
                                deleted_data_files += 1
                                print(f"  Deleted old episode data file: {filename}")
                    except Exception as e:
                        print(f" Error processing {file_path}: {e}")
                
                print(f" Cleaned up {deleted_data_files} old episode data files")
                
            except Exception as e:
                print(f" Error cleaning episodes_data directory: {e}")
        
        print(f" Cleanup completed - Deleted {deleted_files} audio files")
        
    except Exception as e:
        print(f" Cleanup error: {e}")

def get_episode_count():
    """Get current episode count for monitoring"""
    try:
        episodes_file = "episodes.json"
        if os.path.exists(episodes_file):
            with open(episodes_file, 'r') as f:
                episodes = json.load(f)
            return len(episodes)
        return 0
    except:
        return 0

def get_storage_info():
    """Get storage information for monitoring"""
    try:
        tts_dir = "tts_output"
        if not os.path.exists(tts_dir):
            return {"total_files": 0, "total_size_mb": 0}
        
        files = glob.glob(os.path.join(tts_dir, "*"))
        total_size = sum(os.path.getsize(f) for f in files if os.path.isfile(f))
        
        return {
            "total_files": len(files),
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }
    except:
        return {"total_files": 0, "total_size_mb": 0}

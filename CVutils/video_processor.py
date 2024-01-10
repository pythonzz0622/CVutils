import os 
import subprocess
import json
import cv2
import numpy as np
import datetime 
import glob

def cut_video(input_file, start_time, end_time, output_file):
    """
    Use FFmpeg to cut a video from a specific start time to an end time.
    Args:
    input_file (str): Path to the input video file.
    start_time (str): Start time in 'HH:MM:SS' format.
    end_time (str): End time in 'HH:MM:SS' format.
    output_file (str): Path to the output video file.
    """
    command = [
        "ffmpeg",
        "-ss", start_time,
        "-i", input_file,
        "-t", end_time,
        "-c", "copy",
        output_file
    ]
    os.system(' '.join( command))

def generate_ffmpeg_command(rtsp_url,output_dir, duration_hours=2, codec='libx264'):
    # Create a filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.mp4"

    # Full path for the output file
    output_path = os.path.join(output_dir, filename)

    # Duration in seconds
    duration_seconds = duration_hours * 60 * 60

    # Construct the FFmpeg command
    command = f"ffmpeg -hide_banner -y -loglevel error -rtsp_transport tcp -use_wallclock_as_timestamps 1 \
    -i {rtsp_url} -vcodec copy -an \
    -f segment -reset_timestamps 1 -segment_time {duration_seconds} \
    -segment_format mkv -segment_atclocktime 1 -strftime 1 {output_path}/%Y%m%dT%H%M%S.mp4"

    return command

def convert_videos_to_jpg(input_folder, output_folder, fps=0.5):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Find all MP4 files in the input folder
    video_files = glob.glob(os.path.join(input_folder, "*.mp4"))

    for video_file in video_files:
        # Extract the base name of the video file to create a subfolder for its frames
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        video_output_folder = os.path.join(output_folder, base_name)

        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        # Output file pattern
        output_file_pattern = os.path.join(video_output_folder, "frame_%04d.jpg")

        # FFmpeg command
        command = [
            "ffmpeg",
            "-i", video_file,
            "-vf", f"fps={fps}",
            output_file_pattern
        ]

        # Execute the command
        subprocess.run(command, check=True)

def get_video_resolution(video_path):
    # ffprobe 명령어 실행
    command = ['ffprobe', 
               '-v', 'error', 
               '-select_streams', 'v:0', 
               '-show_entries', 'stream=width,height', 
               '-of', 'json', video_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 결과 파싱
    try:
        video_info = json.loads(result.stdout)
        width = video_info['streams'][0]['width']
        height = video_info['streams'][0]['height']
        return width, height
    except Exception as e:
        print(f"Error parsing video info: {e}")
        return None
    
def draw_text(frame ,query , x,y):
    texts = [f'{k} : {v}'for k,v in query.items()]
    for text in texts:
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        y += 30  # Move to the next line
        
def draw_polygons(frame, polygons : dict):
    for points in polygons.values():
        overlay = frame.copy()
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(overlay, [pts], (0, 255, 0))
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        
def draw_overlay_polygons(frame, polygons : dict):
    for points in polygons.values():
        overlay = frame.copy()
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(overlay, [pts], (0, 0, 255))
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
def draw_lines(frame , lines : dict):
    for line in lines.values():
        cv2.line(frame, tuple(line[0]), tuple(line[1]), (255, 0, 0), thickness=2)
import os
import subprocess

# 검색할 디렉토리 경로
search_dir = "/home/mim/project/ultralytics/infer_test.txt"

# 주어진 디렉토리에서 모든 .mp4 파일을 찾는 함수
def find_mp4_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                yield os.path.join(root, file)
                
def find_mp4_files_by_txt(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    yield from lines

# 각 .mp4 파일에 대해 작업을 수행하는 함수
def process_file(file_path):
    print(file_path)

    # Python 스크립트 실행
    python_command = "/home/mim/anaconda3/envs/py39_torch1_13/bin/python"
    script_path = "infer_args.py"
    subprocess.run([python_command, script_path, file_path])

    # 파일 이름 처리
    filename = os.path.basename(file_path)
    filename_without_extension = os.path.splitext(filename)[0]

    # FFmpeg 명령 실행
    ffmpeg_command = "ffmpeg"
    framerate = "120"
    input_pattern = "./test/test*.jpg"
    output_file = f"./outputs/{filename_without_extension}_converted.mp4"
    subprocess.run([ffmpeg_command, "-framerate", framerate, "-pattern_type", "glob", "-i", input_pattern, "-c:v", "nvenc_h264", output_file])

# 메인 스크립트 실행
for file in find_mp4_files_by_txt(search_dir):
    print(search_dir)
    process_file(file)

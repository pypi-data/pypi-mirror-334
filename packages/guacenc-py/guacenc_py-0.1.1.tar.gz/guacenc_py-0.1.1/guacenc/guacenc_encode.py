import logging
import os
import shutil
import subprocess
import tempfile
import threading
import time
import gzip

from tqdm import tqdm

from .guacenc_instruction import *
from .guacenc_parse import GuacamoleParser
from .guacenc_types import *

max_read_size = 1024 * 300


logger = logging.getLogger("guacenc.encoder")


class ImageToVideoWorker(threading.Thread):

    def __init__(
        self, root_dir, image_files: list[str], video_path: str, width: int, height: int
    ) -> None:
        super().__init__()
        self.root_dir = root_dir
        self.image_files = image_files
        self.video_path = video_path
        self.width = width
        self.height = height
        self._ffmpeg_process = None
        self._interval = 1
        self._completed = False
        self._success = False
        self._error = None
        self._lock = threading.Lock()

    def __str__(self):
        return f"ImageToVideoWorker(root_dir={self.root_dir}, video_path={self.video_path})"

    def run(self):
        """
        Thread method that starts the FFmpeg process to convert images to video.
        """
        try:
            self._encode_video()
            with self._lock:
                self._completed = True
                self._success = True
        except Exception as e:
            with self._lock:
                self._completed = True
                self._success = False
                self._error = str(e)
            logger.warning(f"Error in FFmpeg worker: {str(e)}")

    def start(self):
        super().start()

    def wait(self, timeout=None):
        self.join(timeout=timeout)
        with self._lock:
            return self._success

    def is_completed(self):
        with self._lock:
            return self._completed

    def get_error(self) -> str:
        """
        Get the error message if encoding failed.

        Returns:
            str: Error message or None if no error
        """
        with self._lock:
            return self._error

    def _encode_video(self) -> None:
        """
        Start the FFmpeg process to convert the image files to a video.
        Uses the specified interval between frames for proper timing.
        """
        if not self.image_files:
            logger.warning("No image files to process.")
            return
        list_file_path = os.path.join(self.root_dir, "images_list.txt")
        lenght = len(self.image_files)
        with open(list_file_path, "w") as fd:
            for index, image_info in enumerate(self.image_files):
                duration = self._interval
                fd.write(f"file '{image_info.file_path}'\n")
                if index < lenght - 1:
                    next_image_info = self.image_files[index + 1]
                    duration = (next_image_info.timestamp - image_info.timestamp) / 1000
                    fd.write(f"duration {duration}\n")
                else:
                    fd.write(f"duration {self._interval}\n")
            fd.write(f"file '{self.image_files[-1].file_path}'\n")
        # print(f"Image list file created at {list_file_path}")
        logger.debug(f"Starting FFmpeg process to encode video to {self.video_path}")
        command = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_file_path,
            "-vf",
            f"scale={self.width}:{self.height}:force_original_aspect_ratio=decrease,pad={self.width}:{self.height}:(ow-iw)/2:(oh-ih)/2",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",  # Compatible color format
            self.video_path,
        ]
        self._ffmpeg_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.root_dir,  # Run in the directory containing the images
        )
        # Wait for the process to complete
        stdout, stderr = self._ffmpeg_process.communicate()

        if self._ffmpeg_process.returncode != 0:
            logger.warning(f"FFmpeg error: {stderr.decode()}")
            raise RuntimeError(
                f"FFmpeg failed with error code {self._ffmpeg_process.returncode}"
            )

        video_name = os.path.basename(self.video_path)
        logger.debug(f"Video segment successfully created: {video_name}, and removed images in {self.root_dir}")
        shutil.rmtree(self.root_dir, ignore_errors=True)


class ImageInfo(object):

    def __init__(self, file_path: str, timestamp: int) -> None:
        self.file_path = file_path
        self.timestamp = timestamp


class GuacencEncoder:

    def __init__(
        self,
        file_path: str,
        video_path: str,
        width: int,
        hight: int,
        verbosity: int = 0,
    ) -> None:
        """
        Initialize the GuacencEncoder with the given file path and size.

        Args:
            file_path (str): Path to the input recording file.
            size (str): Size of the output video in WIDTHxHEIGHT format.
        """
        self.file_path = file_path
        self.video_path = video_path
        self.width = width
        self.height = hight

        self.display = Display(width, hight, callback=self.display_callback)
        self.parser = GuacamoleParser()
        self._read_size = 0
            # Determine file size properly for both regular and gzip files
        if file_path.endswith(".gz"):
            # Get the uncompressed size for gzip files
            with gzip.open(file_path, 'rb') as f:
                # Seek to the end to get uncompressed size
                f.seek(0, 2)
                self._file_size = f.tell()
        else:
            self._file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        if not self._file_size:
            raise ValueError(f"File not found or empty: {file_path}")
        self._work_tmp_dir = tempfile.mkdtemp(prefix="guacenc_tmp_")
        if not self._work_tmp_dir:
            raise RuntimeError("Failed to create temporary directory for encoding.")
        logger.debug(f"Temporary directory created at {self._work_tmp_dir}")
        self._videos = []
        self._images = []
        self._workers_process = []
        self._current_image_files = []
        self._current_image_count = 0
        self._current_image_index = None
        self._need_write_image = False
        self._precent = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()
        return False

    def cleanup(self):
        """
        Clean up all resources used by the encoder.
        """
        # Wait for any running worker threads to finish
        for worker in self._workers_process:
            try:
                if worker.is_alive():
                    worker.join(timeout=2.0)
            except Exception as e:
                logger.warning(f"Warning: Error waiting for worker thread: {e}")

        # Clean up temporary directory
        if (
            hasattr(self, "_work_tmp_dir")
            and self._work_tmp_dir
            and os.path.exists(self._work_tmp_dir)
        ):
            try:
                # print(f"Cleaning up temporary directory {self._work_tmp_dir}")
                shutil.rmtree(self._work_tmp_dir, ignore_errors=True)
            except Exception as e:
                logger.warning(f"Warning: Failed to clean up temporary directory: {e}")

    def encode(self) -> None:
        work_dir = self._work_tmp_dir
        images_dir = os.path.join(work_dir, "images")
        videos_dir = os.path.join(work_dir, "videos")
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        
        openfunc = open
        is_gzip = self.file_path.endswith(".gz")
        if is_gzip:
            openfunc = gzip.open
        with openfunc(self.file_path, "rt") as fd:
            progress_bar = tqdm(
                total=self._file_size,
                unit="B",
                unit_scale=True,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
                unit_divisor=1024,
                desc="Processing",
            )
            while True:
                read = fd.read(max_read_size)
                if not read:
                    break
                bytes_read = len(read)
                for item in self.parser.parse(read):
                    inst = Instruction(item[0], *item[1:])
                    guacenc_handle_instruction(self.display, inst)
                progress_bar.update(bytes_read)
            progress_bar.close()
        if len(self._current_image_files) > 0:
            self.start_ffmpeg_worker()

        for worker in self._workers_process:
            if not worker.wait():
                err = worker.get_error()
                raise RuntimeError(f"FFmpeg worker {worker} failed: {err}")
        self.conbine_videos()
        self.cleanup()

    def conbine_videos(self) -> None:
        work_dir = self._work_tmp_dir
        videos_dir = os.path.join(work_dir, "videos")
        if not os.path.exists(videos_dir):
            raise FileNotFoundError(f"Videos directory not found: {videos_dir}")
        video_path = self.video_path
        logger.debug(f"Combining video segment files into {video_path}")
        with open(os.path.join(videos_dir, "videos_list.txt"), "w") as fd:
            for video in self._videos:
                fd.write(f"file '{video}'\n")
        command = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            os.path.join(videos_dir, "videos_list.txt"),
            "-c",
            "copy",
            video_path,
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logger.warning(f"FFmpeg error: {result.stderr.decode()}")
            raise RuntimeError(f"FFmpeg failed with error code {result.returncode}")
        logger.debug(f"Video saved to {video_path}")

    def start_ffmpeg_worker(self):
        work_dir = self._work_tmp_dir
        images_dir = os.path.join(work_dir, "images")
        videos_dir = os.path.join(work_dir, "videos")
        image_index = self.get_current_image_index()
        current_image_index_dir = os.path.join(images_dir, f"{image_index}")
        video_filename = f"video_{image_index}.mp4"
        video_path = os.path.join(videos_dir, video_filename)
        self._videos.append(video_path)
        image_files = self._current_image_files
        logger.debug(
            f"Starting FFmpeg worker to encode video {video_filename} on backgroud"
        )
        worker = ImageToVideoWorker(
            current_image_index_dir, image_files, video_path, self.width, self.height
        )
        self._workers_process.append(worker)
        worker.start()
        self._current_image_index += 1
        self._images.append(self._current_image_index)
        self._current_image_count = 0
        self._current_image_files = []

    def display_callback(self, display: Display, instruction: Instruction) -> None:
        """
        Callback function to handle display updates during encoding.

        Args:
            display (Display): The display object.
            instruction (Instruction): The current instruction processed.
        """
        work_dir = self._work_tmp_dir
        images_dir = os.path.join(work_dir, "images")
        videos_dir = os.path.join(work_dir, "videos")
        image_index = self.get_current_image_index()
        current_image_index_dir = os.path.join(images_dir, f"{image_index}")
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        if not os.path.exists(current_image_index_dir):
            os.makedirs(current_image_index_dir)

        if instruction.cmd == "sync":
            if self._need_write_image:
                image_file_name = f"image_{self._current_image_count:04d}.png"
                image_file_path = os.path.join(current_image_index_dir, image_file_name)
                self._current_image_count += 1
                self.display.save(image_file_path)
                image_info = ImageInfo(image_file_path, display.last_sync)
                self._current_image_files.append(image_info)
            self._need_write_image = False
        else:
            self._need_write_image = True

        if self._current_image_count >= 1000:
            self.start_ffmpeg_worker()

    def get_current_image_index(self) -> int:
        """
        Get the current image index.

        Returns:
            int: The current image index.
        """
        if self._current_image_index is None:
            self._current_image_index = 0
            self._images.append(self._current_image_index)
        return self._current_image_index


def check_ffmpeg_installed() -> bool:
    """
    Check if ffmpeg is installed on the system.

    Returns:
        bool: True if ffmpeg is installed, False otherwise.
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("ffmpeg is not installed or not found in PATH.")
        return False
    except Exception as e:
        print(f"Error checking ffmpeg installation: {e}")
        return False


def encode_recording(
    input_path: str, output_path: str, size: str, verbosity: int = 0
) -> None:
    """
    Encode a Guacamole recording into a video file.

    Args:
        input_path (str): Path to the input recording file.
        output_path (str): Path to the output video file.
    """

    width, height = map(int, size.split("x"))
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid size: {size}. Expected format is WIDTHxHEIGHT.")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not os.path.isfile(input_path):
        raise ValueError(f"Input path is not a file: {input_path}")
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + ".mp4"

    if not check_ffmpeg_installed():
        raise RuntimeError("ffmpeg is not installed or not found in PATH.")
    start = time.time()
    logger.info(f"Encoding replay from {input_path} to {output_path} with size {size}")

    with GuacencEncoder(input_path, output_path, width, height, verbosity) as encoder:
        encoder.encode()
    end = time.time()
    logger.info(f"Encoding completed in {end - start:.2f} seconds.")

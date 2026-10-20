import shutil
import subprocess
import time

from pathlib import Path
from threading import Lock

from config import (
    # Camera devices
    LEFT_CAMERA_DEVICE,
    RIGHT_CAMERA_DEVICE,
    DORSAL_CAMERA_DEVICE,

    # Left
    LEFT_IMAGE_WIDTH,
    LEFT_IMAGE_HEIGHT,
    LEFT_CAMERA_FRAMERATE,

    # Right
    RIGHT_IMAGE_WIDTH,
    RIGHT_IMAGE_HEIGHT,
    RIGHT_CAMERA_FRAMERATE,

    # Dorsal
    DORSAL_IMAGE_WIDTH,
    DORSAL_IMAGE_HEIGHT,
    DORSAL_CAMERA_FRAMERATE,

    # Arducam
    ARDUCAM_AUTO_EXPOSURE,
    ARDUCAM_EXPOSURE,
    ARDUCAM_GAIN,
    ARDUCAM_BACKLIGHT_COMPENSATION,
    ARDUCAM_EXPOSURE_DYNAMIC_FRAMERATE,
    ARDUCAM_POWER_LINE_FREQUENCY,
    ARDUCAM_AUTO_WHITE_BALANCE,
    ARDUCAM_BRIGHTNESS,
    ARDUCAM_CONTRAST,
    ARDUCAM_SATURATION,
    ARDUCAM_HUE,
    ARDUCAM_HUE_AUTOMATIC,
    ARDUCAM_GAMMA,
    ARDUCAM_SHARPNESS,
    ARDUCAM_AUTO_FOCUS,
    ARDUCAM_FOCUS_ABSOLUTE,
    ARDUCAM_CONTROL_SETTLE_SECONDS,
    ARDUCAM_CONFIGURE_BEFORE_CAPTURE,
    ARDUCAM_CONFIGURE_ON_STARTUP,

    # Capture
    CAMERA_WARMUP_FRAMES,
    CAMERA_SWITCH_DELAY_SECONDS,
    PHOTO_DIR,
)

from errors import HardwareMeasurementError


# =========================================================
# Camera Lock
#
# 여러 측정 요청이 동시에 들어와도
# 카메라는 한 측정 세션에서만 사용
# =========================================================

camera_lock = Lock()


# =========================================================
# Arducam Configuration
#
# 현재 설정:
#
# Resolution : 3264 x 2448
# Exposure   : Manual
# Exposure   : .env 값 사용
# Gain       : 0
# Sharpness  : 3
# Auto Focus : OFF
# Focus      : 350
# Auto WB    : ON
# =========================================================

def configure_arducam(
    device: str,
    camera_name: str
):

    if not Path(device).exists():

        raise HardwareMeasurementError(
            reason="DEVICE_DISCONNECTED",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} Arducam 장치를 "
                f"찾을 수 없습니다: {device}"
            )
        )


    controls = [

        f"auto_exposure="
        f"{ARDUCAM_AUTO_EXPOSURE}",

        f"exposure_time_absolute="
        f"{ARDUCAM_EXPOSURE}",

        f"gain="
        f"{ARDUCAM_GAIN}",

        (
            "backlight_compensation="
            f"{ARDUCAM_BACKLIGHT_COMPENSATION}"
        ),

        (
            "exposure_dynamic_framerate="
            f"{ARDUCAM_EXPOSURE_DYNAMIC_FRAMERATE}"
        ),

        (
            "power_line_frequency="
            f"{ARDUCAM_POWER_LINE_FREQUENCY}"
        ),

        (
            "white_balance_automatic="
            f"{1 if ARDUCAM_AUTO_WHITE_BALANCE else 0}"
        ),

        f"brightness="
        f"{ARDUCAM_BRIGHTNESS}",

        f"contrast="
        f"{ARDUCAM_CONTRAST}",

        f"saturation="
        f"{ARDUCAM_SATURATION}",

        f"hue="
        f"{ARDUCAM_HUE}",

        f"hue_automatic="
        f"{ARDUCAM_HUE_AUTOMATIC}",

        f"gamma="
        f"{ARDUCAM_GAMMA}",

        f"sharpness="
        f"{ARDUCAM_SHARPNESS}",

        (
            "focus_automatic_continuous="
            f"{ARDUCAM_AUTO_FOCUS}"
        ),

        f"focus_absolute="
        f"{ARDUCAM_FOCUS_ABSOLUTE}"
    ]


    command = [
        "v4l2-ctl",
        "-d",
        device,
        "--set-ctrl="
        + ",".join(controls)
    ]


    print()
    print("=" * 72)
    print(
        f"[ARDUCAM CONFIG] "
        f"{camera_name}"
    )
    print(
        f"[DEVICE] {device}"
    )
    print(
        f"[EXPOSURE] "
        f"{ARDUCAM_EXPOSURE}"
    )
    print(
        f"[GAIN] "
        f"{ARDUCAM_GAIN}"
    )
    print(
        f"[SHARPNESS] "
        f"{ARDUCAM_SHARPNESS}"
    )
    print(
        f"[FOCUS] "
        f"{ARDUCAM_FOCUS_ABSOLUTE}"
    )
    print(
        f"[AUTO WB] "
        f"{ARDUCAM_AUTO_WHITE_BALANCE}"
    )
    print("=" * 72)


    try:

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )


    except FileNotFoundError:

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                "v4l2-ctl 명령을 "
                "찾을 수 없습니다."
            )
        )


    except subprocess.TimeoutExpired:

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} "
                "Arducam 설정 timeout"
            )
        )


    if result.returncode != 0:

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} "
                f"Arducam 설정 실패: "
                f"{result.stderr.strip()}"
            )
        )


    if (
        ARDUCAM_CONTROL_SETTLE_SECONDS
        > 0
    ):

        time.sleep(
            ARDUCAM_CONTROL_SETTLE_SECONDS
        )


    print(
        f"[ARDUCAM CONFIG COMPLETE] "
        f"{camera_name}"
    )


# =========================================================
# Server Startup Configuration
# =========================================================

def configure_arducams_on_startup():

    if not ARDUCAM_CONFIGURE_ON_STARTUP:
        return


    cameras = [

        (
            "left_plantar",
            LEFT_CAMERA_DEVICE
        ),

        (
            "right_plantar",
            RIGHT_CAMERA_DEVICE
        )
    ]


    for (
        camera_name,
        device
    ) in cameras:

        try:

            configure_arducam(
                device=device,
                camera_name=camera_name
            )


        except HardwareMeasurementError as e:

            # 서버 자체는 계속 실행.
            # 실제 촬영 직전에 다시 설정 시도.
            print()
            print(
                "[ARDUCAM STARTUP WARNING]"
            )
            print(
                f"Camera : "
                f"{camera_name}"
            )
            print(
                f"Reason : "
                f"{e.reason}"
            )
            print(
                f"Detail : "
                f"{e.detail}"
            )


# =========================================================
# Capture One Camera
#
# 중요:
#
# Input:
#   MJPEG
#
# 기존 방식:
#   MJPEG
#   -> decode
#   -> select filter
#   -> JPEG 재인코딩
#
# 현재 방식:
#   MJPEG
#   -> codec copy
#   -> 원본 JPEG frame 저장
#
# Auto WB 안정화를 위해 처음 N개 frame을 받은 뒤
# 마지막 원본 MJPEG frame만 최종 이미지로 사용
# =========================================================

def capture_photo(
    session_id: int,
    camera_name: str,
    device: str,
    width: int,
    height: int,
    framerate: int
) -> Path:


    # -----------------------------------------------------
    # Camera existence
    # -----------------------------------------------------

    if not Path(device).exists():

        raise HardwareMeasurementError(
            reason="DEVICE_DISCONNECTED",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} 카메라 장치를 "
                f"찾을 수 없습니다: {device}"
            )
        )


    # -----------------------------------------------------
    # Filename
    # -----------------------------------------------------

    timestamp = (
        time.strftime(
            "%Y%m%d_%H%M%S"
        )
    )


    filename = (
        PHOTO_DIR
        / (
            f"session_{session_id}_"
            f"{camera_name}_"
            f"{timestamp}.jpg"
        )
    )


    # -----------------------------------------------------
    # Temporary directory
    #
    # warmup frame들도 원본 MJPEG 그대로 임시 저장한 뒤
    # 마지막 frame 하나만 최종 파일로 남김
    # -----------------------------------------------------

    temp_dir = (
        PHOTO_DIR
        / (
            f".capture_"
            f"{session_id}_"
            f"{camera_name}_"
            f"{time.time_ns()}"
        )
    )


    temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    temp_pattern = (
        temp_dir
        / "frame_%03d.jpg"
    )


    # 최소 1 frame
    frame_count = max(
        1,
        CAMERA_WARMUP_FRAMES + 1
    )


    print()
    print("=" * 72)

    print(
        f"[CAMERA] {camera_name}"
    )

    print(
        f"[DEVICE] {device}"
    )

    print(
        f"[RESOLUTION] "
        f"{width}x{height}"
    )

    print(
        f"[FPS] {framerate}"
    )

    print(
        "[FORMAT] MJPEG ORIGINAL"
    )

    print(
        f"[WARMUP] "
        f"{CAMERA_WARMUP_FRAMES} frames"
    )

    print("=" * 72)


    # -----------------------------------------------------
    # FFmpeg
    #
    # -c:v copy
    #
    # ★ 디코딩 / 필터 / 재인코딩 없음
    # ★ 카메라가 출력한 MJPEG packet 그대로 저장
    # -----------------------------------------------------

    command = [

        "ffmpeg",

        "-hide_banner",

        "-loglevel",
        "error",

        "-f",
        "v4l2",

        "-input_format",
        "mjpeg",

        "-video_size",
        f"{width}x{height}",

        "-framerate",
        str(framerate),

        "-i",
        device,

        "-map",
        "0:v:0",

        "-c:v",
        "copy",

        "-frames:v",
        str(frame_count),

        "-f",
        "image2",

        "-y",

        str(temp_pattern)
    ]


    try:

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )


    except subprocess.TimeoutExpired:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} "
                "카메라 촬영 timeout"
            )
        )


    except FileNotFoundError:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                "ffmpeg 명령을 "
                "찾을 수 없습니다."
            )
        )


    # -----------------------------------------------------
    # FFmpeg failure
    # -----------------------------------------------------

    if result.returncode != 0:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} "
                f"카메라 촬영 실패: "
                f"{result.stderr.strip()}"
            )
        )


    # -----------------------------------------------------
    # Get captured frames
    # -----------------------------------------------------

    frame_files = sorted(
        temp_dir.glob(
            "frame_*.jpg"
        )
    )


    if not frame_files:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} "
                "MJPEG frame이 생성되지 않았습니다."
            )
        )


    # -----------------------------------------------------
    # Last frame
    #
    # Auto WB warmup 이후 마지막 frame 사용
    # -----------------------------------------------------

    final_frame = frame_files[-1]


    if (
        not final_frame.exists()
        or final_frame.stat().st_size == 0
    ):

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} "
                "MJPEG frame 크기가 "
                "0 byte입니다."
            )
        )


    # -----------------------------------------------------
    # Move original JPEG frame
    #
    # 파일 내용을 다시 인코딩하지 않고
    # 마지막 MJPEG frame 파일 자체를 이동
    # -----------------------------------------------------

    shutil.move(
        str(final_frame),
        str(filename)
    )


    # 나머지 warmup frame 삭제
    shutil.rmtree(
        temp_dir,
        ignore_errors=True
    )


    # -----------------------------------------------------
    # Final validation
    # -----------------------------------------------------

    if (
        not filename.exists()
        or filename.stat().st_size == 0
    ):

        raise HardwareMeasurementError(
            reason="CAMERA_ERROR",
            message=(
                "사진 촬영에 실패했습니다. "
                "다시 시도해주세요."
            ),
            detail=(
                f"{camera_name} "
                "최종 이미지 저장 실패"
            )
        )


    print()
    print(
        f"[CAMERA SAVE] "
        f"{filename}"
    )

    print(
        f"[FILE SIZE] "
        f"{filename.stat().st_size} bytes"
    )

    print(
        "[ENCODING] "
        "MJPEG ORIGINAL / NO RE-ENCODE"
    )


    return filename


# =========================================================
# Capture All Cameras
#
# Sequence:
#
# LEFT
# ->
# RIGHT
# ->
# DORSAL
#
# 세 카메라를 동시에 스트리밍하지 않음
# =========================================================

def capture_all_photos(
    session_id: int
) -> dict:


    with camera_lock:


        print()
        print("=" * 72)
        print(
            "[CAMERA SEQUENCE START]"
        )
        print(
            "LEFT -> RIGHT -> DORSAL"
        )
        print("=" * 72)


        # =================================================
        # 1. LEFT Arducam
        # =================================================

        print()
        print(
            "[CAMERA 1/3] LEFT OPEN"
        )


        if ARDUCAM_CONFIGURE_BEFORE_CAPTURE:

            configure_arducam(
                device=
                    LEFT_CAMERA_DEVICE,

                camera_name=
                    "left_plantar"
            )


        left = capture_photo(

            session_id=
                session_id,

            camera_name=
                "left_plantar",

            device=
                LEFT_CAMERA_DEVICE,

            width=
                LEFT_IMAGE_WIDTH,

            height=
                LEFT_IMAGE_HEIGHT,

            framerate=
                LEFT_CAMERA_FRAMERATE
        )


        print(
            "[CAMERA 1/3] LEFT CLOSED"
        )


        if CAMERA_SWITCH_DELAY_SECONDS > 0:

            time.sleep(
                CAMERA_SWITCH_DELAY_SECONDS
            )


        # =================================================
        # 2. RIGHT Arducam
        # =================================================

        print()
        print(
            "[CAMERA 2/3] RIGHT OPEN"
        )


        if ARDUCAM_CONFIGURE_BEFORE_CAPTURE:

            configure_arducam(
                device=
                    RIGHT_CAMERA_DEVICE,

                camera_name=
                    "right_plantar"
            )


        right = capture_photo(

            session_id=
                session_id,

            camera_name=
                "right_plantar",

            device=
                RIGHT_CAMERA_DEVICE,

            width=
                RIGHT_IMAGE_WIDTH,

            height=
                RIGHT_IMAGE_HEIGHT,

            framerate=
                RIGHT_CAMERA_FRAMERATE
        )


        print(
            "[CAMERA 2/3] RIGHT CLOSED"
        )


        if CAMERA_SWITCH_DELAY_SECONDS > 0:

            time.sleep(
                CAMERA_SWITCH_DELAY_SECONDS
            )


        # =================================================
        # 3. DORSAL Webcam
        # =================================================

        print()
        print(
            "[CAMERA 3/3] DORSAL OPEN"
        )


        dorsal = capture_photo(

            session_id=
                session_id,

            camera_name=
                "dorsal",

            device=
                DORSAL_CAMERA_DEVICE,

            width=
                DORSAL_IMAGE_WIDTH,

            height=
                DORSAL_IMAGE_HEIGHT,

            framerate=
                DORSAL_CAMERA_FRAMERATE
        )


        print(
            "[CAMERA 3/3] DORSAL CLOSED"
        )


        print()
        print("=" * 72)
        print(
            "[CAMERA SEQUENCE COMPLETE]"
        )
        print("=" * 72)


        return {

            "left":
                left,

            "right":
                right,

            "dorsal":
                dorsal
        }


# =========================================================
# Camera Status
# =========================================================

def get_camera_status():

    return {

        "leftPlantar": {

            "device":
                LEFT_CAMERA_DEVICE,

            "exists":
                Path(
                    LEFT_CAMERA_DEVICE
                ).exists(),

            "resolution":
                (
                    f"{LEFT_IMAGE_WIDTH}"
                    f"x{LEFT_IMAGE_HEIGHT}"
                )
        },


        "rightPlantar": {

            "device":
                RIGHT_CAMERA_DEVICE,

            "exists":
                Path(
                    RIGHT_CAMERA_DEVICE
                ).exists(),

            "resolution":
                (
                    f"{RIGHT_IMAGE_WIDTH}"
                    f"x{RIGHT_IMAGE_HEIGHT}"
                )
        },


        "dorsal": {

            "device":
                DORSAL_CAMERA_DEVICE,

            "exists":
                Path(
                    DORSAL_CAMERA_DEVICE
                ).exists(),

            "resolution":
                (
                    f"{DORSAL_IMAGE_WIDTH}"
                    f"x{DORSAL_IMAGE_HEIGHT}"
                )
        }
    }

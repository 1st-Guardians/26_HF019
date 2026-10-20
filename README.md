<div align="center">

  # <img width="150" alt="FeetFit 로고" src="https://github.com/user-attachments/assets/29aed26f-43c3-45c2-bfdd-4cd4637af80f" />


**FeetFit: 멀티모달 기반 발 상태 분석 및 건강 관리 시스템**  
*누구나 간편하게 발을 측정하고, 변화까지 관리할 수 있도록*

`2026 한이음 드림업` · `26_HF019` · `Team Guardians (가디언즈)`


<img width="800" alt="FeetFit 시스템 개요" src="https://github.com/user-attachments/assets/a3c66129-80a3-48e8-869a-f68483fcf924" />

</div>

---

</br>

## 💡 1. 프로젝트 개요

### 1-1. 프로젝트 소개

<p align="center">
  <img src="https://github.com/user-attachments/assets/d11f090e-bed1-4d82-a241-4cd8f26606ad" width="90%" />
</p>

- **FeetFit**: 멀티모달 기반 발 상태 분석 및 건강 관리 시스템
- 카메라와 압력 센서로 발의 외형·피부 상태·족저 하중을 분석하고, **맞춤형 관리 정보와 신발 추천, 변화 추적**까지 제공하는 발 건강 관리 서비스

</br>

### 1-2. 개발 배경 및 필요성
발 길이가 같더라도 발볼, 발의 형태, 하중이 집중되는 위치는 서로 다릅니다. 그러나 자신의 발 상태를 객관적으로 확인하고 꾸준히 관리할 기회는 제한적입니다. FeetFit은 **누구나 간편하게 발 상태를 측정하고, 결과를 일상 속 관리로 연결**할 수 있도록 개발되었습니다.

</br>

### 1-3. 프로젝트 특·장점
- **멀티모달 통합 분석**: 발 이미지와 24개 FSR 센서로 외형·피부·족저 하중을 함께 분석
- **일관된 측정 환경**: 자체 제작 디바이스로 촬영 및 센서 측정 환경을 표준화
- **데이터 기반 신발 추천**: 발 측정 결과와 신발 특성·실제 착용 리뷰를 비교해 적합도 및 추천 근거 제공
- **지속적인 발 관리**: 측정 결과를 누적해 이전 상태와의 변화 확인 및 맞춤 관리 지원

</br>

### 1-4. 주요 기능

- 👣 **발 상태 측정**: 상·하단 카메라와 압력 센서로 발 이미지 및 상대 하중 데이터 수집, 온·습도는 보조 데이터로 활용
- 🛠️ **AI 발 상태 분석**: 발 치수·외형 정렬, 피부 이상 의심 영역, 발바닥 접촉 영역, 좌·우 하중 균형 분석
- 📊 **시각화 리포트**: 발 상태 점수, 족저 하중 히트맵, 분석 결과 및 PDF 리포트 제공
- 💊 **맞춤형 추천**: 개인의 발 특성에 따른 신발 적합도와 추천 사유, 의약품 및 관리용품 정보 제공
- 📈 **변화 추적 및 관리**: 날짜별 측정 이력, 상태 변화 그래프, 개인별 관리 팁과 실천 항목 제공

</br>

### 1-5. 기대 효과 및 활용 분야

<p align="center">
  <img src="https://github.com/user-attachments/assets/232c5ac4-db48-4cc9-a276-97b2310d23dd" width="45%" />
  <img src="https://github.com/user-attachments/assets/18f78c69-0885-462e-8611-ad900c043b17" width="45%" />
</p>

- **기대 효과**: 발 상태의 객관적 확인부터 맞춤 관리, 반복 측정까지 연결하여 지속적인 발 관리 지원
- **활용 분야**: 신발 매장·러닝 전문점, 운동·웰니스 시설, 신발·인솔 연구개발 등

</br>

### 1-6. 기술 스택

| 구분 | 기술 및 장비 |
|:---|:---|
| **iOS** | Swift, SwiftUI |
| **Backend** | Java, Spring Boot, MySQL, WebSocket/STOMP |
| **AI** | Python, FastAPI, YOLO11n-seg, SegFormer, OpenCV, BGE-M3 |
| **Hardware** | Raspberry Pi 4, ABKO APC920W QHD 웹캠, Arducam IMX219 카메라 모듈 2대, IMS-C20 FSR 센서 24개, BME280 |
| **Infra** | AWS EC2·RDS·S3, Docker, Nginx |
| **Collaboration** | GitHub, Figma, Notion |

---

</br>

## 👥 2. 팀원 소개

| **멘티 1** | **멘티 2** | **멘티 3** | **멘티 4** | **멘토** |
|:---:|:---:|:---:|:---:|:---:|
| 프로젝트 총괄<br>iOS·H/W 통합 | iOS 앱 개발<br>발 외형 분석 | 백엔드 개발<br>피부·접촉 영역 분석 | 백엔드 개발<br>신발 추천 알고리즘 | 프로젝트 멘토링<br>기술 자문 |

---

</br>

## 🏗️ 3. 시스템 구성도

### 3-1. 서비스 구성도


<p align="center">
  <img width="80%" alt="FeetFit 서비스 구성도" src="https://github.com/user-attachments/assets/4352b342-b091-4b0c-b0f0-ecf8e97b3fc2" />
</p>

앱에서 측정을 시작하면 **Raspberry Pi가 센서 데이터를 수집**하고, **AI 서버가 분석**한 결과를 **Spring Boot 서버를 통해 iOS 앱**에 전달합니다. 측정 진행 상태는 WebSocket/STOMP로 동기화합니다.

### 3-2. 하드웨어 구성도

<img width="100%" alt="FeetFit 하드웨어 설계도" src="https://github.com/user-attachments/assets/5bfebef8-5a1b-451c-a628-074cdc0a651b" />

상·하단 카메라, 양발 압력 센서, 온·습도 센서, Raspberry Pi를 결합한 **발 측정 디바이스**입니다.

---

</br>

## 🎥 4. 작품 소개영상

<p align="center">
  <a href="https://youtu.be/uXCO0hV9jac">
    <img
      src="https://img.youtube.com/vi/uXCO0hV9jac/maxresdefault.jpg"
      alt="FeetFit 프로젝트 소개 영상"
      width="750"
    />
  </a>
</p>



---

</br>

## 💻 5. 핵심 소스코드

<details>
<summary><strong>① [Backend] 측정 상태에 따른 하드웨어 자동 제어</strong></summary>

측정 상태를 확인하여 사진 촬영, 온·습도, 압력 측정 중 필요한 하드웨어 작업을 실행합니다. 

```java
MeasurementStatus currentStatus = measurementSession.getStatus();
if (previousStatus == currentStatus) return;

Runnable hardwareRequest = switch (currentStatus) {
    case READY_FOR_PHOTO -> () -> measurementHardwareClient.requestPhotoCapture(
            measurementSession.getId(), authorizationHeader);
    case READY_FOR_ENVIRONMENT -> () -> measurementHardwareClient.requestEnvironmentMeasurement(
            measurementSession.getId(), authorizationHeader);
    case READY_FOR_PRESSURE -> () -> measurementHardwareClient.requestPressureMeasurement(
            measurementSession.getId(), authorizationHeader);
    default -> null;
};

if (hardwareRequest == null) return;
requestHardwareTaskAfterCommit(hardwareRequest);
```

</details>

<details>
<summary><strong>② [Backend] 측정 완료 검증 및 중복 처리 방지</strong></summary>

모든 분석이 완료됐는지 확인하고, 비관적 잠금으로 중복 완료 처리를 방지합니다.

```java
if (!analysisStatus.isReadyToComplete()
        || measurementSession.getStatus() == MeasurementStatus.COMPLETED
        || measurementSession.getStatus() == MeasurementStatus.FAILED) {
    return;
}

MeasurementSession lockedMeasurementSession = measurementSessionRepository
        .findByIdForUpdate(measurementSession.getId())
        .orElseThrow(() -> new MeasurementHandler(ErrorStatus.MEASUREMENT_NOT_FOUND));

if (lockedMeasurementSession.getStatus() == MeasurementStatus.COMPLETED
        || lockedMeasurementSession.getStatus() == MeasurementStatus.FAILED) {
    return;
}

lockedMeasurementSession.updateStatus(
        MeasurementStatus.COMPLETED,
        resolveMeasurementDurationSec(lockedMeasurementSession, measurementDurationSec)
);
measurementSocketService.sendMeasurementStatusChanged(lockedMeasurementSession);
```

</details>

<details>
<summary><strong>③ [Backend] AI 기반 신발 추천 실행</strong></summary>

추천할 신발 데이터와 중복 요청 여부를 확인한 뒤 AI 추천 서버를 호출합니다.

```java
long shoeCount = shoeRepository.count();
if (shoeCount <= 0) return;

int expectedCount = Math.toIntExact(shoeCount);
claimed = recovery
        ? runService.claimAutomaticRetry(userId, measurementSessionId, expectedCount)
        : runService.claimAutomaticRun(userId, measurementSessionId, expectedCount);

if (!claimed) return;

String accessToken = tokenProvider.createAccessToken(userId);
aiClient.requestAllShoeRecommendations(measurementSessionId, accessToken);
runService.completeRun(userId, measurementSessionId);
```

</details>

<details>
<summary><strong>④ [iOS] WebSocket/STOMP 메시지 처리</strong></summary>

백엔드에서 수신한 측정 진행 상태를 STOMP 프레임 종류별로 구분해 iOS 앱에 반영합니다.

```swift
private func handleStompFrame(_ text: String) {
    if text.hasPrefix("CONNECTED") {
        isConnected = true
        DispatchQueue.main.async { self.onConnected?() }
        return
    }

    if text.hasPrefix("MESSAGE") {
        let body = extractBody(from: text)
        DispatchQueue.main.async {
            self.onMeasurementMessage?(body)
        }
        return
    }

    if text.hasPrefix("ERROR") {
        print("STOMP ERROR 수신:", text)
        return
    }
}
```

</details>

<details>
<summary><strong>⑤ [Hardware] LED 제어 및 발 이미지 촬영</strong></summary>

촬영 시작 상태를 백엔드에 전달하고 LED 제어 후 이미지를 AI 서버로 전송합니다.

```python
patch_status(session_id, "CAPTURING_PHOTO")

try:
    led_on()
    photos = capture_all_photos(session_id)
finally:
    led_off()

ai_result = send_photo(session_id, photos)
```

</details>

<details>
<summary><strong>⑥ [Hardware] FSR 압력 센서 보정 및 노이즈 제거</strong></summary>

센서별 무하중 기준값을 차감하고 음수 출력을 제거하여 상대 하중값을 보정합니다.

```python
def correct_value(raw, baseline):
    value = raw - baseline
    if value < 0:
        value = 0.0
    return value
```

반복 측정값에는 중앙값 필터를 적용합니다.

```python
if MEDIAN_WINDOW == 1:
    filtered = values
else:
    half = MEDIAN_WINDOW // 2
    filtered = [
        statistics.median(values[max(0, i-half):min(len(values), i+half+1)])
        for i in range(len(values))
    ]

return float(statistics.mean(filtered))
```

</details>

> **참고:** 위 코드는 설계서의 실제 코드 중 핵심 로직을 발췌한 것으로, 일부 메서드 선언·의존성·예외 처리가 생략되어 있습니다.


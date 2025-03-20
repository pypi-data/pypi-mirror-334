import abc
from abc import ABCMeta, abstractmethod
from collections.abc import AsyncGenerator, Awaitable, Coroutine
from typing import Any, Callable, Generic, overload

from PIL import Image as Image
from typing_extensions import Literal, NotRequired, Protocol, TypedDict, TypeVar

from .hybrid_observer import HybridObservable

# Literals
FrameType = Literal["video", "motion"]
CameraType = Literal["camera", "doorbell"]
ZoneType = Literal["intersect", "contain"]
ZoneFilter = Literal["include", "exclude"]
ObjectClass = Literal["person", "vehicle", "animal", "motion", "other"]
CameraRole = Literal["high-resolution", "mid-resolution", "low-resolution", "snapshot"]
DecoderFormat = Literal["yuv420p", "rgb24", "nv12"]
ImageInputFormat = Literal["yuv420p", "nv12", "rgb", "rgba", "gray"]
ImageOutputFormat = Literal["rgb", "rgba", "gray"]
CameraExtension = Literal[
    "cameraController", "hub", "motionDetection", "objectDetection", "audioDetection", "ptz"
]
CameraFrameWorkerDecoder = Literal["pillow", "wasm", "rust", "gpu"]
CameraFrameWorkerResolution = Literal[
    "640x480",
    "640x360",
    "320x240",
    "320x180",
]
AudioCodec = Literal["PCMU", "PCMA", "MPEG4-GENERIC", "opus", "G722", "MPA", "PCM", "FLAC"]
AudioFFmpegCodec = Literal[
    "pcm_mulaw", "pcm_alaw", "aac", "libopus", "g722", "mp3", "pcm_s16be", "pcm_s16le", "flac"
]
VideoCodec = Literal["H264", "H265", "VP8", "VP9", "AV1", "JPEG", "RAW"]
VideoFFmpegCodec = Literal["h264", "hevc", "vp8", "vp9", "av1", "mjpeg", "rawvideo"]
PythonVersion = Literal["3.9", "3.10", "3.11", "3.12"]
InternalSourceType = Literal["aac", "opus", "pcma"]
StateNames = Literal["light", "motion", "audio", "doorbell", "siren", "battery", "object"]
CameraPublicProperties = Literal[
    "_id",
    "audioDetectionPluginId",
    "cameraControllerPluginId",
    "detectionSettings",
    "detectionZones",
    "disabled",
    "frameWorkerSettings",
    "hasBattery",
    "hasBinarySensor",
    "hasLight",
    "hasSiren",
    "info",
    "isCloud",
    "motionDetectionPluginId",
    "name",
    "nativeId",
    "objectDetectionPluginId",
    "pluginId",
    "ptzPluginId",
    "snapshotTTL",
    "sources",
    "type",
]
DeviceManagerEventType = Literal[
    "cameraSelected",
    "cameraDeselected",
]
JsonSchemaType = Literal["string", "number", "boolean", "object", "array", "button"]
LoggerLevel = Literal["error", "warn", "info", "debug", "trace", "attention", "success"]
APIEventType = Literal["finishLaunching", "shutdown"]
InternalRole = Literal["AAC", "OPUS", "PCMA"]
Callback = Callable[..., Any] | Callable[..., Coroutine[Any, Any, Any]]
JSONValue = str | int | float | bool | dict[str, Any] | list[Any]
JSONObject = dict[str, JSONValue]
JSONArray = list[JSONValue]
Path = list[int | str] | int | str

class CameraInformation(TypedDict, total=False):
    model: str
    manufacturer: str
    hardware: str
    serialNumber: str
    firmwareVersion: str
    supportUrl: str

Point = tuple[float, float]
BoundingBox = tuple[float, float, float, float]

class Detection(TypedDict):
    id: NotRequired[str]
    label: ObjectClass
    confidence: float
    boundingBox: BoundingBox
    inputWidth: int
    inputHeight: int
    origWidth: int
    origHeight: int

class ZoneCoord(TypedDict):
    _id: str
    points: Point

class ZoneRegion(TypedDict):
    _id: str
    coords: list[ZoneCoord]
    type: ZoneType
    filter: ZoneFilter
    classes: list[ObjectClass]
    isPrivacyMask: bool
    color: str

class CameraZone(TypedDict):
    name: str
    regions: list[ZoneRegion]

class DetectionZone(TypedDict):
    name: str
    points: list[Point]
    type: ZoneType
    filter: ZoneFilter
    classes: list[ObjectClass]
    isPrivacyMask: bool
    color: str

class MotionDetectionSettings(TypedDict):
    timeout: int

class ObjectDetectionSettings(TypedDict):
    confidence: float

class CameraDetectionSettings(TypedDict):
    motion: MotionDetectionSettings
    object: ObjectDetectionSettings

class CameraFrameWorkerSettings(TypedDict):
    decoder: CameraFrameWorkerDecoder
    fps: int
    resolution: CameraFrameWorkerResolution

class CameraInput(TypedDict):
    _id: str
    name: str
    role: CameraRole
    useForSnapshot: bool
    hotMode: bool
    urls: StreamUrls
    internal: InternalRole | None

class RTPInfo(TypedDict):
    payload: int | None
    codec: str
    rate: int | None
    encoding: int | None

class FMTPInfo(TypedDict):
    payload: int
    config: str

class AudioCodecProperties(TypedDict):
    sampleRate: int
    channels: int
    payloadType: int
    fmtpInfo: FMTPInfo | None

class VideoCodecProperties(TypedDict):
    clockRate: int
    payloadType: int
    fmtpInfo: FMTPInfo | None

class AudioStreamInfo(TypedDict):
    codec: AudioCodec
    ffmpegCodec: AudioFFmpegCodec
    properties: AudioCodecProperties
    direction: Literal["sendonly", "recvonly", "sendrecv", "inactive"]

class VideoStreamInfo(TypedDict):
    codec: VideoCodec
    ffmpegCodec: VideoFFmpegCodec
    properties: VideoCodecProperties
    direction: Literal["sendonly", "recvonly", "sendrecv", "inactive"]

class ProbeConfig(TypedDict, total=False):
    video: VideoCodec
    audio: AudioCodec
    microphone: AudioCodec

class ProbeStream(TypedDict):
    sdp: str
    audio: list[AudioStreamInfo]
    video: list[VideoStreamInfo]

class StreamUrls(TypedDict):
    ws: Go2RtcWSSource
    rtsp: Go2RtcRTSPSource
    www: Go2RtcEndpoint

class Go2RtcRTSPSource(TypedDict):
    default: str
    defaultMicrophone: str
    muted: str
    h264: str
    h265: str
    aac: str
    opus: str
    pcma: str
    mp4: str
    onvif: str

class Go2RtcEndpoint(TypedDict):
    webrtc: str
    mse: str
    lmp4: str
    mmp4: str
    mp4: str
    mp4Snapshot: str
    jpegSnapshot: str
    lHlsTs: str
    lHlsFmp4: str
    mHlsFmp4: str
    mjpeg: str
    mjpegHtml: str

class Go2RtcSource(TypedDict):
    name: str
    src: str
    ws: str

class Go2RtcWSSource(TypedDict):
    webrtc: str
    mse: str

T = TypeVar(
    "T",
    bound="LightStateWithoutLastEvent"
    | "AudioStateWithoutLastEvent"
    | "MotionStateWithoutLastEvent"
    | "ObjectStateWithoutLastEvent"
    | "SirenStateWithoutLastEvent"
    | "BatteryStateWithoutLastEvent"
    | "DoorbellStateWithoutLastEvent",
)

class BaseState(TypedDict, Generic[T]):
    timestamp: int
    lastEvent: NotRequired[T | None]

class BaseStateWithoutLastEvent(TypedDict):
    timestamp: int

class MotionSetEvent(TypedDict):
    state: bool
    detections: NotRequired[list[Detection] | None]

class AudioSetEvent(TypedDict):
    state: bool
    db: NotRequired[float | None]

class ObjectSetEvent(TypedDict):
    detections: list[Detection]

class LightSetEvent(TypedDict):
    state: bool

class DoorbellSetEvent(TypedDict):
    state: bool

class SirenSetEvent(TypedDict):
    state: bool
    level: NotRequired[int | None]

class BatterySetEvent(TypedDict):
    level: int
    lowBattery: NotRequired[bool | None]
    charging: NotRequired[bool | None]

class LightState(BaseState["LightStateWithoutLastEvent"], LightSetEvent): ...
class LightStateWithoutLastEvent(BaseStateWithoutLastEvent, LightSetEvent): ...
class MotionState(BaseState["MotionStateWithoutLastEvent"], MotionSetEvent): ...
class MotionStateWithoutLastEvent(BaseStateWithoutLastEvent, MotionSetEvent): ...
class AudioState(BaseState["AudioStateWithoutLastEvent"], AudioSetEvent): ...
class AudioStateWithoutLastEvent(BaseStateWithoutLastEvent, AudioSetEvent): ...
class DoorbellState(BaseState["DoorbellStateWithoutLastEvent"], DoorbellSetEvent): ...
class DoorbellStateWithoutLastEvent(BaseStateWithoutLastEvent, DoorbellSetEvent): ...
class SirenState(BaseState["SirenStateWithoutLastEvent"], SirenSetEvent): ...
class SirenStateWithoutLastEvent(BaseStateWithoutLastEvent, SirenSetEvent): ...
class ObjectState(BaseState["ObjectStateWithoutLastEvent"], ObjectSetEvent): ...
class ObjectStateWithoutLastEvent(BaseStateWithoutLastEvent, ObjectSetEvent): ...
class BatteryState(BaseState["BatteryStateWithoutLastEvent"], BatterySetEvent): ...
class BatteryStateWithoutLastEvent(BaseStateWithoutLastEvent, BatterySetEvent): ...

class StateValues(TypedDict):
    light: LightState
    motion: MotionState
    audio: AudioState
    object: ObjectState
    doorbell: DoorbellState
    siren: SirenState
    battery: BatteryState

class SetValues(TypedDict):
    light: LightSetEvent
    motion: MotionSetEvent
    audio: AudioSetEvent
    object: ObjectSetEvent
    doorbell: DoorbellSetEvent
    siren: SirenSetEvent
    battery: BatterySetEvent

class FrameData(TypedDict):
    data: bytes
    timestamp: int
    metadata: FrameMetadata
    info: ImageInformation

class FrameMetadata(TypedDict):
    format: DecoderFormat
    frameSize: float | int
    width: int
    origWidth: int
    height: int
    origHeight: int

class ImageInformation(TypedDict):
    width: int
    height: int
    channels: Literal[1, 3, 4]
    format: ImageInputFormat

class ImageCrop(TypedDict):
    top: int
    left: int
    width: int
    height: int

class ImageResize(TypedDict):
    width: int
    height: int

class ImageFormat(TypedDict):
    to: ImageOutputFormat

class ImageOptions(TypedDict, total=False):
    format: ImageFormat
    crop: ImageCrop
    resize: ImageResize

class FrameImage(TypedDict):
    image: Image.Image
    info: ImageInformation

class FrameBuffer(TypedDict):
    image: bytes
    info: ImageInformation

class MotionDetectionFrame(TypedDict):
    frame: FrameData
    state: MotionSetEvent

class VideoFrame(Protocol):
    @property
    def data(self) -> bytes: ...
    @property
    def metadata(self) -> FrameMetadata: ...
    @property
    def info(self) -> ImageInformation: ...
    @property
    def timestamp(self) -> int: ...
    @property
    def motion(self) -> MotionSetEvent | None: ...
    @property
    def input_width(self) -> int: ...
    @property
    def input_height(self) -> int: ...
    @property
    def input_format(self) -> DecoderFormat: ...
    async def to_buffer(self, options: ImageOptions | None = None) -> FrameBuffer: ...
    async def to_image(self, options: ImageOptions | None = None) -> FrameImage: ...
    async def save(self, path: str, options: ImageOptions | None = None) -> None: ...

class CameraInputSettings(TypedDict):
    _id: str
    name: str
    role: CameraRole
    useForSnapshot: bool
    hotMode: bool
    urls: list[str]
    internal: InternalRole | None

class CameraConfigInputSettings(TypedDict):
    name: str
    role: CameraRole
    useForSnapshot: bool
    hotMode: bool
    urls: list[str]

class BaseCameraConfig(TypedDict):
    name: str
    nativeId: str | None
    isCloud: bool | None
    hasLight: bool | None
    hasSiren: bool | None
    hasBinarySensor: bool | None
    hasBattery: bool | None
    disabled: bool | None
    info: CameraInformation | None

class CameraConfig(BaseCameraConfig):
    sources: list[CameraConfigInputSettings]

class CameraDelegate(Protocol):
    async def snapshot(self, source_id: str, force_new: bool | None = None) -> bytes | None: ...

class CameraPTZDelegate(Protocol):
    async def moveAbsolute(self, pan: float, tilt: float, zoom: float) -> None: ...
    async def moveRelative(self, pan: float, tilt: float, zoom: float) -> None: ...
    async def moveContinuous(self, pan: float, tilt: float, zoom: float) -> None: ...
    async def stop(self) -> None: ...

class CameraDelegates(TypedDict):
    cameraDelegate: CameraDelegate
    ptzDelegate: CameraPTZDelegate

class CameraBaseSource(Protocol):
    id: str
    name: str
    role: CameraRole
    useForSnapshot: bool
    hotMode: bool
    urls: StreamUrls
    internal: InternalRole | None
    async def snapshot(self, force_new: bool | None = None) -> bytes | None: ...
    async def probe_stream(
        self, probe_config: ProbeConfig | None = None, refresh: bool | None = None
    ) -> ProbeStream | None: ...
    def create_webrtc_session(self) -> None: ...
    def create_rtsp_session(self) -> None: ...
    def create_fmp4_session(self) -> None: ...

class CameraDeviceSource(CameraBaseSource, Protocol):
    def get_internal_source(self, type: InternalSourceType) -> CameraBaseSource: ...

class WebRTCConnectionOptions(TypedDict, total=False):
    iceServers: list[IceServer]

class RTSPConnectionOptions(TypedDict, total=False):
    target: Literal[
        "default",
        "defaultMicrophone",
        "h264",
        "h265",
        "aac",
        "opus",
        "pcma",
        "h264aac",
        "h265aac",
        "h264opus",
        "h265opus",
        "h264pcma",
        "h265pcma",
        "mp4",
    ]

SpawnInput = str | int

class FfmpegOptions(TypedDict):
    ffmpegPath: str
    input: list[SpawnInput] | None
    video: list[SpawnInput] | None
    audio: list[SpawnInput] | None
    output: list[SpawnInput]
    logger: dict[str, Any] | None

class ReturnAudioFFmpegOptions(TypedDict):
    ffmpegPath: str
    input: list[SpawnInput]
    logPrefix: str | None

class BaseCamera(TypedDict):
    _id: str
    nativeId: str | None
    pluginId: str
    name: str
    disabled: bool
    isCloud: bool
    hasLight: bool
    hasSiren: bool
    hasBinarySensor: bool
    hasBattery: bool
    info: CameraInformation
    type: CameraType
    snapshotTTL: int
    detectionSettings: CameraDetectionSettings
    frameWorkerSettings: CameraFrameWorkerSettings

class Camera(BaseCamera):
    cameraControllerPluginId: str | None
    audioDetectionPluginId: str | None
    motionDetectionPluginId: str | None
    objectDetectionPluginId: str | None
    ptzPluginId: str | None
    sources: list[CameraInput]
    detectionZones: list[DetectionZone]

StateValue = LightState | MotionState | AudioState | DoorbellState | SirenState | ObjectState | BatteryState
SV = TypeVar("SV", bound=StateValue)

class CameraStateChangedObject(TypedDict, Generic[SV]):
    old_state: SV
    new_state: SV

class CameraPropertyObservableObject(TypedDict):
    property: str
    old_state: Any
    new_state: Any

class CameraConfigInputSettingsPartial(TypedDict, total=False):
    name: str
    role: CameraRole
    useForSnapshot: bool
    hotMode: bool
    urls: list[str]

class CameraDevice(Protocol):
    @property
    def id(self) -> str: ...
    @property
    def native_id(self) -> str | None: ...
    @property
    def plugin_id(self) -> str: ...
    @property
    def connected(self) -> bool: ...
    @property
    def frameworker_connected(self) -> bool: ...
    @property
    def disabled(self) -> bool: ...
    @property
    def name(self) -> str: ...
    @property
    def type(self) -> CameraType: ...
    @property
    def snapshot_ttl(self) -> int: ...
    @property
    def info(self) -> CameraInformation: ...
    @property
    def is_cloud(self) -> bool: ...
    @property
    def has_light(self) -> bool: ...
    @property
    def has_siren(self) -> bool: ...
    @property
    def has_binary_sensor(self) -> bool: ...
    @property
    def has_battery(self) -> bool: ...
    @property
    def has_motion_detector(self) -> bool: ...
    @property
    def has_audio_detector(self) -> bool: ...
    @property
    def has_object_detector(self) -> bool: ...
    @property
    def has_ptz(self) -> bool: ...
    @property
    def detection_zones(self) -> list[DetectionZone]: ...
    @property
    def detection_settings(self) -> CameraDetectionSettings: ...
    @property
    def frameworker_settings(self) -> CameraFrameWorkerSettings: ...
    @property
    def stream_source(self) -> CameraDeviceSource: ...
    @property
    def high_resolution_source(self) -> CameraDeviceSource | None: ...
    @property
    def mid_resolution_source(self) -> CameraDeviceSource | None: ...
    @property
    def low_resolution_source(self) -> CameraDeviceSource | None: ...
    @property
    def snapshot_source(self) -> CameraBaseSource | None: ...
    @property
    def ptz(self) -> CameraPTZDelegate: ...
    @property
    def sources(self) -> list[CameraDeviceSource]: ...
    @property
    def internal_sources(self) -> list[CameraBaseSource]: ...
    on_connected: HybridObservable[bool]
    on_frameworker_connected: HybridObservable[bool]
    on_light_switched: HybridObservable[LightState]
    on_motion_detected: HybridObservable[MotionState]
    on_audio_detected: HybridObservable[AudioState]
    on_object_detected: HybridObservable[ObjectState]
    on_doorbell_pressed: HybridObservable[DoorbellState]
    on_siren_detected: HybridObservable[SirenState]
    on_battery_changed: HybridObservable[BatteryState]
    logger: LoggerService
    @overload
    def on_state_change(
        self, state_name: Literal["light"]
    ) -> HybridObservable[CameraStateChangedObject[LightState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["motion"]
    ) -> HybridObservable[CameraStateChangedObject[MotionState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["audio"]
    ) -> HybridObservable[CameraStateChangedObject[AudioState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["doorbell"]
    ) -> HybridObservable[CameraStateChangedObject[DoorbellState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["siren"]
    ) -> HybridObservable[CameraStateChangedObject[SirenState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["battery"]
    ) -> HybridObservable[CameraStateChangedObject[BatteryState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["object"]
    ) -> HybridObservable[CameraStateChangedObject[ObjectState]]: ...
    def on_property_change(
        self, property: CameraPublicProperties | list[CameraPublicProperties]
    ) -> HybridObservable[CameraPropertyObservableObject]: ...
    @overload
    def get_value(self, state_name: Literal["light"]) -> LightState: ...
    @overload
    def get_value(self, state_name: Literal["motion"]) -> MotionState: ...
    @overload
    def get_value(self, state_name: Literal["audio"]) -> AudioState: ...
    @overload
    def get_value(self, state_name: Literal["object"]) -> ObjectState: ...
    @overload
    def get_value(self, state_name: Literal["doorbell"]) -> DoorbellState: ...
    @overload
    def get_value(self, state_name: Literal["siren"]) -> SirenState: ...
    @overload
    def get_value(self, state_name: Literal["battery"]) -> BatteryState: ...
    @overload
    def set_delegate(self, name: Literal["cameraDelegate"], delegate: CameraDelegate) -> None: ...
    @overload
    def set_delegate(self, name: Literal["ptzDelegate"], delegate: CameraPTZDelegate) -> None: ...
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    @overload
    def get_frames(
        self, frame_type: Literal["video"], options: ImageOptions | None = None
    ) -> AsyncGenerator[VideoFrame, None]: ...
    @overload
    def get_frames(
        self, frame_type: Literal["motion"], options: ImageOptions | None = None
    ) -> AsyncGenerator[VideoFrame, None]: ...
    @overload
    async def update_state(self, state_name: Literal["light"], event_data: LightSetEvent) -> None: ...
    @overload
    async def update_state(
        self, state_name: Literal["motion"], event_data: MotionSetEvent, frame: VideoFrame | None = None
    ) -> None: ...
    @overload
    async def update_state(self, state_name: Literal["audio"], event_data: AudioSetEvent) -> None: ...
    @overload
    async def update_state(self, state_name: Literal["object"], event_data: ObjectSetEvent) -> None: ...
    @overload
    async def update_state(self, state_name: Literal["doorbell"], event_data: DoorbellSetEvent) -> None: ...
    @overload
    async def update_state(self, state_name: Literal["siren"], event_data: SirenSetEvent) -> None: ...
    @overload
    async def update_state(self, state_name: Literal["battery"], event_data: BatterySetEvent) -> None: ...
    async def add_camera_source(self, source: CameraConfigInputSettings) -> None: ...
    async def update_camera_source(
        self, source_id: str, source: CameraConfigInputSettingsPartial
    ) -> None: ...
    async def remove_camera_source(self, source_id: str) -> None: ...

CameraSelectedCallback = (
    Callable[[CameraDevice, CameraExtension], None]
    | Callable[[CameraDevice, CameraExtension], Coroutine[None, None, None]]
)
CameraDeselectedCallback = (
    Callable[[str, CameraExtension], None] | Callable[[str, CameraExtension], Coroutine[None, None, None]]
)

class DeviceManager(Protocol):
    async def create_camera(self, camera_config: CameraConfig) -> CameraDevice: ...
    async def get_camera_by_name(self, camera_name: str) -> CameraDevice | None: ...
    async def get_camera_by_id(self, camera_id: str) -> CameraDevice | None: ...
    async def remove_camera_by_name(self, camera_name: str) -> None: ...
    async def remove_camera_by_id(self, camera_id: str) -> None: ...
    @overload
    def on(self, event: Literal["cameraSelected"], f: CameraSelectedCallback) -> Any: ...
    @overload
    def on(self, event: Literal["cameraDeselected"], f: CameraDeselectedCallback) -> Any: ...
    @overload
    def once(self, event: Literal["cameraSelected"], f: CameraSelectedCallback) -> Any: ...
    @overload
    def once(self, event: Literal["cameraDeselected"], f: CameraDeselectedCallback) -> Any: ...
    @overload
    def remove_listener(self, event: Literal["cameraSelected"], f: CameraSelectedCallback) -> None: ...
    @overload
    def remove_listener(self, event: Literal["cameraDeselected"], f: CameraDeselectedCallback) -> None: ...
    def remove_all_listeners(self, event: DeviceManagerEventType | None = None) -> None: ...

class CoreManager(Protocol):
    async def connect_to_plugin(self, plugin_name: str) -> PluginInterface | None: ...
    async def get_ffmpeg_path(self) -> str: ...
    async def get_hwaccel_info(self, target_codec: Literal["h264"] | Literal["h265"]) -> FfmpegArgs: ...
    async def get_server_addresses(self) -> list[str]: ...
    async def get_ice_servers(self) -> list[IceServer]: ...

class FfmpegArgs(TypedDict):
    codec: str
    hwaccel: str
    hwaccelArgs: list[str]
    hwaccelFilters: list[str]
    hwDeviceArgs: list[str]
    threads: str

class IceServer(TypedDict):
    urls: list[str]
    username: str | None
    credential: str | None

PluginConfig = dict[str, Any]
J = TypeVar("J")

class JsonBaseSchema(TypedDict, Generic[J]):
    key: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    required: NotRequired[bool]
    readonly: NotRequired[bool]
    placeholder: NotRequired[str]
    hidden: NotRequired[bool]
    group: NotRequired[str]
    defaultValue: NotRequired[J]
    store: NotRequired[bool]
    onSet: NotRequired[Callable[[Any, Any], Awaitable[None | Any]] | Callable[[Any, Any], None | Any]]
    onGet: NotRequired[Callable[[], Awaitable[Any | None]] | Callable[[], Any | None]]

class JsonSchemaString(JsonBaseSchema[str]):
    type: Literal["string"]
    format: NotRequired[
        Literal["date-time", "date", "time", "email", "uuid", "ipv4", "ipv6", "password", "qrCode", "image"]
    ]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]

class JsonSchemaNumber(JsonBaseSchema[float]):
    type: Literal["number"]
    minimum: NotRequired[float]
    maximum: NotRequired[float]
    step: NotRequired[float]

class JsonSchemaBoolean(JsonBaseSchema[bool]):
    type: Literal["boolean"]

class JsonSchemaEnum(JsonBaseSchema[str]):
    type: Literal["string"]
    enum: list[str]
    multiple: NotRequired[bool]

class JsonSchemaObject(JsonBaseSchema[Any]):
    type: Literal["object"]
    opened: NotRequired[bool]
    properties: NotRequired[JsonSchemaForm]

class JsonSchemaArray(JsonBaseSchema[Any]):
    type: Literal["array"]
    opened: NotRequired[bool]
    items: NotRequired[JsonSchema]

class JsonSchemaButton(JsonBaseSchema[Any]):
    type: Literal["button"]
    color: NotRequired[Literal["success", "info", "warn", "danger"]]

class JsonSchemaObjectButton(TypedDict):
    label: str
    onSubmit: str
    color: NotRequired[Literal["success", "info", "warn", "danger"]]

class JsonSchemaObjectWithButtons(JsonSchemaObject):
    buttons: list[JsonSchemaObjectButton]

JsonSchema = (
    JsonSchemaString
    | JsonSchemaNumber
    | JsonSchemaBoolean
    | JsonSchemaEnum
    | JsonSchemaObject
    | JsonSchemaObjectWithButtons
    | JsonSchemaArray
    | JsonSchemaButton
)
JsonSchemaForm = dict[str, JsonSchema]

class RootSchema(TypedDict):
    schema: JsonSchemaForm

class ToastMessage(TypedDict):
    type: Literal["info", "success", "warning", "error"]
    message: str

class FormSubmitSchema(TypedDict):
    config: JsonSchemaObjectWithButtons

class FormSubmitResponse(TypedDict, total=False):
    toast: ToastMessage
    schema: FormSubmitSchema

class SchemaConfig(TypedDict):
    rootSchema: RootSchema
    config: dict[str, Any]

class ImageMetadata(TypedDict):
    width: int
    height: int

class AudioMetadata(TypedDict):
    mimeType: Literal["audio/mpeg", "audio/wav", "audio/ogg"]

class MotionDetectionPluginResponse(TypedDict):
    videoData: bytes

class ObjectDetectionPluginResponse(TypedDict):
    detections: list[Detection]

class AudioDetectionPluginResponse(TypedDict):
    detected: bool

class BasePlugin(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, logger: LoggerService, api: PluginAPI) -> None: ...
    @abstractmethod
    async def onFormSubmit(self, action_id: str, payload: Any) -> FormSubmitResponse | None: ...
    @abstractmethod
    async def configureCameras(self, cameras: list[CameraDevice]) -> None: ...

class MotionDetectionPlugin(BasePlugin, metaclass=abc.ABCMeta):
    @abstractmethod
    async def interfaceSchema(self) -> RootSchema | None: ...
    @abstractmethod
    async def detectMotion(
        self, video_data: bytes, config: dict[str, Any]
    ) -> MotionDetectionPluginResponse: ...

class ObjectDetectionPlugin(BasePlugin, metaclass=abc.ABCMeta):
    @abstractmethod
    async def interfaceSchema(self) -> RootSchema | None: ...
    @abstractmethod
    async def detectObjects(
        self, image_data: bytes, metadata: ImageMetadata, config: dict[str, Any]
    ) -> ObjectDetectionPluginResponse: ...

class AudioDetectionPlugin(BasePlugin, metaclass=abc.ABCMeta):
    @abstractmethod
    async def interfaceSchema(self) -> RootSchema | None: ...
    @abstractmethod
    async def detectAudio(
        self, audio_data: bytes, metadata: AudioMetadata, config: dict[str, Any]
    ) -> AudioDetectionPluginResponse: ...

class PluginInterface(Protocol):
    async def onFormSubmit(self, action_id: str, payload: Any) -> FormSubmitResponse | None: ...
    async def configureCameras(self, camera_devices: list[CameraDevice]) -> None: ...
    async def interfaceSchema(self) -> RootSchema | None: ...
    async def detectMotion(
        self, video_data: bytes, config: dict[str, Any]
    ) -> MotionDetectionPluginResponse: ...
    async def detectObjects(
        self, image_data: bytes, metadata: ImageMetadata, config: dict[str, Any]
    ) -> ObjectDetectionPluginResponse: ...
    async def detectAudio(
        self, audio_data: bytes, metadata: AudioMetadata, config: dict[str, Any]
    ) -> AudioDetectionPluginResponse: ...

class LoggerService(Protocol):
    def log(self, *args: Any) -> None: ...
    def error(self, *args: Any) -> None: ...
    def warn(self, *args: Any) -> None: ...
    def debug(self, *args: Any) -> None: ...
    def trace(self, *args: Any) -> None: ...
    def attention(self, *args: Any) -> None: ...
    def success(self, *args: Any) -> None: ...

PA = TypeVar("PA", bound="CameraStorage[Any]", default="CameraStorage[Any]")

class PluginAPI(Protocol):
    core_manager: CoreManager
    device_manager: DeviceManager
    storage_controller: StorageController
    config_service: ConfigService
    storage_path: str
    config_file: str
    def on(self, event: APIEventType, f: Callback) -> Any: ...
    def once(self, event: APIEventType, f: Callback) -> Any: ...
    def remove_listener(self, event: APIEventType, f: Callback) -> None: ...
    def remove_all_listeners(self, event: APIEventType | None = None) -> None: ...

class ConfigService(Protocol):
    def get(
        self,
        key: Path,
        default_value: JSONValue | None = None,
        validate: Callable[[Any], bool] | None = None,
        refresh: bool = False,
        write_if_not_valid: bool = False,
    ) -> Any: ...
    def has(self, key: Path, refresh: bool = False) -> bool: ...
    def ensure_exists(self, key: Path, default_value: JSONValue, write: bool = False) -> None: ...
    def set(self, key: Path, value: Any, write: bool = False) -> None: ...
    def insert(self, key: Path, value: Any, at: int = 0, write: bool = False) -> None: ...
    def push(self, key: Path, write: bool = False, *items: Any) -> None: ...
    def delete(self, key: Path, write: bool = False) -> None: ...
    def all(self, refresh: bool = False) -> dict[str, Any]: ...
    def replace(self, config: dict[str, Any], write: bool = False) -> None: ...
    def update_value(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        target_key: str,
        new_value: Any,
        write: bool = False,
    ) -> None: ...
    def replace_or_add_item(
        self, path: str, search_key: str, search_value: Any, new_item: Any, write: bool = False
    ) -> None: ...

V1 = TypeVar("V1", default=str)
V2 = TypeVar("V2", default=dict[str, Any])

class CameraStorage(Protocol, Generic[V2]):
    values: V2
    schema: JsonSchemaForm
    @overload
    async def getValue(self, path: str) -> V1 | None: ...
    @overload
    async def getValue(self, path: str, default_value: V1) -> V1: ...
    async def setValue(self, path: str, new_value: Any) -> None: ...
    def hasValue(self, path: str) -> bool: ...
    async def getConfig(self) -> SchemaConfig: ...
    async def setConfig(self, new_config: V2) -> None: ...
    @overload
    async def addSchema(self, schema_or_path: JsonSchemaForm) -> None: ...
    @overload
    async def addSchema(self, schema_or_path: str, schema: JsonSchema) -> None: ...
    def removeSchema(self, path: str) -> None: ...
    async def changeSchema(self, path: str, new_schema: dict[str, Any]) -> None: ...
    def getSchema(self, path: str) -> JsonSchema | None: ...
    def hasSchema(self, path: str) -> bool: ...

S = TypeVar("S", default=CameraStorage[Any], covariant=True)

class StorageController(Protocol[S]):
    def create_camera_storage(
        self, instance: Any, camera_id: str, schema: JsonSchemaForm | None = None
    ) -> S: ...
    def get_camera_storage(self, camera_id: str) -> S | None: ...
    async def remove_camera_storage(self, camera_id: str) -> None: ...

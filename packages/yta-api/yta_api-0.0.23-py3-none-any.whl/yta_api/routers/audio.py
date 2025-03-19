from yta_api.dataclasses import Response
from yta_audio.voice.transcription import DefaultTimestampedAudioTranscriptor, DefaultAudioTranscriptor
from yta_audio.voice.enums import VoiceNarrationEngine, VoiceSpeed, VoiceEmotion, VoicePitch, NarrationLanguage
from yta_audio.voice.generation.narrator import GoogleVoiceNarrator
from fastapi.responses import JSONResponse, FileResponse
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from io import BytesIO


PREFIX = 'audio'

router = APIRouter(
    prefix = f'/{PREFIX}'
)

# Validations here below
def validate_voice_narration_engine(
    engine: str
) -> VoiceNarrationEngine:
    try:
        return VoiceNarrationEngine.to_enum(engine)
    except:
        raise HTTPException(
            status_code = 400,
            detail = f'The "engine" parameter provided is not valid. The valid values are: "{VoiceNarrationEngine.get_all_values_as_str()}".'
        )

def validate_text(
    text: str
) -> str:
    if not text.strip():  # Validación manual de si el string está vacío
        raise HTTPException(
            status_code = 400,
            detail = f'No "text" parameter provided or the parameter is empty.'
        )
    
    return text

def validate_language(
    voice_engine,
    language: NarrationLanguage
) -> NarrationLanguage:
    # No language provided
    if language is None:
        raise HTTPException(
            status_code = 400,
            detail = f'No "language" parameter provided.'
        )
    
    # Language provided but not a language actually
    try:
        language = NarrationLanguage.to_enum(language)
    except:
        raise HTTPException(
            status_code = 400,
            detail = f'The "language" parameter provided is not a valid NarrationLanguage instance.'
        )
    
    # Language provided and valid but no accepted by
    # the engine they are requesting
    if language not in voice_engine.get_available_languages():
        valid_languages_str = ', '.join([
            valid_language.value
            for valid_language in voice_engine.get_available_languages()
        ])

        raise HTTPException(
            status_code = 400,
            detail = f'The "language" parameter provided is not valid. The valid values are: "{valid_languages_str}".'
        )
    
    return language

def validate_name(
    voice_engine,
    language: NarrationLanguage,
    name: str
) -> str:
    # No voice name provided
    if name in ['', None]:
        raise HTTPException(
            status_code = 400,
            detail = f'No "name" parameter provided.'
        )
    
    # Name provided but no accepted by the engine
    # they are requesting
    if name not in voice_engine.get_available_narrator_names(language):
        valid_names_str = ', '.join(voice_engine.get_available_narrator_names(language))

        raise HTTPException(
            status_code = 400,
            detail = f'The "name" parameter provided is not valid for the given language "{language.value}". The valid values are: "{valid_names_str}".'
        )
    
    return name

def validate_emotion(
    voice_engine,
    emotion: VoiceEmotion
) -> VoiceEmotion:
    # No emotion provided
    if emotion is None:
        raise HTTPException(
            status_code = 400,
            detail = f'No "emotion" parameter provided.'
        )
    
    # Emotion provided but not a language actually
    try:
        emotion = VoiceEmotion.to_enum(emotion)
    except:
        raise HTTPException(
            status_code = 400,
            detail = f'The "emotion" parameter provided is not a valid VoiceEmotion instance. The valid values are: "{VoiceEmotion.get_all_values_as_str()}".'
        )
    
    # Emotion provided but no accepted by the engine
    # they are requesting
    if emotion not in voice_engine.get_available_emotions():
        valid_emotions_str = ', '.join([
            valid_emotion.value
            for valid_emotion in voice_engine.get_available_emotions()
        ])

        raise HTTPException(
            status_code = 400,
            detail = f'The "emotion" parameter provided is not valid. The valid values are: "{valid_emotions_str}".'
        )
    
    return emotion

def validate_speed(
    voice_engine,
    speed: VoiceSpeed
) -> VoiceSpeed:
    # No speed provided
    if speed is None:
        raise HTTPException(
            status_code = 400,
            detail = f'No "speed" parameter provided.'
        )
    
    # Speed provided but not a language actually
    try:
        speed = VoiceSpeed.to_enum(speed)
    except:
        raise HTTPException(
            status_code = 400,
            detail = f'The "speed" parameter provided is not a valid VoiceSpeed instance. The valid values are: "{VoiceSpeed.get_all_values_as_str()}".'
        )
    
    # Speed provided but no accepted by the engine
    # they are requesting
    if speed not in voice_engine.get_available_speeds():
        valid_speeds_str = ', '.join([
            valid_speed.value
            for valid_speed in voice_engine.get_available_speeds()
        ])

        raise HTTPException(
            status_code = 400,
            detail = f'The "speed" parameter provided is not valid. The valid values are: "{valid_speeds_str}".'
        )
    
    return speed

def validate_pitch(
    voice_engine,
    pitch: VoicePitch
) -> VoicePitch:
    # No pitch provided
    if pitch is None:
        raise HTTPException(
            status_code = 400,
            detail = f'No "pitch" parameter provided.'
        )
    
    # Pitch provided but not a language actually
    try:
        pitch = VoicePitch.to_enum(pitch)
    except:
        raise HTTPException(
            status_code = 400,
            detail = f'The "pitch" parameter provided is not a valid VoicePitch instance. The valid values are: "{VoicePitch.get_all_values_as_str()}".'
        )
    
    # Pitch provided but no accepted by the engine
    # they are requesting
    if pitch not in voice_engine.get_available_pitches():
        valid_pitches_str = ', '.join([
            valid_pitch.value
            for valid_pitch in voice_engine.get_available_pitches()
        ])

        raise HTTPException(
            status_code = 400,
            detail = f'The "pitch" parameter provided is not valid. The valid values are: "{valid_pitches_str}".'
        )
    
    return pitch
# Validations here above

# Options here below
@router.options('/narrate-engines')
def route_narrate_text_engine_options() -> list[str]:
    return VoiceNarrationEngine.get_all_values()

@router.options('/narrate-languages')
def route_narrate_text_languages_options() -> list[str]:
    return NarrationLanguage.get_all_values()

@router.options('/narrate-emotions')
def route_narrate_text_emotions_options() -> list[str]:
    return VoiceEmotion.get_all_values()

@router.options('/narrate-speeds')
def route_narrate_text_speeds_options() -> list[str]:
    return VoiceSpeed.get_all_values()

@router.options('/narrate-pitches')
def route_narrate_text_pitches_options() -> list[str]:
    return VoicePitch.get_all_values()

@router.options('/narrate-engine-languages')
def route_narrate_text_engine_languages_options(
    engine: str = Depends(validate_voice_narration_engine)
) -> list[str]:
    return engine.get_voice_narrator_class().get_available_languages()

@router.options('/narrate-engine-names')
def route_narrate_text_name_options(
    engine: str = Depends(validate_voice_narration_engine),
    language: NarrationLanguage = None
) -> list[str]:
    voice_engine = engine.get_voice_narrator_class()
    language = validate_language(
        voice_engine = voice_engine,
        language = language
    )

    return voice_engine.get_available_narrator_names(language)

@router.options('/narrate-engine-emotions')
def route_narrate_text_engine_emotion_options(
    engine: str = Depends(validate_voice_narration_engine)
) -> list[str]:
    return engine.get_voice_narrator_class().get_available_emotions()

@router.options('/narrate-engine-speeds')
def route_narrate_text_engine_speed_options(
    engine: str = Depends(validate_voice_narration_engine)
) -> list[str]:
    return engine.get_voice_narrator_class().get_available_speeds()

@router.options('/narrate-engine-pitches')
def route_narrate_text_engine_pitch_options(
    engine: str = Depends(validate_voice_narration_engine)
) -> list[str]:
    return engine.get_voice_narrator_class().get_available_pitches()
# Options here above

# Routes here below
@router.get('/narrate-simple')
def route_narrate_text(text: str):
    voice_narration_filename = GoogleVoiceNarrator.narrate(text)

    return FileResponse(voice_narration_filename)

@router.get('/narrate')
def route_narrate_text(
    text: str,
    engine: str = Depends(validate_voice_narration_engine),
    # TODO: Implement validation here (?)
    name: str = None,
    emotion: str = None,
    speed: str = None,
    pitch: str = None,
    language: str = None
):
    """
    A method to create a voice narration with all the
    parameters we can handle and customize.
    """
    voice_engine = engine.get_voice_narrator_class()

    # TODO: This validations could have be done with
    # the parameters
    text = validate_text(text)
    language = validate_language(voice_engine, language)
    name = validate_name(voice_engine, language, name)
    emotion = validate_emotion(voice_engine, emotion)
    speed = validate_speed(voice_engine, speed)
    pitch = validate_pitch(voice_engine, pitch)

    voice_narration_filename = engine.get_voice_narrator_class().narrate(
        text = text,
        name = name,
        emotion = emotion,
        speed = speed,
        pitch = pitch,
        language = language
    )

    return FileResponse(voice_narration_filename)

@router.post('/transcribe-timestamps-file')
async def route_transcribe_file(
    file: UploadFile = File(...)
):
    # TODO: Validate file is accepted audio file
    # File comes like this: UploadFile(filename='voz_panning.m4a', size=356161, headers=Headers({'content-disposition': 'form-data; name="file"; filename="voz_panning.m4a"', 'content-type': 'audio/mp4'}))
    transcription = DefaultTimestampedAudioTranscriptor.transcribe(
        audio = BytesIO(await file.read())
    )

    return JSONResponse(
        content = Response(
            transcription.as_dict
        ).as_dict
    )

@router.post('/transcribe-file')
async def route_transcribe_file(
    file: UploadFile = File(...)
):
    # TODO: Validate file is accepted audio file
    # File comes like this: UploadFile(filename='voz_panning.m4a', size=356161, headers=Headers({'content-disposition': 'form-data; name="file"; filename="voz_panning.m4a"', 'content-type': 'audio/mp4'}))
    transcription = DefaultAudioTranscriptor.transcribe(
        audio = BytesIO(await file.read())
    )

    return JSONResponse(
        content = Response(
            transcription.text
        ).as_dict
    )

# @router.get('/transcribe')
# def route_transcribe_audio(
#     audio_file_url: str
# ):
#     # TODO: Check this to receive files
#     # https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile
#     # TODO: Check that 'url' is a valid audio path or audio url
#     #transcription = get_transcription_text(url)

#     transcription = DefaultTimestampedAudioTranscriptor.transcribe(
#         Downloader.download_audio(
#             audio_file_url,
#             output_filename = Temp.create_filename('audio.mp3')
#         )
#     )

#     # TODO: Build an specific format to give to our responses
#     # TODO: Store information about who made the requested
#     # TODO: Limit the amount of requests per user
#     # Maybe 'timestamp'

#     return JSONResponse(
#         content = Response(
#             transcription.as_dict
#         ).as_dict
#     )
# Routes here above





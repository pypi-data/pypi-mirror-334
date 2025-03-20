from setuptools import setup, find_packages


VERSION = '0.0.28'
DESCRIPTION = 'Youtube Autonomous Audio Module.'
LONG_DESCRIPTION = 'This is the Youtube Autonomous Audio module'

setup(
        name = "yta_audio", 
        version = VERSION,
        author = "Daniel Alcalá",
        author_email = "<danielalcalavalera@gmail.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = [
            'yta_general_utils',
            'pydub',
            'moviepy',
            'deepfilternet',
            'whisper_timestamped',
            'faster_whisper',
            'tts', # This is conflictive because of its version (v0.22.0 was ok)
            #'open_voice', # No pypi: https://github.com/myshell-ai/OpenVoice/blob/main/setup.py
            'torch',
            'torchaudio',
            #'melotts', # No pypi: https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md#cli
            'pyttsx3',
            'gtts',
            'scamp',
            'elevenlabs',
            #'pymusixmatch', # No pypi: https://github.com/utstikkar/pyMusiXmatch
            'librosa',
            'pedalboard',
            'soundfile',
            'scipy',
            # The 'spleeter' library has been removed temporary because
            # it causes conflicts with 'click' library and also with
            # 'httpx' that makes the library unable to be deployed
            # properly in Render service. Version was 'spleeter=2.4.0'
            #'spleeter', # This one is installing click-7.1.2 which is in conflict with manim and others
        ],
        
        keywords = [
            'youtube autonomous audio module software'
        ],
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
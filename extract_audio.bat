@echo off
setlocal

:: Extracts an FMOD sample bank from Sky: Children of the Light.
:: Dependencies:
:: - FSB file extractor: http://aluigi.altervista.org/papers/fsbext.zip
:: - FSB audio extractor: https://zenhax.com/viewtopic.php?f=17&t=1901
:: - FFmpeg
::
:: Usage: fmod_extract.bat filename
:: (Typically, the filename extension will be `.streams.bank`.)

set PATH=%PATH%;%~dp0\bin

:: Rewrite wrapped FSB (RIFF format) to .dat file
mkdir raw_%1
fsbext -o -1 -d raw_%1 -s %1.dat %1

:: Rebuild FSB without RIFF wrapping, so that fsb_aud_extr can read it
fsbext -d raw_%1 -s %1.dat -r %1.fsb

mkdir wav_%1
move %1.fsb wav_%1
cd wav_%1

:: Extract audio
fsb_aud_extr %1.fsb

:: Convert WAV (actually Vorbis exported as WAV) to Opus
for %%i in (*.wav) do (
  if not exist "%%~ni.opus" (ffmpeg -i "%%~ni.wav" "%%~ni.opus" && del "%%~ni.wav")
)

:: Clean up
del %1.fsb
cd ..
del /q raw_%1
rmdir raw_%1
del %1.dat

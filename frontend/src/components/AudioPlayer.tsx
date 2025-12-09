import { useState, useRef, useEffect } from "react";
import { Play, Pause, SkipBack, SkipForward, Volume2, VolumeX, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";

interface AudioPlayerProps {
  title: string;
  audioUrl: string;
  duration?: string;
  coverImage?: string;
}

export const AudioPlayer = ({ title, audioUrl, duration, coverImage }: AudioPlayerProps) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [totalDuration, setTotalDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    // Construct full audio URL
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
    const fullAudioUrl = audioUrl.startsWith('http')
      ? audioUrl
      : `${API_BASE_URL}${audioUrl}`;

    console.log('Loading audio from:', fullAudioUrl);

    // Create audio element
    const audio = new Audio(fullAudioUrl);
    audioRef.current = audio;

    // Event listeners
    const handleLoadedMetadata = () => {
      setTotalDuration(audio.duration);
      setIsLoading(false);
    };

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime);
    };

    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };

    const handleError = (e: Event) => {
      setIsLoading(false);
      console.error("Failed to load audio:", fullAudioUrl, e);
      console.error("Audio error details:", audio.error);
    };

    audio.addEventListener("loadedmetadata", handleLoadedMetadata);
    audio.addEventListener("timeupdate", handleTimeUpdate);
    audio.addEventListener("ended", handleEnded);
    audio.addEventListener("error", handleError);

    return () => {
      audio.removeEventListener("loadedmetadata", handleLoadedMetadata);
      audio.removeEventListener("timeupdate", handleTimeUpdate);
      audio.removeEventListener("ended", handleEnded);
      audio.removeEventListener("error", handleError);
      audio.pause();
    };
  }, [audioUrl]);

  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.play().catch(console.error);
      } else {
        audioRef.current.pause();
      }
    }
  }, [isPlaying]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = isMuted ? 0 : volume;
    }
  }, [volume, isMuted]);

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  const handleSkipBackward = () => {
    if (audioRef.current) {
      audioRef.current.currentTime = Math.max(0, currentTime - 15);
    }
  };

  const handleSkipForward = () => {
    if (audioRef.current) {
      audioRef.current.currentTime = Math.min(totalDuration, currentTime + 15);
    }
  };

  const handleSeek = (value: number[]) => {
    const newTime = value[0];
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  const handleVolumeChange = (value: number[]) => {
    setVolume(value[0]);
    if (isMuted && value[0] > 0) {
      setIsMuted(false);
    }
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  const handleDownload = async () => {
    try {
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

      // Get the audio filename from the URL
      const audioFilename = audioUrl.split('/').pop() || 'story.mp3';

      // Use the dedicated download endpoint
      const downloadUrl = audioUrl.startsWith('http')
        ? `${audioUrl}/download`
        : `${API_BASE_URL}${audioUrl}/download`;

      // Create download link
      const link = document.createElement('a');
      link.href = downloadUrl;

      // Generate clean filename from title
      const filename = `${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.mp3`;
      link.download = filename;
      link.target = '_blank'; // Open in new tab if needed

      // Trigger download
      document.body.appendChild(link);
      link.click();

      // Cleanup
      document.body.removeChild(link);
    } catch (error) {
      console.error('Download failed:', error);
      // Fallback: try blob method
      try {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const fullAudioUrl = audioUrl.startsWith('http')
          ? audioUrl
          : `${API_BASE_URL}${audioUrl}`;

        const response = await fetch(fullAudioUrl);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        const filename = `${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.mp3`;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } catch (fallbackError) {
        console.error('Fallback download also failed:', fallbackError);
      }
    }
  };

  const formatTime = (seconds: number) => {
    if (!isFinite(seconds)) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  const progressPercent = totalDuration > 0 ? (currentTime / totalDuration) * 100 : 0;

  return (
    <div className="bg-gradient-to-br from-card to-secondary/30 rounded-3xl p-6 shadow-xl border-2 border-border">
      <div className="flex items-center gap-4">
        {/* Cover Image */}
        <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-lavender flex items-center justify-center shadow-lg flex-shrink-0">
          {coverImage ? (
            <img src={coverImage} alt={title} className="w-full h-full object-cover rounded-2xl" />
          ) : (
            <span className="text-3xl">📖</span>
          )}
        </div>

        {/* Info & Controls */}
        <div className="flex-1 space-y-3 min-w-0">
          <div>
            <h4 className="font-display font-semibold text-foreground text-lg truncate">{title}</h4>
            <p className="text-sm text-muted-foreground font-body">
              {duration || (totalDuration > 0 ? formatTime(totalDuration) : "Loading...")}
            </p>
          </div>

          {/* Progress Bar */}
          <div className="space-y-1">
            {isLoading ? (
              <div className="h-2 bg-muted rounded-full overflow-hidden">
                <div className="h-full bg-primary/30 animate-pulse" />
              </div>
            ) : (
              <Slider
                value={[currentTime]}
                max={totalDuration}
                step={0.1}
                onValueChange={handleSeek}
                className="cursor-pointer"
              />
            )}
            <div className="flex justify-between text-xs text-muted-foreground font-body">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(totalDuration)}</span>
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleSkipBackward}
              className="rounded-full"
              disabled={isLoading}
            >
              <SkipBack className="w-4 h-4" />
            </Button>

            <Button
              variant="magic"
              size="icon"
              onClick={togglePlay}
              className="w-12 h-12 rounded-full"
              disabled={isLoading}
            >
              {isPlaying ? (
                <Pause className="w-5 h-5" />
              ) : (
                <Play className="w-5 h-5 ml-0.5" />
              )}
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={handleSkipForward}
              className="rounded-full"
              disabled={isLoading}
            >
              <SkipForward className="w-4 h-4" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={handleDownload}
              className="rounded-full"
              disabled={isLoading}
              title="Download audio"
            >
              <Download className="w-4 h-4" />
            </Button>

            <div className="flex-1" />

            {/* Volume Control */}
            <div className="hidden sm:flex items-center gap-2 min-w-[120px]">
              <Button
                variant="ghost"
                size="icon"
                onClick={toggleMute}
                className="rounded-full flex-shrink-0"
              >
                {isMuted || volume === 0 ? (
                  <VolumeX className="w-4 h-4" />
                ) : (
                  <Volume2 className="w-4 h-4" />
                )}
              </Button>
              <Slider
                value={[isMuted ? 0 : volume]}
                max={1}
                step={0.01}
                onValueChange={handleVolumeChange}
                className="w-20"
              />
            </div>

            {/* Mobile volume toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleMute}
              className="rounded-full sm:hidden"
            >
              {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

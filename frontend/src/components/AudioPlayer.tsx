import { useState, useRef, useEffect } from "react";
import { Play, Pause, SkipBack, SkipForward, Volume2, VolumeX } from "lucide-react";
import { Button } from "@/components/ui/button";

interface AudioPlayerProps {
  title: string;
  duration: string;
  coverImage?: string;
}

export const AudioPlayer = ({ title, duration, coverImage }: AudioPlayerProps) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const totalDuration = 240; // 4 minutes in seconds

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPlaying && currentTime < totalDuration) {
      interval = setInterval(() => {
        setCurrentTime((prev) => Math.min(prev + 1, totalDuration));
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying, currentTime]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  const progressPercent = (currentTime / totalDuration) * 100;

  return (
    <div className="bg-gradient-to-br from-card to-secondary/30 rounded-3xl p-6 shadow-xl border-2 border-border">
      <div className="flex items-center gap-4">
        {/* Cover Image */}
        <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-lavender flex items-center justify-center shadow-lg">
          {coverImage ? (
            <img src={coverImage} alt={title} className="w-full h-full object-cover rounded-2xl" />
          ) : (
            <span className="text-3xl">📖</span>
          )}
        </div>

        {/* Info & Controls */}
        <div className="flex-1 space-y-3">
          <div>
            <h4 className="font-display font-semibold text-foreground text-lg">{title}</h4>
            <p className="text-sm text-muted-foreground font-body">Duration: {duration}</p>
          </div>

          {/* Progress Bar */}
          <div className="space-y-1">
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-primary to-lavender rounded-full transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
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
              onClick={() => setCurrentTime(Math.max(0, currentTime - 15))}
              className="rounded-full"
            >
              <SkipBack className="w-4 h-4" />
            </Button>

            <Button
              variant="magic"
              size="icon"
              onClick={() => setIsPlaying(!isPlaying)}
              className="w-12 h-12 rounded-full"
            >
              {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => setCurrentTime(Math.min(totalDuration, currentTime + 15))}
              className="rounded-full"
            >
              <SkipForward className="w-4 h-4" />
            </Button>

            <div className="flex-1" />

            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsMuted(!isMuted)}
              className="rounded-full"
            >
              {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

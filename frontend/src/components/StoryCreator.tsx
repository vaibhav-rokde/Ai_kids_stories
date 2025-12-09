import { useState } from "react";
import { Wand2, Sparkles, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { apiService, StoryResponse, StoryStatusResponse } from "@/lib/api";
import { AudioPlayer } from "./AudioPlayer";

const themePrompts = [
  { emoji: "🦊", label: "A fox who learns to share" },
  { emoji: "🐿️", label: "A brave squirrel adventure" },
  { emoji: "🌙", label: "A bedtime moon journey" },
  { emoji: "🦋", label: "A butterfly's first flight" },
  { emoji: "🐻", label: "A bear finds new friends" },
  { emoji: "🌈", label: "A magical rainbow quest" },
];

const stageMessages: Record<string, string> = {
  pending: "Preparing your story...",
  generating_story: "✨ Creating your magical story...",
  generating_speech: "🎤 Adding natural narration...",
  generating_music: "🎵 Composing background music...",
  mixing_audio: "🎧 Mixing audio elements...",
  completed: "✅ Your story is ready!",
  failed: "❌ Something went wrong",
};

export const StoryCreator = () => {
  const [theme, setTheme] = useState("");
  const [characterName, setCharacterName] = useState("");
  const [ageGroup, setAgeGroup] = useState("5-7");

  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedStory, setGeneratedStory] = useState<StoryResponse | null>(null);
  const [progress, setProgress] = useState(0);
  const [currentStage, setCurrentStage] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!theme.trim()) return;

    setIsGenerating(true);
    setError(null);
    setProgress(0);
    setCurrentStage("pending");

    try {
      // Create story
      const story = await apiService.createStory({
        theme: theme.trim(),
        character_name: characterName.trim() || undefined,
        age_group: ageGroup,
      });

      // Poll for completion
      const completedStory = await apiService.pollStoryStatus(
        story.id,
        (status: StoryStatusResponse) => {
          setProgress(status.progress_percentage);
          setCurrentStage(status.status);
        }
      );

      setGeneratedStory(completedStory);
      setProgress(100);
      setCurrentStage("completed");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate story");
      setCurrentStage("failed");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setGeneratedStory(null);
    setProgress(0);
    setCurrentStage("");
    setError(null);
  };

  return (
    <section id="create" className="py-20 bg-background relative">
      <div className="container mx-auto px-4">
        <div className="text-center space-y-4 mb-12 animate-slide-up">
          <div className="inline-flex items-center gap-2 bg-secondary rounded-full px-4 py-2 text-sm font-body text-secondary-foreground">
            <Wand2 className="w-4 h-4 text-primary" />
            Story Generator
          </div>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold text-foreground">
            Create Your <span className="text-primary">Magical</span> Story
          </h2>
          <p className="text-lg text-muted-foreground font-body max-w-2xl mx-auto">
            Enter a theme or idea, and watch as AI transforms it into an immersive audio adventure
            with narration, sound effects, and music.
          </p>
        </div>

        <div className="max-w-3xl mx-auto space-y-6">
          {/* Story Form */}
          {!generatedStory && (
            <Card className="border-2 border-lavender/30 shadow-magic animate-scale-in animation-delay-200">
              <CardHeader className="text-center pb-4">
                <CardTitle className="flex items-center justify-center gap-2">
                  <Sparkles className="w-6 h-6 text-sunshine" />
                  Story Theme
                </CardTitle>
                <CardDescription>
                  Choose a quick prompt or describe your own adventure
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Quick prompts */}
                <div className="flex flex-wrap gap-2 justify-center">
                  {themePrompts.map((prompt) => (
                    <button
                      key={prompt.label}
                      onClick={() => setTheme(prompt.label)}
                      disabled={isGenerating}
                      className={`px-4 py-2 rounded-xl text-sm font-body transition-all duration-200 border-2 ${
                        theme === prompt.label
                          ? "bg-primary text-primary-foreground border-primary"
                          : "bg-muted text-muted-foreground border-transparent hover:border-primary/50 hover:bg-muted/80"
                      } disabled:opacity-50 disabled:cursor-not-allowed`}
                    >
                      <span className="mr-2">{prompt.emoji}</span>
                      {prompt.label}
                    </button>
                  ))}
                </div>

                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-primary/10 via-lavender/10 to-sunshine/10 rounded-xl blur-xl" />
                  <Textarea
                    placeholder="Or describe your own story idea... e.g., 'A curious kitten who discovers a hidden garden filled with talking flowers'"
                    value={theme}
                    onChange={(e) => setTheme(e.target.value)}
                    disabled={isGenerating}
                    className="relative min-h-[140px] text-base"
                  />
                </div>

                {/* Character Name & Age Group */}
                <div className="grid sm:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-body font-medium text-foreground">
                      Main Character Name (optional)
                    </label>
                    <Input
                      placeholder="e.g., Luna, Max, Bella"
                      value={characterName}
                      onChange={(e) => setCharacterName(e.target.value)}
                      disabled={isGenerating}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-body font-medium text-foreground">
                      Child's Age Group
                    </label>
                    <select
                      className="flex h-12 w-full rounded-xl border-2 border-input bg-card px-4 py-3 text-base font-body transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed"
                      value={ageGroup}
                      onChange={(e) => setAgeGroup(e.target.value)}
                      disabled={isGenerating}
                    >
                      <option value="3-5">3-5 years (Toddler)</option>
                      <option value="5-7">5-7 years (Early Reader)</option>
                      <option value="7-10">7-10 years (Elementary)</option>
                    </select>
                  </div>
                </div>

                <Button
                  variant="hero"
                  className="w-full"
                  onClick={handleGenerate}
                  disabled={!theme.trim() || isGenerating}
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Creating Magic...
                    </>
                  ) : (
                    <>
                      <Wand2 className="w-5 h-5" />
                      Generate Story
                    </>
                  )}
                </Button>

                <p className="text-center text-sm text-muted-foreground font-body">
                  Stories are 3-5 minutes long with natural AI narration, sound effects, and background music.
                </p>
              </CardContent>
            </Card>
          )}

          {/* Progress Indicator */}
          {isGenerating && (
            <Card className="border-2 border-primary/30 animate-scale-in">
              <CardContent className="pt-6 space-y-4">
                <div className="text-center">
                  <div className="inline-flex items-center gap-2 text-lg font-display font-semibold text-foreground mb-2">
                    <Loader2 className="w-5 h-5 animate-spin text-primary" />
                    {stageMessages[currentStage] || "Processing..."}
                  </div>
                  <Progress value={progress} className="h-3" />
                  <p className="text-sm text-muted-foreground mt-2">{Math.round(progress)}% complete</p>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Error Message */}
          {error && (
            <Alert variant="destructive" className="animate-scale-in">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Generated Story */}
          {generatedStory && generatedStory.status === "completed" && (
            <div className="space-y-6 animate-scale-in">
              <Alert className="border-2 border-primary/30 bg-primary/5">
                <CheckCircle2 className="h-5 w-5 text-primary" />
                <AlertDescription className="text-base font-medium">
                  Your magical story is ready! 🎉
                </AlertDescription>
              </Alert>

              {/* Story Details */}
              <Card className="border-2 border-primary/30">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-primary" />
                    {generatedStory.theme}
                  </CardTitle>
                  {generatedStory.character_name && (
                    <CardDescription>
                      Featuring: {generatedStory.character_name}
                    </CardDescription>
                  )}
                </CardHeader>
                <CardContent className="space-y-4">
                  {generatedStory.story_text && (
                    <div className="prose prose-sm max-w-none">
                      <p className="text-muted-foreground">{generatedStory.story_text}</p>
                    </div>
                  )}

                  {generatedStory.audio_url && (
                    <AudioPlayer
                      title={generatedStory.theme}
                      audioUrl={generatedStory.audio_url}
                      duration="4:00"
                    />
                  )}

                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={handleReset}
                  >
                    Create Another Story
                  </Button>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

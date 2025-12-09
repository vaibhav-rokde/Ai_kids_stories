import { useState } from "react";
import { Wand2, Sparkles, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const themePrompts = [
  { emoji: "🦊", label: "A fox who learns to share" },
  { emoji: "🐿️", label: "A brave squirrel adventure" },
  { emoji: "🌙", label: "A bedtime moon journey" },
  { emoji: "🦋", label: "A butterfly's first flight" },
  { emoji: "🐻", label: "A bear finds new friends" },
  { emoji: "🌈", label: "A magical rainbow quest" },
];

export const StoryCreator = () => {
  const [theme, setTheme] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = () => {
    if (!theme.trim()) return;
    setIsGenerating(true);
    // Simulated generation
    setTimeout(() => setIsGenerating(false), 3000);
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

        <div className="max-w-3xl mx-auto">
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
                    className={`px-4 py-2 rounded-xl text-sm font-body transition-all duration-200 border-2 ${
                      theme === prompt.label
                        ? "bg-primary text-primary-foreground border-primary"
                        : "bg-muted text-muted-foreground border-transparent hover:border-primary/50 hover:bg-muted/80"
                    }`}
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
                  className="relative min-h-[140px] text-base"
                />
              </div>

              {/* Character Name (optional) */}
              <div className="grid sm:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-body font-medium text-foreground">
                    Main Character Name (optional)
                  </label>
                  <Input placeholder="e.g., Luna, Max, Bella" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-body font-medium text-foreground">
                    Child's Age Group
                  </label>
                  <select className="flex h-12 w-full rounded-xl border-2 border-input bg-card px-4 py-3 text-base font-body transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary">
                    <option value="3-5">3-5 years (Toddler)</option>
                    <option value="5-7" selected>5-7 years (Early Reader)</option>
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
        </div>
      </div>
    </section>
  );
};

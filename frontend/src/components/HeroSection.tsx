import { Sparkles, Play, Wand2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { FloatingElements } from "./FloatingElements";
import heroImage from "@/assets/hero-illustration.png";

export const HeroSection = () => {
  return (
    <section className="relative min-h-screen gradient-hero overflow-hidden pt-16">
      <FloatingElements />
      
      <div className="container mx-auto px-4 py-12 lg:py-20">
        <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">
          {/* Text Content */}
          <div className="relative z-10 text-center lg:text-left space-y-6 animate-slide-up">
            <div className="inline-flex items-center gap-2 bg-secondary/80 backdrop-blur-sm rounded-full px-4 py-2 text-sm font-body text-secondary-foreground">
              <Sparkles className="w-4 h-4 text-primary" />
              AI-Powered Storytelling for Kids
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold text-foreground leading-tight">
              Create <span className="text-primary">Magical</span> Stories{" "}
              <span className="text-lavender">Your Kids</span> Will Love
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground font-body max-w-xl mx-auto lg:mx-0">
              Transform simple ideas into immersive audio adventures with natural narration, 
              sound effects, and enchanting background music.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button variant="hero" className="gap-2">
                <Wand2 className="w-5 h-5" />
                Create a Story
              </Button>
              <Button variant="outline" size="xl" className="gap-2">
                <Play className="w-5 h-5" />
                Listen to Demo
              </Button>
            </div>
            
            <div className="flex items-center gap-6 justify-center lg:justify-start pt-4">
              <div className="text-center">
                <div className="text-2xl font-display font-bold text-primary">3-5</div>
                <div className="text-sm text-muted-foreground font-body">Minutes</div>
              </div>
              <div className="w-px h-12 bg-border" />
              <div className="text-center">
                <div className="text-2xl font-display font-bold text-lavender">100%</div>
                <div className="text-sm text-muted-foreground font-body">Kid-Safe</div>
              </div>
              <div className="w-px h-12 bg-border" />
              <div className="text-center">
                <div className="text-2xl font-display font-bold text-sunshine">AI</div>
                <div className="text-sm text-muted-foreground font-body">Powered</div>
              </div>
            </div>
          </div>
          
          {/* Hero Image */}
          <div className="relative z-10 animate-slide-up animation-delay-200">
            <div className="relative rounded-3xl overflow-hidden shadow-2xl">
              <img 
                src={heroImage} 
                alt="Magical owl reading a storybook under a starry night sky" 
                className="w-full h-auto object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background/20 to-transparent" />
            </div>
            
            {/* Floating card */}
            <div className="absolute -bottom-4 -left-4 bg-card rounded-2xl p-4 shadow-xl animate-float animation-delay-500">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-mint to-sky flex items-center justify-center">
                  <Play className="w-6 h-6 text-foreground" />
                </div>
                <div>
                  <div className="font-display font-semibold text-foreground">Now Playing</div>
                  <div className="text-sm text-muted-foreground font-body">The Brave Little Fox</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Bottom wave */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full">
          <path 
            d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" 
            fill="hsl(var(--background))"
          />
        </svg>
      </div>
    </section>
  );
};

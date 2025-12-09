import { BookOpen, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Header = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-lavender flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="font-display text-xl font-bold text-foreground">StoryMagic</span>
        </div>
        
        <nav className="hidden md:flex items-center gap-8">
          <a href="#create" className="font-body text-muted-foreground hover:text-primary transition-colors">Create Story</a>
          <a href="#stories" className="font-body text-muted-foreground hover:text-primary transition-colors">Sample Stories</a>
          <a href="#how-it-works" className="font-body text-muted-foreground hover:text-primary transition-colors">How It Works</a>
        </nav>
        
        <Button variant="magic" size="sm" className="gap-2">
          <Sparkles className="w-4 h-4" />
          <span className="hidden sm:inline">Get Started</span>
        </Button>
      </div>
    </header>
  );
};

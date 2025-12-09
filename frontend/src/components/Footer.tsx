import { BookOpen, Heart } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="bg-foreground text-primary-foreground py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Logo & Description */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-lavender flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-primary-foreground" />
              </div>
              <span className="font-display text-xl font-bold">StoryMagic</span>
            </div>
            <p className="text-primary-foreground/70 font-body max-w-md">
              Creating magical audio adventures for children through the power of AI. 
              Safe, immersive, and unforgettable storytelling.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-display font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 font-body text-primary-foreground/70">
              <li><a href="#create" className="hover:text-primary-foreground transition-colors">Create Story</a></li>
              <li><a href="#stories" className="hover:text-primary-foreground transition-colors">Sample Stories</a></li>
              <li><a href="#how-it-works" className="hover:text-primary-foreground transition-colors">How It Works</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-display font-semibold mb-4">Resources</h4>
            <ul className="space-y-2 font-body text-primary-foreground/70">
              <li><a href="#" className="hover:text-primary-foreground transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-primary-foreground transition-colors">API Reference</a></li>
              <li><a href="#" className="hover:text-primary-foreground transition-colors">Privacy Policy</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-primary-foreground/20 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-primary-foreground/60 font-body">
            © 2024 StoryMagic. All rights reserved.
          </p>
          <p className="text-sm text-primary-foreground/60 font-body flex items-center gap-1">
            Made with <Heart className="w-4 h-4 text-primary fill-primary" /> for little dreamers everywhere
          </p>
        </div>
      </div>
    </footer>
  );
};

import { Star, Sparkles, Moon, Cloud } from "lucide-react";

export const FloatingElements = () => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Stars */}
      <Star className="absolute top-20 left-[10%] w-6 h-6 text-sunshine animate-sparkle opacity-60" />
      <Star className="absolute top-40 right-[15%] w-4 h-4 text-sunshine animate-sparkle animation-delay-300 opacity-50" />
      <Star className="absolute top-32 left-[30%] w-5 h-5 text-sunshine animate-sparkle animation-delay-500 opacity-40" />
      <Star className="absolute top-60 right-[25%] w-3 h-3 text-sunshine animate-sparkle animation-delay-700 opacity-60" />
      
      {/* Sparkles */}
      <Sparkles className="absolute top-28 right-[35%] w-8 h-8 text-coral animate-float-slow opacity-50" />
      <Sparkles className="absolute top-52 left-[20%] w-6 h-6 text-lavender animate-float animation-delay-200 opacity-40" />
      
      {/* Moon */}
      <Moon className="absolute top-16 right-[8%] w-10 h-10 text-sunshine animate-pulse-soft opacity-70" />
      
      {/* Clouds */}
      <Cloud className="absolute top-36 left-[5%] w-12 h-12 text-sky/50 animate-float-slow animation-delay-300" />
      <Cloud className="absolute top-24 right-[40%] w-8 h-8 text-lavender/40 animate-float animation-delay-500" />
    </div>
  );
};

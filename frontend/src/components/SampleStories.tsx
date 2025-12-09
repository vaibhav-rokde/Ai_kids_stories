import { Play, Clock, Star, Headphones } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AudioPlayer } from "./AudioPlayer";
import { useState } from "react";

const stories = [
  {
    id: 1,
    title: "The Brave Little Fox",
    description: "Luna the fox discovers courage she never knew she had when her forest friends need her help.",
    duration: "4:32",
    emoji: "🦊",
    gradient: "from-primary to-coral-light",
    rating: 4.9,
    listens: "2.3k",
  },
  {
    id: 2,
    title: "Starlight Dreams",
    description: "A magical journey through the night sky where Oliver meets the friendly moon and dancing stars.",
    duration: "3:45",
    emoji: "🌙",
    gradient: "from-lavender to-sky",
    rating: 4.8,
    listens: "1.8k",
  },
  {
    id: 3,
    title: "The Rainbow Garden",
    description: "Bella the butterfly finds a secret garden where flowers of every color share their wisdom.",
    duration: "4:15",
    emoji: "🦋",
    gradient: "from-mint to-sunshine",
    rating: 5.0,
    listens: "3.1k",
  },
];

export const SampleStories = () => {
  const [activeStory, setActiveStory] = useState<number | null>(null);

  return (
    <section id="stories" className="py-20 bg-gradient-to-b from-background to-secondary/20 relative">
      <div className="container mx-auto px-4">
        <div className="text-center space-y-4 mb-12">
          <div className="inline-flex items-center gap-2 bg-mint/30 rounded-full px-4 py-2 text-sm font-body text-foreground">
            <Headphones className="w-4 h-4 text-primary" />
            Sample Stories
          </div>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold text-foreground">
            Listen to <span className="text-lavender">Magic</span> in Action
          </h2>
          <p className="text-lg text-muted-foreground font-body max-w-2xl mx-auto">
            Hear how our AI creates immersive audio stories with natural narration, 
            sound effects, and enchanting background music.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {stories.map((story, index) => (
            <Card
              key={story.id}
              className={`group cursor-pointer transition-all duration-300 hover:-translate-y-2 animate-slide-up border-2 ${
                activeStory === story.id ? "border-primary shadow-lg" : "border-transparent hover:border-lavender/50"
              }`}
              style={{ animationDelay: `${index * 100}ms` }}
              onClick={() => setActiveStory(activeStory === story.id ? null : story.id)}
            >
              <CardContent className="p-0">
                {/* Cover */}
                <div className={`h-40 bg-gradient-to-br ${story.gradient} rounded-t-2xl flex items-center justify-center relative overflow-hidden`}>
                  <span className="text-6xl group-hover:scale-110 transition-transform duration-300">
                    {story.emoji}
                  </span>
                  
                  {/* Play overlay */}
                  <div className="absolute inset-0 bg-foreground/0 group-hover:bg-foreground/10 transition-colors flex items-center justify-center">
                    <div className="w-14 h-14 rounded-full bg-card/90 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-lg">
                      <Play className="w-6 h-6 text-primary ml-1" />
                    </div>
                  </div>
                </div>

                {/* Info */}
                <div className="p-5 space-y-3">
                  <div className="flex items-start justify-between">
                    <h3 className="font-display font-semibold text-lg text-foreground group-hover:text-primary transition-colors">
                      {story.title}
                    </h3>
                    <div className="flex items-center gap-1 text-sunshine">
                      <Star className="w-4 h-4 fill-current" />
                      <span className="text-sm font-body">{story.rating}</span>
                    </div>
                  </div>

                  <p className="text-sm text-muted-foreground font-body line-clamp-2">
                    {story.description}
                  </p>

                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      <span className="font-body">{story.duration}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Headphones className="w-4 h-4" />
                      <span className="font-body">{story.listens}</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Active Player */}
        {activeStory && (
          <div className="max-w-2xl mx-auto animate-scale-in">
            <AudioPlayer
              title={stories.find((s) => s.id === activeStory)?.title || ""}
              duration={stories.find((s) => s.id === activeStory)?.duration || ""}
            />
          </div>
        )}
      </div>
    </section>
  );
};

import { Shield, Zap, Heart, Globe, Palette, Volume2 } from "lucide-react";

const features = [
  {
    icon: Shield,
    title: "100% Kid-Safe",
    description: "All content is AI-filtered for age-appropriate themes and language.",
    color: "bg-mint",
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Generate complete audio stories in under 2 minutes.",
    color: "bg-sunshine",
  },
  {
    icon: Heart,
    title: "Emotional Range",
    description: "Stories that make kids laugh, wonder, and feel inspired.",
    color: "bg-coral-light",
  },
  {
    icon: Globe,
    title: "Multi-Language",
    description: "Create stories in multiple languages for global families.",
    color: "bg-lavender",
  },
  {
    icon: Palette,
    title: "Customizable",
    description: "Personalize characters, themes, and story length.",
    color: "bg-sky",
  },
  {
    icon: Volume2,
    title: "Premium Audio",
    description: "Studio-quality narration with immersive soundscapes.",
    color: "bg-peach",
  },
];

export const Features = () => {
  return (
    <section className="py-20 bg-secondary/30 relative">
      <div className="container mx-auto px-4">
        <div className="text-center space-y-4 mb-12">
          <h2 className="text-3xl md:text-4xl font-display font-bold text-foreground">
            Why Kids & Parents <span className="text-primary">Love Us</span>
          </h2>
          <p className="text-lg text-muted-foreground font-body max-w-2xl mx-auto">
            Every feature is designed with children's safety, engagement, and wonder in mind.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="bg-card rounded-2xl p-6 border-2 border-border hover:border-primary/30 transition-all duration-300 hover:shadow-lg group animate-slide-up"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className={`w-12 h-12 ${feature.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-6 h-6 text-foreground" />
              </div>

              <h3 className="font-display font-semibold text-lg text-foreground mb-2">
                {feature.title}
              </h3>

              <p className="text-muted-foreground font-body text-sm">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

import { Lightbulb, Cpu, Mic2, Music, Sparkles } from "lucide-react";

const steps = [
  {
    icon: Lightbulb,
    title: "Enter Your Theme",
    description: "Describe your story idea or choose from our magical prompts. A simple theme is all you need!",
    color: "from-sunshine to-coral-light",
    number: "01",
  },
  {
    icon: Cpu,
    title: "AI Creates Story",
    description: "Our advanced AI crafts a unique, age-appropriate narrative with engaging characters and plot.",
    color: "from-primary to-lavender",
    number: "02",
  },
  {
    icon: Mic2,
    title: "Natural Narration",
    description: "Professional-quality Text-to-Speech brings your story to life with expressive, natural voices.",
    color: "from-lavender to-sky",
    number: "03",
  },
  {
    icon: Music,
    title: "Sound Magic",
    description: "Contextual sound effects and ambient music are layered in to create an immersive experience.",
    color: "from-mint to-sunshine",
    number: "04",
  },
];

export const HowItWorks = () => {
  return (
    <section id="how-it-works" className="py-20 bg-background relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-lavender/20 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-80 h-80 bg-primary/10 rounded-full blur-3xl" />

      <div className="container mx-auto px-4 relative z-10">
        <div className="text-center space-y-4 mb-16">
          <div className="inline-flex items-center gap-2 bg-sunshine/30 rounded-full px-4 py-2 text-sm font-body text-foreground">
            <Sparkles className="w-4 h-4 text-primary" />
            How It Works
          </div>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold text-foreground">
            From Idea to <span className="text-primary">Audio Adventure</span>
          </h2>
          <p className="text-lg text-muted-foreground font-body max-w-2xl mx-auto">
            Four simple steps transform your imagination into a fully produced, 
            immersive audio story your kids will treasure.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8">
          {steps.map((step, index) => (
            <div
              key={step.number}
              className="relative group animate-slide-up"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              {/* Connector line (desktop) */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-16 left-[60%] w-full h-0.5 bg-gradient-to-r from-border to-transparent" />
              )}

              <div className="bg-card rounded-3xl p-6 border-2 border-border hover:border-lavender/50 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 h-full">
                {/* Step number */}
                <div className="absolute -top-3 -right-3 w-10 h-10 rounded-xl bg-secondary text-secondary-foreground font-display font-bold text-sm flex items-center justify-center">
                  {step.number}
                </div>

                {/* Icon */}
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg`}>
                  <step.icon className="w-8 h-8 text-primary-foreground" />
                </div>

                <h3 className="font-display font-semibold text-xl text-foreground mb-2">
                  {step.title}
                </h3>

                <p className="text-muted-foreground font-body text-sm leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

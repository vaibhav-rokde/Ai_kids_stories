import { Header } from "@/components/Header";
import { HeroSection } from "@/components/HeroSection";
import { StoryCreator } from "@/components/StoryCreator";
import { SampleStories } from "@/components/SampleStories";
import { HowItWorks } from "@/components/HowItWorks";
import { Features } from "@/components/Features";
import { Footer } from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <HeroSection />
        <StoryCreator />
        <SampleStories />
        <HowItWorks />
        <Features />
      </main>
      <Footer />
    </div>
  );
};

export default Index;

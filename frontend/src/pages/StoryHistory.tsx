import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { AudioPlayer } from '@/components/AudioPlayer';
import { Loader2, BookOpen, Calendar, Clock, ArrowLeft, ChevronDown, ChevronUp, RefreshCw, History } from 'lucide-react';
import { toast } from 'sonner';
import { VersionHistoryDialog } from '@/components/VersionHistoryDialog';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

interface Story {
  id: number;
  story_title: string;
  story_text: string;
  story_text_html?: string;
  theme: string;
  character_name: string | null;
  age_group: string;
  status: string;
  audio_url: string | null;
  duration_seconds: number | null;
  created_at: string;
  completed_at: string | null;
  current_version: number;
}

interface StoriesResponse {
  stories: Story[];
  total: number;
  page: number;
  page_size: number;
}

export default function StoryHistory() {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [stories, setStories] = useState<Story[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [expandedStories, setExpandedStories] = useState<Set<number>>(new Set());
  const [regeneratingIds, setRegeneratingIds] = useState<Set<number>>(new Set());
  const [versionDialogStoryId, setVersionDialogStoryId] = useState<number | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    loadStories();
  }, [isAuthenticated, navigate]);

  const loadStories = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${API_BASE_URL}/api/v1/stories/my-stories`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to load stories');
      }

      const data: StoriesResponse = await response.json();
      setStories(data.stories);
      setTotal(data.total);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to load stories');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatDuration = (seconds: number | null) => {
    if (!seconds) return 'N/A';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'failed':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    }
  };

  const toggleExpanded = (storyId: number) => {
    setExpandedStories((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(storyId)) {
        newSet.delete(storyId);
      } else {
        newSet.add(storyId);
      }
      return newSet;
    });
  };

  const handleRegenerate = async (storyId: number) => {
    try {
      setRegeneratingIds((prev) => new Set(prev).add(storyId));
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${API_BASE_URL}/api/v1/stories/${storyId}/regenerate`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to regenerate story');
      }

      toast.success('Story regeneration started! It will be ready soon.');

      // Reload stories to show updated status
      setTimeout(() => {
        loadStories();
        setRegeneratingIds((prev) => {
          const newSet = new Set(prev);
          newSet.delete(storyId);
          return newSet;
        });
      }, 1000);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to regenerate story');
      setRegeneratingIds((prev) => {
        const newSet = new Set(prev);
        newSet.delete(storyId);
        return newSet;
      });
    }
  };

  const handleViewVersions = (storyId: number) => {
    setVersionDialogStoryId(storyId);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-secondary/30 to-accent/10 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/30 to-accent/10 px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-display font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              My Stories
            </h1>
            <p className="text-muted-foreground font-body mt-2">
              {total} {total === 1 ? 'story' : 'stories'} created
            </p>
          </div>
          <Button
            onClick={() => navigate('/')}
            variant="outline"
            className="font-body border-2"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
        </div>

        {/* Stories List */}
        {stories.length === 0 ? (
          <Card className="border-2 shadow-lg">
            <CardContent className="py-12 text-center">
              <BookOpen className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
              <h3 className="text-xl font-display font-bold mb-2">No stories yet</h3>
              <p className="text-muted-foreground font-body mb-6">
                Start creating your first magical story!
              </p>
              <Button
                onClick={() => navigate('/')}
                className="font-body bg-gradient-to-r from-primary to-accent"
              >
                Create Story
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {stories.map((story) => (
              <Card key={story.id} className="border-2 shadow-lg overflow-hidden">
                <CardHeader className="bg-gradient-to-r from-secondary/50 to-accent/20">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-2xl font-display font-bold text-foreground">
                        {story.story_title || 'Untitled Story'}
                      </CardTitle>
                      <div className="flex flex-wrap gap-2 mt-3">
                        <Badge variant="outline" className="font-body">
                          {story.theme}
                        </Badge>
                        {story.character_name && (
                          <Badge variant="outline" className="font-body">
                            {story.character_name}
                          </Badge>
                        )}
                        <Badge variant="outline" className="font-body">
                          Age: {story.age_group}
                        </Badge>
                        <Badge className={`${getStatusColor(story.status)} font-body border`}>
                          {story.status}
                        </Badge>
                        <Badge variant="outline" className="font-body">
                          Version: {story.current_version}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex gap-2 ml-4">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleRegenerate(story.id)}
                        disabled={regeneratingIds.has(story.id) || story.status !== 'completed'}
                        className="font-body"
                      >
                        {regeneratingIds.has(story.id) ? (
                          <>
                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                            Regenerating...
                          </>
                        ) : (
                          <>
                            <RefreshCw className="w-4 h-4 mr-2" />
                            Regenerate
                          </>
                        )}
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleViewVersions(story.id)}
                        disabled={story.current_version === 1}
                        className="font-body"
                      >
                        <History className="w-4 h-4 mr-2" />
                        Versions
                      </Button>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4 pt-6">
                  {/* Story Text Preview */}
                  {story.story_text && (
                    <div className="bg-secondary/30 rounded-xl p-4 space-y-2">
                      {story.story_text_html ? (
                        <div
                          className={`font-body text-sm prose prose-sm max-w-none ${
                            expandedStories.has(story.id) ? '' : 'line-clamp-3'
                          }`}
                          dangerouslySetInnerHTML={{ __html: story.story_text_html }}
                        />
                      ) : (
                        <p className={`font-body text-sm whitespace-pre-wrap ${
                          expandedStories.has(story.id) ? '' : 'line-clamp-3'
                        }`}>
                          {story.story_text}
                        </p>
                      )}
                      {story.story_text.length > 200 && (
                        <button
                          onClick={() => toggleExpanded(story.id)}
                          className="text-primary hover:text-primary/80 text-sm font-medium flex items-center gap-1 transition-colors"
                        >
                          {expandedStories.has(story.id) ? (
                            <>
                              <span>Read less</span>
                              <ChevronUp className="w-4 h-4" />
                            </>
                          ) : (
                            <>
                              <span>Read more</span>
                              <ChevronDown className="w-4 h-4" />
                            </>
                          )}
                        </button>
                      )}
                    </div>
                  )}

                  {/* Metadata */}
                  <div className="flex flex-wrap gap-4 text-sm text-muted-foreground font-body">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {formatDate(story.created_at)}
                    </div>
                    {story.duration_seconds && (
                      <div className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {formatDuration(story.duration_seconds)}
                      </div>
                    )}
                  </div>

                  {/* Audio Player */}
                  {story.audio_url && (
                    <div className="space-y-2">
                      {story.status !== 'completed' && (
                        <p className="text-xs text-muted-foreground font-body">
                          Playing previous version while new one is being generated...
                        </p>
                      )}
                      <AudioPlayer
                        title={story.story_title || 'Your Story'}
                        audioUrl={story.audio_url}
                        duration={story.duration_seconds ? formatDuration(story.duration_seconds) : undefined}
                      />
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Version History Dialog */}
      {versionDialogStoryId && (
        <VersionHistoryDialog
          storyId={versionDialogStoryId}
          open={versionDialogStoryId !== null}
          onOpenChange={(open) => !open && setVersionDialogStoryId(null)}
        />
      )}
    </div>
  );
}

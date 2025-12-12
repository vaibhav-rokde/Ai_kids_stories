import { useEffect, useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AudioPlayer } from '@/components/AudioPlayer';
import { Loader2, Calendar, Clock, Download } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { toast } from 'sonner';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

interface StoryVersion {
  id: number;
  story_id: number;
  version_number: number;
  theme: string;
  character_name: string | null;
  age_group: string;
  story_text: string | null;
  story_text_html: string | null;
  story_title: string | null;
  audio_url: string | null;
  word_count: number | null;
  duration_seconds: number | null;
  created_at: string;
}

interface VersionHistoryDialogProps {
  storyId: number;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function VersionHistoryDialog({
  storyId,
  open,
  onOpenChange,
}: VersionHistoryDialogProps) {
  const [versions, setVersions] = useState<StoryVersion[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedVersions, setExpandedVersions] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (open && storyId) {
      loadVersions();
    }
  }, [open, storyId]);

  const loadVersions = async () => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `${API_BASE_URL}/api/v1/stories/${storyId}/versions`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to load version history');
      }

      const data = await response.json();
      setVersions(data.versions);
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : 'Failed to load version history'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatDuration = (seconds: number | null) => {
    if (!seconds) return 'N/A';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const toggleExpanded = (versionId: number) => {
    setExpandedVersions((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(versionId)) {
        newSet.delete(versionId);
      } else {
        newSet.add(versionId);
      }
      return newSet;
    });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[80vh] p-0">
        <DialogHeader className="p-6 pb-4">
          <DialogTitle className="text-2xl font-display font-bold">
            Version History
          </DialogTitle>
          <DialogDescription className="font-body">
            View all previous versions of this story
          </DialogDescription>
        </DialogHeader>

        <ScrollArea className="px-6 pb-6 max-h-[calc(80vh-120px)]">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
          ) : versions.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground font-body">
                No previous versions found
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {versions.map((version) => (
                <Card key={version.id} className="border-2 shadow-sm">
                  <CardHeader className="bg-secondary/30 pb-3">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg font-display font-bold">
                          {version.story_title || 'Untitled Story'}
                        </CardTitle>
                        <div className="flex flex-wrap gap-2 mt-2">
                          <Badge variant="outline" className="font-body text-xs">
                            Version {version.version_number}
                          </Badge>
                          <Badge variant="outline" className="font-body text-xs">
                            {version.word_count || 0} words
                          </Badge>
                          {version.duration_seconds && (
                            <Badge variant="outline" className="font-body text-xs">
                              <Clock className="w-3 h-3 mr-1" />
                              {formatDuration(version.duration_seconds)}
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-1 text-xs text-muted-foreground font-body mt-2">
                      <Calendar className="w-3 h-3" />
                      {formatDate(version.created_at)}
                    </div>
                  </CardHeader>

                  <CardContent className="pt-4 space-y-3">
                    {/* Story Text */}
                    {version.story_text && (
                      <div className="bg-secondary/20 rounded-lg p-3">
                        {version.story_text_html ? (
                          <div
                            className={`font-body text-sm prose prose-sm max-w-none ${
                              expandedVersions.has(version.id)
                                ? ''
                                : 'line-clamp-3'
                            }`}
                            dangerouslySetInnerHTML={{
                              __html: version.story_text_html,
                            }}
                          />
                        ) : (
                          <p
                            className={`font-body text-sm whitespace-pre-wrap ${
                              expandedVersions.has(version.id)
                                ? ''
                                : 'line-clamp-3'
                            }`}
                          >
                            {version.story_text}
                          </p>
                        )}
                        {version.story_text.length > 200 && (
                          <button
                            onClick={() => toggleExpanded(version.id)}
                            className="text-primary hover:text-primary/80 text-xs font-medium mt-2"
                          >
                            {expandedVersions.has(version.id)
                              ? 'Show less'
                              : 'Show more'}
                          </button>
                        )}
                      </div>
                    )}

                    {/* Audio Player */}
                    {version.audio_url && (
                      <AudioPlayer
                        title={version.story_title || 'Version ' + version.version_number}
                        audioUrl={version.audio_url}
                        duration={
                          version.duration_seconds
                            ? formatDuration(version.duration_seconds)
                            : undefined
                        }
                      />
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}

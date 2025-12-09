import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { User, Mail, Calendar, LogOut, BookOpen } from 'lucide-react';
import { toast } from 'sonner';

export default function Profile() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  if (!user) {
    navigate('/login');
    return null;
  }

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/');
  };

  const getInitials = () => {
    if (user.full_name) {
      return user.full_name
        .split(' ')
        .map((n) => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
    return user.username.slice(0, 2).toUpperCase();
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/30 to-accent/10 px-4 py-8">
      <div className="max-w-2xl mx-auto space-y-6">
        {/* Profile Card */}
        <Card className="border-2 shadow-xl">
          <CardHeader className="text-center space-y-4">
            <div className="flex justify-center">
              <Avatar className="w-24 h-24 border-4 border-primary shadow-lg">
                <AvatarFallback className="bg-gradient-to-br from-primary to-accent text-white text-2xl font-display font-bold">
                  {getInitials()}
                </AvatarFallback>
              </Avatar>
            </div>
            <div>
              <CardTitle className="text-3xl font-display font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                {user.full_name || user.username}
              </CardTitle>
              <CardDescription className="text-base font-body mt-2">
                @{user.username}
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* User Info */}
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-3 rounded-lg bg-secondary/50">
                <Mail className="w-5 h-5 text-primary" />
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground font-body">Email</p>
                  <p className="font-body font-semibold">{user.email}</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-3 rounded-lg bg-secondary/50">
                <User className="w-5 h-5 text-primary" />
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground font-body">Username</p>
                  <p className="font-body font-semibold">{user.username}</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-3 rounded-lg bg-secondary/50">
                <Calendar className="w-5 h-5 text-primary" />
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground font-body">Member Since</p>
                  <p className="font-body font-semibold">{formatDate(user.created_at)}</p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3 pt-4 border-t">
              <Button
                onClick={() => navigate('/story-history')}
                className="w-full font-body font-semibold bg-gradient-to-r from-primary to-accent hover:opacity-90"
                size="lg"
              >
                <BookOpen className="w-4 h-4 mr-2" />
                View My Stories
              </Button>

              <Button
                onClick={handleLogout}
                variant="outline"
                className="w-full font-body font-semibold border-2 hover:bg-destructive hover:text-destructive-foreground"
                size="lg"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

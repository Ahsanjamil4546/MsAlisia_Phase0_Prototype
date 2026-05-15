import { useState } from 'react';
import { createProfile, getSessionSummary, sendChatMessage } from './api';
import { AdminSnapshot } from './components/AdminSnapshot';
import { ChatPanel } from './components/ChatPanel';
import { Header } from './components/Header';
import { OnboardingPanel } from './components/OnboardingPanel';
import { ParentSummary } from './components/ParentSummary';
import { WaitlistPanel } from './components/WaitlistPanel';
import type { ChatMessage, ParentProfile, StudentProfile, SummaryResponse } from './types';

const initialParent: ParentProfile = {
  parent_name: 'Demo Parent',
  email: 'parent@example.com',
};

const initialStudent: StudentProfile = {
  child_name: 'Ava',
  grade: '4',
  confidence_level: 'medium',
  learning_pace: 'normal',
  support_style: 'balanced',
  focus_notes: 'Prefers short steps and encouragement.',
};

function App() {
  const [parent, setParent] = useState<ParentProfile>(initialParent);
  const [student, setStudent] = useState<StudentProfile>(initialStudent);
  const [profileId, setProfileId] = useState<number>();
  const [savingProfile, setSavingProfile] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [message, setMessage] = useState('');
  const [sessionId, setSessionId] = useState<string>();
  const [loadingChat, setLoadingChat] = useState(false);
  const [summary, setSummary] = useState<SummaryResponse>();
  const [provider, setProvider] = useState<string>();
  const [model, setModel] = useState<string>();
  const [error, setError] = useState<string>();

  async function saveProfile() {
    setSavingProfile(true);
    setError(undefined);
    try {
      const response = await createProfile(parent, student);
      setProfileId(response.profile_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not save profile.');
    } finally {
      setSavingProfile(false);
    }
  }

  async function sendMessage() {
    const cleanMessage = message.trim();
    if (!cleanMessage) return;

    setLoadingChat(true);
    setError(undefined);
    setMessages((current) => [...current, { role: 'user', content: cleanMessage }]);
    setMessage('');

    try {
      const response = await sendChatMessage({
        profileId,
        sessionId,
        student: profileId ? undefined : student,
        message: cleanMessage,
      });
      setSessionId(response.session_id);
      setProvider(response.provider);
      setModel(response.model);
      setMessages((current) => [...current, { role: 'assistant', content: response.reply }]);
    } catch (err) {
      const detail = err instanceof Error ? err.message : 'Could not send message.';
      setError(detail);
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: 'I could not connect right now. Please check the backend and Groq API key.' },
      ]);
    } finally {
      setLoadingChat(false);
    }
  }

  async function refreshSummary() {
    if (!sessionId) return;
    setError(undefined);
    try {
      setSummary(await getSessionSummary(sessionId));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load summary.');
    }
  }

  return (
    <main className="app-shell">
      <Header />

      {error ? <div className="error-banner">{error}</div> : null}

      <div className="content-grid">
        <div className="main-column">
          <OnboardingPanel
            parent={parent}
            student={student}
            onParentChange={setParent}
            onStudentChange={setStudent}
            onSave={saveProfile}
            saving={savingProfile}
            profileId={profileId}
          />
          <ChatPanel
            student={student}
            messages={messages}
            message={message}
            onMessageChange={setMessage}
            onSend={sendMessage}
            loading={loadingChat}
            provider={provider}
            model={model}
          />
        </div>
        <aside className="side-column">
          <ParentSummary summary={summary} onRefresh={refreshSummary} disabled={!sessionId} />
          <WaitlistPanel />
          <AdminSnapshot />
        </aside>
      </div>

      <footer className="footer-note">
        MsAlisia is a learning support tool. Parents and students should verify important answers with a teacher or trusted adult.
      </footer>
    </main>
  );
}

export default App;

import type { ChatMessage, StudentProfile } from '../types';

interface Props {
  student: StudentProfile;
  messages: ChatMessage[];
  message: string;
  onMessageChange: (value: string) => void;
  onSend: () => void;
  loading: boolean;
  provider?: string;
  model?: string;
}

const quickPrompts = [
  'Can you help me with LCM of 4 and 6?',
  'I need help understanding fractions.',
  'What does 3 x 4 mean?',
  'Can you give me a Grade 4 word problem?'
];

export function ChatPanel({ student, messages, message, onMessageChange, onSend, loading, provider, model }: Props) {
  return (
    <section className="panel tall-panel">
      <div className="section-heading compact">
        <p className="eyebrow">Step 2</p>
        <h2>Learn with Ms Alisia</h2>
        <p>Designed for simple, child-friendly tutoring: short guidance and one question at a time.</p>
      </div>

      <div className="learner-card">
        <div>
          <strong>{student.child_name || 'Student'}</strong>
          <span>Grade {student.grade}</span>
        </div>
        <div className="status-dot">Ready</div>
      </div>

      <div className="quick-prompts" aria-label="Quick prompt examples">
        {quickPrompts.map((prompt) => (
          <button key={prompt} type="button" onClick={() => onMessageChange(prompt)}>
            {prompt}
          </button>
        ))}
      </div>

      <div className="chat-window">
        {messages.length === 0 ? (
          <div className="empty-state">
            <strong>Try a simple math question.</strong>
            <p>Ms Alisia will respond with a short explanation and one quick check.</p>
          </div>
        ) : (
          messages.map((item, index) => (
            <div className={`chat-bubble ${item.role}`} key={`${item.role}-${index}`}>
              <span>{item.role === 'assistant' ? 'Ms Alisia' : 'Student'}</span>
              <p>{item.content}</p>
            </div>
          ))
        )}
      </div>

      <div className="chat-input-row">
        <textarea
          value={message}
          onChange={(event) => onMessageChange(event.target.value)}
          placeholder="Type a math question here..."
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault();
              onSend();
            }
          }}
        />
        <button className="primary-button" onClick={onSend} disabled={loading || !message.trim()}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </div>

      <p className="microcopy">
        Provider: {provider || 'not used yet'} {model ? `• Model: ${model}` : ''}
      </p>
    </section>
  );
}

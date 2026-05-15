import { useState } from 'react';
import { joinWaitlist } from '../api';

export function WaitlistPanel() {
  const [parentName, setParentName] = useState('');
  const [email, setEmail] = useState('');
  const [childGrade, setChildGrade] = useState<'3' | '4' | '5' | 'not_sure'>('not_sure');
  const [note, setNote] = useState('');
  const [status, setStatus] = useState<string>();
  const [loading, setLoading] = useState(false);

  async function submit() {
    setLoading(true);
    setStatus(undefined);
    try {
      const response = await joinWaitlist({ parent_name: parentName, email, child_grade: childGrade, note });
      setStatus(response.message);
      setParentName('');
      setEmail('');
      setNote('');
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'Could not save waitlist signup.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <div className="section-heading compact">
        <p className="eyebrow">Optional</p>
        <h2>Waitlist capture</h2>
        <p>Simple Phase 0 form to validate parent interest.</p>
      </div>
      <div className="form-grid single">
        <label>
          Parent name
          <input value={parentName} onChange={(event) => setParentName(event.target.value)} />
        </label>
        <label>
          Email
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
        </label>
        <label>
          Child grade
          <select value={childGrade} onChange={(event) => setChildGrade(event.target.value as typeof childGrade)}>
            <option value="not_sure">Not sure yet</option>
            <option value="3">Grade 3</option>
            <option value="4">Grade 4</option>
            <option value="5">Grade 5</option>
          </select>
        </label>
        <label>
          Optional note
          <textarea value={note} onChange={(event) => setNote(event.target.value)} />
        </label>
      </div>
      <button className="secondary-button" onClick={submit} disabled={loading || !parentName || !email}>
        {loading ? 'Saving...' : 'Join waitlist'}
      </button>
      {status ? <p className="success-text">{status}</p> : null}
    </section>
  );
}

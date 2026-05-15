import { useState } from 'react';
import { getAdminSnapshot } from '../api';
import type { AdminSnapshot as Snapshot } from '../types';

export function AdminSnapshot() {
  const [snapshot, setSnapshot] = useState<Snapshot>();
  const [loading, setLoading] = useState(false);

  async function refresh() {
    setLoading(true);
    try {
      setSnapshot(await getAdminSnapshot());
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <div className="section-heading compact">
        <p className="eyebrow">Internal</p>
        <h2>Simple admin snapshot</h2>
        <p>Lightweight visibility for Phase 0 validation.</p>
      </div>
      <button className="secondary-button" onClick={refresh} disabled={loading}>
        {loading ? 'Loading...' : 'Load snapshot'}
      </button>
      {snapshot ? (
        <div className="metric-grid">
          <div><span>Profiles</span><strong>{snapshot.profiles}</strong></div>
          <div><span>Waitlist</span><strong>{snapshot.waitlist_signups}</strong></div>
          <div><span>Sessions</span><strong>{snapshot.sessions}</strong></div>
          <div><span>Messages</span><strong>{snapshot.messages}</strong></div>
        </div>
      ) : null}
    </section>
  );
}

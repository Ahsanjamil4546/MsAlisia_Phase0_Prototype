import type { ParentProfile, StudentProfile } from '../types';

interface Props {
  parent: ParentProfile;
  student: StudentProfile;
  onParentChange: (parent: ParentProfile) => void;
  onStudentChange: (student: StudentProfile) => void;
  onSave: () => void;
  saving: boolean;
  profileId?: number;
}

export function OnboardingPanel({ parent, student, onParentChange, onStudentChange, onSave, saving, profileId }: Props) {
  return (
    <section className="panel">
      <div className="section-heading">
        <p className="eyebrow">Step 1</p>
        <h2>Set up the learner</h2>
        <p>Simple fields for non-technical users. This context helps Ms Alisia guide the child gently.</p>
      </div>

      <div className="form-grid">
        <label>
          Parent name
          <input
            value={parent.parent_name}
            onChange={(event) => onParentChange({ ...parent, parent_name: event.target.value })}
            placeholder="Parent name"
          />
        </label>
        <label>
          Parent email
          <input
            type="email"
            value={parent.email}
            onChange={(event) => onParentChange({ ...parent, email: event.target.value })}
            placeholder="parent@example.com"
          />
        </label>
        <label>
          Child name
          <input
            value={student.child_name}
            onChange={(event) => onStudentChange({ ...student, child_name: event.target.value })}
            placeholder="Child first name"
          />
        </label>
        <label>
          Grade
          <select
            value={student.grade}
            onChange={(event) => onStudentChange({ ...student, grade: event.target.value as StudentProfile['grade'] })}
          >
            <option value="3">Grade 3</option>
            <option value="4">Grade 4</option>
            <option value="5">Grade 5</option>
          </select>
        </label>
        <label>
          Confidence level
          <select
            value={student.confidence_level}
            onChange={(event) =>
              onStudentChange({ ...student, confidence_level: event.target.value as StudentProfile['confidence_level'] })
            }
          >
            <option value="low">Needs reassurance</option>
            <option value="medium">Balanced</option>
            <option value="high">Confident</option>
          </select>
        </label>
        <label>
          Learning pace
          <select
            value={student.learning_pace}
            onChange={(event) =>
              onStudentChange({ ...student, learning_pace: event.target.value as StudentProfile['learning_pace'] })
            }
          >
            <option value="slow">Slow and careful</option>
            <option value="normal">Normal</option>
            <option value="fast">Moves quickly</option>
          </select>
        </label>
        <label className="wide">
          Support preference
          <select
            value={student.support_style}
            onChange={(event) =>
              onStudentChange({ ...student, support_style: event.target.value as StudentProfile['support_style'] })
            }
          >
            <option value="more_encouragement">More encouragement</option>
            <option value="balanced">Balanced support</option>
            <option value="direct_guidance">Direct guidance</option>
          </select>
        </label>
        <label className="wide">
          Optional learning notes
          <textarea
            value={student.focus_notes || ''}
            onChange={(event) => onStudentChange({ ...student, focus_notes: event.target.value })}
            placeholder="Example: gets frustrated with multi-step problems, likes visual examples..."
          />
        </label>
      </div>

      <div className="action-row">
        <button className="primary-button" onClick={onSave} disabled={saving}>
          {saving ? 'Saving...' : profileId ? 'Update profile' : 'Save learner profile'}
        </button>
        {profileId ? <span className="success-pill">Profile saved #{profileId}</span> : null}
      </div>
    </section>
  );
}

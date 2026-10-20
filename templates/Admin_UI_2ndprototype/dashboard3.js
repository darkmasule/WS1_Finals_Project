const API_BASE = "";  //API for db natin need dito

const rows = document.getElementById("studentRows");
const form = document.getElementById("studentForm");
const notice = document.getElementById("notice");
const idInput = document.getElementById("studentId");
const nameInput = document.getElementById("studentName");
const courseInput = document.getElementById("course");
const statusInput = document.getElementById("studentStatus");
const formHeading = document.getElementById("formHeading");
const submitBtn = document.getElementById("submitBtn");
const cancelEditBtn = document.getElementById("cancelEditBtn");
const tableSearch = document.getElementById("tableSearch");
const globalSearch = document.getElementById("globalSearch");
const statusFilter = document.getElementById("statusFilter");

let students = [];
let editingId = null;

function showNotice(message, type = "success") {
  notice.textContent = message;
  notice.className = `notice ${type}`;
  notice.hidden = false;
}
function clearNotice() {
  notice.hidden = true;
  notice.textContent = "";
}
function escapeHTML(value = "") {
  return String(value).replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}
function studentKey(student) {
  return String(student.student_id ?? student._id ?? "");
}
function updateStats() {
  document.getElementById("totalCount").textContent = students.length;
  document.getElementById("activeCount").textContent =
    students.filter(s => (s.status || "Active") === "Active").length;
}
function visibleStudents() {
  const query = (tableSearch.value || globalSearch.value).trim().toLowerCase();
  const status = statusFilter.value;
  return students.filter(student => {
    const matchesQuery = !query ||
      [student.student_id, student.name, student.course_section]
        .some(value => String(value || "").toLowerCase().includes(query));
    const matchesStatus = status === "all" || (student.status || "Active") === status;
    return matchesQuery && matchesStatus;
  });
}
function renderStudents() {
  const filtered = visibleStudents();
  updateStats();
  document.getElementById("resultCount").textContent =
    `Showing ${filtered.length} of ${students.length} students`;
  if (!filtered.length) {
    rows.innerHTML = '<tr><td colspan="6" class="empty">No students found.</td></tr>';
    return;
  }
  rows.innerHTML = filtered.map((student, index) => {
    const status = student.status || "Active";
    const id = studentKey(student);
    return `<tr>
      <td>${index + 1}</td>
      <td>${escapeHTML(student.student_id || id)}</td>
      <td>${escapeHTML(student.name || "")}</td>
      <td>${escapeHTML(student.course_section || "—")}</td>
      <td><span class="status ${status === "Active" ? "active" : "inactive"}">${escapeHTML(status)}</span></td>
      <td><div class="actions">
        <button class="icon-button edit-button" type="button" data-action="edit" data-id="${escapeHTML(id)}" aria-label="Edit ${escapeHTML(student.name || "student")}" title="Edit">✎</button>
        <button class="icon-button delete-button" type="button" data-action="delete" data-id="${escapeHTML(id)}" aria-label="Delete ${escapeHTML(student.name || "student")}" title="Delete">▤</button>
      </div></td>
    </tr>`;
  }).join("");
}
async function loadStudents() {
  rows.innerHTML = '<tr><td colspan="6" class="empty">Loading students...</td></tr>';
  try {
    const response = await fetch(`${API_BASE}/students`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || "Could not load students.");
    students = Array.isArray(data) ? data : (data.students || []);
    renderStudents();
  } catch (error) {
    rows.innerHTML = '<tr><td colspan="6" class="empty">Could not connect to the API. Check that Flask is running and GET /api/students exists.</td></tr>';
    document.getElementById("resultCount").textContent = "API unavailable";
    showNotice(error.message, "error");
  }
}
function resetForm() {
  form.reset();
  editingId = null;
  idInput.disabled = false;
  formHeading.textContent = "Add New Student";
  submitBtn.textContent = "＋ Add Student";
  cancelEditBtn.hidden = true;
}
function beginEdit(id) {
  const student = students.find(s => studentKey(s) === id);
  if (!student) return;
  editingId = id;
  idInput.value = student.student_id || id;
  idInput.disabled = true;
  nameInput.value = student.name || "";
  courseInput.value = student.course_section || "";
  statusInput.value = student.status || "Active";
  formHeading.textContent = "Edit Student";
  submitBtn.textContent = "Save Changes";
  cancelEditBtn.hidden = false;
  form.scrollIntoView({ behavior: "smooth", block: "start" });
}
form.addEventListener("submit", async event => {
  event.preventDefault();
  clearNotice();
  const payload = {
    student_id: idInput.value.trim(),
    name: nameInput.value.trim(),
    course_section: courseInput.value.trim(),
    status: statusInput.value
  };
  if (!payload.student_id || !payload.name) {
    showNotice("Student ID and full name are required.", "error");
    return;
  }
  const url = editingId
    ? `${API_BASE}/students/${encodeURIComponent(editingId)}`
    : `${API_BASE}/students`;
  const method = editingId ? "PUT" : "POST";
  submitBtn.disabled = true;
  try {
    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.message || "The request failed.");
    showNotice(result.message || (editingId ? "Student updated." : "Student added."));
    resetForm();
    await loadStudents();
  } catch (error) {
    showNotice(error.message || "Could not reach the Flask API.", "error");
  } finally {
    submitBtn.disabled = false;
  }
});
rows.addEventListener("click", async event => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const { action, id } = button.dataset;
  if (action === "edit") {
    beginEdit(id);
    return;
  }
  const student = students.find(s => studentKey(s) === id);
  if (!student || !confirm(`Delete student "${student.name}" (${student.student_id})? This cannot be undone.`)) return;
  try {
    const response = await fetch(`${API_BASE}/students/${encodeURIComponent(id)}`, { method: "DELETE" });
    const result = await response.json();
    if (!response.ok) throw new Error(result.message || "Could not delete student.");
    showNotice(result.message || "Student deleted.");
    if (editingId === id) resetForm();
    await loadStudents();
  } catch (error) {
    showNotice(error.message || "Could not reach the Flask API.", "error");
  }
});
cancelEditBtn.addEventListener("click", resetForm);
tableSearch.addEventListener("input", () => {
  globalSearch.value = "";
  renderStudents();
});
globalSearch.addEventListener("input", () => {
  tableSearch.value = "";
  renderStudents();
});
statusFilter.addEventListener("change", renderStudents);
document.getElementById("refreshBtn").addEventListener("click", loadStudents);

//dito we need to implement a CRUD API operation para sa admin js natin
loadStudents();
